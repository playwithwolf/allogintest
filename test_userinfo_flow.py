#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试完整的用户信息获取流程
模拟Java客户端通过authCode获取用户信息的完整流程
"""

import requests
import json
import time

def test_userinfo_api():
    """测试用户信息获取API"""
    
    # 服务器地址
    server_url = "http://localhost:8000"
    
    # 模拟的authCode（实际应用中由支付宝SDK返回）
    # 注意：这是一个模拟的authCode，实际测试需要真实的授权码
    test_auth_code = "test_auth_code_12345"
    
    print("=" * 60)
    print("测试用户信息获取流程")
    print("=" * 60)
    
    # 1. 测试获取用户信息接口
    print("\n1. 测试 /api/auth/userinfo 接口")
    print(f"发送请求到: {server_url}/api/auth/userinfo")
    
    # 构建请求数据（模拟Java客户端发送的格式）
    request_data = {
        "authCode": test_auth_code
    }
    
    print(f"请求数据: {json.dumps(request_data, indent=2, ensure_ascii=False)}")
    
    try:
        # 发送POST请求
        response = requests.post(
            f"{server_url}/api/auth/userinfo",
            json=request_data,
            headers={
                "Content-Type": "application/json"
            },
            timeout=30
        )
        
        print(f"响应状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        
        if response.status_code == 200:
            response_data = response.json()
            print(f"响应数据: {json.dumps(response_data, indent=2, ensure_ascii=False)}")
            
            # 验证响应格式
            if response_data.get("success"):
                print("✅ 接口调用成功")
                
                data = response_data.get("data", {})
                user_info = data.get("user_info", {})
                token_info = data.get("token_info", {})
                
                print(f"用户信息: {json.dumps(user_info, indent=2, ensure_ascii=False)}")
                print(f"令牌信息: {json.dumps(token_info, indent=2, ensure_ascii=False)}")
                
                # 模拟Java客户端接收到的最终回调数据
                java_callback_data = {
                    "code": 0,
                    "message": "登录成功",
                    "authCode": test_auth_code,
                    "alipayOpenId": "",
                    "loginType": "alipay",
                    "userInfo": user_info,
                    "tokenInfo": token_info
                }
                
                print("\n📱 模拟Java客户端最终回调数据:")
                print(json.dumps(java_callback_data, indent=2, ensure_ascii=False))
                
            else:
                print("❌ 接口返回失败")
                print(f"错误信息: {response_data.get('message', '未知错误')}")
        else:
            print(f"❌ HTTP请求失败: {response.status_code}")
            print(f"错误响应: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 请求异常: {str(e)}")
    except json.JSONDecodeError as e:
        print(f"❌ JSON解析失败: {str(e)}")
    except Exception as e:
        print(f"❌ 其他异常: {str(e)}")

def test_with_real_authcode():
    """使用真实authCode进行测试的说明"""
    print("\n" + "=" * 60)
    print("使用真实authCode测试说明")
    print("=" * 60)
    print("""
要使用真实的authCode进行测试，需要：

1. 在Android应用中集成支付宝SDK
2. 调用支付宝授权接口获取真实的authCode
3. 将获取到的authCode替换上面的test_auth_code
4. 确保服务器端的支付宝配置正确（App ID、私钥等）

真实测试流程：
1. Android应用 -> 支付宝SDK授权 -> 获取authCode
2. Android应用 -> 调用服务器/api/auth/userinfo -> 传入authCode
3. 服务器 -> 调用支付宝API -> 获取access_token和用户信息
4. 服务器 -> 返回用户信息给Android应用
5. Android应用 -> 执行登录回调 -> 完成登录流程
    """)

if __name__ == "__main__":
    print("支付宝用户信息获取流程测试")
    print(f"测试时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 测试用户信息API
    test_userinfo_api()
    
    # 显示真实测试说明
    test_with_real_authcode()
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)