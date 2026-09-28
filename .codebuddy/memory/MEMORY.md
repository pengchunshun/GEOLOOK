# 项目长期记忆 (MEMORY.md)

## 环境关键信息
- **系统**：Windows（PowerShell），无全局 `python` / `python3` 命令。
- **可用 Python 解释器**：`C:\Users\Administrator\.venv-html-to-docx\Scripts\python.exe`（Python 3.12.14）。
  - 该 venv 原本无 pip，需用 `python -m ensurepip --upgrade` 引导出 pip 25.0.1。
  - **关键陷阱**：此 venv 是 **ephemeral（沙箱临时）**——每次 PowerShell 沙箱会话结束 venv 状态会被重置回初始，每次新会话必须重新跑 `ensurepip` + `pip install requests beautifulsoup4 lxml`。如果不重装就启动看板，看板会立刻报 `ModuleNotFoundError: requests` 退出，浏览器端 fetch 全部失败，前端兜底弹出"失败：连续失败，服务未响应"——这正是 2026-08-21 用户截图报错（红线指向 DEEPSEEK_API_KEY 输入框，右下角红框为"失败：连续失败，服务未响应"）的真实根因，与 API KEY 本身无关。
- **外网连通**：python.org 返回 200，可正常 pip install。
- **Windows 兼容性**：项目自带 `scripts/fcntl.py`（msvcrt 兼容层），可原生 Windows 直接跑，无需 WSL。

## 项目技术栈
- 纯 Python 3.9+ 项目，仅 3 个第三方依赖：requests / beautifulsoup4 / lxml。
- 无 package.json / go.mod / requirements.txt / pyproject.toml（依赖在 README 里以 pip 命令给出）。
- 前端是单文件 `scripts/ui.html`（零依赖），后端用标准库 http.server。
- 入口 CLI：`scripts/geo.py`（ui / new / init / serve / sample ...）。看板默认 http://127.0.0.1:8765。

## 启动命令模板（必须用解释器完整路径）
```
cd g:\AI_SPACE\CodeBuddy\geolook
C:\Users\Administrator\.venv-html-to-docx\Scripts\python.exe scripts/geo.py ui
```
注意：SKILL.md 中的 `/Users/brucejan/geo` 仅为作者示例路径，本项目根目录是 `g:\AI_SPACE\CodeBuddy\geolook`。

## 当前工作区未跟踪/改动文件（2026-08-21 状态）
- `scripts/fcntl.py`：新增的 Windows fcntl 兼容层（项目能原生跑 Windows 的关键）。
- `scripts/sample.py`：被修改过（本地改动）。
- `scripts/ensure-deps.ps1`：新增（每次新会话重装依赖，规避 venv 沙箱重置）。
- `docs/geolook-guide.html` / `docs/geolook-guide.md`：新增文档。

## 已交付功能：修改品牌信息（名称/域名）
- 需求：允许用户自定义品牌名 + 域名，含输入界面、域名校验、二次确认流程、修改历史追溯、全局生效。
- 采用最小改动策略（用户明确"最小改动即可"），**不改 work/<slug>/ 目录名**（slug 保持目录名权威，geo.json.slug 字段同步，避免路径耦合 bug）。
- 改动文件：
  - `scripts/geolib.py`：新增 `validate_domain()`（RFC1123 宽松校验）、`update_brand(slug,name,site)`（带 project_lock、写 history/brand-changes.jsonl）、`read_brand_history()`；`read_json` 加 GBK fallback 兼容历史乱码文件并自动转 UTF-8 重写。
  - `scripts/dashboard.py`：新增路由 `PUT /api/project/<slug>/brand`（X-Confirm 头做二次确认 + 预检只校验）、`/api/project/<slug>/brand-history`；新增 `do_PUT` 委托 `do_POST`（保持 self.command=='PUT'，路由据此要求 X-Confirm）。
  - `scripts/ui.html`：设置页"当前品牌"行加"修改品牌信息"按钮 → `editBrand()` 弹窗（名称+域名+确认勾选+历史表格）；`saveBrand()` 先预检再带 X-Confirm 保存后 `load(SLUG,true)` 全局刷新；zh/en/ja 三语言字典新增 12 个键。
  - `scripts/geolib.py`：顶部加 `_ensure_dependencies()`——任何子进程 import geolib 时如果缺 requests/bs4/lxml，自动 ensurepip + pip install。修复"onboard autopilot 因 venv 沙箱重置子进程缺依赖失败"问题（用户截图"全自动引导失败 / ModuleNotFoundError: requests"第三次出现）。
- autopilot 验证（smoketest）：用 `--no-site --skip-llm` 跑完整 8 步（抓取/体检/推导/采样/工单/资产/报告/交付）全通，生成 report.html + tasks.json + blueprint.json + delivery 目录，无 ModuleNotFoundError。
- 限制：SLUG_OK 正则 `^[a-z0-9一-鿿-]{0,47}$` 不含下划线，测试时 `__smoke__` slug 被拒；合法形式是 `smoketest` / `my-brand-1`。
- 坑：dashboard 原只有 do_GET/do_POST，PUT 会 501，必须显式加 do_PUT；brand 路由用 self.headers.get("X-Confirm") 而非未定义的 headers 变量；PowerShell Get-Content 会以 GBK 渲染 UTF-8 文件（视觉乱码，文件本身正确）。
- 验证：同一命令块内 ensure-deps → 启动看板 → 调 API。坏域名被拦、好域名预检 ok、确认后 changed 正确、slug 不变、UTF-8 正确、历史可读。

## 另一个项目：workflow_1.0.1（星火之光·小红书图文发布系统 v1.5）
- 路径：`d:\senveyAIKnow\02.创富\星火之光\02.AIGC商业项目\03.产品开发\workflow_1.0.1`（注意路径含中文与空格，PowerShell 需加引号）。
- 技术栈：FastAPI + uvicorn + Pillow + Jinja2 + PyYAML，入口 `hongshuPublish.py`，端口 8000，前端 `static/index.html`。
- 启动前必做（venv ephemeral）：`python -m ensurepip --upgrade` → `pip install -r requirements.txt`。
- 后台启动：`Start-Process` + `-RedirectStandardOutput server.log -RedirectStandardError server.err`；健康检查 `http://127.0.0.1:8000/api/health`。
- 有 `.env`（已配 DeepSeek LLM），`hs_config.py` 会自动加载 .env 补全环境变量。
