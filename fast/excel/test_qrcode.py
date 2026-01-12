#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
二维码识别测试脚本 - 仅处理前N行数据用于测试
"""

import pandas as pd
import cv2
import numpy as np
import requests
from io import BytesIO
from PIL import Image

def download_and_decode(url):
    """下载并识别二维码"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url.strip(), headers=headers, timeout=10)
        response.raise_for_status()
        
        # 转换为OpenCV格式
        img = Image.open(BytesIO(response.content))
        img_array = np.array(img)
        
        if len(img_array.shape) == 3 and img_array.shape[2] == 4:
            img_array = cv2.cvtColor(img_array, cv2.COLOR_RGBA2BGR)
        elif len(img_array.shape) == 3:
            img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        
        # 识别二维码
        detector = cv2.QRCodeDetector()
        data, _, _ = detector.detectAndDecode(img_array)
        
        return data if data else None
    except Exception as e:
        return f"错误: {str(e)}"

# 读取Excel
input_file = "fat.xlsx"
df = pd.read_excel(input_file)

# 只处理前5行作为测试
test_rows = 5
print(f"测试前 {test_rows} 行数据...\n")

for idx in range(min(test_rows, len(df))):
    row = df.iloc[idx]
    print(f"{'='*60}")
    print(f"第 {idx+1} 行 (ID: {row['id']})")
    print(f"{'='*60}")
    
    # 识别qrcode
    print("识别 qrcode...")
    qrcode_content = download_and_decode(row['qrcode'])
    print(f"  内容: {qrcode_content}")
    
    # 识别qrcode_s3
    print("识别 qrcode_s3...")
    qrcode_s3_content = download_and_decode(row['qrcode_s3'])
    print(f"  内容: {qrcode_s3_content}")
    
    # 对比
    if qrcode_content and qrcode_s3_content and not qrcode_content.startswith("错误") and not qrcode_s3_content.startswith("错误"):
        is_match = qrcode_content == qrcode_s3_content
        print(f"\n结果: {'✓ 一致' if is_match else '✗ 不一致'}")
        if not is_match:
            print(f"  差异:")
            print(f"    qrcode:    {qrcode_content}")
            print(f"    qrcode_s3: {qrcode_s3_content}")
    else:
        print(f"\n结果: 无法对比（识别失败）")
    print()

print("测试完成！如果测试正常，可以运行完整版本的 qrcode_processor.py")
