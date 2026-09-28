"""Encrypted persistence for sensitive provider keys (AES via Fernet).

Secret env vars (``*_API_KEY`` / ``*_SECRET_KEY``) are encrypted into
``secrets.enc`` and removed from plaintext ``.env``. On startup they are
decrypted into ``os.environ`` so the rest of the app (sampler, connectors,
``GET /api/keys``) reads them unchanged. A single master key lives in
``.env`` as ``GEOLOOK_SECRETS_KEY`` and is auto-generated on first use.

Design goals aligned with 产品设计说明书 §9.4:
  - 加密 Key 持久化存储，重启后可读并显示
  - 多平台独立配置（每个平台一个 env 名，互不影响）
  - 保存/读取一致（同一 env 名做加解密 key）
  - 读取失败/为空时不影响其它平台（调用方按 key 捕获异常）
"""
import json
import os
import re
from pathlib import Path

from cryptography.fernet import Fernet

ROOT = Path(__file__).resolve().parent.parent
SECRETS_FILE = ROOT / "secrets.enc"
MASTER_ENV = "GEOLOOK_SECRETS_KEY"
ENV_FILE = ROOT / ".env"

# 敏感变量的后缀；主密钥本身排除，避免自我加密造成循环
_SECRET_SUFFIXES = ("_API_KEY", "_SECRET_KEY")


def is_secret(name: str) -> bool:
    """判断一个环境变量名是否为敏感密钥（需要加密存储）。"""
    n = name.upper()
    if n == MASTER_ENV:
        return False
    return any(n.endswith(s) for s in _SECRET_SUFFIXES)


def _master_key() -> bytes:
    k = os.environ.get(MASTER_ENV)
    if k:
        return k.encode()
    # 不在 os.environ 时优先从 .env 读取持久主密钥；否则每次新进程都会重新生成，
    # 覆盖 .env 里的旧主密钥，导致已加密的 secrets.enc 解密失败（本次排查发现的失配根因）。
    if ENV_FILE.exists():
        m = re.search(rf"^\s*(?:export\s+)?{re.escape(MASTER_ENV)}\s*=(.*)$",
                      ENV_FILE.read_text("utf-8"), re.M)
        if m and m.group(1).strip():
            k = m.group(1).strip()
            os.environ[MASTER_ENV] = k
            return k.encode()
    k = Fernet.generate_key().decode()
    os.environ[MASTER_ENV] = k
    _upsert_env(MASTER_ENV, k)
    return k.encode()


def _upsert_env(name: str, value: str) -> None:
    lines = ENV_FILE.read_text("utf-8").splitlines() if ENV_FILE.exists() else []
    pat = re.compile(rf"\s*(export\s+)?{re.escape(name)}\s*=")
    lines = [ln for ln in lines if not pat.match(ln)]
    lines.append(f"{name}={value}")
    ENV_FILE.write_text("\n".join(lines) + "\n", "utf-8")


def _read_store() -> dict:
    if not SECRETS_FILE.exists():
        return {}
    try:
        raw = SECRETS_FILE.read_bytes()
        if not raw.strip():
            return {}
        return json.loads(Fernet(_master_key()).decrypt(raw))
    except Exception:
        # 文件损坏/主密钥不匹配 -> 返回空；调用方按平台容错，不影响其它平台
        return {}


def _write_store(store: dict) -> None:
    data = Fernet(_master_key()).encrypt(json.dumps(store).encode())
    SECRETS_FILE.write_bytes(data)


def get_secret(name: str):
    return _read_store().get(name)


def set_secret(name: str, value: str) -> None:
    """写入（加密）或删除（空值）某个平台密钥，并剥除 .env 中的明文行；
    同时同步当前进程 os.environ，使 GET /api/keys 与采样器保存后立即生效（无需重启）。"""
    store = _read_store()
    if value:
        store[name] = value
        os.environ[name] = value
    else:
        store.pop(name, None)
        os.environ.pop(name, None)
    _write_store(store)
    if ENV_FILE.exists():
        pat = re.compile(rf"\s*(export\s+)?{re.escape(name)}\s*=")
        lines = [ln for ln in ENV_FILE.read_text("utf-8").splitlines() if not pat.match(ln)]
        ENV_FILE.write_text("\n".join(lines) + "\n", "utf-8")


def delete_secret(name: str) -> None:
    set_secret(name, "")


def load_secrets_into_env() -> None:
    """启动时解密 secrets.enc 进 os.environ，并把 .env 明文密钥迁移到加密存储。"""
    store = _read_store()
    for name, val in store.items():
        os.environ.setdefault(name, val)
    # 迁移：.env 中残留的明文敏感变量 -> 加密存储，并从 .env 剥除
    if ENV_FILE.exists():
        raw = ENV_FILE.read_text("utf-8").splitlines()
        new_lines = []
        changed = False
        for ln in raw:
            m = re.match(r"^\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=(.*)$", ln)
            if m and is_secret(m.group(1)) and m.group(1) not in store:
                store[m.group(1)] = m.group(2).strip().strip("'\"").strip('"')
                changed = True
                continue
            new_lines.append(ln)
        if changed:
            _write_store(store)
            ENV_FILE.write_text("\n".join(new_lines) + "\n", "utf-8")
            for n, v in store.items():
                os.environ.setdefault(n, v)


def mask_key(value: str) -> str:
    """把密钥掩码化用于界面回显：保留前缀与尾号，中间打码。"""
    if not value:
        return ""
    if len(value) <= 8:
        return "•" * len(value)
    return value[:4] + "•" * max(4, len(value) - 8) + value[-4:]
