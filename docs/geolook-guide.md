# GEOLOOK 专业应用指导文档

> 面向技术用户与 GEO 顾问的完整操作指南：从项目架构、核心模块，到设计理念、典型场景与落地建议。
> 本指南依据 `scripts/` 代码实现与 `references/method.md` 实证口径整理。文档与代码同源，出现分歧时以代码为准。

- **版本基线**：2026-08
- **运行入口**：`python scripts/geo.py <command>`
- **看板**：`geo.py ui` → http://127.0.0.1:8765/
- **环境自检**：`python scripts/geo.py doctor`

---

## 概述

GEOLOOK 是一套面向"星火之光生成式引擎优化（GEO）"的**可运行方法论**：它把抽象的"让 AI 更懂你的品牌"拆解成一组可被抓取、计算、验收、交付的工程动作。所有评分口径并非拍脑袋，而是来自 `references/` 中记录的实测数据（如 CNN/GEO、CN-GEO 论文与 citation-lab 实证数字）。

工具提供两条使用路径：

- **可视化看板**（`dashboard.py`，适合客户演示与团队协作）
- **命令行**（`geo.py`，适合自动化与批量处理）

两者共享同一套 `scripts/` 业务逻辑，产出统一存放在 `work/<slug>/` 工作区。

### 标准工作流

| 步骤 | 命令 | 说明 |
|---|---|---|
| STEP 0 | `doctor` | 环境自检：依赖 / API Key / 浏览器 |
| STEP 1 | `init` | 建项目 + facts 事实卡 |
| STEP 2 | `audit` | 页面 GEO 体检 + 评分 |
| STEP 3 | `sample` | AI 答案采样 |
| STEP 4 | `plan` | 生成工单 |
| STEP 5 | `generate` | 产出资产 |
| STEP 6 | `verify` | 自动验收 |
| STEP 7 | `deliver` | 交付客户 |

---

## 1 · 项目架构说明

GEOLOOK 采用"薄入口 + 厚逻辑 + 单一真相源"的分层结构。所有命令都经 `geo.py` 分发，业务逻辑在独立模块中，执行状态集中在 `work/<slug>/tasks.json`。

### 三层架构

**① 入口层（命令分发与交互）**
- `geo.py` — CLI 主入口
- `dashboard.py` — Web 看板（Flask）
- `doctor.py` — 环境自检
- `webui.py` — 看板后端 API

**② 逻辑层（核心业务能力）**
- `audit.py` — 体检评分
- `sample.py` — 答案采样
- `tasks.py` — 工单生成
- `generate.py` — 资产生成
- `verify.py` — 自动验收
- `report.py` / `deliver.py` — 报告与交付

**③ 支撑层（基础设施）**
- `geolib.py` — 公共库 / 抓取 / 配置
- `fcntl.py` — Windows 文件锁兼容
- `config.py` — 配置加载
- `fetch.py` — 抓取器
- `tests/` — 单元与回归测试

### 工作区产物（`work/<slug>/`）

| 路径 | 含义 |
|---|---|
| `config.json` | 项目配置：域名、市场（cn/en/both）、语言、关注竞品 |
| `content/facts.md` | **事实卡**：一句话定义、关键数字、适用/不适用场景——评分与资产生成的唯一事实源 |
| `audit.json` | 页面体检结果 + 0–100 评分 + issue 清单 |
| `samples/` · `metrics/` | 各平台 AI 答案采样与可见性指标 |
| `tasks.json` | **单一真相源**：工单的生成 / 状态 / 验收回写都在这里 |
| `assets/` | llms.txt、JSON-LD、HTML 片段、内容大纲与初稿 |
| `delivery/<日期>/` | 可直接发给客户的交付包 |

> **设计要点**：`tasks.json` 是"执行状态的唯一真相源"。`plan` 生成工单、`generate` 回写资产路径、`verify` 回写验收状态——三阶段都围绕同一份文件读写，避免多份状态互相打架。

---

## 2 · 核心模块功能介绍

每个模块职责单一、可独立运行，通过 `geolib` 公共库共享抓取与配置能力。

### audit.py — 页面 GEO 体检
把 citation-lab 实证结论变成可计算分数：
- 长度（Top 四分位 1,943 词 vs Bottom 170 词，11.4×）
- 结构（标题 / 段落 / 列表密度）
- 抽取块（数字 +61.6%、定义 +57.3%、对比 +55.3%、how-to +41.2%）
- 对题性（`llm_relevance_score`，r=0.432 最强预测因子）

### sample.py — AI 答案采样
把问题库打到各引擎量化"品牌在 AI 答案里的可见性"。三种模式：
- `api`：有 API 直跑（DeepSeek / 千问 / Kimi / 任意 OpenAI 兼容端点）
- `browser`：网页端由 Claude 逐条采，结果 import 回来
- `manual`：导出问题清单，人工粘贴答案后 import

**关键口径**：API 结果 ≠ 网页端结果，同一产品 Web 与 App 的信源集合都有系统性差异（CN-GEO 论文结论），所以每个平台 + 终端单独记录，绝不混算。

### tasks.py — 工单系统
把诊断变成分派 / 验收 / 追踪的执行任务。**每条工单必须含**：依据（追到 method.md 哪条）、负责角色、验收标准、市场。无验收标准的不叫工单叫愿望。内置风险分级（low / watch / high）。

### generate.py — 资产生成器
产出到 `assets/`，中英分开：llms.txt、JSON-LD、定义 / FAQ 片段、内容大纲、可选 LLM 初稿。

**分工原则**：结构性资产由代码确定性生成（不漏字段、不写错格式）；文章正文由 LLM 按大纲写（代码写不出好文案）。

### verify.py — 验收闭环
重抓站点 → 跑 checker → 回写 tasks.json 状态。"建议"与"服务"的分界：能自动验收的，不靠人说做完了。支持 `site.` / `pages.` / `metrics.` / `external.` 四类共 20+ 种校验规则。

### report.py / deliver.py — 报告与交付
把一期产出打成可直接发客户的目录：总览 HTML、诊断报告、30/60/90 执行方案、工单表、验收表、资产包。面向客户故不出现内部脚本名，每个结论写清依据，不承诺任何平台必然引用。

### 验收规则语法（verify）

| 类别 | 示例规则 | 含义 |
|---|---|---|
| site. | `site.no_ai_bot_block` | robots 不再整站封 AI 抓取器 |
| site. | `site.llms_txt_valid` | llms.txt 抽样链接全部有效且未被封 |
| site. | `site.avg_score_gte:70` | 重跑 audit 均分达标 |
| pages. | `pages.has_jsonld` | 受影响页面已挂 JSON-LD |
| pages. | `pages.block:定义` | 缺该抽取块的页面数下降 ≥50% |
| metrics. | `metrics.mention_rate_gte:cn:0.3` | 指定市场平均无提示提及率达标 |
| external. | `external.any:a.com,b.com` | 采样里出现任一目标域名的引用 |

> **相对型指标**（如"下降 50%"）用工单的 `baseline_count`（生成工单时的真实缺口数）做基线，而非凭空设定目标。这是验收可信的关键。

---

## 3 · 设计理念与实现逻辑

GEOLOOK 的底层信念：GEO 不是玄学，是一组可被度量、可被工程化、可被验收的"可见性动作"。

### 四条核心理念

**① 实证驱动，拒绝拍脑袋**
所有评分阈值与权重来自 `references/method.md` 的实测数字。规则与数据可回溯，结论可辩护。

**② 代码确定性 vs 人写文案**
结构性资产（llms.txt、JSON-LD、HTML 片段）由代码生成，保证不漏 schema 字段、不写错格式；文章正文交给 LLM 按大纲写，代码不越俎代庖。

**③ 单一真相源 + 自动验收**
`tasks.json` 是执行状态唯一来源，`verify` 不修改内容只重抓判定，把"建议"升级为"服务"。

**④ 风险分级与保护性纪律**
优先级说"多重要"，风险说"动手多小心"，二者独立。解封 robots 是 P0 也是**高风险**（错一行封全站），执行顺序按"先低风险、高风险单独排期并留回滚"。

### 关键工程取舍

- **跨平台兼容**：`fcntl.py` 是 Windows 文件锁兼容层（基于 `msvcrt`），使原本依赖 Unix `fcntl` 的代码可在 Windows 原生运行，无需 WSL。
- **平台隔离**：`sample.py` 的 `PROVIDERS` 注册表区分 cn / en 市场与观测集合；Web 与 App 答案分终端单独记录，避免混算失真。
- **三语安全**：抽取块正则同时覆盖中 / 英 / 日表述，否则会把日文页整体误判为"缺块"；"如何 / 怎么"等弱信号必须配合列表结构才计为操作步骤块，防止问句标题刷分。
- **功能页豁免**：登录 / 注册 / 购物车 / 联系页等天然低内容，不按 SPA 空壳 P0 误报（`FUNC_PAGE` 正则）。
- **最小检索单元**：按 H2 把正文切成段落组——一段能独立回答问题的文字可赢过竞品整页（GEO Readiness Manual）。

---

## 4 · 典型应用场景

| 场景 | 做法 |
|---|---|
| **A. 出海品牌的双语 GEO** | 配置 `market: both`，audit 与 sample 双市场并行，generate 自动产出 `llms.txt` 与 `llms.en.txt`；verify 用 `site.lang_balance` / `site.en_pages_gte` 验收中英文页面均衡度。 |
| **B. SaaS 产品的可引用性改造** | audit 识别"缺数字 / 定义 / 对比 / FAQ 块"的页面，generate 产出 definition/faq 片段与 JSON-LD，verify 用 `pages.block:*` 验收抽取块补齐。 |
| **C. AI 爬虫被误封的恢复** | audit 报 `site.no_ai_bot_block` / `site.no_ai_ua_block`，plan 生成高风险工单，verify 重抓确认 robots 放行——典型"P0 + 高风险"排期。 |
| **D. 代理机构批量客户交付** | 每客户一个 slug，dashboard 切换项目；`deliver` 输出客户友好的 HTML/CSV 包，不暴露内部脚本名，结论附依据。 |
| **E. 竞品可见性基准对比** | config 配置 `competitors`，sample 量化自身与竞品在各引擎的提及 / 引用率，`metrics.own_cite_gte` 跟踪官网被引用占比。 |
| **F. 持续监测闭环** | 周期性重跑 `sample → verify`，用 `external.any` 与 `metrics.*` 监控外站引用与品牌提及趋势，形成月度 / 季度报告。 |

---

## 5 · 使用建议

### ① 启动与运行
- **看板方式（推荐客户演示 / 团队协作）**：`python scripts/geo.py ui` → 浏览器打开 http://127.0.0.1:8765/
- **命令行方式（推荐自动化 / 批量）**：直接调用 `geo.py <command>`
- **Windows 用户**：无需 WSL，脚本自带 `fcntl` 兼容层。运行时确保 `scripts/` 在 `PYTHONPATH` 中（本地 `fcntl.py` 优先于系统模块被导入）。
- **启动前自检**：`python scripts/geo.py doctor` 自检依赖、API Key、浏览器是否就绪，避免中途中断。

### ② 标准操作流程

```bash
# 1) 建项目并填写事实卡（最关键的一步）
python scripts/geo.py init   # 按提示填 facts.md

# 2) 体检 + 采样（可并行）
python scripts/geo.py audit
python scripts/geo.py sample

# 3) 生成工单 → 产出资产 → 自动验收
python scripts/geo.py plan
python scripts/geo.py generate
python scripts/geo.py verify

# 4) 交付
python scripts/geo.py deliver
```

> **事实卡是第一生产力。** `content/facts.md` 是评分与资产生成的唯一事实源。定义一句话、关键数字表、适用 / 不适用场景填得越准，下游 llms.txt 与 JSON-LD 质量越高。务必先把它写扎实。

### ③ 工单执行纪律
- **优先级 ≠ 风险**：按"先低风险快速优化，高风险技术改造单独排期并留回滚"的顺序推进。
- **没有验收标准的不接**：工单必须有可校验的 `acceptance.check`，否则是愿望不是任务。
- **watch 类任务看窗口**：改已有页面内容后，按 7 / 14 / 28 天观察窗看真实数据再判定。

### ④ 避坑清单

**不要做**
- 不要混算不同平台 / 终端的采样结果
- 不要把"建议"当"已交付"——以 verify 结果为界
- 不要在没回滚预案时动 robots / WAF / noindex
- 不要向客户承诺"某平台一定引用"

**应该做**
- 先 `doctor` 自检再开跑
- 把事实卡 / 工单 / 资产统一收进一个 slug
- 结构性资产用 generate 确定性产出
- 周期性 `sample → verify` 形成监测闭环

> **依赖说明**：部分模块（`sample` / `generate` 调用的 LLM）需要 `requests / bs4 / lxml` 与对应平台 API Key（如 `ZHIPUAI_API_KEY`、`ARK_API_KEY`）。缺失 API Key 时，相关平台自动降级为 manual 采样，不会中断整期。

---

## 6 · 附录 · 命令速查

| 命令 | 作用 |
|---|---|
| `geo.py doctor` | 环境自检（依赖 / API Key / 浏览器） |
| `geo.py init` | 新建项目，初始化 facts.md 与 config.json |
| `geo.py audit` | 抓取并体检页面，产出 audit.json + 评分 |
| `geo.py sample` | 对各引擎采样 AI 答案，产出 samples/metrics |
| `geo.py plan` | 从诊断生成可验收工单（tasks.json） |
| `geo.py generate` | 按工单确定性生成资产（assets/） |
| `geo.py verify` | 重抓并重跑 checker，回写工单状态 |
| `geo.py report` | 生成本期诊断与可见性报告 |
| `geo.py deliver` | 打包客户交付目录 |
| `geo.py ui` | 启动 Web 看板（默认 8765 端口） |

> 本文档与代码同源：所有评分口径、规则语法、风险分级均可在 `scripts/` 对应模块与 `references/method.md` 中查到对应实现。当文档与代码出现分歧时，以代码为准。
