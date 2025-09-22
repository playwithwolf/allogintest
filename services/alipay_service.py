import urllib.parse
import logging
import json
import time
import random
import base64
from typing import Dict, Any
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.request.AlipaySystemOauthTokenRequest import AlipaySystemOauthTokenRequest
from alipay.aop.api.request.AlipayUserInfoShareRequest import AlipayUserInfoShareRequest
from alipay.aop.api.util import SignatureUtils
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
            
            # 调试：检查配置参数类型
            logger.info(f"app_id类型: {type(alipay_config.app_id)}, 值: {alipay_config.app_id}")
            logger.info(f"sign_type类型: {type(alipay_config.sign_type)}, 值: {alipay_config.sign_type}")
            logger.info(f"gateway_url类型: {type(alipay_config.gateway_url)}, 值: {alipay_config.gateway_url}")
            
            # 创建支付宝客户端配置
            self.alipay_client_config = AlipayClientConfig()
            self.alipay_client_config.server_url = str(alipay_config.gateway_url)
            self.alipay_client_config.app_id = str(alipay_config.app_id)
            self.alipay_client_config.app_private_key = str(alipay_config.get_private_key())
            self.alipay_client_config.alipay_public_key = str(alipay_config.get_public_key())
            self.alipay_client_config.sign_type = str(alipay_config.sign_type)

            logger.info(self.alipay_client_config.app_private_key)

            logger.info(self.alipay_client_config.alipay_public_key)
            
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
            # 构建授权URL参数 - redirect_uri不需要预先编码
            params = {
                'app_id': alipay_config.app_id,
                'scope': alipay_config.scope,
                'redirect_uri': redirect_uri
            }
            
            # 添加state参数（可选）
            if state:
                params['state'] = state
            
            # 构建完整的授权URL - urlencode会自动处理编码
            query_string = urllib.parse.urlencode(params)
            auth_url = f"{alipay_config.oauth_gateway_url}?{query_string}"
            
            logger.info(f"生成授权URL: {auth_url}")
            return auth_url
            
        except Exception as e:
            logger.error(f"生成授权URL失败: {str(e)}")
            raise
    
    # def get_access_token(self, auth_code: str) -> Dict[str, Any]:
    #     """使用授权码获取访问令牌
        
    #     Args:
    #         auth_code: 授权码
            
    #     Returns:
    #         Dict[str, Any]: 包含访问令牌信息的字典
    #     """
    #     try:
    #         # 创建获取令牌请求
    #         request = AlipaySystemOauthTokenRequest()
    #         request.grant_type = "authorization_code"
    #         request.code = auth_code
            
    #         # 调试：检查请求参数类型
    #         logger.info(f"grant_type类型: {type(request.grant_type)}, 值: {request.grant_type}")
    #         logger.info(f"code类型: {type(request.code)}, 值: {request.code}")
    #         logger.info(f"auth_code参数类型: {type(auth_code)}, 值: {auth_code}")
            
    #         # 执行请求
    #         logger.info("开始执行支付宝API请求...")
    #         logger.info(f"开始获取访问令牌，授权码: {auth_code}")
    #         response = self.alipay_client.execute(request)
    #         logger.info(f"支付宝API响应: {response}")
    #         logger.info(f"支付宝API响应  response.code : { response.code}")
    #         # 记录完整的响应信息用于调试
    #         # logger.info(f"支付宝API响应: code={getattr(response, 'code', None)}, msg={getattr(response, 'msg', None)}, sub_code={getattr(response, 'sub_code', None)}, sub_msg={getattr(response, 'sub_msg', None)}")
            
    #         # 检查响应
    #         if hasattr(response, 'code') and response.code == '10000':
    #             # 安全地转换数值类型字段
    #             def safe_int(value, default=0):
    #                 try:
    #                     if isinstance(value, (list, tuple)) and len(value) > 0:
    #                         return int(value[0])
    #                     return int(value) if value is not None else default
    #                 except (ValueError, TypeError):
    #                     return default
                
    #             token_info = {
    #                 'access_token': response.access_token,
    #                 'expires_in': safe_int(getattr(response, 'expires_in', None)),
    #                 'refresh_token': response.refresh_token,
    #                 're_expires_in': safe_int(getattr(response, 're_expires_in', None)),
    #                 'user_id': getattr(response, 'user_id', None),
    #                 'open_id': getattr(response, 'open_id', None),
    #                 'auth_start': getattr(response, 'auth_start', None)
    #             }
                
    #             logger.info(f"获取访问令牌成功，用户ID: {token_info.get('user_id')}")
    #             return token_info
    #         else:
    #             # 详细的错误信息
    #             error_code = getattr(response, 'code', 'unknown')
    #             error_msg = getattr(response, 'msg', '未知错误')
    #             sub_code = getattr(response, 'sub_code', None)
    #             sub_msg = getattr(response, 'sub_msg', None)
                
    #             detailed_error = f"获取访问令牌失败 - 错误码: {error_code}, 错误信息: {error_msg}"
    #             if sub_code:
    #                 detailed_error += f", 子错误码: {sub_code}, 子错误信息: {sub_msg}"
                
    #             logger.error(detailed_error)
    #             raise Exception(detailed_error)
                
    #     except Exception as e:
    #         logger.error(f"获取访问令牌异常: {str(e)}")
    #         raise
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
            
            # 调试：检查请求参数类型
            logger.info(f"grant_type类型: {type(request.grant_type)}, 值: {request.grant_type}")
            logger.info(f"code类型: {type(request.code)}, 值: {request.code}")
            logger.info(f"auth_code参数类型: {type(auth_code)}, 值: {auth_code}")
            
            # 执行请求
            logger.info("开始执行支付宝API请求...")
            logger.info(f"开始获取访问令牌，授权码: {auth_code}")
            response = self.alipay_client.execute(request)
            logger.info(f"支付宝API响应: {response}")
            
            # 解析响应为字典
            if isinstance(response, str):
                try:
                    response = json.loads(response)
                except json.JSONDecodeError as e:
                    logger.error(f"解析响应失败: {e}")
                    raise Exception(f"解析响应失败: {e}")
            
            # 检查响应
            if isinstance(response, dict) and 'access_token' in response:
                # 安全地转换数值类型字段
                def safe_int(value, default=0):
                    try:
                        if isinstance(value, (list, tuple)) and len(value) > 0:
                            return int(value[0])
                        return int(value) if value is not None else default
                    except (ValueError, TypeError):
                        return default
                
                token_info = {
                    'access_token': response.get('access_token'),
                    'expires_in': safe_int(response.get('expires_in')),
                    'refresh_token': response.get('refresh_token'),
                    're_expires_in': safe_int(response.get('re_expires_in')),
                    'user_id': response.get('user_id'),
                    'open_id': response.get('open_id'),
                    'auth_start': response.get('auth_start')
                }
                
                logger.info(f"获取访问令牌成功，用户ID: {token_info.get('user_id')}")
                return token_info
            else:
                # 详细的错误信息
                error_code = response.get('code', 'unknown')
                error_msg = response.get('msg', '未知错误')
                sub_code = response.get('sub_code', None)
                sub_msg = response.get('sub_msg', None)
                
                detailed_error = f"获取访问令牌失败 - 错误码: {error_code}, 错误信息: {error_msg}"
                if sub_code:
                    detailed_error += f", 子错误码: {sub_code}, 子错误信息: {sub_msg}"
                
                logger.error(detailed_error)
                raise Exception(detailed_error)
                
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
            
            # 设置访问令牌到udf_params中
            udf_params = dict()
            udf_params['auth_token'] = access_token
            request.udf_params = udf_params
            
            # 执行请求
            response = self.alipay_client.execute(request)
            
            # 解析响应
            if isinstance(response, str):
                try:
                    response_dict = json.loads(response)
                    
                    # 检查是否是嵌套格式
                    if 'alipay_user_info_share_response' in response_dict:
                        response_data = response_dict['alipay_user_info_share_response']
                    else:
                        # 直接的响应格式
                        response_data = response_dict
                    
                    if response_data.get('code') == '10000':
                        user_info = {
                            'user_id': response_data.get('user_id', ''),
                            'open_id': response_data.get('open_id', ''),
                            'nick_name': response_data.get('nick_name', response_data.get('user_name', '')),
                            'avatar': response_data.get('avatar', ''),
                            'gender': response_data.get('gender', ''),
                            'city': response_data.get('city', ''),
                            'province': response_data.get('province', ''),
                            'country_code': response_data.get('country_code', ''),
                            'is_student_certified': response_data.get('is_student_certified', ''),
                            'user_type': response_data.get('user_type', ''),
                            'user_status': response_data.get('user_status', ''),
                            'is_certified': response_data.get('is_certified', ''),
                            'is_certify_grade_a': response_data.get('is_certify_grade_a', ''),
                            'email': response_data.get('email', ''),
                            'display_name': response_data.get('display_name', ''),
                            'age': response_data.get('age', ''),
                            'cert_no': response_data.get('cert_no', ''),
                            'cert_type': response_data.get('cert_type', '')
                        }
                        
                        logger.info(f"获取用户信息成功，用户: {user_info.get('nick_name', user_info.get('user_id'))}")
                        return user_info
                    else:
                        error_msg = f"获取用户信息失败: {response_data.get('msg', '未知错误')}"
                        logger.error(error_msg)
                        raise Exception(error_msg)
                        
                except json.JSONDecodeError as e:
                    logger.error(f"解析响应失败: {e}")
                    raise Exception(f"解析响应失败: {e}")
            else:
                # 检查响应对象
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
                # 安全地转换数值类型字段
                def safe_int(value, default=0):
                    try:
                        if isinstance(value, (list, tuple)) and len(value) > 0:
                            return int(value[0])
                        return int(value) if value is not None else default
                    except (ValueError, TypeError):
                        return default
                
                token_info = {
                    'access_token': response.access_token,
                    'expires_in': safe_int(getattr(response, 'expires_in', None)),
                    'refresh_token': response.refresh_token,
                    're_expires_in': safe_int(getattr(response, 're_expires_in', None)),
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
    
    def build_auth_info_map(self, pid: str, target_id: str = None, rsa2: bool = True) -> Dict[str, str]:
        """构造授权参数列表
        参考Android SDK的OrderInfoUtil2_0.buildAuthInfoMap方法
        
        Args:
            pid: 商户签约拿到的pid，如：2088102123816631
            target_id: 商户唯一标识，如果不提供则自动生成
            rsa2: 是否使用RSA2签名，默认True
            
        Returns:
            Dict[str, str]: 授权参数字典
        """
        # 如果没有提供target_id，则自动生成
        if not target_id:
            target_id = f"auth_{int(time.time() * 1000)}_{random.randint(1000, 9999)}"
        
        key_values = {
            # 商户签约拿到的app_id
            "app_id": alipay_config.app_id,
            
            # 商户签约拿到的pid
            "pid": pid,
            
            # 服务接口名称，固定值
            "apiname": "com.alipay.account.auth",
            
            # 服务接口名称，固定值
            "methodname": "alipay.open.auth.sdk.code.get",
            
            # 商户类型标识，固定值
            "app_name": "mc",
            
            # 业务类型，固定值
            "biz_type": "openservice",
            
            # 产品码，固定值
            "product_id": "APP_FAST_LOGIN",
            
            # 授权范围，固定值
            "scope": "kuaijie",
            
            # 商户唯一标识
            "target_id": target_id,
            
            # 授权类型，固定值
            "auth_type": "AUTHACCOUNT",
            
            # 签名类型
            "sign_type": "RSA2" if rsa2 else "RSA"
        }
        
        return key_values
    
    def build_order_param(self, param_map: Dict[str, str]) -> str:
        """构造订单参数信息
        参考Android SDK的OrderInfoUtil2_0.buildOrderParam方法
        
        Args:
            param_map: 参数字典
            
        Returns:
            str: 参数字符串
        """
        keys = list(param_map.keys())
        
        sb = []
        for i in range(len(keys) - 1):
            key = keys[i]
            value = param_map[key]
            sb.append(self._build_key_value(key, value, True))
            sb.append("&")
        
        tail_key = keys[-1]
        tail_value = param_map[tail_key]
        sb.append(self._build_key_value(tail_key, tail_value, True))
        
        return "".join(sb)
    
    def _build_key_value(self, key: str, value: str, is_encode: bool) -> str:
        """拼接键值对
        
        Args:
            key: 键
            value: 值
            is_encode: 是否编码
            
        Returns:
            str: 键值对字符串
        """
        sb = [key, "="]
        if is_encode:
            try:
                sb.append(urllib.parse.quote(value, safe=''))
            except Exception:
                sb.append(value)
        else:
            sb.append(value)
        return "".join(sb)
    
    def get_sign(self, param_map: Dict[str, str], rsa_key: str, rsa2: bool = True) -> str:
        """对支付参数信息进行签名
        参考Android SDK的OrderInfoUtil2_0.getSign方法
        
        Args:
            param_map: 待签名授权信息
            rsa_key: RSA私钥
            rsa2: 是否使用RSA2签名
            
        Returns:
            str: 签名字符串
        """
        keys = list(param_map.keys())
        # key排序
        keys.sort()
        
        auth_info = []
        for i in range(len(keys) - 1):
            key = keys[i]
            value = param_map[key]
            auth_info.append(self._build_key_value(key, value, False))
            auth_info.append("&")
        
        tail_key = keys[-1]
        tail_value = param_map[tail_key]
        auth_info.append(self._build_key_value(tail_key, tail_value, False))
        
        auth_info_str = "".join(auth_info)
        
        # 使用cryptography库进行RSA签名
        try:
            # 处理PKCS#1格式的私钥（支付宝非Java环境使用PKCS#1格式）
            # 如果私钥没有PEM头部，添加PKCS#1格式的头部和尾部
            if not rsa_key.startswith('-----BEGIN'):
                # Base64字符串，添加PKCS#1格式的PEM头部
                pem_private_key = f"-----BEGIN RSA PRIVATE KEY-----\n{rsa_key}\n-----END RSA PRIVATE KEY-----"
            else:
                pem_private_key = rsa_key
            
            # 加载PKCS#1格式的私钥
            private_key = serialization.load_pem_private_key(
                pem_private_key.encode('utf-8'),
                password=None
            )
            
            # 进行签名
            if rsa2:
                # RSA2使用SHA256
                signature = private_key.sign(
                    auth_info_str.encode('utf-8'),
                    padding.PKCS1v15(),
                    hashes.SHA256()
                )
            else:
                # RSA使用SHA1
                signature = private_key.sign(
                    auth_info_str.encode('utf-8'),
                    padding.PKCS1v15(),
                    hashes.SHA1()
                )
            
            # Base64编码签名结果
            ori_sign = base64.b64encode(signature).decode('utf-8')
            
        except Exception as e:
            logger.error(f"签名失败: {str(e)}")
            raise
        
        # URL编码签名结果
        try:
            encoded_sign = urllib.parse.quote(ori_sign, safe='')
        except Exception:
            encoded_sign = ori_sign
        
        return f"sign={encoded_sign}"
    
    def generate_auth_info(self, pid: str, target_id: str = None, rsa2: bool = True) -> str:
        """生成完整的authInfo字符串
        供Android应用调用，生成用于支付宝授权的完整参数字符串
        
        Args:
            pid: 商户签约拿到的pid
            target_id: 商户唯一标识，如果不提供则自动生成
            rsa2: 是否使用RSA2签名，默认True
            
        Returns:
            str: 完整的authInfo字符串
        """
        try:
            # 构建授权参数
            auth_info_map = self.build_auth_info_map(pid, target_id, rsa2)
            
            # 构建参数字符串
            info = self.build_order_param(auth_info_map)
            
            # 获取私钥 - 直接使用原始私钥字符串，不添加格式化标记
            private_key = alipay_config.app_private_key
            
            # 生成签名
            sign = self.get_sign(auth_info_map, private_key, rsa2)
            
            # 拼接完整的authInfo
            auth_info = f"{info}&{sign}"
            
            logger.info(f"生成authInfo成功，target_id: {auth_info_map.get('target_id')}")
            return auth_info
            
        except Exception as e:
            logger.error(f"生成authInfo失败: {str(e)}")
            raise