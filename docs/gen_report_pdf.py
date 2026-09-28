# -*- coding: utf-8 -*-
"""Generate GEO open-source comparison report as a PDF using reportlab."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, PageBreak
)

OUT = r"g:\AI_SPACE\CodeBuddy\geolook\docs\geo-open-source-comparison.pdf"

# ---- styles ----
styles = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=styles["Title"], fontSize=20, leading=26,
                    textColor=colors.HexColor("#2b2348"), spaceAfter=4)
SUB = ParagraphStyle("SUB", parent=styles["Normal"], fontSize=11, leading=15,
                     textColor=colors.HexColor("#5b6478"), alignment=TA_CENTER)
H2 = ParagraphStyle("H2", parent=styles["Heading2"], fontSize=14, leading=18,
                    textColor=colors.HexColor("#3a2f63"), spaceBefore=10, spaceAfter=2)
CAP = ParagraphStyle("CAP", parent=styles["Normal"], fontSize=9, leading=12,
                     textColor=colors.HexColor("#9184d9"), fontName="Courier")
BODY = ParagraphStyle("BODY", parent=styles["Normal"], fontSize=10, leading=14,
                      textColor=colors.HexColor("#1f2430"), alignment=TA_LEFT,
                      spaceBefore=4, spaceAfter=4)
TH = ParagraphStyle("TH", parent=styles["Normal"], fontSize=9, leading=12,
                    textColor=colors.white, fontName="Helvetica-Bold")
TD = ParagraphStyle("TD", parent=styles["Normal"], fontSize=8.5, leading=11,
                    textColor=colors.HexColor("#23272f"))
NOTE = ParagraphStyle("NOTE", parent=BODY, fontSize=10, leading=14,
                      textColor=colors.HexColor("#1f2430"))

story = []

def P(t, s=BODY):
    return Paragraph(t, s)

def cell(t):
    return Paragraph(t, TD)

def hcell(t):
    return Paragraph(t, TH)

# ---- header ----
story.append(P("同类开源前沿方案对比", H1))
story.append(P("GEO / AI 可见性优化（SparklightAI Generative Engine Optimization）", SUB))
story.append(P("功能类似 GEOLOOK 的开源软件与平台 · 候选方案与资源获取明细", SUB))
story.append(Spacer(1, 4))
story.append(P("生成日期：2026-08-21 ｜ GEOLOOK 自身即开源方案，本文聚焦功能相近的开源竞品对比", SUB))
story.append(Spacer(1, 8))
story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#9184d9")))
story.append(Spacer(1, 8))

# ---- data ----
schemes = [
    {
        "name": "GeoBench",
        "repo": "NomaDamas/geobench",
        "cap": "对标 Profound/Semrush/AthenaHQ 的开源 GEO Benchmark。覆盖 OpenAI、Anthropic、Google、Perplexity、xAI、OpenRouter 等 6 家供应商，计算命中率、语义排名 MRR、竞品声量份额 SoV、引用率、情感分析，带 Bootstrap 95% 置信区间与本地只读仪表盘（Vite，:5173）。支持跨“API/CLI/浏览器”三角验证、断点续跑。",
        "rows": [
            ("源码仓库", "GitHub", "<font name='Courier'>git clone https://github.com/NomaDamas/geobench</font>"),
            ("运行时", "Bun 官方", "按 bun.sh 文档安装 Bun（仓库用 <font name='Courier'>bun install</font>，非 npm）"),
            ("依赖库", "包生态", "<font name='Courier'>bun install</font> 拉取依赖；配置文件 <font name='Courier'>bun.lock</font> / <font name='Courier'>biome.json</font>"),
            ("自托管仪表盘", "仓库内置", "<font name='Courier'>bun scripts/seed-demo-runs.ts</font> 生成免费用演示数据 → <font name='Courier'>geobench dash</font> 启本地面板"),
            ("数据集/查询集", "仓库 fixtures", "<font name='Courier'>fixtures/sample.yaml</font>（品牌 spec）、<font name='Courier'>fixtures/triangulation-frozen-50.yaml</font>（冻结验证集）"),
            ("方法论文档", "仓库 docs/", "<font name='Courier'>docs/methodology.md</font>、<font name='Courier'>docs/runbooks/profile-workflow.md</font>"),
            ("供应商 API Key", "各厂商", "<font name='Courier'>.env</font> 填 OPENAI_API_KEY/ANTHROPIC_API_KEY/…（或用 Claude Code/Codex/Gemini CLI 代理免 Key）"),
            ("社区渠道", "GitHub", "Issues / PR（当前 65★，无外部 Discord）；GitHub Discussions 平台级"),
        ],
    },
    {
        "name": "GEOVisibilityTool",
        "repo": "MasashiToda1/GEOVisibilityTool（原 KnightMafiaLau）",
        "cap": "模块化 GEO 测试 harness，由 6 个 Claude Code Skill 组成（生成测试问题 → 浏览器操作真实 LLM 网页端提问 → 算 0–100 可见度分 → 出 CEO 报告 → 给投放渠道建议）。支持国内 Kimi/豆包/DeepSeek/文心/千问/元宝；probe.py 仅用 Python 标准库、零外部依赖；全本地运行，数据存 ~/.geo-kb/kb.sqlite。Apache-2.0。",
        "rows": [
            ("源码仓库", "GitHub", "<font name='Courier'>git clone https://github.com/KnightMafiaLau/GEOVisibilityTool.git</font>"),
            ("客户端", "Anthropic", "安装 Claude Code（或任意支持 Anthropic Skills 的 Claude 客户端）"),
            ("技能安装", "本地目录", "将 <font name='Courier'>skills/</font> 下 6 个模块 <font name='Courier'>cp</font> 到 <font name='Courier'>~/.claude/skills/</font>，重启客户端"),
            ("浏览器自动化", "MCP", "配置浏览器 MCP server 供 <font name='Courier'>probe.py</font> 操作 LLM 网页端"),
            ("数据集", "运行时生成", "测试问题由 <font name='Courier'>geo-queries</font> 基于品牌信息动态生成；无外部公开数据集"),
            ("知识库", "本地 SQLite", "每次运行累积到 <font name='Courier'>~/.geo-kb/kb.sqlite</font>，备份即 <font name='Courier'>cp</font>；示例见 <font name='Courier'>examples/</font>"),
            ("Hooks 约束", "仓库 hooks/", "<font name='Courier'>hooks/install.sh</font>（需 jq，自动备份 ~/.claude/settings.json）"),
            ("社区渠道", "GitHub", "Issues / Discussions / CONTRIBUTING.md / TASKS.md 路线图"),
        ],
    },
    {
        "name": "OneGlanse",
        "repo": "aryamantodkar/oneglanse",
        "cap": "自称“唯一免费开源 GEO 追踪器”。通过抗指纹浏览器（Camoufox/Playwright）<b>对抗真实产品 UI</b>（非 API）捕获 ChatGPT/Gemini/Perplexity/Claude/Google AI Overview 的实际回复、内联引用、竞品共现；自带 LLM Key 做 GEO 打分；ClickHouse 时序存储；单命令 Docker 部署。MIT，153★。",
        "rows": [
            ("源码仓库", "GitHub", "<font name='Courier'>git clone https://github.com/aryamantodkar/oneglanse</font>"),
            ("运行环境", "Node/Docker", "Node.js 20+ / pnpm 10+ / Docker；<font name='Courier'>cp .env.example .env</font> → <font name='Courier'>pnpm local</font> 启动 :3000"),
            ("关键依赖库", "开源生态", "Camoufox（MPL-2.0）、Playwright、BullMQ、ClickHouse、Drizzle ORM、Better Auth、Turndown"),
            ("分析模型", "自带 Key", "<font name='Courier'>.env</font> 配置 OPENAI_API_KEY 或 ANTHROPIC_API_KEY 做响应分析"),
            ("数据源", "用户真实会话", "在 <font name='Courier'>/providers</font> 连接自有 ChatGPT/Gemini 等账号；VPS 部署需住宅代理"),
            ("文档站", "官方", "docs.oneglanse.com（部署/代理指南）、落地页 oneglanse.com"),
            ("社区渠道", "GitHub", "Issues / PR、CONTRIBUTING.md、CODE_OF_CONDUCT.md、SECURITY.md"),
        ],
    },
    {
        "name": "Aperture",
        "repo": "anyin-ai/aperture",
        "cap": "开源“AI 可见性基础设施”，Profound/Peec AI 的免费自托管替代。监控 ChatGPT/Perplexity/Google AI Overviews 等是否在关键查询推荐你的品牌，对比竞品被引用原因，跨模型/语言/市场做结构化审计，随时间追踪。BYOK、自托管、MIT。当前 25★（早期项目）。",
        "rows": [
            ("源码仓库", "GitHub", "<font name='Courier'>git clone https://github.com/anyin-ai/aperture</font>"),
            ("部署", "Docker", "<font name='Courier'>docker-compose.yml</font> 一键编排；详见 DOCS.md / DEPLOY.md / README.md"),
            ("运行时存储", "内置", "本地 SQLite（无需外部 DB；MVP 期密钥明文存，仅限 localhost/私网或加反代鉴权）"),
            ("BYOK 提供商", "各厂商", "配 OpenAI（gpt-4o-mini）、Perplexity（sonar）Key；支持任意 OpenAI 兼容端点"),
            ("数据集", "用户定义", "审计查询、品牌/竞品列表、目标市场与语言由用户自定"),
            ("构建方资源", "Anyin", "关联 AEO 代理公司 anyin.ai（无独立论坛）"),
            ("社区渠道", "GitHub", "Issues / PR（CONTRIBUTING.md）；含 AGENTS.md/CLAUDE.md；当前 35 commits、25★"),
        ],
    },
    {
        "name": "GEO-AEO Tracker",
        "repo": "Bright Data · danishashko/geo-aeo-tracker",
        "cap": "Bright Data 官方开源的本地优先 AI 可见性仪表盘。Prompt Hub 并行跑 6 个模型（ChatGPT/Perplexity/Gemini/Grok/Google AI Mode/Copilot），生成 0–100 可见度评分、引用机会、SRO 优化分析、Drift 告警、竞品 Battlecards。数据存浏览器 IndexedDB，无外部数据库。",
        "rows": [
            ("源码仓库", "GitHub", "<font name='Courier'>git clone https://github.com/danishashko/geo-aeo-tracker.git</font>"),
            ("在线 Demo", "Bright Data", "demos.brightdata.com/geo-tracker（免 Key 试用）"),
            ("运行", "npm", "<font name='Courier'>npm install</font> → <font name='Courier'>.env</font> 填 BRIGHT_DATA_KEY + 6 个 dataset ID → <font name='Courier'>npm run dev</font>"),
            ("数据源（核心）", "Bright Data", "LLM Scrapers、SERP API、Web Unlocker（按量计费 ~$1.50/1K 记录，BYOK）"),
            ("增强依赖", "Google", "Gemini API（SRO 管道第 1 阶段 Grounding）"),
            ("数据集", "实时查询", "无静态数据集；回答经 <font name='Courier'>normalizeAnswer()</font> 统一格式后存 IndexedDB"),
            ("配套文章", "Bright Data 博客", "brightdata.com/blog/ai/ai-visibility-tracker（含架构与抓取细节）"),
            ("社区渠道", "GitHub", "仓库 Issues/PR；以 Bright Data 官方社区/文档为外围支持"),
        ],
    },
]

for i, s in enumerate(schemes, 1):
    story.append(P(f"{i}. {s['name']}", H2))
    story.append(P(s["repo"], CAP))
    story.append(P(s["cap"], BODY))
    data = [[hcell("资源类型"), hcell("可能来源"), hcell("获取路径描述")]]
    for a, b, c in s["rows"]:
        data.append([cell(a), cell(b), cell(c)])
    t = Table(data, colWidths=[24*mm, 24*mm, 110*mm], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#5b4ea8")),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#c9c4e0")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f4f2fb")]),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(Spacer(1, 4))
    story.append(t)
    story.append(Spacer(1, 8))

# ---- comparison table ----
story.append(PageBreak())
story.append(P("横向速览", H2))
story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#9184d9")))
story.append(Spacer(1, 6))
cmp_header = ["方案", "开源协议", "引擎覆盖", "诊断→执行闭环", "自托管", "标杆度"]
cmp_rows = [
    ("GEOLOOK（参照）", "MIT", "17 引擎（含 7 国内）", "✅ 工单+资产+验收+交付", "✅ 纯 Python", "最完整实现平台"),
    ("GeoBench", "未注明(Public)", "6 家(API/CLI/浏览器)", "❌ 仅 benchmark", "✅ Bun", "指标严谨、带 CI"),
    ("GEOVisibilityTool", "Apache-2.0", "国内 6 家 + 自定义", "❌ 测量+策略报告", "✅ Claude Skill", "国内覆盖强、零依赖"),
    ("OneGlanse", "MIT", "5 家(真实 UI)", "❌ 监控+评分", "✅ Docker", "星标最高、UI 真实捕获"),
    ("Aperture", "MIT", "ChatGPT/Perplexity(规划扩)", "❌ 监控+审计", "✅ Docker", "早期、轻量"),
    ("GEO-AEO Tracker", "未注明", "6 家(经 Bright Data)", "❌ 监控+评分", "✅ 浏览器本地", "企业数据源、需付费 Key"),
]
cdata = [[hcell(h) for h in cmp_header]]
for r in cmp_rows:
    cdata.append([cell(x) for x in r])
ct = Table(cdata, colWidths=[30*mm, 22*mm, 38*mm, 34*mm, 20*mm, 24*mm], repeatRows=1)
ct.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#5b4ea8")),
    ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#c9c4e0")),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f4f2fb")]),
    ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ("TOPPADDING", (0, 0), (-1, -1), 4),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
]))
story.append(ct)
story.append(Spacer(1, 10))

# ---- conclusion ----
story.append(P("结论建议", H2))
story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#9184d9")))
story.append(Spacer(1, 4))
for t in [
    "与 GEOLOOK 最可比的是 <b>GeoBench</b>（指标方法论最严谨）与 <b>OneGlanse</b>（真实 UI 捕获、社区最活跃）。",
    "若关注<b>国内市场</b>，则 <b>GEOVisibilityTool</b> 的国内引擎覆盖最直接互补。",
    "三者均为纯监测/分析层，只有 GEOLOOK 覆盖了“诊断 → 生成可部署资产 → 自动验收 → 客户交付”的完整实现闭环。",
]:
    story.append(P("• " + t, NOTE))

# ---- build ----
doc = SimpleDocTemplate(
    OUT, pagesize=A4,
    leftMargin=16*mm, rightMargin=16*mm, topMargin=16*mm, bottomMargin=16*mm,
    title="同类开源前沿方案对比（GEO / AI 可见性优化）",
    author="GEOLOOK",
)

def footer(canvas, d):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#9aa3b2"))
    canvas.drawString(16*mm, 10*mm, "GEOLOOK · 2026-08-21 · 同类开源前沿方案对比")
    canvas.drawRightString(A4[0]-16*mm, 10*mm, "第 %d 页" % d.page)
    canvas.restoreState()

doc.build(story, onFirstPage=footer, onLaterPages=footer)
print("PDF written:", OUT)
