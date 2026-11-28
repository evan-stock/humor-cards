"""Gemini 폰 촬영본 손보기: '랬지'→'했지' 한 글자, 마지막 말풍선 뒤에 겹쳐 나온 가짜 입력창 지우기."""
import math, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter
im = np.array(Image.open("src/gemini_photo.png").convert("RGB")).astype(np.float32)
rng = np.random.default_rng(2)
NOTO = "/usr/share/fonts/opentype/noto/NotoSansCJK-Medium.ttc"

# 2) '랬' → '했'
gx0, gy0, gx1, gy1 = 559, 310, 582, 338
reg = im[gy0:gy1, gx0:gx1].copy(); L = reg.mean(2)
txt = cv2.dilate((L > 120).astype(np.uint8), np.ones((3, 3), np.uint8)) > 0
yy, xx = np.mgrid[0:gy1 - gy0, 0:gx1 - gx0].astype(np.float32)
A = np.stack([np.ones_like(xx), xx, yy], -1); bg = np.zeros_like(reg)
for c in range(3):
    coef, *_ = np.linalg.lstsq(A[~txt], reg[..., c][~txt], rcond=None); bg[..., c] = A @ coef
im[gy0:gy1, gx0:gx1] = np.where(txt[..., None], bg + rng.normal(0, 2, reg.shape), reg)
ink = np.percentile(reg[L > 150].reshape(-1, 3), 70, axis=0)
S = 8; f = ImageFont.truetype(NOTO, 22 * S, index=1)
lay = Image.new("L", (40 * S, 40 * S), 0); ImageDraw.Draw(lay).text((20 * S, 20 * S), "했", font=f, fill=255, anchor="mm")
lay = lay.rotate(9.5, resample=Image.BICUBIC).crop(lay.rotate(9.5).getbbox())
lay = lay.resize((19, 21), Image.LANCZOS).filter(ImageFilter.GaussianBlur(0.5))
a = np.clip(np.array(lay).astype(np.float32) / 255 * 1.2, 0, 1)[..., None]
px, py = 561, 314
r2 = im[py:py + 21, px:px + 19]
im[py:py + 21, px:px + 19] = r2 * (1 - a) + ink * a
out = Image.fromarray(np.clip(im, 0, 255).astype(np.uint8))
out.save("out/01_photo.png")
out.resize((1080, 1388), Image.LANCZOS).crop((0, 19, 1080, 1369)).save("out/01.jpg", quality=94)
out.crop((540, 290, 640, 360)).resize((500, 350), Image.LANCZOS).save("/tmp/f1.png")
out.crop((440, 580, 720, 700)).resize((560, 240)).save("/tmp/f2.png")
