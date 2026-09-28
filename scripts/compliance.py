"""合规审计（P4 / M19）：中立、可信、不编造、不泄露。

逐项检查：
1. 引用真实性：答案提到品牌但引用未指向自有站 → 需人工核实（不臆造来源）。
2. 披露 presence：成稿/资产是否带有 AI 生成或赞助披露声明。
3. PII 扫描：草稿与事实文件里是否泄露手机号/邮箱/身份证等个人敏感信息。
4. 监测 Webhook 配置（仅记录前缀，不回显完整地址避免泄露）。

结果写入 work/<slug>/compliance.json，供「合规审计」视图与协作看板调用。
采样侧检查复用 sample.list_samples 的元数据（brand_mentioned / own_domain_cited）。
"""

from __future__ import annotations

import re

import geolib as G
import sample as S

PII_PATTERNS = {
    "手机号": re.compile(r"(?<!\d)(1[3-9]\d{9})(?!\d)"),
    "邮箱": re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
    "身份证": re.compile(r"(?<!\d)(\d{17}[\dXx])(?!\d)"),
}
DISCLOSURE_PAT = re.compile(r"(AI\s*生成|由\s*AI|人工智能生成|赞助|商务合作|推广|本内容由)")


def audit(slug: str) -> dict:
    pdir = G.project_dir(slug)
    cfg = G.load_config(slug)
    brand = (cfg.get("brand", {}) or {}).get("name", "")
    checks = []

    # 1) 引用真实性（复用采样元数据）
    recs = S.list_samples(slug, limit=800) or {}
    rows = recs.get("rows", []) if isinstance(recs, dict) else []
    total = len(rows)
    mention_no_own = 0
    for r in rows:
        if r.get("brand_mentioned") and not r.get("own_domain_cited") and (r.get("citations") or 0) > 0:
            mention_no_own += 1
    checks.append({
        "name": "引用真实指向品牌站",
        "status": "warn" if mention_no_own else "pass",
        "detail": f"抽样 {total} 条答案，其中 {mention_no_own} 条提到品牌但引用未指向自有站"
                  + ("（需人工核实来源，不得臆造）" if mention_no_own else "（引用链路可追溯）"),
    })

    # 2) 披露 presence（扫描成稿）
    disclosure_hits = 0
    scanned = 0
    cdir = pdir / "content"
    if cdir.exists():
        for f in cdir.glob("*.md"):
            scanned += 1
            if DISCLOSURE_PAT.search(f.read_text("utf-8", "replace")):
                disclosure_hits += 1
    checks.append({
        "name": "AI/赞助披露",
        "status": "pass" if (scanned and disclosure_hits) else ("warn" if scanned else "info"),
        "detail": f"扫描 {scanned} 篇成稿，{disclosure_hits} 篇含披露声明"
        + ("" if disclosure_hits else "（建议发布前补一句 AI 生成/赞助说明）"),
    })

    # 3) PII 扫描
    pii_found = []
    targets = []
    if cdir.exists():
        targets += list(cdir.glob("*.md"))
    adir = pdir / "assets" / "drafts"
    if adir.exists():
        targets += list(adir.glob("*.md"))
    for f in targets:
        txt = f.read_text("utf-8", "replace")
        for label, pat in PII_PATTERNS.items():
            if pat.search(txt):
                pii_found.append(f"{f.name}:{label}")
    checks.append({
        "name": "个人敏感信息（PII）",
        "status": "fail" if pii_found else "pass",
        "detail": ("发现疑似泄露：" + "、".join(pii_found[:8])
                   + ("…" if len(pii_found) > 8 else "")) if pii_found
        else "草稿/成稿/事实文件未检出手机号、邮箱、身份证",
    })

    # 4) 监测 Webhook 配置（不回显完整地址）
    mon = cfg.get("monitor") or {}
    wh = (mon.get("webhook") or "").strip()
    checks.append({
        "name": "监测 Webhook 配置",
        "status": "pass" if wh else "info",
        "detail": (f"已配置（{wh[:18]}…）" if wh else "未配置：波动告警不会外推，可在设置里填"),
    })

    score = round(sum(1 for c in checks if c["status"] == "pass") / max(1, len(checks)) * 100)
    result = {"checked_at": G.today(), "score": score, "checks": checks}
    G.write_json(pdir / "compliance.json", result)
    return result
