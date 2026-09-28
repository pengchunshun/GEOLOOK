# 一次性脚本：每次新 PowerShell 沙箱会话启动 GEOLOOK 看板前先跑这个
# 用途：本环境下的 venv 是 ephemeral（沙箱临时），新会话会被重置回无依赖状态
# 不跑这个直接启看板 → 立刻报 ModuleNotFoundError: requests → UI 端连续 fetch 失败 → "失败：连续失败，服务未响应"
$ErrorActionPreference = "Stop"
$VenvPy = "C:\Users\Administrator\.venv-html-to-docx\Scripts\python.exe"
Write-Host "[ensure-deps] bootstrapping pip..." -ForegroundColor Cyan
& $VenvPy -m ensurepip --upgrade | Out-Null
Write-Host "[ensure-deps] installing requests / beautifulsoup4 / lxml..." -ForegroundColor Cyan
& $VenvPy -m pip install --quiet requests beautifulsoup4 lxml
Write-Host "[ensure-deps] verifying..." -ForegroundColor Cyan
& $VenvPy -c "import requests, bs4, lxml; print('[ensure-deps] OK', requests.__version__, bs4.__version__, lxml.__version__)"
Write-Host "[ensure-deps] done. you can now run: & '$VenvPy' scripts/geo.py ui" -ForegroundColor Green
