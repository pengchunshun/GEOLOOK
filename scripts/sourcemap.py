"""信源地图（M16 / P2）：聚合各平台采样答案里的引用来源，按域名归类。

采样元数据（`sample.list_samples`）已把每条答案的引用域名、是否提到品牌、提到哪些竞品
抽取好，这里直接复用，避免二次读取全文：
- cited_domains：本答案引用的域名列表
- brand_mentioned / own_domain_cited：是否提到品牌 / 是否引用了自有站
- competitors：本答案提到的竞品名列表

输出：
- top：引用最多的域名（含 kind=first_party/third_party、覆盖到的平台）
- first_party / third_party：自有站 vs 第三方信源
- groups：按一级域名归并后的信源气泡（用于信源地图可视化）
"""

from __future__ import annotations

import re
from collections import defaultdict

import geolib as G
import sample as S

_DOMAIN_RE = re.compile(r"https?://([^/]+)/?")


def _host(url: str) -> str | None:
    if not url:
        return None
    m = _DOMAIN_RE.match(url) if "://" in (url or "") else None
    if m:
        h = m.group(1).lower()
        return h[4:] if h.startswith("www.") else h
    h = (url or "").lower().strip()
    return h[4:] if h.startswith("www.") else h


def _site_host(cfg: dict) -> str:
    return _host((cfg.get("brand", {}) or {}).get("site") or "") or ""


def build(slug: str, date: str = "") -> dict:
    cfg = G.load_config(slug)
    site_host = _site_host(cfg)
    recs = S.list_samples(slug, date=date, limit=2000) or {}
    rows = recs.get("rows", []) if isinstance(recs, dict) else []

    by_domain: dict[str, dict] = defaultdict(
        lambda: {"count": 0, "platforms": set(), "kinds": set()})
    for r in rows:
        for host in (r.get("cited_domains") or []):
            if not host:
                continue
            d = by_domain[host]
            d["count"] += 1
            d["platforms"].add(r.get("platform"))
            d["kinds"].add("first_party" if (site_host and host == site_host) else "third_party")

    out = []
    for host, d in by_domain.items():
        out.append({
            "domain": host,
            "count": d["count"],
            "platforms": sorted(d["platforms"]),
            "kind": "first_party" if "first_party" in d["kinds"] else "third_party",
            "kind_full": sorted(d["kinds"]),
        })
    out.sort(key=lambda x: (-x["count"], x["domain"]))

    first = [x for x in out if x["kind"] == "first_party"]
    third = [x for x in out if x["kind"] == "third_party"]

    groups: dict[str, dict] = defaultdict(lambda: {"count": 0, "domains": set(), "kind": set()})
    for x in out:
        parts = x["domain"].split(".")
        top = ".".join(parts[-2:]) if len(parts) >= 2 else x["domain"]
        g = groups[top]
        g["count"] += x["count"]
        g["domains"].add(x["domain"])
        g["kind"].add(x["kind"])
    group_list = [{
        "group": k,
        "count": v["count"],
        "domains": sorted(v["domains"]),
        "kind": "first_party" if "first_party" in v["kind"] else "third_party",
    } for k, v in groups.items()]
    group_list.sort(key=lambda x: (-x["count"], x["group"]))

    return {
        "site_host": site_host,
        "total_citations": sum(x["count"] for x in out),
        "domain_count": len(out),
        "first_party_count": len(first),
        "third_party_count": len(third),
        "top": out[:40],
        "first_party": first[:20],
        "third_party": third[:40],
        "groups": group_list[:40],
    }


def compete(slug: str) -> dict:
    """竞品并排（P2/M16）：各平台上「你 vs 各竞品」的提及 presence。

    用采样元数据里的 brand_mentioned（你）与 competitors（竞品命中列表）做 presence 判定，
    与采样指标同口径，无需再读全文。
    """
    cfg = G.load_config(slug)
    me = (cfg.get("brand", {}) or {}).get("name", "")
    rivals = [c.get("name", "") for c in (cfg.get("competitors") or []) if c.get("name")]
    recs = S.list_samples(slug, limit=3000) or {}
    rows = recs.get("rows", []) if isinstance(recs, dict) else []
    if not rows:
        return {"me": me, "rivals": rivals, "platforms": []}

    plats: dict[str, dict] = {}
    for r in rows:
        code = r.get("platform")
        row = plats.setdefault(code, {"platform": code, "me": 0, "total": 0,
                                      "rivals": {rv: 0 for rv in rivals}})
        row["total"] += 1
        if r.get("brand_mentioned"):
            row["me"] += 1
        comp_list = r.get("competitors") or []
        for rv in rivals:
            if rv and rv in comp_list:
                row["rivals"][rv] += 1

    out_rows = []
    for code, row in plats.items():
        t = max(1, row["total"])
        out_rows.append({
            "platform": code,
            "total": row["total"],
            "me_rate": round(row["me"] / t, 3),
            "rivals": {rv: round(c / t, 3) for rv, c in row["rivals"].items()},
        })
    out_rows.sort(key=lambda x: x["platform"])
    return {"me": me, "rivals": rivals, "platforms": out_rows}
