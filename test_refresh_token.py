#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 refresh_token API 接口
"""

import requests
import json

def test_refresh_token():
    """测试刷新令牌接口"""
    url = "http://localhost:8000/api/auth/refresh"
    
    # 模拟一个 refresh_token（实际使用时需要从授权流程中获取）
    test_data = {
        "refresh_token": "test_refresh_token_123456"
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=test_data, headers=headers)
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 接口调用成功")
            print(f"响应数据: {json.dumps(result, indent=2, ensure_ascii=False)}")
        else:
            print("❌ 接口调用失败")
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")

def test_rate_limit():
    """测试频率限制功能"""
    url = "http://localhost:8000/api/auth/authinfo/2088151008240524"
    
    print("测试频率限制功能...")
    for i in range(7):  # 超过限制的 5 次
        try:
            response = requests.get(url)
            print(f"第 {i+1} 次请求 - 状态码: {response.status_code}")
            if response.status_code == 429:
                result = response.json()
                print(f"触发限流: {result}")
                break
        except Exception as e:
            print(f"请求异常: {e}")

if __name__ == "__main__":
    print("=== 测试 refresh_token 接口 ===")
    test_refresh_token()
    
    print("\n=== 测试频率限制 ===")
    test_rate_limit()