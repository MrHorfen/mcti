# 🍔 MCTI（McDonald's Consumption Type Indicator）

> 基于你的麦当劳消费习惯，生成一套**幽默的麦门人格画像**，并产出一张可截图分享的麦当劳风格卡片。
> 你是「深夜囤券王」还是「元气挥霍怪」？让数据说话。

「MCTI」是 2026 麦当劳程序员创意开发大赛的参赛 Skill：它读取你真实的麦当劳消费数据（通过官方 MCP），从**下单时段 / 就餐方式 / 积分囤积 / 用券频率**四个维度，把你映射成 16 种麦门人格之一，并生成一张红金配色、可直接发朋友圈 / 小红书的分享卡片。

## ✨ 特性

- 🧩 **真实数据驱动**：直接调用麦当劳官方 MCP（order-list / 积分 / 优惠券），不是瞎编的趣味测试。
- 🃏 **16 种麦门人格**：夜行者 / 晨型人 × 宅送派 / 到店党 × 囤积狂 / 挥霍派 × 猎券猎手 / 随心所欲。
- 📱 **可分享卡片**：一键生成单文件 HTML 卡片，截图即发，社交属性拉满（这也正是它容易拿 Star 的原因）。
- 🪶 **零依赖**：核心逻辑纯 Python 标准库，无需 `pip install`。

## 🎯 目标用户

- 麦门信徒 / 麦当劳重度用户，想看看自己的「消费人格」；
- 喜欢趣味人格测试、爱在社交平台分享的人；
- 想给朋友「算一卦」的整活达人。

## 🚀 安装与使用

### 方式一：作为 WorkBuddy Skill 使用（推荐，参赛联动）

1. 在 WorkBuddy 左侧【连接器】中配置麦当劳 MCP（见 `mcp-config.example.json`，把 Token 存入环境变量 `MCD_MCP_TOKEN`）。
2. 把本仓库作为自定义 Skill 载入，直接对话：「帮我测一下我的MCTI」。
3. Skill 会自动调用 MCP 拉取你的数据 → 计算人格 → 生成分享卡片。

### 方式二：命令行直接跑

```bash
# 用内置样例体验（无需 MCP Token）
python mcti.py demo

# 用你自己的特征 JSON 生成卡片
python mcti.py samples/sample_features.json my_card.html

# 从原始订单/账户/券数据算特征再出卡片
python mcti.py --raw samples/raw_sample.json my_card.html
```

生成的 `*.html` 用浏览器打开即可截图分享。

## 🧠 四维模型

| 维度 | 左 | 右 | 判定依据 |
|---|---|---|---|
| 时段 | 夜行者 (N) | 晨型人 (D) | 21:00–06:00 下单占比 |
| 方式 | 宅送派 (H) | 到店党 (W) | 外送订单占比 |
| 囤积 | 囤积狂 (K) | 挥霍派 (S) | 积分余额 + 未用券存量 |
| 用券 | 猎券猎手 (Q) | 随心所欲 (X) | 订单用券频率 |

十六种组合对应十六种幽默人格（详见 `mcti.py` 的 `TYPES` 表）。

## 📂 仓库结构

```
mcti/
├── mcti.py              # 核心逻辑 + 卡片生成（零依赖）
├── build_badges.py      # 生成可分享工牌卡（单人格 / 16 型全集）
├── build_gallery.py     # 生成 16 型全家福画廊
├── SKILL.md             # WorkBuddy Skill 定义
├── README.md            # 本文件
├── MCP_INTEGRATION.md   # MCP 接入与工具说明（参赛必需）
├── CONTEST_DECLARATION.md # 参赛声明（官方原版，勿改）
├── mcp-config.example.json # 脱敏 MCP 配置示例
├── workbuddy.md         # WorkBuddy 开发对话上下文（联动奖励）
├── VISUAL_GUIDE.md      # 视觉规范（品牌色 / 生图铁律）
├── assets/              # 16 型人格橘猫图（CODE.png）
├── samples/             # 样例数据
└── gallery.html         # 16 型画廊（浏览器打开预览）
```

## ⚠️ 声明

本项目为大赛创意作品，非麦当劳官方产品，仅供娱乐，不构成任何专业建议。详见 `CONTEST_DECLARATION.md`。

---

⭐ 觉得好玩？点个 Star 让更多麦门信徒看到！

## 🎯 真机演示（麦当劳 MCP 真实数据）

用大赛发放的麦当劳 MCP Token 拉取真实订单 / 积分 / 券，套本作品管道生成的工牌分享卡示例：

- [`real_badge_card.html`](real_badge_card.html) — 真机数据生成的「门店自助王」工牌卡（演示账号数据，仅供娱乐）
- [`run_real.py`](run_real.py) — 一键拉取 MCP 真实数据并生成卡片的脚本（依赖 `D:/workbuddy_cache/temp/mcp_raw.json` 本地 dump）

> 注：演示 Token 为大赛沙盒账号（仅 6 笔午市到店订单），非个人真实消费史；接入本人账号 Token 即出本人卡。
