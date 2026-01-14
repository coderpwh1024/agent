import httpx
import ssl


def test_connection():
    endpoint = ""

    print("=== 测试1: 基本HTTPS连接 ===")
    try:
        response = httpx.get(endpoint, timeout=10.0)
        print(f"✓ 连接成功: {response.status_code}")
    except Exception as e:
        print(f"✗ 连接失败: {e}")

    print("\n=== 测试2: 禁用SSL验证 ===")
    try:
        response = httpx.get(endpoint, verify=False, timeout=10.0)
        print(f"✓ 连接成功: {response.status_code}")
    except Exception as e:
        print(f"✗ 连接失败: {e}")

    print("\n=== 测试3: 自定义SSL上下文 ===")
    try:
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        response = httpx.get(endpoint, verify=ssl_context, timeout=10.0)
        print(f"✓ 连接成功: {response.status_code}")
    except Exception as e:
        print(f"✗ 连接失败: {e}")


if __name__ == "__main__":
    test_connection()