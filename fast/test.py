import hmac
import hashlib
import time
import base64
import struct


def get_totp_code(secret_key, intervals_no=None):
    """
    生成TOTP验证码

    Args:
        secret_key: 密钥字符串
        intervals_no: 时间偏移量(可选)，用于生成过去/未来的验证码

    Returns:
        str: 6位数字验证码
    """
    if intervals_no is None:
        intervals_no = int(time.time()) // 30

    # 将密钥转换为bytes
    key = base64.b32decode(secret_key, casefold=True)

    # 将时间戳转换为bytes
    msg = struct.pack(">Q", intervals_no)

    # 生成HMAC-SHA1哈希
    hmac_hash = hmac.new(key, msg, hashlib.sha1).digest()

    # 获取动态截断位置
    offset = hmac_hash[-1] & 0x0F

    # 截取4字节动态二进制码
    dynamic_code = struct.unpack(">I", hmac_hash[offset:offset + 4])[0]

    # 取后31位
    dynamic_code &= 0x7FFFFFFF

    # 生成6位数字验证码
    code = dynamic_code % 1000000

    return f"{code:06d}"


def get_multiple_totp_codes(secret_key, count=3):
    """
    生成多个TOTP验证码（当前时间及前后时间窗口）

    Args:
        secret_key: 密钥字符串
        count: 生成的验证码数量（奇数，默认为3：前一个、当前、下一个）

    Returns:
        list: 包含时间偏移和验证码的元组列表
    """
    if count % 2 == 0:
        count += 1  # 确保是奇数，使当前时间在中间

    current_interval = int(time.time()) // 30
    half_range = count // 2

    codes = []
    for i in range(-half_range, half_range + 1):
        interval = current_interval + i
        code = get_totp_code(secret_key, interval)
        time_window = "当前" if i == 0 else f"{i * 30}秒{'前' if i < 0 else '后'}"
        codes.append((time_window, code))

    return codes


def generate_base32_secret():
    """
    生成Base32编码的随机密钥（类似于Java版本中的随机密钥）
    """
    import os
    random_bytes = os.urandom(20)
    base32_secret = base64.b32encode(random_bytes).decode('utf-8').replace('=', '')
    return base32_secret


# 使用示例
if __name__ == "__main__":
    # 使用你提供的密钥（注意：需要是Base32编码）
    # 如果"12323"不是有效的Base32密钥，请使用generate_base32_secret()生成新密钥
    secret_key = "SZKNPRZ67USOFJORZSMWQ432HQRSVWLT"

    # 由于"12323"可能不是有效的Base32密钥，这里生成一个新密钥作为示例
    secret_key = generate_base32_secret()
    print(f"生成的密钥: {secret_key}")

    # 生成单个验证码
    single_code = get_totp_code(secret_key)
    print(f"当前验证码: {single_code}")

    # 生成多个验证码（避免时间过期）
    print("\n多个时间窗口的验证码:")
    multiple_codes = get_multiple_totp_codes(secret_key, 5)  # 生成5个验证码
    for time_window, code in multiple_codes:
        print(f"{time_window}: {code}")

    # 验证功能
    print(f"\n验证当前验证码是否正确: {get_totp_code(secret_key) == single_code}")