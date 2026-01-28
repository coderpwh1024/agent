#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
提取 caizongim_t_group.xlsx 中 qrcode_s3 字段 URL 对应的二维码内容
生成 caizongim_t_group_qrcode_result.xlsx，新增 qrcode_content 列
"""

import cv2
import numpy as np
import pandas as pd
import requests
import sys
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed


def extract_qrcode(url, timeout=10):
    """
    下载图片并解码二维码内容

    Args:
        url: 二维码图片 URL
        timeout: 超时时间（秒）

    Returns:
        解码后的文本内容，失败返回 'error'
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        resp = requests.get(url.strip(), headers=headers, timeout=timeout)
        if resp.status_code != 200:
            return 'error: http_' + str(resp.status_code)

        img_array = np.frombuffer(resp.content, dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        if img is None:
            return 'error: invalid_image'

        detector = cv2.QRCodeDetector()
        data, points, _ = detector.detectAndDecode(img)

        if points is not None and data:
            return data
        return 'error: no_qrcode_found'
    except requests.exceptions.Timeout:
        return 'error: timeout'
    except Exception as e:
        return f'error: {type(e).__name__}'


def process(input_file, output_file, max_workers=10):
    """
    读取 Excel，提取 qrcode_s3 URL 中的二维码内容，输出结果
    """
    print(f"读取文件: {input_file}")
    df = pd.read_excel(input_file)
    print(f"总行数: {len(df)}")

    df['qrcode_content'] = ''

    tasks = {}
    for idx, row in df.iterrows():
        url = row.get('qrcode_s3')
        if pd.isna(url) or not str(url).strip():
            continue
        tasks[idx] = str(url).strip()

    print(f"需要提取的URL数: {len(tasks)}")
    print("开始提取...")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_map = {
            executor.submit(extract_qrcode, url): idx
            for idx, url in tasks.items()
        }
        for future in tqdm(as_completed(future_map), total=len(future_map), desc="提取进度"):
            idx = future_map[future]
            try:
                result = future.result()
            except Exception:
                result = 'error: unknown'
            df.at[idx, 'qrcode_content'] = result

    print(f"\n保存结果到: {output_file}")
    df.to_excel(output_file, index=False, engine='openpyxl')

    success_count = len(df[(df['qrcode_content'] != '') & (~df['qrcode_content'].str.startswith('error'))])
    error_count = len(df[df['qrcode_content'].str.startswith('error')])
    skip_count = len(df[df['qrcode_content'] == ''])

    print("\n" + "=" * 50)
    print("提取完成！统计信息：")
    print("=" * 50)
    print(f"总行数:       {len(df)}")
    print(f"跳过(空值):   {skip_count}")
    print(f"提取成功:     {success_count}")
    print(f"提取失败:     {error_count}")
    print("=" * 50)


if __name__ == "__main__":
    input_file = "caizongim_t_group.xlsx"
    output_file = "caizongim_t_group_qrcode_result.xlsx"

    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    if len(sys.argv) > 2:
        output_file = sys.argv[2]

    process(input_file, output_file)
