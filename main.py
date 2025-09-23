from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import os
from typing import Optional
from dotenv import load_dotenv
import logging

# 加载环境变量
load_dotenv()

# 导入自定义模块
from config.alipay_config import AlipayConfig
from services.alipay_service import AlipayService
from models.user_models import UserInfo, LoginResponse
from pydantic import BaseModel
from rate_limiter import auth_rate_limiter

# 请求模型
class AuthInfoRequest(BaseModel):
    pid: str
    target_id: Optional[str] = None
    rsa2: Optional[bool] = True

app = FastAPI(
    title="支付宝H5登录系统",
    description="基于FastAPI的支付宝OAuth授权登录系统",
    version="1.0.0"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 静态文件服务
app.mount("/static", StaticFiles(directory="static"), name="static")

# 初始化支付宝服务
alipay_service = AlipayService()

@app.get("/", response_class=HTMLResponse)
async def root():
    """首页 - 显示登录页面"""
    with open("static/login.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.post("/auth/alipay")
async def alipay_auth(request: Request):
    """支付宝授权登录 - 返回授权URL"""
    try:
        # 构建回调URL
        base_url = str(request.base_url).rstrip('/')
        redirect_uri = f"{base_url}/auth/alipay/callback"
        
        # 生成授权URL
        auth_url = alipay_service.get_auth_url(redirect_uri)
        
        return JSONResponse({
            "success": True,
            "auth_url": auth_url,
            "message": "授权URL生成成功"
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"授权失败: {str(e)}")

@app.get("/auth/alipay/callback")
async def alipay_callback(auth_code: Optional[str] = None, state: Optional[str] = None):
    """支付宝授权回调处理"""
    import logging
    logger = logging.getLogger(__name__)
    
    logger.info(f"收到支付宝回调请求 - auth_code: {auth_code}, state: {state}")
    
    if not auth_code:
        logger.error("授权码为空")
        raise HTTPException(status_code=400, detail="授权码不能为空")
    
    try:
        logger.info(f"开始获取访问令牌，授权码: {auth_code[:10]}...")
        # 使用授权码获取访问令牌
        token_info = alipay_service.get_access_token(auth_code)
        logger.info(f"成功获取访问令牌: {token_info}")
        
        # 使用访问令牌获取用户信息
        logger.info(f"开始获取用户信息，访问令牌: {token_info['access_token'][:10]}...")
        user_info = alipay_service.get_user_info(token_info['access_token'])
        logger.info(f"成功获取用户信息: {user_info}")
        
        # 这里可以将用户信息保存到数据库
        # 重定向到成功页面并传递用户信息
        import urllib.parse
        import json
        
        user_info_encoded = urllib.parse.quote(json.dumps(user_info, ensure_ascii=False))
        token_info_encoded = urllib.parse.quote(json.dumps({
            "access_token": token_info['access_token'],
            "expires_in": token_info['expires_in']
        }, ensure_ascii=False))
        
        success_url = f"/static/success.html?user_info={user_info_encoded}&token={token_info_encoded}"
        return RedirectResponse(url=success_url, status_code=302)
    except Exception as e:
        logger.error(f"登录失败，详细错误: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"登录失败: {str(e)}")

@app.post("/api/user/info")
async def get_user_info(access_token: str):
    """获取用户信息API"""
    try:
        user_info = alipay_service.get_user_info(access_token)
        return {
            "success": True,
            "data": user_info
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取用户信息失败: {str(e)}")

@app.post("/api/auth/authinfo")
async def generate_auth_info_post(request: Request):
    """生成支付宝授权信息字符串 - POST方式
    
    Args:
        request: 包含pid、target_id和rsa2参数的请求体
        
    Returns:
        dict: 包含authInfo的响应
    """
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        # 获取客户端IP用于频率限制
        client_ip = request.client.host
        
        # 检查频率限制
        if not auth_rate_limiter.is_allowed(client_ip):
            remaining_time = auth_rate_limiter.get_remaining_time(client_ip)
            raise HTTPException(
                status_code=429, 
                detail=f"请求过于频繁，请等待 {remaining_time} 秒后再试。为避免触发支付宝限流，建议使用 refresh_token 刷新令牌。"
            )
        
        # 解析请求体
        body = await request.json()
        pid = body.get('pid')
        target_id = body.get('target_id')
        rsa2 = body.get('rsa2', True)
        
        if not pid:
            raise HTTPException(status_code=400, detail="pid不能为空")
        
        logger.info(f"收到生成authInfo请求，PID: {pid}, target_id: {target_id}")
        
        # 生成authInfo
        auth_info = alipay_service.generate_auth_info(
            pid=pid,
            target_id=target_id,
            rsa2=rsa2
        )
        
        return {
            "success": True,
            "data": {
                "authInfo": auth_info,
                "pid": pid,
                "target_id": target_id or "auto_generated",
                "sign_type": "RSA2" if rsa2 else "RSA"
            },
            "message": "authInfo生成成功"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"生成authInfo失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"生成authInfo失败: {str(e)}"
        )

@app.get("/api/auth/authinfo/{pid}")
async def generate_auth_info_get(request: Request, pid: str, target_id: Optional[str] = None, rsa2: Optional[bool] = True):
    """生成支付宝授权信息字符串 - GET方式
    
    Args:
        request: FastAPI请求对象
        pid: 商户签约拿到的pid
        target_id: 商户唯一标识，可选
        rsa2: 是否使用RSA2签名，默认True
        
    Returns:
        dict: 包含authInfo的响应
    """
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        # 获取客户端IP用于频率限制
        client_ip = request.client.host
        
        # 检查频率限制
        if not auth_rate_limiter.is_allowed(client_ip):
            remaining_time = auth_rate_limiter.get_remaining_time(client_ip)
            raise HTTPException(
                status_code=429, 
                detail=f"请求过于频繁，请等待 {remaining_time} 秒后再试。为避免触发支付宝限流，建议使用 refresh_token 刷新令牌。"
            )
        
        logger.info(f"收到生成authInfo请求，PID: {pid}, target_id: {target_id}")
        
        # 生成authInfo
        auth_info = alipay_service.generate_auth_info(
            pid=pid,
            target_id=target_id,
            rsa2=rsa2
        )
        
        return {
            "success": True,
            "data": {
                "authInfo": auth_info,
                "pid": pid,
                "target_id": target_id or "auto_generated",
                "sign_type": "RSA2" if rsa2 else "RSA"
            },
            "message": "authInfo生成成功"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"生成authInfo失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"生成authInfo失败: {str(e)}"
        )

@app.post("/api/auth/userinfo")
async def get_user_info_by_auth_code(request: Request):
    """通过authCode获取用户信息 - 供Android应用调用
    
    Args:
        request: 包含authCode的请求体
        
    Returns:
        dict: 包含用户信息的响应
    """
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        # 解析请求体
        body = await request.json()
        auth_code = body.get('authCode')
        
        if not auth_code:
            raise HTTPException(status_code=400, detail="authCode不能为空")
        
        logger.info(f"收到获取用户信息请求，authCode: {auth_code[:10]}...")
        
        # 使用授权码获取访问令牌
        token_info = alipay_service.get_access_token(auth_code)
        logger.info(f"成功获取访问令牌: {token_info}")
        
        # 使用访问令牌获取用户信息
        user_info = alipay_service.get_user_info(token_info['access_token'])
        logger.info(f"成功获取用户信息: {user_info}")
        
        return {
            "success": True,
            "data": {
                "user_info": user_info,
                "token_info": {
                    "access_token": token_info['access_token'],
                    "expires_in": token_info['expires_in'],
                    "refresh_token": token_info.get('refresh_token'),  # 返回 refresh_token
                    "re_expires_in": token_info.get('re_expires_in'),
                    "user_id": token_info['user_id'],
                    "open_id": token_info['open_id']
                }
            },
            "message": "获取用户信息成功"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取用户信息失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"获取用户信息失败: {str(e)}"
        )

@app.post("/api/auth/refresh")
async def refresh_token_endpoint(request: Request):
    """刷新访问令牌接口
    
    Args:
        request: 包含refresh_token的请求体
        
    Returns:
        dict: 包含新的访问令牌信息的响应
    """
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        # 解析请求体
        body = await request.json()
        refresh_token = body.get('refresh_token')
        
        if not refresh_token:
            raise HTTPException(status_code=400, detail="refresh_token不能为空")
        
        logger.info(f"收到刷新令牌请求，refresh_token: {refresh_token[:20]}...")
        
        # 使用刷新令牌获取新的访问令牌
        token_info = alipay_service.refresh_access_token(refresh_token)
        logger.info(f"成功刷新访问令牌: {token_info}")
        
        return {
            "success": True,
            "data": {
                "access_token": token_info['access_token'],
                "expires_in": token_info['expires_in'],
                "refresh_token": token_info['refresh_token'],
                "re_expires_in": token_info['re_expires_in'],
                "user_id": token_info['user_id'],
                "open_id": token_info['open_id']
            },
            "message": "刷新访问令牌成功"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"刷新访问令牌失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"刷新访问令牌失败: {str(e)}"
        )

@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {"status": "healthy", "message": "支付宝H5登录系统运行正常"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )