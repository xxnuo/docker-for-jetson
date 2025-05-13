# docker-for-jetson
# NVIDIA Jetson 和 JetPack-L4T 机器学习容器
Machine Learning Containers for NVIDIA Jetson and JetPack-L4T

## 简介 | Introduction
这个项目提供了一系列为 NVIDIA Jetson 设备优化的 Docker 容器，专门用于机器学习和深度学习应用。这些容器预装了常用的机器学习框架和工具，使得在 Jetson 设备上部署 AI 应用变得更加简单。

This project provides a set of Docker containers optimized for NVIDIA Jetson devices, specifically designed for machine learning and deep learning applications. These containers come pre-installed with commonly used ML frameworks and tools, making it easier to deploy AI applications on Jetson devices.

## 特性 | Features
- 🚀 基于官方 PyTorch 容器构建 | Built on official PyTorch container
- 📦 预装常用机器学习库 | Pre-installed common ML libraries
- 🔧 针对 Jetson 平台优化 | Optimized for Jetson platform
- 🌐 集成清华镜像源加速 | Integrated Tsinghua mirror for faster downloads
- 🤖 支持 Ollama 本地大语言模型 | Support for Ollama local LLM deployment

## 预装软件 | Pre-installed Software
- PyTorch (CUDA 12.8 支持 | with CUDA 12.8 support)
- FFMPEG
- Python 3.x
- Ollama
- 更多 NVIDIA Jetson 特定包 | Additional NVIDIA Jetson-specific packages

## 使用方法 | Usage
### 构建容器 | Building the Container
```bash
cd base
make build
```

### 运行容器 | Running the Container
```bash
make run
```

## 系统要求 | System Requirements
- NVIDIA Jetson 设备 (Nano, Xavier, Orin 等) | NVIDIA Jetson device (Nano, Xavier, Orin, etc.)
- JetPack-L4T
- Docker

## 目录结构 | Directory Structure
```
.
├── base/                  # 基础容器配置 | Base container configuration
│   ├── Dockerfile        # 容器定义文件 | Container definition
│   ├── Makefile         # 构建脚本 | Build scripts
│   ├── requirements-*.txt # 依赖配置文件 | Dependency configurations
│   └── install-ollama.sh # Ollama 安装脚本 | Ollama installation script
└── README.md            # 项目文档 | Project documentation
```

## 许可证 | License
本项目采用 MIT 许可证。查看 [LICENSE](LICENSE) 文件了解更多信息。

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 贡献 | Contributing
欢迎提交 Pull Requests 和 Issues！

Pull Requests and Issues are welcome!
