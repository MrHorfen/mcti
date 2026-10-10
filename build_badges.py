# -*- coding: utf-8 -*-
"""生成 MCTI 工牌徽章分享卡
- badge_card.html : 单人格、base64 内联、可单文件截图分享（默认深夜囤券王 NHKQ）
- all_badges.html : 16 人格全集展示页（引用 assets/CODE.png，轻量预览用）
"""
import base64
import io
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).parent
ASSETS = ROOT / "assets"

# 16 人格文案：名字只提炼「最突出的反差」，不再以夜/早开头堆叠维度词
TYPES = {
    "NHKQ": dict(name="外卖券管家", en="Coupon Butler", bubble="券不过夜<br>单不过点。", mate="早八攒券僧", mate_q="麦咖啡配囤券，绝配。", mate_desc="同是攒券党，昼夜互补"),
    "NHKX": dict(name="囤券咸鱼", en="Chill Hoarder", bubble="囤着<br>不一定用。", mate="早八囤券叔", mate_q="早八的券，归你囤。", mate_desc="佛系囤券搭子"),
    "NHSQ": dict(name="满减狙击手", en="Deal Sniper", bubble="差一块<br>也能凑。", mate="早餐满减怪", mate_q="早餐的满，我来凑。", mate_desc="凑单狂魔联盟"),
    "NHSX": dict(name="外卖散财喵", en="Midnight Spender", bubble="深夜不加价<br>不舒服。", mate="早八散财鸟", mate_q="早饭我请，别比价。", mate_desc="散财猫鸟组"),
    "NWHKQ": dict(name="门店守夜人", en="Store Nightwatch", bubble="打烊前<br>我必到。", mate="晨间门店僧", mate_q="开门第一单，归我。", mate_desc="门店早晚 CP"),
    "NWHKX": dict(name="夜游囤券鬼", en="Night Stroller", bubble="散步顺手<br>囤张券。", mate="晨店随心人", mate_q="早上看啥点啥。", mate_desc="随心昼夜组"),
    "NWSQ": dict(name="堂食满减王", en="Dine-in Deal King", bubble="堂食<br>也要满。", mate="门店满减王", mate_q="门店满减，一家亲。", mate_desc="满减双王"),
    "NWSX": dict(name="门店豪横猫", en="Store Big-spender", bubble="门店里<br>点最贵的。", mate="门店自助王", mate_q="门店当自助，安排。", mate_desc="豪横门店组"),
    "DHKQ": dict(name="早八攒券僧", en="Morning Coupon Monk", bubble="麦咖啡<br>续命。", mate="外卖券管家", mate_q="深夜的券，归你管。", mate_desc="攒券昼夜互补"),
    "DHKX": dict(name="早八囤券叔", en="Early Hoard Uncle", bubble="早餐券<br>先囤为敬。", mate="囤券咸鱼", mate_q="深夜的券，你囤着。", mate_desc="佛系囤券搭子"),
    "DHSQ": dict(name="早餐满减怪", en="Breakfast Deal Freak", bubble="早餐的满<br>我来凑。", mate="满减狙击手", mate_q="深夜的满，我狙。", mate_desc="凑单狂魔联盟"),
    "DHSX": dict(name="早八散财鸟", en="Early Spender Bird", bubble="早饭<br>不比价。", mate="外卖散财喵", mate_q="深夜的散财，你上。", mate_desc="散财猫鸟组"),
    "DWHKQ": dict(name="晨间门店僧", en="Morning Store Monk", bubble="开门第一单<br>我包了。", mate="门店守夜人", mate_q="打烊前的单，归我。", mate_desc="门店早晚 CP"),
    "DWKX": dict(name="晨店随心人", en="Morning Free Soul", bubble="看啥点啥<br>不纠结。", mate="夜游囤券鬼", mate_q="夜里散步顺手囤。", mate_desc="随心昼夜组"),
    "DWSQ": dict(name="门店满减王", en="Store Deal King", bubble="门店满减<br>一家亲。", mate="堂食满减王", mate_q="堂食满减，我来。", mate_desc="满减双王"),
    "DWSX": dict(name="门店自助王", en="Store Buffet King", bubble="门店<br>当自助。", mate="门店豪横猫", mate_q="深夜点最贵，你先。", mate_desc="豪横门店组"),
}

DESC = {
    "NHKQ": "深夜的外卖从不错过任何一张券，你的快乐是「券到手 + 门铃响」双响炮。",
    "NHKX": "券在卡包里睡大觉，你懒得凑也懒得用，囤本身就有安全感。",
    "NHSQ": "再晚也要把券用满，精致懒人晚期，省下的钱都花在刀刃上。",
    "NHSX": "深夜情绪价值拉满，下单从不看单价，快乐是唯一 KPI。",
    "NWHKQ": "夜宵必须到店才有灵魂，路过柜台顺手把券囤成小金库。",
    "NWHKX": "没有计划就是最好的计划，散步到店顺手囤券，随缘即正义。",
    "NWSQ": "夜里到店堂食，券一张不落全用掉，主打一个干净利落。",
    "NWSX": "夜猫子本猫，到店就点最贵的那几个，深夜的奢侈属于你。",
    "DHKQ": "一天从麦咖啡和囤好的券开始，规律得像打卡机。",
    "DHKX": "早餐靠外送续命，点单全凭肌肉记忆，券随缘。",
    "DHSQ": "早餐也要把券用出仪式感，省下的钱转身买了杯咖啡。",
    "DHSX": "早起的人有权任性，早餐不比价，快乐第一位。",
    "DWHKQ": "清晨溜达去门店，先囤券再点单，仪式感拉满。",
    "DWKX": "晨光里的随心派，走到柜台看今天想宠幸哪一款。",
    "DWSQ": "到店吃早餐也要把券算到最后一分，精致的懒人天花板。",
    "DWSX": "清晨到店豪横点单，吃饱喝足才是元气满格的打开方式。",
}


def prep(src: Path, crop_bottom: int, width: int = 760) -> str:
    img = Image.open(src).convert("RGB")
    w, h = img.size
    img = img.crop((0, 0, w, h - crop_bottom))
    ratio = width / img.width
    img = img.resize((width, int(img.height * ratio)), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=80, optimize=True)
    return base64.b64encode(buf.getvalue()).decode()


CARD_CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{min-height:100vh;display:flex;justify-content:center;align-items:flex-start;
  background:#f2efea;
  font-family:"PingFang SC","Microsoft YaHei","Source Han Sans SC",sans-serif;
  padding:28px 12px 56px}
.stage{position:relative;width:420px;max-width:96vw;padding-top:26px}
.lead{display:none}
.big-title{position:relative;display:inline-block;transform:rotate(-3deg);z-index:3;left:50%;margin-left:-130px}
.big-title .cn{font-size:50px;font-weight:900;letter-spacing:2px;color:#f5c518;
  -webkit-text-stroke:2px #fff;text-shadow:0 2px 0 #fff,0 4px 10px rgba(120,90,0,.35)}
.big-title .en{display:block;margin-top:2px;font-size:18px;font-weight:800;color:#fff;
  -webkit-text-stroke:1px #e2a400;text-shadow:0 2px 4px rgba(120,90,0,.4)}
.badge{position:relative;margin-top:10px;border-radius:26px;padding:22px 20px 18px;
  background:linear-gradient(160deg,#e9c23b,#d9a415);
  box-shadow:0 14px 30px rgba(140,100,10,.28),inset 0 2px 0 rgba(255,255,255,.4);z-index:2}
.badge .desc{font-size:16px;line-height:1.55;font-weight:700;color:#4a3a05;margin-bottom:12px}
.badge .photo{position:relative;border-radius:18px;overflow:hidden;box-shadow:0 6px 16px rgba(90,60,0,.25)}
.badge .photo img{display:block;width:100%}
.bubble{position:absolute;right:-6px;top:42%;max-width:150px;background:#fff;
  border-radius:14px;padding:10px 12px;font-size:14px;font-weight:800;color:#3c3003;
  box-shadow:0 4px 10px rgba(90,60,0,.22)}
.bubble::before{content:"";position:absolute;left:-7px;top:18px;width:14px;height:14px;
  background:#fff;transform:rotate(45deg);border-radius:3px}
.mate{margin-top:22px;display:flex;align-items:center;gap:14px}
.mate .ava{width:64px;height:64px;border-radius:50%;overflow:hidden;flex:none;
  border:3px solid #fff;box-shadow:0 4px 10px rgba(0,0,0,.12);background:#fff}
.mate .ava img{display:block;width:100%;height:100%;object-fit:cover;object-position:50% 28%}
.mate .t1{font-size:14px;color:#8a8478;margin-bottom:2px}
.mate .t2{font-size:21px;font-weight:900;color:#3c3003}
.mate .t2 .q{font-size:13px;font-weight:700;color:#b08900;margin-left:8px}
.mate .t3{font-size:13px;color:#a09a8c;margin-top:3px}
.tag{position:absolute;top:8px;right:12px;background:rgba(255,255,255,.85);color:#a33e10;
  font-size:11px;font-weight:800;letter-spacing:1px;padding:4px 10px;border-radius:999px;z-index:6}
"""

FOOT = '.foot{margin-top:18px;text-align:center;font-size:11px;color:#b3ad9f}'


def one_badge(code: str, char_b64: str = None, ava_b64: str = None, online: bool = False) -> str:
    t = TYPES[code]
    desc = DESC[code]
    if online:
        char_src = f"assets/{code}.png"
        ava_src = f"assets/{code}.png"
    else:
        char_src = f"data:image/jpeg;base64,{char_b64}"
        ava_src = f"data:image/jpeg;base64,{ava_b64}"
    return f"""
  <div class="stage">
    <div class="tag">MCTI</div>
    <div class="lead"></div>
    <div class="big-title"><span class="cn">{t['name']}</span><span class="en">{t['en']}</span></div>
    <div class="badge">
      <p class="desc">{desc}</p>
      <div class="photo">
        <img src="{char_src}" alt="{t['name']}">
        <div class="bubble">{t['bubble']}</div>
      </div>
    </div>
    <div class="mate">
      <div class="ava"><img src="{ava_src}" alt=""></div>
      <div>
        <div class="t1">与你最搭：</div>
        <div class="t2">#{t['mate']} <span class="q">"{t['mate_q']}"</span></div>
        <div class="t3">{t['mate_desc']}</div>
      </div>
    </div>
    <div class="foot">MCTI · McDonald's Consumption Type Indicator · 仅供娱乐</div>
  </div>"""


# ---- 1) 单文件可分享卡（默认深夜囤券王） ----
focus = "NHKQ"
char_b64 = prep(ASSETS / f"{focus}.png", 70, 760)
ava_b64 = prep(ASSETS / f"{focus}.png", 70, 200)
single = f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>MCTI 分享卡 · {TYPES[focus]['name']}</title>
<style>{CARD_CSS}{FOOT}</style></head>
<body>{one_badge(focus, char_b64, ava_b64)}</body></html>"""
(ROOT / "badge_card.html").write_text(single, encoding="utf-8")
print("written badge_card.html", f"{(ROOT/'badge_card.html').stat().st_size/1024:.0f} KB")

# ---- 2) 16 人格全集展示页（引用 assets，轻量） ----
all_html = f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>MCTI · 16 人格全集</title>
<style>{CARD_CSS}{FOOT}
body{{background:#f2efea;flex-direction:column;align-items:center}}
.wrap{{display:flex;flex-wrap:wrap;gap:30px 22px;justify-content:center;max-width:1400px}}
.wrap .stage{{margin-top:0}}
.page-h{{text-align:center;margin:10px 0 6px;color:#a33e10;font-weight:900;font-size:24px}}
.page-s{{text-align:center;color:#8a8478;font-size:13px;margin-bottom:6px}}
</style></head>
<body>
<div class="page-h">MCTI · 16 种人格</div>
<div class="page-s">由你的麦当劳消费习惯生成 · 仅供娱乐 · 原创胖橘猫 IP</div>
<div class="wrap">"""
order = ["NHKQ","NHKX","NHSQ","NHSX","NWHKQ","NWHKX","NWSQ","NWSX",
         "DHKQ","DHKX","DHSQ","DHSX","DWHKQ","DWKX","DWSQ","DWSX"]
for c in order:
    all_html += f"<div>{one_badge(c, online=True)}</div>"
all_html += "</div></body></html>"
(ROOT / "all_badges.html").write_text(all_html, encoding="utf-8")
print("written all_badges.html", f"{(ROOT/'all_badges.html').stat().st_size/1024:.0f} KB")
