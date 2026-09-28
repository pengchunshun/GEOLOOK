"""天级自动监测：周期采样调度辅助 + 波动告警 + 可选 Webhook 推送。

- read_metrics / compute_deltas / check_alerts：把当日期与上一期指标对比，
  波动超过阈值（默认 ±20%）即生成告警，写入 work/<slug>/alerts.json，
  并可选推送到 monitor.webhook。
- freq_to_days / next_run_for：把 geo.json.monitor.freq（daily/weekly）映射成间隔。
- ensure_monitor：给新建项目补上默认监测配置，保证可被调度器接管。
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from datetime import date, timedelta

import geolib as G

ALERT_FILE = "alerts.json"
FREQ_DAYS = {"daily": 1, "weekly": 7, "biweekly": 14, "monthly": 30}

# 需要监控波动的指标：键名 -> 中文标签
METRIC_LABELS = {
    "mention_rate": "提及率",
    "avg_rank": "平均排名",
    "top3_rate": "Top3 率",
    "citations": "引用数",
    "answer_count": "回答数",
}


def freq_to_days(freq: str) -> int:
    return FREQ_DAYS.get((freq or "daily"), 1)


def default_monitor() -> dict:
    return {
        "freq": "daily",
        "enabled": True,
        "every_days": 1,
        "next_run": (date.today() + timedelta(days=1)).isoformat(),
        "alert_threshold": 0.2,
        "webhook": "",
        "last_run": "",
    }


def ensure_monitor(slug: str) -> dict:
    """项目 geo.json 缺 monitor 时补默认；已有则补齐缺省字段。"""
    cfg = G.load_config(slug)
    mon = cfg.get("monitor") or {}
    base = default_monitor()
    base.update({k: v for k, v in mon.items() if v not in (None, "")})
    cfg["monitor"] = base
    if "workspace" not in cfg:
        cfg["workspace"] = default_workspace()
    G.save_config(slug, cfg)
    return cfg["monitor"]


def default_workspace() -> dict:
    try:
        import os
        owner = os.environ.get("USER") or os.environ.get("USERNAME") or "我"
    except Exception:  # noqa: BLE001
        owner = "我"
    return {"team": "默认团队", "dept": "默认部门", "owner": owner, "members": []}


def read_metrics(slug: str) -> list[dict]:
    pdir = G.project_dir(slug)
    mdir = pdir / "metrics"
    out = []
    if not mdir.exists():
        return out
    for f in sorted(mdir.glob("2*.json"), key=lambda x: x.stem):
        d = G.read_json(f, None)
        if d and "platforms" in d:
            out.append(d)
    return out


def _mk(date_: str, scope: str, metric: str, before, after, delta: float) -> dict:
    direction = "上升" if delta > 0 else "下降"
    severity = "高" if abs(delta) >= 0.5 else ("中" if abs(delta) >= 0.35 else "低")
    label = METRIC_LABELS.get(metric, metric)
    scope_label = "全局" if scope == "totals" else scope
    return {
        "id": f"{date_}-{scope}-{metric}",
        "date": date_,
        "scope": scope,
        "scope_label": scope_label,
        "metric": metric,
        "metric_label": label,
        "before": round(before, 4) if isinstance(before, float) else before,
        "after": round(after, 4) if isinstance(after, float) else after,
        "delta": round(delta, 4),
        "direction": direction,
        "severity": severity,
        "type": "波动",
        "msg": f"{scope_label} 的{label} {direction} {abs(delta) * 100:.0f}%（{before}→{after}）",
    }


def compute_deltas(prev: dict, cur: dict, threshold: float = 0.2) -> list[dict]:
    alerts = []
    metrics = list(METRIC_LABELS.keys())
    pt, ct = prev.get("totals", {}), cur.get("totals", {})
    for m in metrics:
        a, b = pt.get(m), ct.get(m)
        if isinstance(a, (int, float)) and isinstance(b, (int, float)) and a not in (0, None):
            delta = (b - a) / a
            if abs(delta) >= threshold:
                alerts.append(_mk(cur["date"], "totals", m, a, b, delta))
    pp, cp = prev.get("platforms", {}), cur.get("platforms", {})
    for code, cval in cp.items():
        pval = pp.get(code)
        if not pval:
            continue
        for m in metrics:
            a, b = pval.get(m), cval.get(m)
            if isinstance(a, (int, float)) and isinstance(b, (int, float)) and a not in (0, None):
                delta = (b - a) / a
                if abs(delta) >= threshold:
                    alerts.append(_mk(cur["date"], code, m, a, b, delta))
    return alerts


def check_alerts(slug: str, threshold: float | None = None) -> list[dict]:
    """对比最近两期 metrics，超阈波动生成告警并落盘 + Webhook。返回本期新告警。"""
    pdir = G.project_dir(slug)
    cfg = G.load_config(slug)
    mon = cfg.get("monitor") or {}
    if threshold is None:
        threshold = mon.get("alert_threshold", 0.2)
    met = read_metrics(slug)
    if len(met) < 2:
        return []
    prev, cur = met[-2], met[-1]
    new = [a for a in compute_deltas(prev, cur, threshold) if abs(a["delta"]) >= threshold]
    if not new:
        return []
    af = pdir / ALERT_FILE
    history = G.read_json(af, []) or []
    history.extend(new)
    # 去重（同一 date+scope+metric 只留一条），保留最近 300
    seen, dedup = set(), []
    for a in reversed(history):
        if a.get("id") in seen:
            continue
        seen.add(a.get("id"))
        dedup.append(a)
    dedup = list(reversed(dedup))[-300:]
    G.write_json(af, dedup)

    wh = (mon.get("webhook") or "").strip()
    if wh:
        try:
            _push_webhook(wh, {"slug": slug, "project": cfg.get("brand", {}).get("name", slug),
                               "alerts": new})
        except Exception:  # noqa: BLE001  告警推送失败绝不阻断主流程
            pass
    return new


def read_alerts(slug: str, limit: int = 30) -> list[dict]:
    pdir = G.project_dir(slug)
    return (G.read_json(pdir / ALERT_FILE, []) or [])[-limit:]


def _push_webhook(url: str, payload: dict) -> None:
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url, data=data, headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req, timeout=10)  # noqa: S310  用户自配的 webhook，风险自负
