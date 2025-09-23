"""
授权频率限制器
防止频繁调用支付宝授权接口，避免触发限流
"""

import time
from typing import Dict, Optional
from threading import Lock

class RateLimiter:
    """简单的频率限制器"""
    
    def __init__(self, max_requests: int = 5, time_window: int = 60):
        """
        初始化频率限制器
        
        Args:
            max_requests: 时间窗口内最大请求数
            time_window: 时间窗口（秒）
        """
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests: Dict[str, list] = {}
        self.lock = Lock()
    
    def is_allowed(self, key: str) -> bool:
        """
        检查是否允许请求
        
        Args:
            key: 请求标识（如IP地址、用户ID等）
            
        Returns:
            bool: 是否允许请求
        """
        with self.lock:
            current_time = time.time()
            
            # 获取该key的请求历史
            if key not in self.requests:
                self.requests[key] = []
            
            request_times = self.requests[key]
            
            # 清理过期的请求记录
            cutoff_time = current_time - self.time_window
            request_times[:] = [t for t in request_times if t > cutoff_time]
            
            # 检查是否超过限制
            if len(request_times) >= self.max_requests:
                return False
            
            # 记录当前请求
            request_times.append(current_time)
            return True
    
    def get_remaining_time(self, key: str) -> Optional[int]:
        """
        获取距离下次可以请求的剩余时间
        
        Args:
            key: 请求标识
            
        Returns:
            Optional[int]: 剩余时间（秒），如果可以立即请求则返回None
        """
        with self.lock:
            if key not in self.requests or len(self.requests[key]) < self.max_requests:
                return None
            
            current_time = time.time()
            oldest_request = min(self.requests[key])
            remaining = self.time_window - (current_time - oldest_request)
            
            return max(0, int(remaining))

# 全局频率限制器实例
# 每分钟最多5次授权请求
auth_rate_limiter = RateLimiter(max_requests=5, time_window=60)