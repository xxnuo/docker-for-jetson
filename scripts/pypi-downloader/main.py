#!/usr/bin/env python3

import concurrent.futures
import hashlib
import json
import logging
import os
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

# 设置日志
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# 全局常量
CHUNK_SIZE = 8192
PROGRESS_FILE = "download_progress.json"
DATA_DIR = "data"


class DownloadManager:
    def __init__(self):
        self.output_dir = Path(DATA_DIR)
        self.output_dir.mkdir(exist_ok=True)
        self.progress = self._load_progress()

    def _load_progress(self):
        """加载下载进度记录"""
        try:
            if os.path.exists(PROGRESS_FILE):
                with open(PROGRESS_FILE, "r") as f:
                    return json.load(f)
        except Exception as e:
            logging.warning(f"无法加载进度文件: {e}")
        return {}

    def _save_progress(self):
        """保存下载进度"""
        try:
            with open(PROGRESS_FILE, "w") as f:
                json.dump(self.progress, f)
        except Exception as e:
            logging.error(f"保存进度失败: {e}")

    def _calculate_file_hash(self, file_path):
        """计算文件的SHA256哈希值"""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(CHUNK_SIZE), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def _get_file_size(self, url):
        """获取远程文件大小"""
        try:
            response = requests.head(url)
            return int(response.headers.get("content-length", 0))
        except:
            return 0

    def download_wheel(self, url):
        """下载wheel文件，支持断点续传"""
        try:
            filename = os.path.basename(url)
            output_path = self.output_dir / filename
            temp_path = self.output_dir / f"{filename}.temp"

            # 检查是否已完成下载
            if url in self.progress and self.progress[url]["status"] == "completed":
                if output_path.exists():
                    file_hash = self._calculate_file_hash(output_path)
                    if file_hash == self.progress[url]["hash"]:
                        logging.info(f"文件已存在且验证通过，跳过: {filename}")
                        return True

            # 获取远程文件大小
            total_size = self._get_file_size(url)

            # 准备断点续传
            headers = {}
            local_size = 0
            if temp_path.exists():
                local_size = temp_path.stat().st_size
                if local_size < total_size:
                    headers["Range"] = f"bytes={local_size}-"
                else:
                    temp_path.unlink()
                    local_size = 0

            # 开始下载
            mode = "ab" if local_size > 0 else "wb"
            response = requests.get(url, headers=headers, stream=True)
            response.raise_for_status()

            with open(temp_path, mode) as f:
                for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                    if chunk:
                        f.write(chunk)
                        local_size += len(chunk)

            # 验证并完成下载
            if temp_path.exists():
                file_hash = self._calculate_file_hash(temp_path)
                temp_path.rename(output_path)
                self.progress[url] = {
                    "status": "completed",
                    "hash": file_hash,
                    "size": local_size,
                }
                self._save_progress()
                logging.info(f"成功下载: {filename}")
                return True

        except requests.RequestException as e:
            logging.error(f"下载失败 {url}: {e}")
            if temp_path.exists():
                temp_path.unlink()
        except Exception as e:
            logging.error(f"处理文件时出错 {url}: {e}")
            if temp_path.exists():
                temp_path.unlink()
        return False


def read_source():
    """读取PyPI源地址"""
    with open("source.txt", "r") as f:
        return f.read().strip()


def read_packages():
    """读取需要下载的包列表"""
    with open("packages.txt", "r") as f:
        return [line.strip() for line in f if line.strip()]


def get_package_page(base_url, package):
    """获取包的页面URL"""
    url = urljoin(base_url, package)
    logging.info(f"正在获取包页面: {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        logging.error(f"获取包 {package} 的页面失败: {e}")
        return None


def get_wheel_urls(page_content, base_url):
    """解析页面内容获取wheel文件的URL"""
    soup = BeautifulSoup(page_content, "html.parser")
    links = soup.find_all("a")
    wheel_urls = [
        urljoin(base_url, link["href"])
        for link in links
        if link.get("href", "").endswith(".whl")
    ]
    logging.info(f"找到 {len(wheel_urls)} 个wheel文件")
    if not wheel_urls:
        logging.debug(f"页面内容: {page_content[:500]}...")
    return wheel_urls


def main():
    base_url = read_source()
    packages = read_packages()
    download_manager = DownloadManager()

    logging.info(f"开始从 {base_url} 下载包")

    for package in packages:
        logging.info(f"处理包: {package}")

        page_content = get_package_page(base_url, package)
        if not page_content:
            continue

        wheel_urls = get_wheel_urls(page_content, base_url)
        if not wheel_urls:
            logging.warning(f"没有找到包 {package} 的wheel文件")
            continue

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            futures = [
                executor.submit(download_manager.download_wheel, url)
                for url in wheel_urls
            ]
            concurrent.futures.wait(futures)


if __name__ == "__main__":
    main()
