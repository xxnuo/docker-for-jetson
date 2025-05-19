# 同步 Jetson 的 PyPI 源
sync:
	nohup uv run sync.py > sync.log 2>&1 & echo $$! > sync.pid

# 停止同步
stop-sync:
	kill -9 `cat sync.pid`

# 启动 PyPI 服务器
pypi-server:
	@echo "Serving pypi on http://localhost:10608/simple/"
	pypi-server run -p 10608 --fallback-url https://pypi.tuna.tsinghua.edu.cn/simple ./pypi

# 启动 PyPI 浏览器
pypi-web:
	@echo "Serving pypi web on http://localhost:10609/"
	PYPI_BROWSER_PYPI_URL=http://localhost:10608/simple/ uv run uvicorn pypi_browser.app:app --host 0.0.0.0 --port 10609

# 启动 PyPI 服务器和浏览器
serve:
	@echo "Starting PyPI server and web interface simultaneously..."
	nohup make pypi-server > pypi-server.log 2>&1 & echo $$! > pypi-server.pid
	nohup make pypi-web > pypi-web.log 2>&1 & echo $$! > pypi-web.pid

# 停止 PyPI 服务器和浏览器
stop-serve:
	kill -9 `cat pypi-server.pid`
	kill -9 `cat pypi-web.pid`

.PHONY: sync stop-sync pypi-server pypi-web serve stop-serve