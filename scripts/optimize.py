"""优化闭环（P3 / M17）：曝光效果综合分 + 优化建议 + 发布后闭环验证。

- exposure_score：把 analytics 的健康度 + 趋势稳定性收敛成一个 0–100 综合分，
  拆解成 可见性 / 权威性 / 覆盖度 / 一致性 四个子分。
- recommend：把未闭环工单、信源缺口、采样缺口转成可执行的优化建议。
- validate：发布内容后再采样，对比发布前后的曝光增量，验证优化是否真的有效。
"""

from __future__ import annotations

import geolib as G
import analytics as AN
import sourcemap as SM


def _pct(a, b) -> float:
    if not a:
        return 0.0
    return round((b - a) / a * 100, 1)


def exposure_score(slug: str) -> dict:
    a = AN.build(slug)
    health = a.get("health", {}) or {}
    trend = AN.trend(slug)
    qcount = a.get("question_count", 0) or 1

    mention = health.get("mention_rate") or 0.0
    visibility = round(min(100.0, mention * 100), 1)
    authority = round(min(100.0, (health.get("citations_total") or 0) / qcount * 50), 1)
    coverage = round((health.get("answered_rate") or 0) * 100, 1)

    consistency = 100.0
    if len(trend) >= 2:
        m0, m1 = trend[-2].get("mention", 0), trend[-1].get("mention", 0)
        if m0:
            consistency = round(max(0.0, 100 - abs(m1 - m0) / m0 * 100), 1)

    score = round(visibility * 0.4 + authority * 0.2 + coverage * 0.2 + consistency * 0.2, 1)
    return {
        "score": score,
        "components": {
            "visibility": visibility,
            "authority": authority,
            "coverage": coverage,
            "consistency": consistency,
        },
        "health": health,
        "date": trend[-1]["date"] if trend else None,
        "samples": a.get("total_samples", 0),
        "trend_points": len(trend),
    }


def recommend(slug: str) -> list[dict]:
    pdir = G.project_dir(slug)
    td = G.read_json(pdir / "tasks.json", {"tasks": []})
    recs = []
    for t in td.get("tasks", []):
        if t.get("status") == "done":
            continue
        recs.append({
            "id": t.get("id"),
            "title": t.get("title"),
            "priority": t.get("priority"),
            "market": t.get("market"),
            "owner": t.get("owner"),
            "acceptance": t.get("acceptance", ""),
            "why": "工单未闭环",
            "kind": "task",
        })
    # 信源缺口：自有站未被任何采样引用
    sm = SM.build(slug)
    if sm.get("site_host") and sm.get("first_party_count", 0) == 0 and sm.get("total_citations"):
        recs.append({
            "id": "src-own",
            "title": f"提升自有站 {sm['site_host']} 在 AI 答案里的引用占比",
            "priority": "P1",
            "why": "抽样信源中没有一条指向品牌自有站，GEO 资产未生效",
            "kind": "source",
        })
    # 采样缺口
    a = AN.build(slug)
    if a.get("question_count") and (a.get("health", {}).get("answered_rate") or 0) < 0.6:
        recs.append({
            "id": "samp-gap",
            "title": "扩大问题库覆盖并补足低覆盖平台采样",
            "priority": "P2",
            "why": f"已答覆盖 {round((a.get('health', {}).get('answered_rate') or 0) * 100)}%，仍有大量问题未进入答案",
            "kind": "sample",
        })
    return recs[:40]


def validate(slug: str) -> dict:
    trend = AN.trend(slug)
    if len(trend) < 2:
        return {"ok": False, "reason": "需要至少两次采样（发布内容后再跑一次监测）才能做闭环验证"}
    first, last = trend[0], trend[-1]
    return {
        "ok": True,
        "first_date": first.get("date"),
        "last_date": last.get("date"),
        "mention_delta_pct": _pct(first.get("mention", 0), last.get("mention", 0)),
        "cite_delta_pct": _pct(first.get("cite", 0), last.get("cite", 0)),
        "health_delta": round((last.get("health", 0) - first.get("health", 0)), 1),
        "samples_delta": last.get("samples", 0) - first.get("samples", 0),
    }
