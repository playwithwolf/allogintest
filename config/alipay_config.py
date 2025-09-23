# 支付宝配置 - 直接硬编码，不依赖环境变量

import os
from pathlib import Path

class AlipayConfig:
    """支付宝配置类"""
    
    def __init__(self):
        # 支付宝应用配置 - 直接硬编码
        self.app_id = "9021000151657305"
        # 沙盒环境私钥 - PKCS#1格式（非Java环境使用PKCS#1，Java环境使用PKCS#8）
        self.app_private_key = "MIIEpQIBAAKCAQEAnNg6Lz+dffDTrtyuhuJzhdwoW2VBAzRfMz6qFlzDVmpyukJFgrP+axHTvkVLP/qYPGk6GmJHP9RotMk4i19efzwR7XY0fbp89sDMXqSQlRvOIxPgKGd6GavXvWcl9xtaPpFyoprBYg+E5Iybv5FgEgCDw4g2TDKAch39wfDfwc5PVOy8duncQudghnHi09Jd+N2lLQ4B+asKKuqSDuosov1TXo0Tl8VacUybJO3CZjjt/tJr2sbmDblE1ITlP4B+pLow0vZ+IhEw2rwMTbdSThO8qDt3llY2BzBHEFGcRs5dn5FlQeTSz+vQT4VIV8fVuIqn0DTjBIeERYo/7HbPrQIDAQABAoIBAQCR3BhIJl39aEBEBuCbee67FuHFFSXfqA28p1MgFsZmD/p/su/XvDInOl3zPZfceNyomac6MBlYh92T+umF23wS0TdO4TWxkwNxqhylC1+V+1S5lFtK1+haBVBNyKYq5poHQ9Ya19ZtrkcFEKoq/jQcqbPf3EW6mOCQv8lkWfCM1yZa3bA6VQMOpRg0RMUTSnnCoASx9cRDQPoZt5ecFUZ4SDZJaRLZ072w/ewT8T5hxa11GMSRP5mT9oE/zOIW62k4+Fn0vv4I8rTzg3tNPsJJOiUiLfRaGtDrPPhh4vBcqaUUSIc7dYMhtz66yvoJULiQz/FtWp4TmzoELL2ammahAoGBAPb3T1T7fOkl5vEAi8g2a4ukn4aEIGLajXpni9AFkPpguwZCvz4txVYJ/QDAAN30ZuZnu5ZdGRABnCKzkBbLA1jQS3PMuqwuFN8cwPSZ1djEAb6Q9PhJkwBn9zr5u6WGztxokPjrvcPonAoujz1XV6iqO6avcxKxQ7c9Trap7uk1AoGBAKKU++U3SC6jYAhSllQ+YfuIxxJOglOMYxn3DYRn5SIwqBULLFp+rQ7FbROp6TDC1kEXC00Xm/1OSlDZIjI14Vav2nP3hjFcTHig0wFJU1Ppl+LhKnQPNagoTn3ger6SW1e9neWqD2youXlyVgwgTZ/Oyuw4sd8eNn/6lz1WNJOZAoGBAIgkjXcrrBBa9JSm2GfmmCLC/a4J6FCWaqevrUNfziw4ZuFsqkB8uuxTVUW0ksXIlXEufhrF96r7ODdpBWWLRK0RJocPtVh1jsvv7e7pXxm/87Y58tFsvbzbk07PnMIDLsYSXtjaHCKDeIGkaRJHs+sm7PtWfPkw/0NkaKAJzcqBAoGBAKBb9KycP00JBdKPqwkC0uAng7rRxwgjQyg8HpAHbeCwP0kqUSAdLBKStkib4Y6fznY7BYGPlONe0jw2Pt1peY5oOz8A2NJc6GxerGDrcw4kLBSy5I2+5ryqrOjJfifz8bZ0J4Z8m2Qgc3iPRsIFJqtGa65dKUwZ38WRZJUyLv+ZAoGAdoY4H/WIB0q73cQs3OyMRg5vneQzaJsSnv5RYq2whz1hbJNQ29UHhDk8Sov7LeEwwM3NOJoa0hlcV3uIp90+IRO0qdli5JUCChAXDJhVdhMDDtApzqd9ejASEUWjrW62sVP/zc5t8o19VXCf7rlbRCUL0UxNg4qdmi4bDg/JblA="
        self.alipay_public_key = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAqRUOzanbew6pZy9TriP6DmqyrMRuGqJ6KfbFBHzRvsPc+QY0D3kOnc+TIhJBi+ymfJPty2RdU+gZIJaoZRxHmHyKEdknz5HA/Lv2jHm6GK6wF3WcROb64k99CgsIUesIVCMjZ7r7RQEmEvsz+R4gAgh5kjhGAhGNO3TJK3i2obqPBQBxYdSKDxLryFhWZZWMChIhhwUpZtraJxQWqNOIz24yIhugdlAALYyvTAc8zSCftLr/Imp05apkHT36eKPo1gWbEHiB94haNvwyWqac0AI7lwYq+kLPudp+JYMg5AGrmFLnYwP+7XhMrmk483OfA9yoF4UObTaPBSQ91C7JGQIDAQAB"
        
        # 支付宝网关地址 - 沙盒环境
        self.gateway_url = "https://openapi-sandbox.dl.alipaydev.com/gateway.do"
        
        # 签名配置
        self.sign_type = "RSA2"
        self.charset = "utf-8"
        self.format = "json"
        self.version = "1.0"
        
        # OAuth授权配置 - 沙盒环境
        self.oauth_gateway_url = "https://openauth-sandbox.dl.alipaydev.com/oauth2/publicAppAuthorize.htm"
        
        # 授权范围
        self.scope = "auth_user"
    
    def validate_config(self) -> bool:
        """验证配置是否完整"""
        required_fields = ["app_id", "app_private_key", "alipay_public_key"]
        for field in required_fields:
            if not getattr(self, field):
                raise ValueError(f"缺少必要配置: {field}")
        return True
    
    # def get_private_key(self) -> str:
    #     """获取私钥内容"""
    #     # 读取私钥文件内容
    #     # current_dir = Path(__file__).parent.parent
    #     # private_key_path = current_dir / "keys" / "app_private_key.pem"
    #     # with open(private_key_path, 'r', encoding='utf-8') as f:
    #     #     return f.read().strip()
    #     private_key = 'MIIEpQIBAAKCAQEAnNg6Lz+dffDTrtyuhuJzhdwoW2VBAzRfMz6qFlzDVmpyukJFgrP+axHTvkVLP/qYPGk6GmJHP9RotMk4i19efzwR7XY0fbp89sDMXqSQlRvOIxPgKGd6GavXvWcl9xtaPpFyoprBYg+E5Iybv5FgEgCDw4g2TDKAch39wfDfwc5PVOy8duncQudghnHi09Jd+N2lLQ4B+asKKuqSDuosov1TXo0Tl8VacUybJO3CZjjt/tJr2sbmDblE1ITlP4B+pLow0vZ+IhEw2rwMTbdSThO8qDt3llY2BzBHEFGcRs5dn5FlQeTSz+vQT4VIV8fVuIqn0DTjBIeERYo/7HbPrQIDAQABAoIBAQCR3BhIJl39aEBEBuCbee67FuHFFSXfqA28p1MgFsZmD/p/su/XvDInOl3zPZfceNyomac6MBlYh92T+umF23wS0TdO4TWxkwNxqhylC1+V+1S5lFtK1+haBVBNyKYq5poHQ9Ya19ZtrkcFEKoq/jQcqbPf3EW6mOCQv8lkWfCM1yZa3bA6VQMOpRg0RMUTSnnCoASx9cRDQPoZt5ecFUZ4SDZJaRLZ072w/ewT8T5hxa11GMSRP5mT9oE/zOIW62k4+Fn0vv4I8rTzg3tNPsJJOiUiLfRaGtDrPPhh4vBcqaUUSIc7dYMhtz66yvoJULiQz/FtWp4TmzoELL2ammahAoGBAPb3T1T7fOkl5vEAi8g2a4ukn4aEIGLajXpni9AFkPpguwZCvz4txVYJ/QDAAN30ZuZnu5ZdGRABnCKzkBbLA1jQS3PMuqwuFN8cwPSZ1djEAb6Q9PhJkwBn9zr5u6WGztxokPjrvcPonAoujz1XV6iqO6avcxKxQ7c9Trap7uk1AoGBAKKU++U3SC6jYAhSllQ+YfuIxxJOglOMYxn3DYRn5SIwqBULLFp+rQ7FbROp6TDC1kEXC00Xm/1OSlDZIjI14Vav2nP3hjFcTHig0wFJU1Ppl+LhKnQPNagoTn3ger6SW1e9neWqD2youXlyVgwgTZ/Oyuw4sd8eNn/6lz1WNJOZAoGBAIgkjXcrrBBa9JSm2GfmmCLC/a4J6FCWaqevrUNfziw4ZuFsqkB8uuxTVUW0ksXIlXEufhrF96r7ODdpBWWLRK0RJocPtVh1jsvv7e7pXxm/87Y58tFsvbzbk07PnMIDLsYSXtjaHCKDeIGkaRJHs+sm7PtWfPkw/0NkaKAJzcqBAoGBAKBb9KycP00JBdKPqwkC0uAng7rRxwgjQyg8HpAHbeCwP0kqUSAdLBKStkib4Y6fznY7BYGPlONe0jw2Pt1peY5oOz8A2NJc6GxerGDrcw4kLBSy5I2+5ryqrOjJfifz8bZ0J4Z8m2Qgc3iPRsIFJqtGa65dKUwZ38WRZJUyLv+ZAoGAdoY4H/WIB0q73cQs3OyMRg5vneQzaJsSnv5RYq2whz1hbJNQ29UHhDk8Sov7LeEwwM3NOJoa0hlcV3uIp90+IRO0qdli5JUCChAXDJhVdhMDDtApzqd9ejASEUWjrW62sVP/zc5t8o19VXCf7rlbRCUL0UxNg4qdmi4bDg/JblA='
    #         private_key = f"-----BEGIN RSA PRIVATE KEY-----\n{private_key}\n-----END RSA PRIVATE KEY-----"
    #     return private_key
    
    # def get_public_key(self) -> str:
    #     """获取公钥内容"""
    #     # 读取公钥文件内容
    #     # current_dir = Path(__file__).parent.parent
    #     # public_key_path = current_dir / "keys" / "alipay_public_key.pem"
    #     # with open(public_key_path, 'r', encoding='utf-8') as f:
    #     #     return f.read().strip()
    #     public_key ='MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAnNg6Lz+dffDTrtyuhuJzhdwoW2VBAzRfMz6qFlzDVmpyukJFgrP+axHTvkVLP/qYPGk6GmJHP9RotMk4i19efzwR7XY0fbp89sDMXqSQlRvOIxPgKGd6GavXvWcl9xtaPpFyoprBYg+E5Iybv5FgEgCDw4g2TDKAch39wfDfwc5PVOy8duncQudghnHi09Jd+N2lLQ4B+asKKuqSDuosov1TXo0Tl8VacUybJO3CZjjt/tJr2sbmDblE1ITlP4B+pLow0vZ+IhEw2rwMTbdSThO8qDt3llY2BzBHEFGcRs5dn5FlQeTSz+vQT4VIV8fVuIqn0DTjBIeERYo/7HbPrQIDAQAB'
    #     public_key = f"-----BEGIN PUBLIC KEY-----\n{public_key}\n-----END PUBLIC KEY-----"
    #     return public_key
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