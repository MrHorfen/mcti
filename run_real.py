#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""用真实 MCP 数据生成本人 MCTI 卡（演示账号数据）。"""
import json, re, sys, datetime
sys.path.insert(0, "C:/Users/Lenovo/Desktop/麦当劳/mcti")
import mcti

RAW = json.load(open("D:/workbuddy_cache/temp/mcp_raw.json", encoding="utf-8"))

# --- 1) 订单 ---
ol_text = RAW["order-list"]["result"]["content"][0]["text"]
m = re.search(r'\{"success".*\}\s*$', ol_text, re.S)
if not m:
    m = re.search(r'## Original Response\s*\n(.*)', ol_text, re.S)
    js = json.loads(re.search(r'\{.*\}', m.group(1), re.S).group(0))
else:
    js = json.loads(m.group(0))
orders_raw = js["data"]["list"]

# orderType 映射：演示账号全为 "1"，且 11 张券均为「到店专用」，
# 故 "1" 判为到店(dinein)；外卖=delivery。
type_map = {"1": "dinein", "2": "delivery", "3": "pickup"}
orders = []
for o in orders_raw:
    ct = o.get("createTime", "")
    hour = int(ct[11:13]) if len(ct) >= 13 else 12
    t = type_map.get(str(o.get("orderType", "")), "dinein")
    orders.append({"hour": hour, "type": t, "used_coupon": False})

# --- 2) 账户 ---
acc_text = RAW["query-my-account"]["result"]["content"][0]["text"]
acc_js = json.loads(re.search(r'\{.*\}', acc_text, re.S).group(0))
points = int(float(acc_js["data"]["availablePoint"]))

# --- 3) 券（数「到店专用」未用券，order-list 无逐单用券字段 → 用券维度由未用券信号推断）
cp_text = RAW["query-my-coupons"]["result"]["content"][0]["text"]
m_cnt = re.search(r'共\s*(\d+)\s*张', cp_text)
unused = int(m_cnt.group(1)) if m_cnt else 0
dinein_coupons = cp_text.count("到店专用")

# --- 4) 组装 raw，喂给 MCTI ---
raw = {
    "orders": orders,
    "account": {"points": points},
    "my_coupons": [{} for _ in range(unused)],
}
feats = mcti.features_from_raw(raw)
print("订单数:", len(orders), "| 积分:", points, "| 未用券:", unused, "(到店专用", dinein_coupons, ")")
print("特征:", json.dumps(feats, ensure_ascii=False))
result = mcti.analyze(feats)
print("判定:", result["code"], result["emoji"], result["name"])

handle = "@MrHorfen"
date_str = datetime.date.today().strftime("%Y.%m.%d")
img_path = str(mcti.ROOT_ASSETS / f"{result['code']}.png")
card = mcti.render_card(result, handle=handle, date_str=date_str, img_path=img_path)
out = "C:/Users/Lenovo/Desktop/麦当劳/mcti/real_card.html"
with open(out, "w", encoding="utf-8") as f:
    f.write(card)
print("卡片 ->", out)
