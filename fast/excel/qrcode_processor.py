#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
二维码识别和对比工具
识别Excel文件中两列二维码URL的内容并进行对比
"""

import pandas as pd
import cv2
import numpy as np
import requests
from io import BytesIO
from PIL import Image
import sys
from tqdm import tqdm
import time

def download_image(url, timeout=10, retry=3):
    """
    下载图片
    
    Args:
        url: 图片URL
        timeout: 超时时间（秒）
        retry: 重试次数
    
    Returns:
        PIL.Image对象或None
    """
    for attempt in range(retry):
        try:
            # 添加headers避免被拒绝
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url.strip(), headers=headers, timeout=timeout)
            response.raise_for_status()
            
            # 转换为PIL Image
            img = Image.open(BytesIO(response.content))
            return img
        except Exception as e:
            if attempt < retry - 1:
                time.sleep(1)  # 等待1秒后重试
                continue
            else:
                print(f"下载图片失败 ({url}): {str(e)}")
                return None

def decode_qrcode(img):
    """
    识别二维码内容
    
    Args:
        img: PIL.Image对象
    
    Returns:
        二维码内容字符串或None
    """
    if img is None:
        return None
    
    try:
        # 将PIL Image转换为OpenCV格式
        img_array = np.array(img)
        
        # 如果是RGBA，转换为RGB
        if len(img_array.shape) == 3 and img_array.shape[2] == 4:
            img_array = cv2.cvtColor(img_array, cv2.COLOR_RGBA2RGB)
        
        # 如果是RGB，转换为BGR（OpenCV格式）
        if len(img_array.shape) == 3:
            img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        
        # 使用OpenCV的QRCodeDetector
        detector = cv2.QRCodeDetector()
        data, bbox, straight_qrcode = detector.detectAndDecode(img_array)
        
        if data:
            return data
        
        # 如果第一次失败，尝试转换为灰度图再试
        gray = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)
        data, bbox, straight_qrcode = detector.detectAndDecode(gray)
        
        if data:
            return data
        
        # 尝试增强对比度
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(gray)
        data, bbox, straight_qrcode = detector.detectAndDecode(enhanced)
        
        return data if data else None
        
    except Exception as e:
        print(f"识别二维码失败: {str(e)}")
        return None

def process_excel(input_file, output_file):
    """
    处理Excel文件，识别二维码并对比
    
    Args:
        input_file: 输入Excel文件路径
        output_file: 输出Excel文件路径
    """
    print(f"读取Excel文件: {input_file}")
    df = pd.read_excel(input_file)
    
    print(f"总共有 {len(df)} 行数据需要处理")
    print("开始处理...")
    
    # 添加新列
    df['qrcode_content'] = ''
    df['qrcode_s3_content'] = ''
    df['is_match'] = ''
    df['status'] = ''
    
    # 处理每一行
    for idx, row in tqdm(df.iterrows(), total=len(df), desc="处理进度"):
        try:
            # 处理qrcode列
            qrcode_url = row['qrcode']
            qrcode_s3_url = row['qrcode_s3']
            
            # 下载并识别qrcode
            qrcode_content = None
            if pd.notna(qrcode_url) and qrcode_url.strip():
                img1 = download_image(qrcode_url)
                if img1:
                    qrcode_content = decode_qrcode(img1)
            
            # 下载并识别qrcode_s3
            qrcode_s3_content = None
            if pd.notna(qrcode_s3_url) and qrcode_s3_url.strip():
                img2 = download_image(qrcode_s3_url)
                if img2:
                    qrcode_s3_content = decode_qrcode(img2)
            
            # 更新数据
            df.at[idx, 'qrcode_content'] = qrcode_content if qrcode_content else '识别失败'
            df.at[idx, 'qrcode_s3_content'] = qrcode_s3_content if qrcode_s3_content else '识别失败'
            
            # 判断是否一致
            if qrcode_content and qrcode_s3_content:
                is_match = qrcode_content == qrcode_s3_content
                df.at[idx, 'is_match'] = '一致' if is_match else '不一致'
                df.at[idx, 'status'] = '成功'
            else:
                df.at[idx, 'is_match'] = '无法对比'
                df.at[idx, 'status'] = '部分失败' if (qrcode_content or qrcode_s3_content) else '全部失败'
            
        except Exception as e:
            print(f"\n处理第 {idx+1} 行时出错: {str(e)}")
            df.at[idx, 'status'] = f'错误: {str(e)}'
    
    # 保存结果
    print(f"\n保存结果到: {output_file}")
    df.to_excel(output_file, index=False, engine='openpyxl')
    
    # 输出统计信息
    print("\n" + "="*60)
    print("处理完成！统计信息：")
    print("="*60)
    print(f"总行数: {len(df)}")
    print(f"成功识别: {len(df[df['status'] == '成功'])}")
    print(f"部分失败: {len(df[df['status'] == '部分失败'])}")
    print(f"全部失败: {len(df[df['status'] == '全部失败'])}")
    print(f"一致: {len(df[df['is_match'] == '一致'])}")
    print(f"不一致: {len(df[df['is_match'] == '不一致'])}")
    print("="*60)

if __name__ == "__main__":
    # 输入和输出文件路径
    input_file = "82.xlsx"  # 修改为你的输入文件路径
    output_file = "82_result.xlsx"  # 输出文件路径
    
    # 如果有命令行参数，使用命令行参数
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    
    try:
        process_excel(input_file, output_file)
    except Exception as e:
        print(f"程序执行出错: {str(e)}")
        import traceback
        traceback.print_exc()
