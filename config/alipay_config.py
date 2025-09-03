from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional

class AlipayConfig(BaseSettings):
    """支付宝配置类"""
    
    # 支付宝应用配置
    app_id: str = Field(default="", description="支付宝应用ID")
    app_private_key: str = Field(default="", description="应用私钥")
    alipay_public_key: str = Field(default="", description="支付宝公钥")
    
    # 支付宝网关地址
    gateway_url: str = Field(default="https://openapi.alipaydev.com/gateway.do", description="支付宝网关地址")
    
    # 签名配置
    sign_type: str = Field(default="RSA2", description="签名类型")
    charset: str = Field(default="utf-8", description="字符集")
    format: str = Field(default="json", description="数据格式")
    version: str = Field(default="1.0", description="API版本")
    
    # OAuth授权配置
    oauth_gateway_url: str = Field(default="https://openauth-sandbox.dl.alipaydev.com/oauth2/publicAppAuthorize.htm", description="OAuth授权网关地址")
    
    # 授权范围
    scope: str = Field(default="auth_user", description="授权范围")
    
    class Config:
        env_prefix = "ALIPAY_"
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"  # 忽略额外字段
    
    def validate_config(self) -> bool:
        """验证配置是否完整"""
        required_fields = ["app_id", "app_private_key", "alipay_public_key"]
        for field in required_fields:
            if not getattr(self, field):
                raise ValueError(f"缺少必要配置: {field}")
        return True
    
    def get_private_key(self) -> str:
        """获取格式化的私钥"""
        private_key = self.app_private_key.strip()
        if not private_key.startswith("-----BEGIN RSA PRIVATE KEY-----"):
            private_key = f"-----BEGIN RSA PRIVATE KEY-----\n{private_key}\n-----END RSA PRIVATE KEY-----"
        return private_key
    
    def get_public_key(self) -> str:
        """获取格式化的公钥"""
        public_key = self.alipay_public_key.strip()
        if not public_key.startswith("-----BEGIN PUBLIC KEY-----"):
            public_key = f"-----BEGIN PUBLIC KEY-----\n{public_key}\n-----END PUBLIC KEY-----"
        return public_key

# 全局配置实例
alipay_config = AlipayConfig()