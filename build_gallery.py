# -*- coding: utf-8 -*-
"""生成 MCTI 16 人格橘猫画廊（引用 assets/CODE.png）"""
ROOT = __import__("pathlib").Path(__file__).parent

# code -> (emoji, 名称, 标语)
TYPES = {
    "NHKQ": ("🌙", "深夜囤券王", "凌晨两点，券比觉多。"),
    "NHKX": ("🛌", "夜送随心霸", "深夜想啥点啥，券？随缘。"),
    "NHSQ": ("💸", "夜送挥霍猎", "深夜也要用券，但绝不将就。"),
    "NHSX": ("🔥", "深夜撒钱怪", "凌晨的麦当劳是我的深夜食堂。"),
    "NWHKQ": ("🏪", "夜店囤券侠", "半夜溜去门店，顺手囤一波券。"),
    "NWHKX": ("🚶", "夜游随心客", "夜里散步到店，看啥吃啥。"),
    "NWSQ": ("🎯", "夜店挥霍猎", "晚上到店，券用满，爽就完事。"),
    "NWSX": ("😈", "夜猫挥霍怪", "深夜到店挥霍，快乐至上。"),
    "DHKQ": ("☕", "晨送囤券翁", "早上靠麦咖啡+囤券开启一天。"),
    "DHKX": ("📦", "晨送随心叔", "早餐送到公司，随便点点。"),
    "DHSQ": ("🎟️", "晨送挥霍猎", "早餐也要用券，精明但不抠。"),
    "DHSX": ("💰", "晨间撒钱党", "早饭不差钱，随手就点。"),
    "DWHKQ": ("🥯", "早餐囤券侠", "到店吃早餐，券先囤为敬。"),
    "DWKX": ("🌞", "晨店随心人", "早上溜达去门店，随缘点。"),
    "DWSQ": ("🍔", "晨店挥霍猎", "门店早餐用券拉满，精致懒人。"),
    "DWSX": ("⚡", "元气挥霍怪", "早上到店挥霍，元气满满出门。"),
}

cards = ""
for code, (emoji, name, tag) in TYPES.items():
    cards += f"""
    <div class="tile">
      <div class="pic"><img src="assets/{code}.png" alt="{code}"></div>
      <div class="code">{emoji} {code}</div>
      <div class="nm">{name}</div>
      <div class="tg">{tag}</div>
    </div>"""

html = f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>MCTI · 16 人格橘猫全家福</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:linear-gradient(135deg,#fff6e0,#ffe9c2);font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif;padding:26px 14px 50px;color:#3a2a06}}
h1{{text-align:center;font-size:26px;font-weight:900;color:#da291c;letter-spacing:2px;margin-bottom:4px}}
.sub{{text-align:center;color:#a8741a;font-size:13px;margin-bottom:22px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:16px;max-width:1000px;margin:0 auto}}
.tile{{background:#fff;border-radius:18px;overflow:hidden;box-shadow:0 8px 18px rgba(150,100,10,.16);border:2px solid #ffcf5a;display:flex;flex-direction:column}}
.pic{{background:#fff8ec;aspect-ratio:1/1;display:flex;align-items:center;justify-content:center;padding:10px}}
.pic img{{width:100%;height:100%;object-fit:contain}}
.code{{background:#da291c;color:#ffc72c;font-weight:900;font-size:15px;text-align:center;padding:6px}}
.nm{{font-size:18px;font-weight:900;color:#3a2a06;text-align:center;padding:8px 6px 2px}}
.tg{{font-size:12.5px;color:#8a6a2a;text-align:center;padding:0 10px 14px;line-height:1.5}}
.foot{{text-align:center;color:#b08a3a;font-size:12px;margin-top:26px}}
</style></head>
<body>
<h1>🐱 MCTI · 16 人格橘猫全家福</h1>
<div class="sub">同一只胖橘猫的 16 种「更圆·更贱·更躺平」状态 · 原创 IP，无官方吉祥物/无文字</div>
<div class="grid">{cards}</div>
<div class="foot">图片命名中 NHKX / NWHKX / DWSX / DHKQ / DWSQ 为同秒生成碰撞后的经验映射，请肉眼校准；如某张姿态与人格名不符，告诉我即可一键换位。</div>
</body></html>"""

out = ROOT / "gallery.html"
out.write_text(html, encoding="utf-8")
print("written", out, f"{out.stat().st_size/1024:.0f} KB")
