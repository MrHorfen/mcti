# WorkBuddy 开发对话上下文（workbuddy.md）

> 本文件用于核验本项目是否真实使用腾讯 WorkBuddy 智能体开发，是参与 WorkBuddy 专项奖励（前 100 名 + 3000 积分）的必需材料。
> 下方为开发过程中的代表性对话摘录（实际提交时请替换为你在 WorkBuddy 中的真实对话导出）。

---

**用户**：帮我做一个麦当劳消费习惯的幽默 MBTI，能分享到朋友圈。
**WorkBuddy**：明白。我设计「麦门四维」：时段(夜/晨)、方式(宅送/到店)、囤积(积分+未用券)、用券(频率)，映射到 16 种人格。先写核心脚本 `mcti.py`，用麦当劳 MCP 的 order-list / query-my-account / query-my-coupons 拉真实数据。
**用户**：卡片要麦当劳红金风，手机截图好看。
**WorkBuddy**：已用 #da291c + #ffc72c 做 400px 移动卡片，含类型码、人格名、四维进度条、本命单品、分享文案。纯标准库零依赖，直接 `python mcti.py demo` 预览。
**用户**：接入 MCP 时别真下单。
**WorkBuddy**：已约束 Skill 只用只读查询工具（order-list / query-my-account / query-my-coupons），禁用 create-order / auto-bind-coupons，安全无副作用。
**用户**：参赛文件齐了吗？
**WorkBuddy**：README / CONTEST_DECLARATION(官方原版) / MCP_INTEGRATION / mcp-config.example.json / workbuddy.md 都已就绪，可发 GitHub 提 Issue 报名。

---

*（以上为示例上下文；正式参赛请将你在 WorkBuddy 中与本项目的真实对话记录导出替换本文件。）*
