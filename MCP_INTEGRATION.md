# MCP 接入说明（MCP_INTEGRATION.md）

## 使用的麦当劳 MCP Server

- **Server**：麦当劳中国官方 MCP（`mcd-mcp`）
- **接入地址**：`https://mcp.mcd.cn`
- **传输协议**：Streamable HTTP
- **认证**：请求头 `Authorization: Bearer ${MCD_MCP_TOKEN}`（Token 通过 https://open.mcd.cn/mcp 申请，存入环境变量，不落库）

## 实际调用的工具（Tool）

| MCP Tool | 用途 | 映射到麦门维度 |
|---|---|---|
| `order-list` | 查询近期到店/外送历史订单（含时间、就餐方式、是否用券） | 时段(N/D)、方式(H/W)、用券(Q/X) |
| `query-my-account` | 查询积分账户（可用/累计/冻结积分） | 囤积(K/S) |
| `query-my-coupons` | 查询当前可用优惠券列表（数量=未用券存量） | 囤积(K/S)、用券(Q/X) |
| `query-store-coupons` | 查询当前门店可用优惠券 | 猎券倾向参考 |
| `available-coupons` | 麦麦省可领券列表 | 猎券倾向参考 |
| `now-time-info` | 获取当前时间 | 报告生成时间戳 |

## 调用流程

1. WorkBuddy 连接器已配置 `mcd-mcp` 并启用。
2. 用户发起「测我的麦门 MBTI」。
3. Skill 依次调用 `order-list` → `query-my-account` → `query-my-coupons`（可选 `query-store-coupons`/`available-coupons`）拉取数据。
4. 将原始数据规整为 `features`（`mcti.py` 的 `features_from_raw`），计算四维比例。
5. `analyze()` 判定 16 种人格之一，`render_card()` 生成单文件 HTML 分享卡片。
6. 返回卡片路径，用户截图分享。

## 业务价值

- **真实数据 + 幽默人格 = 强社交传播**：用户愿意把「自己的麦门人格」发朋友圈/小红书，天然带来转发与 Star。
- **轻量闭环**：只读查询类工具（不下单、不领券），安全无副作用，适合 Demo 与传播。
- **贴合官方 MCP 定位**：充分使用麦当劳 MCP 的订单/会员/优惠能力，验证 MCP 在「个性化内容生成」场景的可用性。

## 注意事项

- Token 限流 600 次/分钟，本项目仅做少量只读查询，远低于限额。
- 所有凭证仅以环境变量占位符出现，仓库不含任何真实 Token（见 `mcp-config.example.json` 与 `CONTEST_DECLARATION.md`）。
- 读取为当前登录会员的真实消费数据，仅本地计算、不出域，符合隐私与合规要求。
