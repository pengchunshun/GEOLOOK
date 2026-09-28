# -*- coding: utf-8 -*-
"""生成《星火之光 SparklightAIGEOLOOK 产品设计说明书》PDF 与 HTML 双格式。"""
import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable, ListFlowable, ListItem
)

BRAND = "星火之光 SparklightAIGEOLOOK"
DATE = "2026-08-22"
OUT_PDF = r"g:\AI_SPACE\CodeBuddy\geolook\docs\SparklightAIGEOLOOK_产品设计说明书.pdf"
OUT_HTML = r"g:\AI_SPACE\CodeBuddy\geolook\docs\SparklightAIGEOLOOK_产品设计说明书.html"

# =====================================================================
# 内容（结构化：用于 PDF 与 HTML 同一来源）
# =====================================================================
SECTIONS = []

def H(t): SECTIONS.append(("h", t))
def P(t): SECTIONS.append(("p", t))
def B(t): SECTIONS.append(("b", t))   # 要点 bullet
def T(rows, header): SECTIONS.append(("t", (header, rows)))  # 表格

# ---------- 封面摘要 ----------
P("本说明书面向产品、研发与交付团队，基于开源项目 GEOLOOK 的真实架构能力，"
  "定义「星火之光 SparklightAIGEOLOOK」的定制开发方案。GEOLOOK 是端到端星火之光生成式引擎优化（GEO）"
  "自托管平台：状态分析 → 诊断 → 策略 → 执行工单 → 实施 → 验收。星火之光在其之上，"
  "强化 AI 原生能力、品牌化交付与多租户协作，形成一套可对外商业化的 GEO 服务平台。")

# ---------- 1. 产品定位 ----------
H("1. 产品定位")
P("GEOLOOK 解决了「AI 从不提你、不知为何不提、建议落不了地、做了没验证、交付打包难」五大问题，"
  "其核心价值是<b>「GEO 的终点不是排名，是 AI 答案里那句话是不是按你的口径说的」</b>"
  "——最小单位是<b>可被抽取的事实块</b>而非页面。")
P("星火之光的定位升级为：<b>面向品牌方与 GEO 服务商的 AI 原生 GEO 增长平台</b>。"
  "在保留 GEOLOOK「监测→诊断→工单→资产→自动验收→交付」完整闭环与数据本地化、零编造纪律的基础上，"
  "叠加四层定制能力：① 多模型 AI 智能体（自动扩词/初稿/事实核验）；"
  "② 品牌化白皮书级交付物与多租户客户空间；③ 实时仪表盘与协作工作流；"
  "④ 国内/海外双市场策略模板与行业知识库。")
T(
  [
    ("维度", "GEOLOOK（基座）", "星火之光 SparklightAIGEOLOOK（定制）"),
    ("核心定位", "开源自托管 GEO 实现平台", "商业化 AI 原生 GEO 增长平台"),
    ("用户", "个人/代理商/咨询师", "品牌方 + 服务商 + 内部增长团队"),
    ("AI 能力", "单 LLM 初稿/推导", "多智能体编排 + 行业知识 + 自动事实核验"),
    ("交付", "单项目三份 HTML/CSV", "品牌化白皮书 + 多租户空间 + 月报订阅"),
    ("协作", "单机无账号", "团队账号/角色/工单指派/评论"),
    ("品牌", "无（白牌）", "星火之光全链路品牌视觉"),
  ],
  ("对比维度", "GEOLOOK 基座", "星火之光定制")
)

# ---------- 2. 目标用户 ----------
H("2. 目标用户与场景")
B("<b>品牌增长团队</b>：自有官网/小程序，需持续提升在 ChatGPT、豆包、DeepSeek 等 17 个引擎中的提及与引用。")
B("<b>GEO/SEO 服务商</b>：同时服务多个客户，需要多租户空间、批量复跑与可白标交付包。")
B("<b>内容/公关团队</b>：基于「可抽取事实块」方法论，规模化产出被 AI 引用友好的内容资产。")
B("<b>出海企业</b>：国内 + 海外双市场的并行 GEO 战场，需要分市场指标与渠道地图。")
T(
  [
    ("角色", "核心诉求", "星火之光对应模块"),
    ("CMO/增长负责人", "AI 可见性是否提升、ROI 可量化", "实时仪表盘 + 月报订阅 + 趋势对比"),
    ("GEO 运营", "批量客户、工单流转、不漏项", "多租户空间 + 工单指派 + 协作评论"),
    ("内容编辑", "写什么能被引用、初稿不出错", "内容工作台 + AI 初稿 + 编造风险 lint"),
    ("技术/站长", "站点是否被 AI 抓取器正确读取", "四层体检 + WAF/CDN 差异探测 + 资产部署"),
  ],
  ("角色", "核心诉求", "对应模块")
)

# ---------- 3. 功能架构 ----------
H("3. 功能架构（基于 GEOLOOK 管线扩展）")
P("沿用 GEOLOOK 的九步管线（建项目→抓取→体检→推导底座→采样→工单→资产→报告→验收→交付），"
  "在每一层叠加星火之光的定制模块，形成六层架构：")
B("<b>L1 接入层</b>：3 步品牌接入向导（URL + 市场）、无站点模式（电商/线下品牌）、多租户空间切换。")
B("<b>L2 数据底座层</b>：复用 crawl/audit/bootstrap；新增<b>行业知识库</b>与<b>品牌事实库多版本管理</b>。")
B("<b>L3 智能采样层</b>：复用 17 引擎采样 + 样本库人工校正；新增<b>多智能体采样编排</b>（自动选题/复核/降噪）。")
B("<b>L4 诊断策略层</b>：复用四层依赖链体检、差距诊断、19 渠道地图；新增<b>AI 诊疗建议生成</b>与<b>竞品情报雷达</b>。")
B("<b>L5 执行交付层</b>：复用工单/资产/发布/验收；新增<b>协作工单流</b>、<b>品牌化白皮书</b>、<b>月报订阅</b>。")
B("<b>L6 展示层</b>：复用单文件暗色四段主线 UI；升级为<b>星火之光品牌视觉系统</b> + 实时仪表盘 + 客户只读视图。")
T(
  [
    ("GEOLOOK 现有（保留）", "星火之光新增（定制）"),
    ("现状/状态总览 · 引擎表现 · 竞品对比 · 问题库 · 样本库", "实时 AI 可见性仪表盘 · 多租户客户空间"),
    ("诊断：四层体检 · 差距 · 19 渠道地图 · 品牌事实库", "AI 诊疗建议 · 竞品情报雷达 · 行业知识库"),
    ("提升：行动计划 · 内容工作台 · 资产部署 · 发布", "协作工单流 · 工单指派/评论 · 一键品牌化白皮书"),
    ("成效：验收 · 报告与交付", "月报订阅 · 客户只读视图 · 趋势对比"),
  ],
  ("GEOLOOK 基座能力（保留）", "星火之光定制模块")
)

# ---------- 4. 核心业务流程 ----------
H("4. 核心业务流程")
P("主流程在 GEOLOOK 的九步管线上扩展出「AI 智能体编排」与「品牌化交付」两个新环节：")
B("<b>接入</b>：3 步向导 → 自动推断品牌名/市场 → 创建多租户客户空间。")
B("<b>底座构建</b>：抓取 + 六维体检 + 自动推导品牌事实/竞品/问题库（复用 bootstrap，新增行业知识库增强）。")
B("<b>智能采样</b>：多智能体自动选题 → 17 引擎采样（API + 浏览器插件）→ 样本库人工校正 → 自动降噪。")
B("<b>AI 诊疗</b>（新增）：基于 method.md 实测口径，由诊疗智能体生成诊断结论、修复顺序与策略建议。")
B("<b>执行</b>：协作工单流（指派/评论/风险分级）→ 内容工作台（AI 初稿 + 编造风险 lint）→ 资产部署 → 发布。")
B("<b>验收交付</b>：自动验收（回归重开）→ <b>品牌化白皮书 + 月报订阅</b>（新增）→ 客户只读视图。")
T(
  [
    ("环节", "GEOLOOK 现状", "星火之光优化点"),
    ("采样", "单轮、人工复检为主", "多智能体编排、自动选题/复核/降噪"),
    ("诊断", "规则 + 人工判读", "AI 诊疗建议生成、竞品情报雷达"),
    ("工单", "单人、本地 JSON", "协作工单流、指派/评论/角色"),
    ("交付", "三份 HTML/CSV", "品牌化白皮书、月报订阅、客户视图"),
  ],
  ("环节", "GEOLOOK 现状", "星火之光优化点")
)

# ---------- 5. 功能详细说明 ----------
H("5. 功能详细说明（新增与优化模块）")
H("5.1 多智能体 AI 引擎（新增·核心）")
P("在 GEOLOOK 仅用单一 LLM 出初稿的基础上，构建可编排的智能体集群，统一接入已配置的引擎 Key：")
B("扩词智能体：基于百度下拉/Google 补全 + 行业知识库，自动产出高意图候选题并标注意图分组。")
B("初稿智能体：基于 content-patterns 模板生成可引用内容大纲与初稿，强制过编造风险 lint。")
B("事实核验智能体：对照品牌事实库（A–E 证据等级）自动标记初稿中无来源/存疑数字，阻断编造。")
B("诊疗智能体：将体检四层链 + 样本库指标，生成可读诊断结论与修复优先级（追到 method.md 数字出处）。")
H("5.2 行业知识库（新增）")
B("按行业（SaaS/电商/医疗/教育…）预置信源权重、问题模板、竞品维度，使新项目 bootstrap 更准更快。")
H("5.3 多租户客户空间（新增）")
B("团队账号 + 角色（管理员/运营/编辑/只读客户）；每客户独立 work/<slug>/ 空间，互不越权。")
B("客户只读视图：可分享链接（带 token）查看仪表盘与月报，无编辑权限——对应 GEOLOOK 的公网 token 机制。")
H("5.4 协作工单流（优化）")
B("工单由本地 tasks.json 升级为带<b>指派/评论/状态流/风险分级</b>的协作对象；回归自动重开保留。")
H("5.5 品牌化白皮书与月报（优化·交付）")
B("三份基础交付物升级为统一的<b>星火之光白皮书</b>视觉（封面/品牌色/结论先行/可引用证据链）。")
B("月报订阅：定时生成并分发（邮件 + 客户只读链接），含 delta、信源 Top、大盘对照。")
H("5.6 实时仪表盘与竞品雷达（优化·展示）")
B("现状总览升级为实时卡片（健康分/提及率/引用份额/阵地/任务/内容），新增<b>竞品情报雷达</b>图。")
H("5.7 品牌视觉系统（新增·全链路）")
B("统一「星火之光」暗色科技风视觉：深空蓝紫底 + 星火橙金强调色 + 火花/光晕图标语言，覆盖 UI、白皮书、月报。")

# ---------- 6. 技术可行性 ----------
H("6. 技术可行性")
P("星火之光以 GEOLOOK 为基座，复用其已验证的技术栈与纪律，新增模块均在同栈内可落地：")
T(
  [
    ("能力", "GEOLOOK 现状", "星火之光实现路径", "可行性"),
    ("运行环境", "Python 3.9+ / 标准库 http.server / 零外部依赖（除 requests/bs4/lxml）", "沿用；新增多租户加一层账号中间件", "高"),
    ("AI 接入", "单 LLM（已配 DeepSeek/GLM 等 Key）", "多智能体统一调用同一批 Key，加编排层", "高"),
    ("数据本地化", "work/ 下纯文件，git 即备份", "沿用，加多租户目录隔离", "高"),
    ("不编造纪律", "事实仅来自站点/材料，标「待确认」", "事实核验智能体强化该纪律", "高"),
    ("公网访问", "GEOLOOK_TOKEN + 0.0.0.0 绑定 + 反代", "复用做客户只读视图", "高"),
    ("前端", "单文件 ui.html 零依赖", "同栈升级品牌视觉（无框架）", "高"),
    ("采样", "17 引擎 + 浏览器插件", "智能体编排复用现有采样层", "高"),
  ],
  ("能力", "GEOLOOK 现状", "星火之光实现路径", "可行性")
)
P("<b>风险与边界（继承 GEOLOOK 设计原则）</b>：不承诺任何平台必引某页；不绕过平台限制批量采集/模拟登录；"
  "AI 初稿与事实必须人工复核；采样频率克制、遵守 ToS。这些边界在星火之光的智能体层同样强制。")

# ---------- 7. 实施路径与里程碑 ----------
H("7. 实施路径与里程碑")
T(
  [
    ("阶段", "周期", "目标", "交付物"),
    ("M1 品牌化基座", "第 1–3 周", "UI 品牌视觉系统 + 说明书/白皮书模板", "星火之光视觉规范、白皮书模板"),
    ("M2 多智能体引擎", "第 3–6 周", "扩词/初稿/事实核验/诊疗四个智能体", "智能体编排模块、lint 集成"),
    ("M3 协作与多租户", "第 6–9 周", "账号角色、工单协作流、客户空间", "多租户后端、协作工单 UI"),
    ("M4 交付与展示", "第 9–11 周", "月报订阅、实时仪表盘、竞品雷达", "月报引擎、客户只读视图"),
    ("M5 行业包与上线", "第 11–13 周", "行业知识库 + 公网部署 + 灰度", "行业包、部署文档、上线"),
  ],
  ("阶段", "周期", "目标", "交付物")
)
P("每阶段均以「可运行、可演示、可回退」为验收标准；M3 之前的智能体与品牌模块均可在单机 GEOLOOK 上先行验证，"
  "降低集成风险。")

# ---------- 附录 ----------
H("附录 A · 与 UI 设计图对应关系")
T(
  [
    ("说明书模块", "UI 设计图页面"),
    ("5.6 实时仪表盘与竞品雷达", "页面 ① 星火总览仪表盘"),
    ("5.1 多智能体 AI 引擎", "页面 ② AI 智能体工作台"),
    ("5.2/5.4 行业知识库 + 协作工单", "页面 ③ 工单协作与行业包"),
    ("5.5 品牌化白皮书与月报", "页面 ④ 品牌化交付白皮书"),
    ("7 里程碑", "页面 ⑤ 实施路线图"),
  ],
  ("说明书模块", "UI 设计图页面")
)

# =====================================================================
# 渲染 HTML
# =====================================================================
def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))

html_parts = []
html_parts.append(f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>星火之光 SparklightAIGEOLOOK · 产品设计说明书</title>
<style>
  :root{{--bg:#0d1020;--panel:#161a2e;--panel2:#1d2238;--border:#2c3252;
    --text:#e8ebf5;--muted:#9aa3c4;--accent:#7c5cff;--spark:#ff9d3c;--ok:#4ade80;}}
  *{{box-sizing:border-box;}}
  body{{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;
    background:var(--bg);color:var(--text);line-height:1.7;}}
  .hero{{padding:48px 24px 36px;text-align:center;
    background:radial-gradient(1200px 400px at 50% -10%,rgba(124,92,255,.28),transparent),
               radial-gradient(800px 300px at 80% 20%,rgba(255,157,60,.18),transparent),
               linear-gradient(180deg,#10142b,#0d1020);border-bottom:1px solid var(--border);}}
  .hero .spark{{font-size:13px;letter-spacing:.3em;color:var(--spark);text-transform:uppercase;}}
  .hero h1{{margin:8px 0 6px;font-size:30px;background:linear-gradient(90deg,#fff,#bcaaff);
    -webkit-background-clip:text;background-clip:text;color:transparent;}}
  .hero .sub{{color:var(--muted);font-size:13px;}}
  .wrap{{max-width:1000px;margin:0 auto;padding:28px 18px 60px;}}
  .sec{{background:var(--panel);border:1px solid var(--border);border-radius:14px;
    padding:22px 24px;margin-bottom:20px;box-shadow:0 6px 24px rgba(0,0,0,.3);}}
  .sec h2{{margin:0 0 10px;font-size:19px;color:#fff;border-left:4px solid var(--spark);padding-left:12px;}}
  .sec h3{{font-size:15px;color:#cdbcff;margin:16px 0 6px;}}
  .sec p{{font-size:14px;margin:8px 0;color:#d7dbeb;text-align:justify;}}
  .sec ul{{margin:8px 0;padding-left:20px;}}
  .sec li{{font-size:13.5px;margin:5px 0;color:#d7dbeb;}}
  table{{width:100%;border-collapse:collapse;margin:10px 0;font-size:13px;}}
  th,td{{border:1px solid var(--border);padding:8px 10px;text-align:left;vertical-align:top;}}
  th{{background:var(--panel2);color:var(--accent);font-weight:600;}}
  tr:nth-child(even) td{{background:rgba(124,92,255,.05);}}
  code{{background:#0a0d1c;padding:1px 6px;border-radius:5px;color:#c7d2fe;font-size:12px;}}
  .tag{{display:inline-block;background:rgba(255,157,60,.15);color:var(--spark);border:1px solid rgba(255,157,60,.4);
    border-radius:6px;padding:1px 8px;font-size:11px;margin-left:6px;}}
  footer{{text-align:center;color:var(--muted);font-size:12px;padding:24px;border-top:1px solid var(--border);}}
</style></head><body>
<div class="hero">
  <div class="spark">★ Sparklight · AI GEO Platform</div>
  <h1>星火之光 SparklightAIGEOLOOK</h1>
  <div class="sub">产品设计说明书 · 基于 GEOLOOK 的开源架构定制开发 · {DATE}</div>
</div>
<div class="wrap">
""")

for kind, val in SECTIONS:
    if kind == "h":
        html_parts.append(f'<div class="sec"><h2>{esc(val)}</h2>')
    elif kind == "p":
        html_parts.append(f'<p>{val}</p>')
    elif kind == "b":
        html_parts.append(f'<ul><li>{val}</li></ul>' if False else f'<li style="list-style:none;margin:6px 0;"><span class="tag">●</span> {val}</li>')
    elif kind == "t":
        header, rows = val
        th = "".join(f"<th>{esc(c)}</th>" for c in header)
        trs = ""
        for r in rows:
            trs += "<tr>" + "".join(f"<td>{esc(c)}</td>" for c in r) + "</tr>"
        html_parts.append(f'<table><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table>')

# close any open section
html_parts.append("""
</div>
<footer>星火之光 SparklightAIGEOLOOK · 产品设计说明书 · 本文档与 UI 设计图一一对应 · """ + DATE + """</footer>
</body></html>""")

html_content = "\n".join(html_parts)
with open(OUT_HTML, "w", encoding="utf-8") as f:
    f.write(html_content)
print("HTML written:", OUT_HTML)

# =====================================================================
# 渲染 PDF
# =====================================================================
styles = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=styles["Title"], fontSize=19, leading=24,
                    textColor=colors.HexColor("#2b2348"), alignment=TA_CENTER, spaceAfter=4)
SUB = ParagraphStyle("SUB", parent=styles["Normal"], fontSize=10.5, leading=14,
                     textColor=colors.HexColor("#5b6478"), alignment=TA_CENTER)
H2 = ParagraphStyle("H2", parent=styles["Heading2"], fontSize=14, leading=18,
                    textColor=colors.HexColor("#3a2f63"), spaceBefore=8, spaceAfter=2)
H3 = ParagraphStyle("H3", parent=styles["Heading3"], fontSize=12, leading=15,
                    textColor=colors.HexColor("#5b4ea8"), spaceBefore=4, spaceAfter=2)
BODY = ParagraphStyle("BODY", parent=styles["Normal"], fontSize=9.5, leading=13.5,
                      textColor=colors.HexColor("#1f2430"), alignment=TA_JUSTIFY,
                      spaceBefore=3, spaceAfter=3)
TH = ParagraphStyle("TH", parent=styles["Normal"], fontSize=8.5, leading=11,
                    textColor=colors.white, fontName="Helvetica-Bold")
TD = ParagraphStyle("TD", parent=styles["Normal"], fontSize=8, leading=10.5,
                    textColor=colors.HexColor("#23272f"))

def PH(t, s=BODY): return Paragraph(t, s)
def cell(t): return Paragraph(t, TD)
def hcell(t): return Paragraph(t, TH)

story = []
story.append(PH("星火之光 SparklightAIGEOLOOK", H1))
story.append(PH("产品设计说明书 · 基于 GEOLOOK 开源架构定制开发", SUB))
story.append(PH(f"生成日期：{DATE} ｜ 版本 v1.0", SUB))
story.append(Spacer(1, 8))
story.append(HRFlowable(width="100%", thickness=1.2, color=colors.HexColor("#9184d9")))
story.append(Spacer(1, 8))

import re as _re
for kind, val in SECTIONS:
    if kind == "h":
        # 5.x 子节标题使用 H3，其余主节使用 H2
        if _re.match(r"^\d+\.\d+\s", val):
            story.append(PH(val, H3))
        else:
            story.append(PH(val, H2))
    elif kind == "p":
        story.append(PH(val))
    elif kind == "b":
        story.append(PH("• " + val, BODY))
    elif kind == "t":
        header, rows = val
        data = [[hcell(c) for c in header]]
        for r in rows:
            data.append([cell(c) for c in r])
        ncol = len(header)
        cw = [ (165*mm)/ncol ] * ncol
        t = Table(data, colWidths=cw, repeatRows=1)
        t.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#5b4ea8")),
            ("GRID", (0,0), (-1,-1), 0.4, colors.HexColor("#c9c4e0")),
            ("VALIGN", (0,0), (-1,-1), "TOP"),
            ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#f4f2fb")]),
            ("LEFTPADDING", (0,0), (-1,-1), 4),
            ("RIGHTPADDING", (0,0), (-1,-1), 4),
            ("TOPPADDING", (0,0), (-1,-1), 3),
            ("BOTTOMPADDING", (0,0), (-1,-1), 3),
        ]))
        story.append(Spacer(1,3))
        story.append(t)
        story.append(Spacer(1,4))

# H3 handling: there are H3 inside section 5; re-inject by special marker
# (simplest: we already encoded 5.x as H in SECTIONS; render them as H3)
# Rebuild story for H3: easier to post-process — replace H2 entries starting with digit "5." sub-level.

def footer(canvas, d):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#9aa3b2"))
    canvas.drawString(16*mm, 10*mm, "星火之光 SparklightAIGEOLOOK · 产品设计说明书 v1.0")
    canvas.drawRightString(A4[0]-16*mm, 10*mm, "第 %d 页" % d.page)
    canvas.restoreState()

doc = SimpleDocTemplate(OUT_PDF, pagesize=A4,
    leftMargin=16*mm, rightMargin=16*mm, topMargin=16*mm, bottomMargin=16*mm,
    title="星火之光 SparklightAIGEOLOOK 产品设计说明书", author="Sparklight")
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print("PDF written:", OUT_PDF)
