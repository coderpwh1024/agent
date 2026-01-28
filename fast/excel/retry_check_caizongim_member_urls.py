#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
caizongim_t_member 异常URL重试检测脚本
针对上次检测结果为 error 的URL进行重新检测，重试上限3次
"""

import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import time
import warnings

warnings.filterwarnings('ignore')

# 配置
INPUT_FILE = 'caizongim_t_member_checked.xlsx'
OUTPUT_FILE = 'caizongim_t_member_checked.xlsx'  # 覆盖原文件
MAX_WORKERS = 10  # 降低并发，提高成功率
TIMEOUT = 15  # 增加超时时间
RETRY_COUNT = 3  # 重试上限3次

# 需要检测的字段
URL_FIELDS = ['qrcode_s3', 'qrcode2_s3', 'icon']


def check_url(url):
    """检测URL是否可访问，重试3次"""
    if pd.isna(url) or url is None or str(url).strip() == '' or str(url).lower() == 'nan':
        return None

    url = str(url).strip()

    for attempt in range(RETRY_COUNT):
        try:
            response = requests.head(
                url,
                timeout=TIMEOUT,
                allow_redirects=True,
                verify=False,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            )
            if response.status_code == 200:
                return 'ok'
            elif response.status_code == 405:
                response = requests.get(
                    url,
                    timeout=TIMEOUT,
                    allow_redirects=True,
                    verify=False,
                    headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                    }
                )
                if response.status_code == 200:
                    return 'ok'
            if attempt == RETRY_COUNT - 1:
                return 'error'
        except Exception:
            if attempt == RETRY_COUNT - 1:
                return 'error'
        time.sleep(1)  # 重试间隔加长到1秒

    return 'error'


def main():
    print("=" * 60)
    print("caizongim_t_member 异常URL重试检测")
    print(f"重试次数上限: {RETRY_COUNT}")
    print("=" * 60)

    # 1. 读取已检测的Excel文件
    print(f"\n[1/3] 正在读取文件: {INPUT_FILE}")
    try:
        df = pd.read_excel(INPUT_FILE)
        print(f"  成功读取 {len(df)} 行数据")
    except Exception as e:
        print(f"  读取文件失败: {e}")
        return

    # 2. 统计需要重试的URL
    print(f"\n[2/3] 统计异常URL:")
    retry_tasks = []  # (index, field) 元组列表

    for field in URL_FIELDS:
        check_field = f'{field}_check'
        error_mask = df[check_field] == 'error'
        error_count = error_mask.sum()
        print(f"  {field}: {error_count} 条异常URL需要重试")

        for idx in df[error_mask].index:
            retry_tasks.append((idx, field))

    total_retries = len(retry_tasks)
    if total_retries == 0:
        print("\n  没有需要重试的异常URL")
        return

    print(f"\n  总计需要重试: {total_retries} 条URL")

    # 3. 并发重试检测
    print(f"\n[3/3] 开始重试检测 (并发线程数: {MAX_WORKERS}, 超时: {TIMEOUT}秒)")
    print()

    success_count = 0
    still_error_count = 0

    def retry_single(task):
        idx, field = task
        url = df.at[idx, field]
        result = check_url(url)
        return idx, field, result

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {
            executor.submit(retry_single, task): task
            for task in retry_tasks
        }

        with tqdm(total=total_retries, desc="重试进度", unit="条") as pbar:
            for future in as_completed(futures):
                try:
                    idx, field, result = future.result()
                    check_field = f'{field}_check'
                    old_result = df.at[idx, check_field]
                    df.at[idx, check_field] = result

                    if result == 'ok':
                        success_count += 1
                    else:
                        still_error_count += 1

                    pbar.update(1)
                except Exception as e:
                    print(f"\n警告: 处理时出错: {e}")
                    pbar.update(1)

    # 4. 保存结果
    print(f"\n正在保存结果到: {OUTPUT_FILE}")
    try:
        df.to_excel(OUTPUT_FILE, index=False)
        print(f"  结果已保存")
    except Exception as e:
        print(f"  保存文件失败: {e}")
        return

    # 5. 统计重试结果
    print("\n" + "=" * 60)
    print("重试结果统计:")
    print("=" * 60)
    print(f"\n  总重试数: {total_retries}")
    print(f"  恢复正常(error->ok): {success_count}")
    print(f"  仍然异常(error): {still_error_count}")

    print("\n最终检测结果:")
    print("-" * 40)
    for field in URL_FIELDS:
        check_field = f'{field}_check'
        total = df[check_field].notna().sum()
        ok_count = (df[check_field] == 'ok').sum()
        error_count = (df[check_field] == 'error').sum()
        skip_count = df[check_field].isna().sum()

        print(f"\n{field}:")
        print(f"  检测总数: {total}")
        print(f"  正常(ok): {ok_count} ({(ok_count / total * 100):.1f}%)" if total > 0 else "  正常(ok): 0")
        print(f"  异常(error): {error_count} ({(error_count / total * 100):.1f}%)" if total > 0 else "  异常(error): 0")
        print(f"  跳过(空值): {skip_count}")

    print("\n" + "=" * 60)
    print("重试检测完成!")
    print("=" * 60)


if __name__ == '__main__':
    main()
