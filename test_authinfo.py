#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试authInfo生成功能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.alipay_service import AlipayService
from config.alipay_config import alipay_config

def test_auth_info_generation():
    """测试authInfo生成"""
    print("=== 测试authInfo生成功能 ===")
    
    # 初始化支付宝服务
    alipay_service = AlipayService()
    
    # 测试参数
    test_pid = "2088102123816631"  # 示例PID，实际使用时需要替换为真实的PID
    
    try:
        print(f"\n1. 测试基本authInfo生成...")
        print(f"PID: {test_pid}")
        print(f"APP_ID: {alipay_config.app_id}")
        
        # 生成authInfo
        auth_info = alipay_service.generate_auth_info(pid=test_pid)
        
        print(f"\n生成的authInfo:")
        print(f"{auth_info}")
        print(f"\n长度: {len(auth_info)} 字符")
        
        # 验证authInfo包含必要的参数
        required_params = [
            "app_id=", "pid=", "apiname=", "methodname=", 
            "app_name=", "biz_type=", "product_id=", "scope=",
            "target_id=", "auth_type=", "sign_type=", "sign="
        ]
        
        print(f"\n2. 验证必要参数...")
        missing_params = []
        for param in required_params:
            if param not in auth_info:
                missing_params.append(param)
            else:
                print(f"✓ {param}")
        
        if missing_params:
            print(f"\n❌ 缺少参数: {missing_params}")
        else:
            print(f"\n✅ 所有必要参数都存在")
        
        # 测试自定义target_id
        print(f"\n3. 测试自定义target_id...")
        custom_target_id = "test_target_123"
        auth_info_custom = alipay_service.generate_auth_info(
            pid=test_pid, 
            target_id=custom_target_id
        )
        
        if f"target_id={custom_target_id}" in auth_info_custom:
            print(f"✅ 自定义target_id设置成功")
        else:
            print(f"❌ 自定义target_id设置失败")
        
        # 测试RSA签名
        print(f"\n4. 测试RSA签名...")
        auth_info_rsa = alipay_service.generate_auth_info(
            pid=test_pid, 
            rsa2=False
        )
        
        if "sign_type=RSA" in auth_info_rsa:
            print(f"✅ RSA签名类型设置成功")
        else:
            print(f"❌ RSA签名类型设置失败")
        
        print(f"\n=== 测试完成 ===")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_auth_info_generation()