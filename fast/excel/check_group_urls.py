#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检测 t_group.xls 中 qrcode_s3 字段的 URL 可用性
生成 t_group_url_result.xls，新增 url_check_result 列
"""

import pandas as pd
import requests
import sys
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed


def check_url(url, timeout=10):
    """
    检测URL是否可正常访问

    Args:
        url: 待检测的URL
        timeout: 超时时间（秒）

    Returns:
        'ok' 或 'error'
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.head(url.strip(), headers=headers, timeout=timeout, allow_redirects=True)
        if response.status_code == 200:
            return 'ok'
        # HEAD 请求某些服务器不支持，降级为 GET
        response = requests.get(url.strip(), headers=headers, timeout=timeout, allow_redirects=True, stream=True)
        if response.status_code == 200:
            return 'ok'
        return 'error'
    except Exception:
        return 'error'


def process(input_file, output_file, max_workers=10):
    """
    读取 Excel，检测 qrcode_s3 URL，输出结果

    Args:
        input_file: 输入文件路径
        output_file: 输出文件路径
        max_workers: 并发线程数
    """
    print(f"读取文件: {input_file}")
    df = pd.read_excel(input_file)
    print(f"总行数: {len(df)}")

    # 初始化结果列
    df['url_check_result'] = ''

    # 收集需要检测的行
    tasks = {}
    for idx, row in df.iterrows():
        url = row.get('qrcode_s3')
        if pd.isna(url) or not str(url).strip():
            df.at[idx, 'url_check_result'] = ''
            continue
        tasks[idx] = str(url).strip()

    print(f"需要检测的URL数: {len(tasks)}")
    print("开始检测...")

    # 多线程并发检测
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_map = {
            executor.submit(check_url, url): idx
            for idx, url in tasks.items()
        }
        for future in tqdm(as_completed(future_map), total=len(future_map), desc="检测进度"):
            idx = future_map[future]
            try:
                result = future.result()
            except Exception:
                result = 'error'
            df.at[idx, 'url_check_result'] = result

    # 保存结果
    print(f"\n保存结果到: {output_file}")
    df.to_excel(output_file, index=False, engine='openpyxl')

    # 统计
    ok_count = len(df[df['url_check_result'] == 'ok'])
    error_count = len(df[df['url_check_result'] == 'error'])
    skip_count = len(df[df['url_check_result'] == ''])

    print("\n" + "=" * 50)
    print("检测完成！统计信息：")
    print("=" * 50)
    print(f"总行数:     {len(df)}")
    print(f"跳过(空值): {skip_count}")
    print(f"正常(ok):   {ok_count}")
    print(f"异常(error):{error_count}")
    print("=" * 50)


if __name__ == "__main__":
    input_file = "t_group.xls"
    output_file = "t_group_url_result.xls"

    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    if len(sys.argv) > 2:
        output_file = sys.argv[2]

    process(input_file, output_file)
