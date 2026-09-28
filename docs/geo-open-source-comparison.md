# 同类开源前沿方案对比（GEO / AI 可见性优化）

> 生成日期：2026-08-21
> 说明：GEOLOOK 自身即开源方案，本文聚焦功能相近的**开源**竞品对比。
> GEOLOOK 定位为「端到端 GEO 实现平台」（诊断 → 工单 → 资产 → 验收 → 交付）。

---

## 1. GeoBench（`NomaDamas/geobench`）

**核心能力简述**：对标 Profound/Semrush/AthenaHQ 的开源 GEO Benchmark。覆盖 OpenAI、Anthropic、Google、Perplexity、xAI、OpenRouter 等 6 家供应商，计算命中率、语义排名 MRR、竞品声量份额 SoV、引用率、情感分析，带 Bootstrap 95% 置信区间与本地只读仪表盘（Vite，:5173）。支持跨"API/CLI/浏览器"三角验证、断点续跑。

**资源获取明细**：

| 资源类型 | 可能来源 | 获取路径描述 |
|---|---|---|
| 源码仓库 | GitHub | `git clone https://github.com/NomaDamas/geobench` |
| 运行时 | Bun 官方 | 按 bun.sh 文档安装 Bun（仓库用 `bun install`，非 npm） |
| 依赖库 | 包生态 | `bun install` 拉取依赖；配置文件 `bun.lock` / `biome.json` |
| 自托管仪表盘 | 仓库内置 | `bun scripts/seed-demo-runs.ts` 生成免费用演示数据 → `geobench dash` 启本地面板 |
| 数据集/查询集 | 仓库 fixtures | `fixtures/sample.yaml`（品牌 spec）、`fixtures/triangulation-frozen-50.yaml`（冻结验证集） |
| 方法论文档 | 仓库 docs/ | `docs/methodology.md`、`docs/runbooks/profile-workflow.md` |
| 供应商 API Key | 各厂商 | `.env` 填 `OPENAI_API_KEY`/`ANTHROPIC_API_KEY`/…（或用 Claude Code/Codex/Gemini CLI 代理免 Key） |
| 社区渠道 | GitHub | Issues / PR（当前 65★，无外部 Discord）；GitHub Discussions 平台级 |

---

## 2. GEOVisibilityTool（`MasashiToda1/GEOVisibilityTool`，原 `KnightMafiaLau`）

**核心能力简述**：模块化 GEO 测试 harness，由 6 个 Claude Code Skill 组成（生成测试问题 → 浏览器操作真实 LLM 网页端提问 → 算 0–100 可见度分 → 出 CEO 报告 → 给投放渠道建议）。支持国内 Kimi/豆包/DeepSeek/文心/千问/元宝；`probe.py` 仅用 Python 标准库、零外部依赖；全本地运行，数据存 `~/.geo-kb/kb.sqlite`。Apache-2.0。

**资源获取明细**：

| 资源类型 | 可能来源 | 获取路径描述 |
|---|---|---|
| 源码仓库 | GitHub | `git clone https://github.com/KnightMafiaLau/GEOVisibilityTool.git` |
| 客户端 | Anthropic | 安装 Claude Code（或任意支持 Anthropic Skills 的 Claude 客户端） |
| 技能安装 | 本地目录 | 将 `skills/` 下 6 个模块 `cp` 到 `~/.claude/skills/`，重启客户端 |
| 浏览器自动化 | MCP | 配置浏览器 MCP server 供 `probe.py` 操作 LLM 网页端 |
| 数据集 | 运行时生成 | 测试问题由 `geo-queries` 基于品牌信息动态生成；无外部公开数据集 |
| 知识库 | 本地 SQLite | 每次运行累积到 `~/.geo-kb/kb.sqlite`，备份即 `cp`；示例见 `examples/`（如简知 App 案例） |
| Hooks 约束 | 仓库 hooks/ | `hooks/install.sh`（需 jq，自动备份 `~/.claude/settings.json`） |
| 社区渠道 | GitHub | Issues（Recipe Broken / Query Feedback / Channel Pattern 模板）、Discussions、CONTRIBUTING.md、TASKS.md 路线图 |

---

## 3. OneGlanse（`aryamantodkar/oneglanse`）

**核心能力简述**：自称"唯一免费开源 GEO 追踪器"。通过抗指纹浏览器（Camoufox/Playwright）**对抗真实产品 UI**（非 API）捕获 ChatGPT/Gemini/Perplexity/Claude/Google AI Overview 的实际回复、内联引用、竞品共现；自带 LLM Key 做 GEO 打分；ClickHouse 时序存储；单命令 Docker 部署。MIT，153★。

**资源获取明细**：

| 资源类型 | 可能来源 | 获取路径描述 |
|---|---|---|
| 源码仓库 | GitHub | `git clone https://github.com/aryamantodkar/oneglanse` |
| 运行环境 | Node/Docker | Node.js 20+ / pnpm 10+ / Docker；`cp .env.example .env` → `pnpm local` 启动 :3000 |
| 关键依赖库 | 开源生态 | Camoufox（MPL-2.0 抗指纹 Firefox）、Playwright、BullMQ、ClickHouse、Drizzle ORM、Better Auth、Turndown |
| 分析模型 | 自带 Key | `.env` 配置 `OPENAI_API_KEY` 或 `ANTHROPIC_API_KEY` 做响应分析 |
| 数据源 | 用户真实会话 | 在 `/providers` 连接自有 ChatGPT/Gemini 等账号；VPS 部署需住宅代理（如 ThorData） |
| 文档站 | 官方 | `docs.oneglanse.com`（含部署/代理指南）、落地页 `oneglanse.com` |
| 社区渠道 | GitHub | Issues / PR、CONTRIBUTING.md、CODE_OF_CONDUCT.md、SECURITY.md；作者欢迎加供应商/改文档 |

---

## 4. Aperture（`anyin-ai/aperture`）

**核心能力简述**：开源"AI 可见性基础设施"，Profound/Peec AI 的免费自托管替代。监控 ChatGPT/Perplexity/Google AI Overviews 等是否在关键查询推荐你的品牌，对比竞品被引用原因，跨模型/语言/市场做结构化审计，随时间追踪。BYOK、自托管、MIT。当前 25★（早期项目）。

**资源获取明细**：

| 资源类型 | 可能来源 | 获取路径描述 |
|---|---|---|
| 源码仓库 | GitHub | `git clone https://github.com/anyin-ai/aperture` |
| 部署 | Docker | `docker-compose.yml` 一键编排；详见仓库 `DOCS.md` / `DEPLOY.md` / `README.md` |
| 运行时存储 | 内置 | 本地 SQLite（无需外部 DB；MVP 期密钥明文存，仅限 localhost/私网或加反代鉴权） |
| BYOK 提供商 | 各厂商 | 配 OpenAI（gpt-4o-mini）、Perplexity（sonar）Key；支持任意 OpenAI 兼容端点（Ollama/vLLM/自定义 Base URL） |
| 数据集 | 用户定义 | 审计查询、品牌/竞品列表、目标市场与语言由用户自定 |
| 构建方资源 | Anyin | 关联 AEO 代理公司 https://anyin.ai（无独立论坛） |
| 社区渠道 | GitHub | Issues / PR（CONTRIBUTING.md）；含 `AGENTS.md`/`CLAUDE.md` AI 编码规则；当前 35 commits、25★ |

---

## 5. GEO-AEO Tracker（Bright Data，`danishashko/geo-aeo-tracker`）

**核心能力简述**：Bright Data 官方开源的本地优先 AI 可见性仪表盘。Prompt Hub 并行跑 6 个模型（ChatGPT/Perplexity/Gemini/Grok/Google AI Mode/Copilot），生成 0–100 可见度评分、引用机会（竞品被引而你未出现的 URL）、SRO 优化分析、Drift 告警、竞品 Battlecards。数据存浏览器 IndexedDB，无外部数据库。

**资源获取明细**：

| 资源类型 | 可能来源 | 获取路径描述 |
|---|---|---|
| 源码仓库 | GitHub | `git clone https://github.com/danishashko/geo-aeo-tracker.git` |
| 在线 Demo | Bright Data | `demos.brightdata.com/geo-tracker`（免 Key 试用） |
| 运行 | npm | `npm install` → `.env` 填 `BRIGHT_DATA_KEY` + 6 个 dataset ID → `npm run dev` |
| 数据源（核心） | Bright Data | LLM Scrapers（6 个模型 dataset ID 从 Scrapers Marketplace 获取）、SERP API、Web Unlocker（按量计费 ~$1.50/1K 记录，BYOK） |
| 增强依赖 | Google | Gemini API（SRO 管道第 1 阶段 Grounding） |
| 数据集 | 实时查询 | 无静态数据集；回答经 `normalizeAnswer()` 统一格式后存 IndexedDB |
| 配套文章 | Bright Data 博客 | `brightdata.com/blog/ai/ai-visibility-tracker`（含架构与抓取细节） |
| 社区渠道 | GitHub | 仓库 Issues/PR；以 Bright Data 官方社区/文档为外围支持 |

---

## 横向速览

| 方案 | 开源协议 | 引擎覆盖 | 是否含"诊断→执行闭环" | 自托管 | 标杆度 |
|---|---|---|---|---|---|
| **GEOLOOK**（参照） | MIT | 17 引擎（含 7 国内） | ✅ 工单+资产+验收+交付 | ✅ 纯 Python | 最完整实现平台 |
| GeoBench | 未注明(Public) | 6 家(API/CLI/浏览器) | ❌ 仅 benchmark | ✅ Bun | 指标严谨、带 CI |
| GEOVisibilityTool | Apache-2.0 | 国内 6 家 + 自定义 | ❌ 测量+策略报告 | ✅ Claude Skill | 国内覆盖强、零依赖 |
| OneGlanse | MIT | 5 家(真实 UI) | ❌ 监控+评分 | ✅ Docker | 星标最高、UI 真实捕获 |
| Aperture | MIT | ChatGPT/Perplexity(规划扩) | ❌ 监控+审计 | ✅ Docker | 早期、轻量 |
| GEO-AEO Tracker | 未注明 | 6 家(经 Bright Data) | ❌ 监控+评分 | ✅ 浏览器本地 | 企业数据源、需付费 Key |

---

## 结论建议

- 与 GEOLOOK 最可比的是 **GeoBench**（指标方法论最严谨）与 **OneGlanse**（真实 UI 捕获、社区最活跃）。
- 若关注**国内市场**，则 **GEOVisibilityTool** 的国内引擎覆盖最直接互补。
- 三者均为纯监测/分析层，只有 GEOLOOK 覆盖了"诊断 → 生成可部署资产 → 自动验收 → 客户交付"的完整实现闭环。
