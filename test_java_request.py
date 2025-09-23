#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试Java客户端请求格式
模拟修改后的Java代码发送的请求
"""

import requests
import json

def test_java_authinfo_request():
    """测试Java客户端的AuthInfo请求格式"""
    
    # 服务器地址
    server_url = "http://localhost:8000/api/auth/authinfo"
    
    # 模拟Java代码发送的JSON格式（修改后）
    request_data = {
        "pid": "2088151008240524",  # Java代码中的appId参数
        "rsa2": True  # Java代码中的rsa2参数
    }
    
    print(f"发送请求到: {server_url}")
    print(f"请求数据: {json.dumps(request_data, indent=2)}")
    
    try:
        # 发送POST请求
        response = requests.post(
            server_url,
            json=request_data,
            headers={
                "Content-Type": "application/json",
                "User-Agent": "Java-Android-Client/1.0"
            },
            timeout=10
        )
        
        print(f"\n响应状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        
        if response.status_code == 200:
            response_data = response.json()
            print(f"\n响应数据: {json.dumps(response_data, indent=2, ensure_ascii=False)}")
            
            if response_data.get('success'):
                auth_info = response_data.get('data', {}).get('authInfo')
                print(f"\n✅ 成功获取AuthInfo: {auth_info[:100]}...")
                return True
            else:
                print(f"\n❌ 服务器返回失败: {response_data.get('message')}")
                return False
        else:
            print(f"\n❌ HTTP错误: {response.status_code}")
            print(f"响应内容: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"\n❌ 请求异常: {e}")
        return False
    except json.JSONDecodeError as e:
        print(f"\n❌ JSON解析异常: {e}")
        print(f"响应内容: {response.text}")
        return False
    except Exception as e:
        print(f"\n❌ 未知异常: {e}")
        return False

if __name__ == "__main__":
    print("=== 测试Java客户端AuthInfo请求格式 ===")
    success = test_java_authinfo_request()
    
    if success:
        print("\n🎉 测试通过！Java客户端请求格式正确")
    else:
        print("\n💥 测试失败！需要进一步检查")