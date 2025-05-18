#!/usr/bin/env python3

import os
import requests
from bs4 import BeautifulSoup
import concurrent.futures
import logging
from urllib.parse import urljoin

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def read_source():
    """读取PyPI源地址"""
    with open('source.txt', 'r') as f:
        return f.read().strip()

def read_packages():
    """读取需要下载的包列表"""
    with open('packages.txt', 'r') as f:
        return [line.strip() for line in f if line.strip()]

def get_package_page(base_url, package):
    """获取包的页面URL"""
    url = urljoin(base_url, package)
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        logging.error(f"获取包 {package} 的页面失败: {e}")
        return None

def get_wheel_urls(page_content, base_url):
    """解析页面内容获取wheel文件的URL"""
    soup = BeautifulSoup(page_content, 'html.parser')
    links = soup.find_all('a')
    return [urljoin(base_url, link['href']) for link in links if link['href'].endswith('.whl')]

def download_wheel(url, output_dir):
    """下载wheel文件"""
    try:
        filename = os.path.basename(url)
        output_path = os.path.join(output_dir, filename)
        
        # 如果文件已存在，跳过下载
        if os.path.exists(output_path):
            logging.info(f"文件已存在，跳过: {filename}")
            return True

        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        logging.info(f"成功下载: {filename}")
        return True
    except requests.RequestException as e:
        logging.error(f"下载失败 {url}: {e}")
        return False

def main():
    # 创建输出目录
    output_dir = 'data'
    os.makedirs(output_dir, exist_ok=True)

    # 读取配置
    base_url = read_source()
    packages = read_packages()

    logging.info(f"开始从 {base_url} 下载包")
    
    # 为每个包下载wheel文件
    for package in packages:
        logging.info(f"处理包: {package}")
        
        # 获取包的页面
        page_content = get_package_page(base_url, package)
        if not page_content:
            continue

        # 获取wheel文件的URL
        wheel_urls = get_wheel_urls(page_content, base_url)
        if not wheel_urls:
            logging.warning(f"没有找到包 {package} 的wheel文件")
            continue

        # 使用线程池并行下载wheel文件
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            futures = [
                executor.submit(download_wheel, url, output_dir)
                for url in wheel_urls
            ]
            concurrent.futures.wait(futures)

if __name__ == '__main__':
    main() 