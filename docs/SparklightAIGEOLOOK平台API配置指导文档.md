# 星火之光 SparklightAIGEOLOOK · 平台 API 配置指导文档

> 基于 GEOLOOK 开源架构 · 引擎与密钥接入指南 · 2026-08-22
> 本文档按星火之光官网（sparklight-ai.com）品牌视觉规范（主靛蓝 #2D326B / 柔珊瑚 #FF6B5B / 暖白 #FBF8F4）整理。

---

## 总览

星火之光 SparklightAIGEOLOOK 的 AI 采样与诊断能力，依赖已配置的模型引擎 Key。看板「引擎与密钥」页面支持 5 家国内主流厂商，Key 写入项目根目录 `.env` 后立即生效。配好任意 1 个引擎即可开始采样，配得越多覆盖越全。建议先配 1 个跑通，再补全其余用于多引擎横评。

| # | 公司 / 平台 | 区域 | 状态 | 环境变量 | 获取链接 |
|---|------------|------|------|----------|---------|
| 1 | 豆包（方舟 API / 火山引擎） | 国内 | 优先推荐 | `ARK_API_KEY` | https://www.volcengine.com/product/ark |
| 2 | 智谱 GLM | 国内 | 未配 | `ZHIPUAI_API_KEY` | https://open.bigmodel.cn/ |
| 3 | DeepSeek | 国内 | 已配（...e956） | `DEEPSEEK_API_KEY` | https://platform.deepseek.com/ |
| 4 | Kimi（月之暗面 Moonshot） | 国内 | 未配 | `MOONSHOT_API_KEY` | https://platform.moonshot.cn/ |
| 5 | MiniMax | 国内/海外 | 未配 | `MINIMAX_API_KEY` | https://www.minimax.io/ |

---

## 1. 豆包 / 方舟 API（火山引擎 Ark） `优先`

- **平台**：字节跳动 · 火山引擎 · 方舟（Ark） · OpenAI 兼容协议
- **环境变量**：`ARK_API_KEY`
- **获取链接**：https://www.volcengine.com/product/ark
- **控制台**：https://console.volcengine.com/ark

### 配置步骤

1. 用火山引擎账号登录；首次使用需完成实名认证。
2. 进入「方舟 → 在线推理」开通「在线推理 - 按量付费」或对应模型。
3. 在「API Key 管理」创建 API Key（可设置失效期与限额）。
4. 在「在线推理 → 模型列表」开通要用的豆包模型（如 `doubao-pro-32k`、`doubao-1-5-pro`）。
5. 将 Key 写入项目 `.env`：

   ```ini
   ARK_API_KEY=你的密钥
   ARK_MODEL=doubao-1-5-pro-32k-250115
   ARK_BASE_URL=https://ark.cn-beijing.volces.com/api/v3
   ```

### ⚠ 特殊说明

必须先「开通模型」才能调用；模型 ID（如 `doubao-...`）填在请求的 `model` 字段，而非写在 Key 里。

---

## 2. 智谱 GLM（BigModel 开放平台）

- **官网**：https://www.zhipuai.cn/
- **开放平台**：https://open.bigmodel.cn/
- **环境变量**：`ZHIPUAI_API_KEY`（变量名沿用旧 SDK 命名）

### 配置步骤

1. 在开放平台注册并完成实名。
2. 「个人中心 → API Keys」→「创建新 Key」，复制保存（仅显示一次）。
3. 在「模型广场」按需开通 GLM-4 / GLM-4-Plus / GLM-Z1 等模型权限。
4. 写入 `.env`：

   ```ini
   ZHIPUAI_API_KEY=你的密钥
   ```

### ⚠ 特殊说明

多数模型需先在「模型广场」开通才能调用；GLM-4-Flash 通常提供 200 万 token 体验包。

---

## 3. DeepSeek `已配置`

- **官网**：https://www.deepseek.com/
- **开放平台**：https://platform.deepseek.com/
- **环境变量**：`DEEPSEEK_API_KEY`
- **协议**：完全兼容 OpenAI（`base_url=https://api.deepseek.com`）

### 配置步骤

1. 注册并登录开放平台。
2. 「API Keys」→「创建新 Key」，命名后立即复制保存。
3. 在「充值 / 账户余额」中确保有可用额度。
4. 写入 `.env`：

   ```ini
   DEEPSEEK_API_KEY=你的密钥
   ```

### ⚠ 特殊说明

截图显示「已配置 …e956」，如需轮换请用看板「修改」。无「开通模型」环节，Key 对所有已上线模型生效。

---

## 4. Kimi（月之暗面 Moonshot AI）

- **官网**：https://www.moonshot.cn/
- **开放平台**：https://platform.moonshot.cn/
- **环境变量**：`MOONSHOT_API_KEY`
- **计费**：按上下文窗口区分（8k / 32k / 128k）

### 配置步骤

1. 注册并登录。
2. 「控制台 → API Key 管理」→「新建 Key」，复制保存。
3. 「账户管理 → 充值」按需充入额度。
4. 写入 `.env`：

   ```ini
   MOONSHOT_API_KEY=你的密钥
   MOONSHOT_BASE_URL=https://api.moonshot.cn/v1
   ```

### ⚠ 特殊说明

长上下文（128k）单价显著高于短上下文；Key 不绑定具体模型，对所有 K 系列生效。

---

## 5. MiniMax

- **官网**：https://www.minimaxi.com/
- **海外站**：https://www.minimax.io/
- **中国版 API**：https://api.minimax.chat/
- **环境变量**：`MINIMAX_API_KEY`

### 配置步骤

1. 进入海外版或中国版注册账号。
2. 「Account → API Keys」→「Create new secret key」。
3. 复制保存（仅显示一次）。
4. 写入 `.env`：

   ```ini
   MINIMAX_API_KEY=你的密钥
   ```

### ⚠ 特殊说明

海外版（minimax.io）与中国版（api.minimax.chat）账号体系不通用，需分别注册。海外版常用 `MiniMax-Text-01`、`MiniMax-VL-01`。

---

## 通用配置提醒

> Key 写入 `work/<项目slug>/.env`，立即生效。配好任意 1 个引擎就能开始采样；配得越多覆盖越全。若仅配 1 个即可跑通全流程，其余用于多引擎横评与可用性对比。

### 「配置失败：连续失败，服务未响应」常见根因

该提示多数情况下 **不是 Key 本身问题**，而是：

1. GEOLOOK 看板进程未运行（依赖被重置导致退出）。
2. 写错了目录（写到了仓库根目录，而非 `work/<slug>/.env`）。

参考项目内的 `ensure-deps.ps1` 与 `geolib.py` 中的 `_ensure_dependencies()` 自愈机制。

---

## 缺失 / 无法识别说明

本次截图清晰可识别所有 5 家厂商，**无缺失项**。

---

*星火之光 SparklightAIGEOLOOK · 平台 API 配置指导文档 v1.1 · 2026-08-22*
