#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试authInfo API接口
"""

import requests
import json

def test_auth_info_api():
    """测试authInfo API接口"""
    print("=== 测试authInfo API接口 ===")
    
    base_url = "http://localhost:8000"
    test_pid = "2088102123816631"  # 示例PID
    
    try:
        # 测试GET方式的API
        print("\n1. 测试GET方式的authInfo接口...")
        get_url = f"{base_url}/api/auth/authinfo/{test_pid}"
        print(f"请求URL: {get_url}")
        
        response = requests.get(get_url)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"响应数据:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            
            if data.get('success') and 'authInfo' in data.get('data', {}):
                auth_info = data['data']['authInfo']
                print(f"\n✅ GET接口测试成功")
                print(f"authInfo长度: {len(auth_info)} 字符")
                print(f"包含sign参数: {'sign=' in auth_info}")
            else:
                print(f"\n❌ GET接口返回数据格式错误")
        else:
            print(f"\n❌ GET接口请求失败: {response.text}")
        
        # 测试POST方式的API
        print("\n2. 测试POST方式的authInfo接口...")
        post_url = f"{base_url}/api/auth/authinfo"
        post_data = {
            "pid": test_pid,
            "target_id": "test_android_123",
            "rsa2": True
        }
        
        print(f"请求URL: {post_url}")
        print(f"请求数据: {json.dumps(post_data, ensure_ascii=False)}")
        
        response = requests.post(post_url, json=post_data)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"响应数据:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            
            if data.get('success') and 'authInfo' in data.get('data', {}):
                auth_info = data['data']['authInfo']
                print(f"\n✅ POST接口测试成功")
                print(f"authInfo长度: {len(auth_info)} 字符")
                print(f"包含自定义target_id: {'test_android_123' in auth_info}")
                print(f"包含sign参数: {'sign=' in auth_info}")
            else:
                print(f"\n❌ POST接口返回数据格式错误")
        else:
            print(f"\n❌ POST接口请求失败: {response.text}")
        
        # 测试RSA签名类型
        print("\n3. 测试RSA签名类型...")
        get_url_rsa = f"{base_url}/api/auth/authinfo/{test_pid}?rsa2=false"
        print(f"请求URL: {get_url_rsa}")
        
        response = requests.get(get_url_rsa)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success') and 'sign_type' in data.get('data', {}):
                sign_type = data['data']['sign_type']
                print(f"签名类型: {sign_type}")
                if sign_type == "RSA":
                    print(f"✅ RSA签名类型测试成功")
                else:
                    print(f"❌ RSA签名类型测试失败")
            else:
                print(f"❌ RSA签名类型测试失败")
        
        print("\n=== API测试完成 ===")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ 无法连接到服务器，请确保服务器正在运行")
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_auth_info_api()