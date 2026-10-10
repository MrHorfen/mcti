#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MCTI (McDonald's Consumption Type Indicator) —— 基于你的麦当劳消费习惯，生成一套幽默的麦门人格画像，
并产出一张可截图分享的麦当劳风格卡片。

纯标准库实现，零依赖。可直接对样例数据运行，也可由 WorkBuddy Skill 在拿到 MCP 数据后调用。

用法：
  python mcti.py demo                      # 用内置样例生成 example_card.html
  python mcti.py features.json card.html   # 用 features JSON 生成卡片
  python mcti.py --raw raw_sample.json out.html   # 从原始订单/账户/券数据算特征再出卡片
"""

import json
import sys
import datetime
import base64
import html
from pathlib import Path

# ---------------------------------------------------------------------------
# 1. 麦门四维模型
#    N/D 夜行者 vs 晨型人   (下单时段)
#    H/W 宅送派 vs 到店党   (就餐方式)
#    K/S 囤积狂 vs 挥霍派   (积分+未用券存量)
#    Q/X 猎券猎手 vs 随心所欲 (用券频率)
# ---------------------------------------------------------------------------

TYPES = {
    "NHKQ": dict(emoji="🛎️", name="外卖券管家",
                 tagline="券不过夜，单不过点。",
                 profile="深夜的外卖从不错过任何一张券，你的快乐是「券到手 + 门铃响」双响炮。",
                 recommend="麦麦送出前一鸡块桶",
                 share="外卖券管家：券不过夜，单不过点。🛎️"),
    "NHKX": dict(emoji="🐟", name="囤券咸鱼",
                 tagline="囤着，但不一定用。",
                 profile="券在卡包里睡大觉，你懒得凑也懒得用，囤本身就有安全感。",
                 recommend="麦辣鸡腿堡",
                 share="囤券咸鱼：囤着，但不一定用。🐟"),
    "NHSQ": dict(emoji="🎯", name="满减狙击手",
                 tagline="差一块，我也能凑。",
                 profile="再晚也要把券用满，精致懒人晚期，省下的钱都花在刀刃上。",
                 recommend="巨无霸套餐",
                 share="满减狙击手：差一块，我也能凑。🎯"),
    "NHSX": dict(emoji="😼", name="外卖散财喵",
                 tagline="深夜不加价，不舒服。",
                 profile="深夜情绪价值拉满，下单从不看单价，快乐是唯一 KPI。",
                 recommend="麦麦送满减桶",
                 share="外卖散财喵：深夜不加价，不舒服。😼"),
    "NWHKQ": dict(emoji="🌃", name="门店守夜人",
                  tagline="打烊前，我必到。",
                  profile="夜宵必须到店才有灵魂，路过柜台顺手把券囤成小金库。",
                  recommend="开心乐园餐（自己吃）",
                  share="门店守夜人：打烊前，我必到。🌃"),
    "NWHKX": dict(emoji="👻", name="夜游囤券鬼",
                  tagline="散步顺手，囤张券。",
                  profile="没有计划就是最好的计划，散步到店顺手囤券，随缘即正义。",
                  recommend="麦旋风味",
                  share="夜游囤券鬼：散步顺手，囤张券。👻"),
    "NWSQ": dict(emoji="👑", name="堂食满减王",
                  tagline="堂食，也要满。",
                  profile="夜里到店堂食，券一张不落全用掉，主打一个干净利落。",
                  recommend="板烧鸡腿堡",
                  share="堂食满减王：堂食，也要满。👑"),
    "NWSX": dict(emoji="🦁", name="门店豪横猫",
                  tagline="门店里，点最贵的。",
                  profile="夜猫子本猫，到店就点最贵的那几个，深夜的奢侈属于你。",
                  recommend="麦当劳限定新品",
                  share="门店豪横猫：门店里，点最贵的。🦁"),
    "DHKQ": dict(emoji="☕", name="早八攒券僧",
                  tagline="麦咖啡，续命。",
                  profile="一天从麦咖啡和囤好的券开始，规律得像打卡机。",
                  recommend="吉士蛋麦满分",
                  share="早八攒券僧：麦咖啡，续命。☕"),
    "DHKX": dict(emoji="📦", name="早八囤券叔",
                  tagline="早餐券，先囤为敬。",
                  profile="早餐靠外送续命，点单全凭肌肉记忆，券随缘。",
                  recommend="猪柳蛋麦满分",
                  share="早八囤券叔：早餐券，先囤为敬。📦"),
    "DHSQ": dict(emoji="🥯", name="早餐满减怪",
                  tagline="早餐的满，我来凑。",
                  profile="早餐也要把券用出仪式感，省下的钱转身买了杯咖啡。",
                  recommend="双吉蛋堡套餐",
                  share="早餐满减怪：早餐的满，我来凑。🥯"),
    "DHSX": dict(emoji="🐦", name="早八散财鸟",
                  tagline="早饭，不比价。",
                  profile="早起的人有权任性，早餐不比价，快乐第一位。",
                  recommend="金拱门早餐全餐",
                  share="早八散财鸟：早饭，不比价。🐦"),
    "DWHKQ": dict(emoji="🛒", name="晨间门店僧",
                  tagline="开门第一单，我包了。",
                  profile="清晨溜达去门店，先囤券再点单，仪式感拉满。",
                  recommend="薯饼",
                  share="晨间门店僧：开门第一单，我包了。🛒"),
    "DWKX": dict(emoji="🌞", name="晨店随心人",
                  tagline="看啥点啥，不纠结。",
                  profile="晨光里的随心派，走到柜台看今天想宠幸哪一款。",
                  recommend="圆筒冰淇淋（早场）",
                  share="晨店随心人：看啥点啥，不纠结。🌞"),
    "DWSQ": dict(emoji="🏆", name="门店满减王",
                  tagline="门店满减，一家亲。",
                  profile="到店吃早餐也要把券算到最后一分，精致的懒人天花板。",
                  recommend="汉堡牛堡",
                  share="门店满减王：门店满减，一家亲。🏆"),
    "DWSX": dict(emoji="🍱", name="门店自助王",
                  tagline="门店，当自助。",
                  profile="清晨到店豪横点单，吃饱喝足才是元气满格的打开方式。",
                  recommend="麦辣鸡翅",
                  share="门店自助王：门店，当自助。🍱"),
}

AXES = [
    ("N", "D", "夜行者", "晨型人"),
    ("H", "W", "宅送派", "到店党"),
    ("K", "S", "囤积狂", "挥霍派"),
    ("Q", "X", "猎券猎手", "随心所欲"),
]


def features_from_raw(raw: dict) -> dict:
    """从原始 MCP 数据（order-list / 账户 / 券）计算四维特征。

    raw 预期结构：
      {
        "orders": [{"hour": 0-23, "type": "delivery"|"pickup"|"dinein", "used_coupon": true/false}, ...],
        "account": {"points": int},
        "my_coupons": [ ... ]   # 长度=未用券数量
      }
    """
    orders = raw.get("orders", [])
    total = len(orders) or 1
    night = sum(1 for o in orders if o.get("hour", 12) >= 21 or o.get("hour", 12) < 6)
    delivery = sum(1 for o in orders if o.get("type") == "delivery")
    used_coupon = sum(1 for o in orders if o.get("used_coupon"))

    points = raw.get("account", {}).get("points", 0)
    unused_coupons = len(raw.get("my_coupons", []))

    night_ratio = night / total
    delivery_ratio = delivery / total
    # 囤积：积分(归一) 与 未用券存量(归一) 取平均
    hoard_score = min(1.0, (min(points / 5000.0, 1.0) + min(unused_coupons / 20.0, 1.0)) / 2.0)
    coupon_ratio = used_coupon / total

    return {
        "night_ratio": round(night_ratio, 3),
        "delivery_ratio": round(delivery_ratio, 3),
        "hoard_score": round(hoard_score, 3),
        "coupon_ratio": round(coupon_ratio, 3),
        "total_orders": len(orders),
        "points": points,
        "unused_coupons": unused_coupons,
    }


def analyze(features: dict) -> dict:
    """根据特征判定麦门人格。"""
    code = (
        ("N" if features["night_ratio"] >= 0.5 else "D")
        + ("H" if features["delivery_ratio"] >= 0.5 else "W")
        + ("K" if features["hoard_score"] >= 0.5 else "S")
        + ("Q" if features["coupon_ratio"] >= 0.5 else "X")
    )
    t = TYPES[code]
    return {
        "code": code,
        "emoji": t["emoji"],
        "name": t["name"],
        "tagline": t["tagline"],
        "profile": t["profile"],
        "recommend": t["recommend"],
        "share": t["share"],
        "traits": [
            ("夜行者" if code[0] == "N" else "晨型人",
             "晨型人" if code[0] == "N" else "夜行者",
             int(features["night_ratio"] * 100) if code[0] == "N" else int((1 - features["night_ratio"]) * 100)),
            ("宅送派" if code[1] == "H" else "到店党",
             "到店党" if code[1] == "H" else "宅送派",
             int(features["delivery_ratio"] * 100) if code[1] == "H" else int((1 - features["delivery_ratio"]) * 100)),
            ("囤积狂" if code[2] == "K" else "挥霍派",
             "挥霍派" if code[2] == "K" else "囤积狂",
             int(features["hoard_score"] * 100) if code[2] == "K" else int((1 - features["hoard_score"]) * 100)),
            ("猎券猎手" if code[3] == "Q" else "随心所欲",
             "随心所欲" if code[3] == "Q" else "猎券猎手",
             int(features["coupon_ratio"] * 100) if code[3] == "Q" else int((1 - features["coupon_ratio"]) * 100)),
        ],
        "features": features,
    }


def render_card(result: dict, handle: str = "@麦门信徒", date_str: str = None,
                 img_path: str = None) -> str:
    if date_str is None:
        date_str = datetime.date.today().strftime("%Y.%m.%d")
    traits_html = ""
    for dom, other, pct in result["traits"]:
        traits_html += f"""
        <div class="trait">
          <div class="trow"><span class="dom">{html.escape(dom)}</span><span class="pct">{pct}%</span></div>
          <div class="bar"><div class="fill" style="width:{pct}%"></div></div>
        </div>"""
    # 橘猫角色图（base64 内联，单文件可分享）
    hero_html = ""
    if img_path and Path(img_path).exists():
        data = base64.b64encode(Path(img_path).read_bytes()).decode()
        hero_html = (f'<div class="hero"><img src="data:image/png;base64,{data}" '
                     f'alt="{html.escape(result["name"])}"></div>')
    return f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>MCTI · {html.escape(result['code'])} {html.escape(result['name'])}</title>
<style>
  *{{box-sizing:border-box;margin:0;padding:0}}
  body{{background:#f3f3f3;font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif;display:flex;justify-content:center;padding:20px}}
  .card{{width:400px;background:#fff;border-radius:22px;overflow:hidden;box-shadow:0 10px 30px rgba(0,0,0,.18)}}
  .hero{{background:linear-gradient(160deg,#ffd76a,#ffc72c);padding:14px;text-align:center}}
  .hero img{{display:block;width:78%;max-width:300px;margin:0 auto;border-radius:16px;box-shadow:0 6px 16px rgba(120,80,0,.25)}}
  .head{{background:linear-gradient(135deg,#da291c,#b81d11);color:#ffc72c;padding:22px 22px 18px;text-align:center}}
  .head .kicker{{font-size:12px;letter-spacing:3px;color:#ffe08a;opacity:.9}}
  .head .code{{font-size:40px;font-weight:900;color:#fff;letter-spacing:4px;margin:4px 0}}
  .head .emoji{{font-size:46px}}
  .head .name{{font-size:22px;font-weight:800;color:#ffc72c;margin-top:2px}}
  .head .sub2{{font-size:10px;letter-spacing:2px;color:#ffe08a;opacity:.85;margin-top:3px}}
  .body{{padding:18px 22px 22px}}
  .tag{{background:#fff4d6;color:#a8741a;border-left:4px solid #ffc72c;padding:10px 12px;border-radius:8px;font-size:14px;font-weight:700;margin-bottom:14px}}
  .traits{{margin:6px 0 14px}}
  .trait{{margin:9px 0}}
  .trow{{display:flex;justify-content:space-between;font-size:13px;font-weight:700;color:#333;margin-bottom:4px}}
  .trow .pct{{color:#da291c}}
  .bar{{height:8px;background:#eee;border-radius:6px;overflow:hidden}}
  .fill{{height:100%;background:linear-gradient(90deg,#ffc72c,#da291c);border-radius:6px}}
  .profile{{font-size:13.5px;color:#444;line-height:1.7;background:#fafafa;border:1px solid #eee;border-radius:10px;padding:12px;margin-bottom:12px}}
  .rec{{font-size:14px;color:#da291c;font-weight:800;margin-bottom:12px}}
  .rec b{{background:#fff4d6;padding:2px 8px;border-radius:6px;color:#a8741a}}
  .share{{font-size:13px;color:#666;font-style:italic;border-top:1px dashed #ddd;padding-top:12px}}
  .foot{{text-align:center;font-size:11px;color:#aaa;padding:12px;background:#fafafa}}
</style></head>
<body>
  <div class="card">
    <div class="head">
      <div class="kicker">MCTI</div>
      <div class="code">{html.escape(result['code'])}</div>
      <div class="emoji">{html.escape(result['emoji'])}</div>
      <div class="name">{html.escape(result['name'])}</div>
      <div class="sub2">McDonald's Consumption Type Indicator</div>
    </div>
    <div class="body">
      {hero_html}
      <div class="tag">「{html.escape(result['tagline'])}」</div>
      <div class="traits">{traits_html}</div>
      <div class="profile">{html.escape(result['profile'])}</div>
      <div class="rec">🍔 你的本命单品：<b>{html.escape(result['recommend'])}</b></div>
      <div class="share">“{html.escape(result['share'])}”<br>—— {html.escape(handle)}</div>
    </div>
    <div class="foot">MCTI · 由你的麦当劳消费习惯生成 · 仅供娱乐 {date_str}</div>
  </div>
</body></html>"""


DEMO_FEATURES = {
    "night_ratio": 0.72,
    "delivery_ratio": 0.65,
    "hoard_score": 0.58,
    "coupon_ratio": 0.81,
    "total_orders": 48,
    "points": 3200,
    "unused_coupons": 13,
}


def main():
    args = sys.argv[1:]
    if not args or args[0] == "demo":
        feats = DEMO_FEATURES
        out = "example_card.html"
    elif args[0] == "--raw":
        with open(args[1], "r", encoding="utf-8") as f:
            raw = json.load(f)
        feats = features_from_raw(raw)
        out = args[2] if len(args) > 2 else "example_card.html"
    else:
        with open(args[0], "r", encoding="utf-8") as f:
            feats = json.load(f)
        out = args[1] if len(args) > 1 else "example_card.html"

    result = analyze(feats)
    img_path = str(ROOT_ASSETS / f"{result['code']}.png")
    card = render_card(result, img_path=img_path)
    with open(out, "w", encoding="utf-8") as f:
        f.write(card)
    print(f"[MCTI] 类型判定：{result['code']} {result['emoji']} {result['name']}")
    print(f"[MCTI] 分享文案：{result['share']}")
    print(f"[MCTI] 卡片已生成：{out}")


ROOT_ASSETS = Path(__file__).parent / "assets"


if __name__ == "__main__":
    main()
