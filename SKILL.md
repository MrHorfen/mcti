---
name: MCTI
description: 基于用户真实的麦当劳消费数据（通过官方 MCP），生成一套幽默的「麦门人格」画像（16 型），并产出一张可截图分享的麦当劳风格卡片。触发词：MCTI、麦当劳人格测试、测我的麦门人格、我的消费人格、麦门人格。
---

# MCTI（McDonald's MBTI）

一个把「麦当劳消费习惯」变成社交货币的趣味 Skill：读取用户真实消费数据 → 算人格 → 出分享卡片。

## 触发场景
- 用户说「测一下我的MCTI / 麦当劳人格 / 我的消费人格」
- 用户分享麦当劳订单截图并想知道自己是什么「麦门人格」

## 前置条件
- WorkBuddy 已配置并启用麦当劳 MCP 连接器（`mcd-mcp`，见 `mcp-config.example.json`）。
- 用户已登录自己的麦当劳会员（MCP 读取的是当前会员真实数据）。

## 执行流程（严格按顺序）
1. **确认 MCP 已连接**：若未连接，提示用户先在【连接器】配置 `mcd-mcp`（Token 存环境变量 `MCD_MCP_TOKEN`）。
2. **拉取数据**（只读，安全）：
   - 调用 `order-list` 取近期历史订单（时间、就餐方式、是否用券）。
   - 调用 `query-my-account` 取积分。
   - 调用 `query-my-coupons` 取当前可用券列表（数量=未用券存量）。
   - 可选：`query-store-coupons` / `available-coupons` 作为猎券倾向参考；`now-time-info` 取时间戳。
3. **规整为 features**：把上述结果整理成 JSON：
   ```json
   {"orders":[{"hour":21,"type":"delivery","used_coupon":true}],"account":{"points":3200},"my_coupons":[1,2,3]}
   ```
   调用 `python mcti.py --raw <数据文件> out.html` 由脚本自动计算；或直接调用 `features_from_raw()`。
4. **判定人格**：`analyze(features)` 返回 16 型之一（含名称、语录、画像、本命单品、分享文案、四维占比）。
5. **生成卡片**：`render_card(result)` 输出单文件 HTML；或运行 `python mcti.py <features.json> out.html`。
6. **回应用户**：展示人格类型 + 卡片路径，并附上分享文案，提示「截图发朋友圈/小红书」。

## 关键约束
- 仅使用**只读查询**类工具，绝不调用 `create-order` / `auto-bind-coupons` 等写入动作（避免真实下单/领券副作用）。
- 不在任何输出或仓库中包含真实 Token / 会员隐私；凭证仅以 `${MCD_MCP_TOKEN}` 占位。
- 明确告知用户：结果仅供娱乐，非专业建议（见 `CONTEST_DECLARATION.md`）。

## 文件
- `mcti.py`：核心逻辑（零依赖），含 `features_from_raw` / `analyze` / `render_card`。
- `MCP_INTEGRATION.md`：MCP 工具与流程详述（参赛必需）。
- `example_card.html`：样例卡片，供用户预览效果。
