"""ChatGPT 손폰 사진의 오타 '많은증이야' → '많은중이야': '증'을 지우고 같은 크기·기울기로 '중'을 새로 씀."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
im = np.array(Image.open("src/chatgpt_photo.png").convert("RGB")).astype(np.float32)
X0, Y0, X1, Y1 = 608, 1150, 635, 1180
# 배경: 위/아래 줄의 바탕색으로 세로 보간
top = np.median(im[1144:1149, X0:X1], 0); bot = np.median(im[1181:1186, X0:X1], 0)
t = np.linspace(0, 1, Y1 - Y0)[:, None, None]
im[Y0:Y1, X0:X1] = top[None] * (1 - t) + bot[None] * t
# '중' 렌더(8배) → 회전 → 축소
S = 8
f = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", 30 * S, index=1)
lay = Image.new("L", (60 * S, 60 * S), 0)
ImageDraw.Draw(lay).text((30 * S, 30 * S), "중", font=f, fill=255, anchor="mm")
lay = lay.rotate(-4.7, resample=Image.BICUBIC)
bb = lay.getbbox()
lay = lay.crop(bb)
# 원래 '증' 크기(가로 22, 세로 23)에 맞춤
lay = lay.resize((22, 24), Image.LANCZOS).filter(ImageFilter.GaussianBlur(0.45))
a = (np.array(lay).astype(np.float32) / 255)[..., None]
a = np.clip(a * 1.25, 0, 1)
ink = np.array([60, 48, 76], np.float32)
px, py = 611, 1152
reg = im[py:py + 24, px:px + 22]
im[py:py + 24, px:px + 22] = reg * (1 - a) + ink * a
im[Y0:Y1, X0:X1] += np.random.default_rng(1).normal(0, 2.5, im[Y0:Y1, X0:X1].shape)
out = Image.fromarray(np.clip(im, 0, 255).astype(np.uint8))
out.save("out/01_chatgpt_fixed.png")
a_ = Image.open("src/chatgpt_photo.png").convert("RGB").crop((560, 1135, 700, 1190)).resize((840, 330), Image.LANCZOS)
b_ = out.crop((560, 1135, 700, 1190)).resize((840, 330), Image.LANCZOS)
o = Image.new("RGB", (840, 670), "white"); o.paste(a_, (0, 0)); o.paste(b_, (0, 340)); o.save("/tmp/cmp.png")
