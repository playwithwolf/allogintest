from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserInfo(BaseModel):
    """用户信息模型"""
    user_id: str  # 支付宝用户ID
    open_id: Optional[str] = None  # 支付宝用户唯一标识
    nick_name: Optional[str] = None  # 用户昵称
    avatar: Optional[str] = None  # 用户头像
    gender: Optional[str] = None  # 用户性别 m:男性 f:女性
    city: Optional[str] = None  # 用户所在城市
    province: Optional[str] = None  # 用户所在省份
    country_code: Optional[str] = None  # 国家码
    is_student_certified: Optional[str] = None  # 是否学生认证
    user_type: Optional[str] = None  # 用户类型
    user_status: Optional[str] = None  # 用户状态
    is_certified: Optional[str] = None  # 是否实名认证
    is_certify_grade_a: Optional[str] = None  # 是否A级认证

class TokenInfo(BaseModel):
    """访问令牌信息模型"""
    access_token: str  # 访问令牌
    expires_in: int  # 访问令牌有效期（秒）
    refresh_token: str  # 刷新令牌
    re_expires_in: int  # 刷新令牌有效期（秒）
    user_id: Optional[str] = None  # 支付宝用户ID
    open_id: Optional[str] = None  # 支付宝用户唯一标识
    auth_start: Optional[str] = None  # 授权开始时间

class LoginResponse(BaseModel):
    """登录响应模型"""
    success: bool
    message: str
    user_info: Optional[UserInfo] = None
    token_info: Optional[TokenInfo] = None

class AuthUrlRequest(BaseModel):
    """授权URL请求模型"""
    redirect_uri: str
    state: Optional[str] = None

class AuthCallbackRequest(BaseModel):
    """授权回调请求模型"""
    auth_code: str
    state: Optional[str] = None
    app_id: Optional[str] = None
    scope: Optional[str] = None

class ApiResponse(BaseModel):
    """通用API响应模型"""
    success: bool
    message: str
    data: Optional[dict] = None
    error_code: Optional[str] = None