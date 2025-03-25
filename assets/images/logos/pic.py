import requests
from bs4 import BeautifulSoup
import os
import re
import sys
from urllib.parse import urlparse

def pic(channel_url=None):
    """
    下载Telegram频道的头像图片
    参数:
        channel_url: Telegram频道的URL地址
    """
    # 如果没有提供URL，则请求用户输入
    if not channel_url:
        channel_url = input("请输入Telegram频道地址 (例如: https://t.me/seguazhongxin): ")

    # 确保URL是有效的
    if not channel_url.startswith(('https://t.me/', 'https://telegram.me/')):
        if channel_url.startswith('@'):
            channel_url = 'https://t.me/' + channel_url[1:]
        else:
            channel_url = 'https://t.me/' + channel_url

    # 从URL中提取频道ID
    parsed_url = urlparse(channel_url)
    channel_id = parsed_url.path.strip('/')

    print(f"正在下载频道 {channel_id} 的头像...")

    try:
        # 获取频道页面内容
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(channel_url, headers=headers)
        response.raise_for_status()

        # 解析HTML内容
        soup = BeautifulSoup(response.text, 'html.parser')

        # 寻找频道头像图片
        # 可能需要根据实际网页结构调整选择器
        img_tag = soup.select_one('.tgme_page_photo_image')

        if not img_tag:
            print(f"未找到频道 {channel_id} 的头像图片")
            return False

        img_url = img_tag.get('src')

        if not img_url:
            print(f"未找到频道 {channel_id} 的头像图片URL")
            return False

        # 下载图片
        img_response = requests.get(img_url, headers=headers)
        img_response.raise_for_status()

        # 保存图片
        filename = f"{channel_id}.jpg"
        with open(filename, 'wb') as f:
            f.write(img_response.content)

        print(f"图片已成功下载为 {filename}")
        return True

    except Exception as e:
        print(f"下载频道 {channel_id} 头像时出错: {str(e)}")
        return False

def download_multiple(channels):
    """
    下载多个频道的头像图片
    参数:
        channels: 频道URL列表
    """
    total = len(channels)
    successful = 0
    failed = 0

    print(f"开始下载 {total} 个频道的头像...")

    for i, channel in enumerate(channels, 1):
        print(f"\n[{i}/{total}] 处理频道: {channel}")
        result = pic(channel)
        if result:
            successful += 1
        else:
            failed += 1

    print(f"\n下载完成! 成功: {successful}, 失败: {failed}, 总计: {total}")
    return successful, failed, total

def main():
    """命令行入口函数"""
    if len(sys.argv) > 1:
        # 有命令行参数
        channels = sys.argv[1:]
        download_multiple(channels)
    else:
        # 无命令行参数，交互式输入
        channels = []
        print("请输入Telegram频道地址，每行一个，输入空行结束:")
        while True:
            channel = input("> ").strip()
            if not channel:
                break
            channels.append(channel)

        if channels:
            download_multiple(channels)
        else:
            pic()  # 如果没有输入任何频道，回退到单个频道模式

if __name__ == "__main__":
    main()
