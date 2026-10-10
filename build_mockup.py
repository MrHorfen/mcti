# -*- coding: utf-8 -*-
"""组装 MCTI 徽章卡片 mockup：裁水印 -> 压缩 -> base64 内联 -> 单文件 HTML"""
import base64
import io
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).parent
ASSETS = ROOT / "assets"

# 1. 裁掉底部 AI 水印 + 压缩
def prep(src: Path, crop_bottom: int, width: int) -> str:
    img = Image.open(src).convert("RGB")
    w, h = img.size
    img = img.crop((0, 0, w, h - crop_bottom))
    ratio = width / img.width
    img = img.resize((width, int(img.height * ratio)), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=82, optimize=True)
    return base64.b64encode(buf.getvalue()).decode()

char_b64 = prep(ASSETS / "3D_felt_fabric_texture_cute_ca_2026-10-10T07-51-21.png", 48, 720)
bg_b64 = prep(ASSETS / "abstract_soft_background_for_m_2026-10-10T07-52-02.png", 56, 760)

html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>MCTI 卡片 Mockup · 深夜囤券王</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{min-height:100vh;display:flex;justify-content:center;align-items:flex-start;
  background:#f2efea;
  font-family:"PingFang SC","Microsoft YaHei","Source Han Sans SC",sans-serif;
  padding:28px 12px 48px}
.stage{position:relative;width:420px;max-width:96vw}

/* 挂绳 + 夹子 */
.lanyard{position:absolute;top:-26px;left:50%;transform:translateX(-50%);z-index:5;
  display:flex;flex-direction:column;align-items:center}
.clip{width:34px;height:44px;position:relative}
.clip::before{content:"";position:absolute;inset:0;background:#c9c9c9;
  border-radius:8px 8px 10px 10px;
  clip-path:polygon(35% 0,65% 0,100% 55%,72% 100%,28% 100%,0 55%)}
.clip::after{content:"";position:absolute;left:7px;top:40px;width:20px;height:20px;
  border:6px solid #bdbdbd;border-radius:50%;border-bottom-color:transparent;border-left-color:transparent;
  transform:rotate(45deg)}
.strap{width:64px;height:56px;margin-top:-30px;border-radius:0 0 8px 8px;
  background:linear-gradient(180deg,#9a9a9a,#c2c2c2)}

/* 顶部引导语 */
.lead{margin:34px 0 6px;font-size:15px;color:#8a8478;letter-spacing:2px}

/* 大标题 */
.big-title{position:relative;display:inline-block;transform:rotate(-3deg);z-index:3}
.big-title .cn{font-size:52px;font-weight:900;letter-spacing:2px;color:#f5c518;
  -webkit-text-stroke:2px #fff;
  text-shadow:0 2px 0 #fff,0 4px 10px rgba(120,90,0,.35)}
.big-title .en{display:block;margin-top:2px;font-size:19px;font-weight:800;color:#fff;
  -webkit-text-stroke:1px #e2a400;text-shadow:0 2px 4px rgba(120,90,0,.4)}

/* 主卡 */
.badge{position:relative;margin-top:10px;border-radius:26px;padding:22px 20px 18px;
  background:linear-gradient(160deg,#e9c23b,#d9a415);
  box-shadow:0 14px 30px rgba(140,100,10,.28),inset 0 2px 0 rgba(255,255,255,.4);
  z-index:2}
.badge .desc{font-size:16.5px;line-height:1.55;font-weight:700;color:#4a3a05;margin-bottom:12px}
.badge .photo{position:relative;border-radius:18px;overflow:hidden;box-shadow:0 6px 16px rgba(90,60,0,.25)}
.badge .photo img{display:block;width:100%}
.bubble{position:absolute;right:-6px;top:44%;max-width:150px;background:#fff;
  border-radius:14px;padding:10px 12px;font-size:14px;font-weight:800;color:#3c3003;
  box-shadow:0 4px 10px rgba(90,60,0,.22)}
.bubble::before{content:"";position:absolute;left:-7px;top:18px;width:14px;height:14px;
  background:#fff;transform:rotate(45deg);border-radius:3px}

/* 底部 CP 区 */
.mate{margin-top:22px;display:flex;align-items:center;gap:14px}
.mate .ava{width:64px;height:64px;border-radius:50%;overflow:hidden;flex:none;
  border:3px solid #fff;box-shadow:0 4px 10px rgba(0,0,0,.12)}
.mate .ava img{display:block;width:100%;height:100%;object-fit:cover;object-position:50% 30%}
.mate .t1{font-size:14px;color:#8a8478;margin-bottom:2px}
.mate .t2{font-size:21px;font-weight:900;color:#3c3003}
.mate .t2 .q{font-size:14px;font-weight:700;color:#b08900;margin-left:8px}
.mate .t3{font-size:13px;color:#a09a8c;margin-top:3px}

/* 角标 */
.tag{position:absolute;top:8px;right:12px;background:rgba(255,255,255,.85);color:#a33e10;
  font-size:11px;font-weight:800;letter-spacing:1px;padding:4px 10px;border-radius:999px;z-index:6}
</style>
</head>
<body>
<div class="stage">
  <div class="lanyard"><div class="clip"></div><div class="strap"></div></div>
  <div class="tag">MCTI · 麦门人格</div>

  <div class="lead">你的麦门人格：</div>
  <div class="big-title"><span class="cn">深夜囤券王</span><span class="en">Night Coupon Hoarder</span></div>

  <div class="badge">
    <p class="desc">凌晨十二点还在翻券包的人，但怪了，第二天总能精准用掉那张最小额的。</p>
    <div class="photo">
      <img src="data:image/jpeg;base64,__CHAR__" alt="深夜囤券王">
      <div class="bubble">囤的是券<br>不是孤独…</div>
    </div>
  </div>

  <div class="mate">
    <div class="ava"><img src="data:image/jpeg;base64,__CHAR__" alt=""></div>
    <div>
      <div class="t1">与你最搭：</div>
      <div class="t2">#元气晨型人 <span class="q">"券要趁热，人要趁早！"</span></div>
      <div class="t3">太阳一升起就用掉早餐券的行动派</div>
    </div>
  </div>
</div>
</body>
</html>
"""

html = html.replace("__CHAR__", char_b64)
# 暂未启用背景板（角色图自带金黄底已足够），背景板留作海报/封面用
out = ROOT / "mockup_card.html"
out.write_text(html, encoding="utf-8")
print("written:", out, f"{out.stat().st_size/1024:.0f} KB")
