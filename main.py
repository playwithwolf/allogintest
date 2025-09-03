from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import os
from typing import Optional

# 导入自定义模块
from config.alipay_config import AlipayConfig
from services.alipay_service import AlipayService
from models.user_models import UserInfo, LoginResponse

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

@app.get("/auth/alipay")
async def alipay_auth(request: Request):
    """支付宝授权登录 - 重定向到支付宝授权页面"""
    try:
        # 构建回调URL
        base_url = str(request.base_url).rstrip('/')
        redirect_uri = f"{base_url}/auth/alipay/callback"
        
        # 生成授权URL
        auth_url = alipay_service.get_auth_url(redirect_uri)
        
        return RedirectResponse(url=auth_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"授权失败: {str(e)}")

@app.get("/auth/alipay/callback")
async def alipay_callback(auth_code: Optional[str] = None, state: Optional[str] = None):
    """支付宝授权回调处理"""
    if not auth_code:
        raise HTTPException(status_code=400, detail="授权码不能为空")
    
    try:
        # 使用授权码获取访问令牌
        token_info = alipay_service.get_access_token(auth_code)
        
        # 使用访问令牌获取用户信息
        user_info = alipay_service.get_user_info(token_info['access_token'])
        
        # 这里可以将用户信息保存到数据库
        # 返回成功页面或重定向到用户主页
        return {
            "success": True,
            "message": "登录成功",
            "user_info": user_info,
            "token_info": {
                "access_token": token_info['access_token'],
                "expires_in": token_info['expires_in']
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"登录失败: {str(e)}")

@app.get("/api/user/info")
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