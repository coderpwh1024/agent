#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
会员表格URL检测脚本
检测 qrcode, qrcode2, icon, img, chat_img, qrcode_s3, qrcode2_s3 字段中的URL是否可访问
"""

import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import time
import warnings

warnings.filterwarnings('ignore')

# 配置
INPUT_FILE = 't_member.xlsx'  # 输入文件名
OUTPUT_FILE = 't_member_checked.xlsx'  # 输出文件名
MAX_WORKERS = 20  # 并发线程数，可根据需要调整
TIMEOUT = 10  # 请求超时时间（秒）
RETRY_COUNT = 2  # 重试次数

# 需要检测的字段
URL_FIELDS = ['qrcode', 'qrcode2', 'icon', 'img', 'chat_img', 'qrcode_s3', 'qrcode2_s3']


def check_url(url):
    """
    检测URL是否可访问
    返回 'ok' 或 'error'
    """
    if pd.isna(url) or url is None or str(url).strip() == '' or str(url).lower() == 'nan':
        return None  # 空值不检查

    url = str(url).strip()

    # 重试机制
    for attempt in range(RETRY_COUNT):
        try:
            response = requests.head(
                url,
                timeout=TIMEOUT,
                allow_redirects=True,
                verify=False,
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            )
            if response.status_code == 200:
                return 'ok'
            elif response.status_code == 405:  # HEAD方法不支持，尝试GET
                response = requests.get(
                    url,
                    timeout=TIMEOUT,
                    allow_redirects=True,
                    verify=False,
                    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
                )
                if response.status_code == 200:
                    return 'ok'
            return 'error'
        except Exception as e:
            if attempt == RETRY_COUNT - 1:  # 最后一次重试
                return 'error'
            time.sleep(0.5)  # 重试前等待

    return 'error'


def process_row(row_data):
    """处理单行数据，检测所有URL字段"""
    index, row = row_data
    results = {}

    for field in URL_FIELDS:
        url = row.get(field)
        check_result = check_url(url)
        results[f'{field}_check'] = check_result

    return index, results


def main():
    print("=" * 60)
    print("会员表格URL检测工具")
    print("=" * 60)

    # 1. 读取Excel文件
    print(f"\n[1/4] 正在读取文件: {INPUT_FILE}")
    try:
        df = pd.read_excel(INPUT_FILE)
        print(f"✓ 成功读取 {len(df)} 行数据")
    except Exception as e:
        print(f"✗ 读取文件失败: {e}")
        return

    # 2. 添加检测结果列
    print(f"\n[2/4] 准备检测字段:")
    for field in URL_FIELDS:
        df[f'{field}_check'] = None
        print(f"  - {field} → {field}_check")

    # 3. 并发检测URL
    print(f"\n[3/4] 开始检测URL (并发线程数: {MAX_WORKERS})")
    print(f"      超时时间: {TIMEOUT}秒, 重试次数: {RETRY_COUNT}")

    total_checks = 0
    for field in URL_FIELDS:
        non_null_count = df[field].notna().sum()
        total_checks += non_null_count

    print(f"      预计检测URL数量: {total_checks}")
    print()

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # 提交所有任务
        futures = {
            executor.submit(process_row, (idx, row)): idx
            for idx, row in df.iterrows()
        }

        # 使用进度条显示进度
        with tqdm(total=len(df), desc="检测进度", unit="行") as pbar:
            for future in as_completed(futures):
                try:
                    index, results = future.result()
                    # 更新结果到DataFrame
                    for field_check, value in results.items():
                        df.at[index, field_check] = value
                    pbar.update(1)
                except Exception as e:
                    print(f"\n警告: 处理行时出错: {e}")
                    pbar.update(1)

    # 4. 保存结果
    print(f"\n[4/4] 正在保存结果到: {OUTPUT_FILE}")
    try:
        df.to_excel(OUTPUT_FILE, index=False)
        print(f"✓ 结果已保存")
    except Exception as e:
        print(f"✗ 保存文件失败: {e}")
        return

    # 5. 统计结果
    print("\n" + "=" * 60)
    print("检测结果统计:")
    print("=" * 60)

    for field in URL_FIELDS:
        check_field = f'{field}_check'
        total = df[check_field].notna().sum()
        ok_count = (df[check_field] == 'ok').sum()
        error_count = (df[check_field] == 'error').sum()

        if total > 0:
            ok_rate = (ok_count / total * 100) if total > 0 else 0
            print(f"\n{field}:")
            print(f"  检测总数: {total}")
            print(f"  正常(ok): {ok_count} ({ok_rate:.1f}%)")
            print(f"  异常(error): {error_count} ({100 - ok_rate:.1f}%)")

    print("\n" + "=" * 60)
    print("✓ 检测完成!")
    print("=" * 60)


if __name__ == '__main__':
    main()