import urllib.parse
import logging
from typing import Dict, Any
from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.request.AlipaySystemOauthTokenRequest import AlipaySystemOauthTokenRequest
from alipay.aop.api.request.AlipayUserInfoShareRequest import AlipayUserInfoShareRequest
from config.alipay_config import alipay_config
from models.user_models import UserInfo, TokenInfo

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AlipayService:
    """支付宝服务类 - 处理OAuth授权和用户信息获取"""
    
    def __init__(self):
        """初始化支付宝客户端"""
        try:
            # 验证配置
            alipay_config.validate_config()
            
            # 创建支付宝客户端配置
            self.alipay_client_config = AlipayClientConfig()
            self.alipay_client_config.server_url = alipay_config.gateway_url
            self.alipay_client_config.app_id = alipay_config.app_id
            self.alipay_client_config.app_private_key = alipay_config.get_private_key()
            self.alipay_client_config.alipay_public_key = alipay_config.get_public_key()
            self.alipay_client_config.sign_type = alipay_config.sign_type
            
            # 创建支付宝客户端
            self.alipay_client = DefaultAlipayClient(alipay_client_config=self.alipay_client_config)
            
            logger.info("支付宝客户端初始化成功")
            
        except Exception as e:
            logger.error(f"支付宝客户端初始化失败: {str(e)}")
            raise
    
    def get_auth_url(self, redirect_uri: str, state: str = None) -> str:
        """生成支付宝OAuth授权URL
        
        Args:
            redirect_uri: 授权回调地址
            state: 状态参数，用于防止CSRF攻击
            
        Returns:
            str: 授权URL
        """
        try:
            # URL编码回调地址
            encoded_redirect_uri = urllib.parse.quote(redirect_uri, safe='')
            
            # 构建授权URL参数
            params = {
                'app_id': alipay_config.app_id,
                'scope': alipay_config.scope,
                'redirect_uri': encoded_redirect_uri
            }
            
            # 添加state参数（可选）
            if state:
                params['state'] = state
            
            # 构建完整的授权URL
            query_string = urllib.parse.urlencode(params)
            auth_url = f"{alipay_config.oauth_gateway_url}?{query_string}"
            
            logger.info(f"生成授权URL: {auth_url}")
            return auth_url
            
        except Exception as e:
            logger.error(f"生成授权URL失败: {str(e)}")
            raise
    
    def get_access_token(self, auth_code: str) -> Dict[str, Any]:
        """使用授权码获取访问令牌
        
        Args:
            auth_code: 授权码
            
        Returns:
            Dict[str, Any]: 包含访问令牌信息的字典
        """
        try:
            # 创建获取令牌请求
            request = AlipaySystemOauthTokenRequest()
            request.grant_type = "authorization_code"
            request.code = auth_code
            
            # 执行请求
            response = self.alipay_client.execute(request)
            
            # 检查响应
            if hasattr(response, 'code') and response.code == '10000':
                token_info = {
                    'access_token': response.access_token,
                    'expires_in': int(response.expires_in),
                    'refresh_token': response.refresh_token,
                    're_expires_in': int(response.re_expires_in),
                    'user_id': getattr(response, 'user_id', None),
                    'open_id': getattr(response, 'open_id', None),
                    'auth_start': getattr(response, 'auth_start', None)
                }
                
                logger.info(f"获取访问令牌成功，用户ID: {token_info.get('user_id')}")
                return token_info
            else:
                error_msg = f"获取访问令牌失败: {getattr(response, 'msg', '未知错误')}"
                logger.error(error_msg)
                raise Exception(error_msg)
                
        except Exception as e:
            logger.error(f"获取访问令牌异常: {str(e)}")
            raise
    
    def get_user_info(self, access_token: str) -> Dict[str, Any]:
        """使用访问令牌获取用户信息
        
        Args:
            access_token: 访问令牌
            
        Returns:
            Dict[str, Any]: 用户信息字典
        """
        try:
            # 创建获取用户信息请求
            request = AlipayUserInfoShareRequest()
            
            # 执行请求
            response = self.alipay_client.execute(request, access_token)
            
            # 检查响应
            if hasattr(response, 'code') and response.code == '10000':
                user_info = {
                    'user_id': getattr(response, 'user_id', ''),
                    'open_id': getattr(response, 'open_id', ''),
                    'nick_name': getattr(response, 'nick_name', ''),
                    'avatar': getattr(response, 'avatar', ''),
                    'gender': getattr(response, 'gender', ''),
                    'city': getattr(response, 'city', ''),
                    'province': getattr(response, 'province', ''),
                    'country_code': getattr(response, 'country_code', ''),
                    'is_student_certified': getattr(response, 'is_student_certified', ''),
                    'user_type': getattr(response, 'user_type', ''),
                    'user_status': getattr(response, 'user_status', ''),
                    'is_certified': getattr(response, 'is_certified', ''),
                    'is_certify_grade_a': getattr(response, 'is_certify_grade_a', '')
                }
                
                logger.info(f"获取用户信息成功，用户: {user_info.get('nick_name', user_info.get('user_id'))}")
                return user_info
            else:
                error_msg = f"获取用户信息失败: {getattr(response, 'msg', '未知错误')}"
                logger.error(error_msg)
                raise Exception(error_msg)
                
        except Exception as e:
            logger.error(f"获取用户信息异常: {str(e)}")
            raise
    
    def refresh_access_token(self, refresh_token: str) -> Dict[str, Any]:
        """刷新访问令牌
        
        Args:
            refresh_token: 刷新令牌
            
        Returns:
            Dict[str, Any]: 新的访问令牌信息
        """
        try:
            # 创建刷新令牌请求
            request = AlipaySystemOauthTokenRequest()
            request.grant_type = "refresh_token"
            request.refresh_token = refresh_token
            
            # 执行请求
            response = self.alipay_client.execute(request)
            
            # 检查响应
            if hasattr(response, 'code') and response.code == '10000':
                token_info = {
                    'access_token': response.access_token,
                    'expires_in': int(response.expires_in),
                    'refresh_token': response.refresh_token,
                    're_expires_in': int(response.re_expires_in),
                    'user_id': getattr(response, 'user_id', None),
                    'open_id': getattr(response, 'open_id', None),
                    'auth_start': getattr(response, 'auth_start', None)
                }
                
                logger.info("刷新访问令牌成功")
                return token_info
            else:
                error_msg = f"刷新访问令牌失败: {getattr(response, 'msg', '未知错误')}"
                logger.error(error_msg)
                raise Exception(error_msg)
                
        except Exception as e:
            logger.error(f"刷新访问令牌异常: {str(e)}")
            raise