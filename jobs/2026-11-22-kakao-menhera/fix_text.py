"""Gemini 손폰 사진(인스타 DM 하트 테마)의 깨진 말풍선 글씨를 펨코 원문으로 다시 쓴다.
원문: https://www.fmkorea.com/10487124543 (진짜 멘헤라 여친의 카톡, 조회 118만)
"""
import os
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = "/home/claude/humor-cards/fonts/Pretendard-Medium.otf"
SS = 4
rng = np.random.default_rng(3)
base = np.array(Image.open(os.path.join(HERE, "src/gemini_base.png")).convert("RGB")).astype(np.float32)

def fit(text, width):
    for s in range(14, 30):
        if ImageFont.truetype(FONT, s * SS).getlength(text) / SS > width:
            return s - 1
SIZE = fit("잇다고해서 오빠 친구들까지 건들 생각은", 636 - 314)
print("size", SIZE)

B = [
    dict(box=(302, 386, 650, 483), x=314, patches=[(470, 455, 628, 483)], tops=[396, 423, 450],
         lines=["우웅..근데 내가 아무리 집착이 좀", "잇다고해서 오빠 친구들까지 건들 생각은", "없서요..."]),
    dict(box=(302, 492, 625, 562), x=313, patches=[(540, 492, 625, 500)], tops=[508, 535],
         lines=["나 진짜 오빠 많이 사랑하고 맨날 같이", "붙어잇고싶지만.. 가두지는않을거야"]),
    dict(box=(302, 752, 478, 795), x=312, patches=[(330, 780, 458, 795)], tops=[759],
         lines=["나 죽는거 보여줄게"], mosaic="죽"),
]
# 첫·둘째 말풍선 사이 틈에 번진 얼룩: 같은 틈의 왼쪽 부분을 옮겨 붙임
base[483:492, 470:600] = base[483:492, 340:470]
out = base.copy()
for b in B:
    x0, y0, x1, y1 = b["box"]
    reg = base[y0:y1, x0:x1]
    g = reg.mean(2)
    txt = cv2.dilate((g > 115).astype(np.uint8), np.ones((5, 5), np.uint8)) > 0
    for px0, py0, px1, py1 in b.get("patches", []):
        txt[py0 - y0:py1 - y0, px0 - x0:px1 - x0] = True
    yy, xx = np.mgrid[0:y1 - y0, 0:x1 - x0].astype(np.float32)
    A = np.stack([np.ones_like(xx), xx, yy, xx * xx, yy * yy, xx * yy], -1)
    bg = np.zeros_like(reg)
    for c in range(3):
        coef, *_ = np.linalg.lstsq(A[~txt], reg[..., c][~txt], rcond=None)
        bg[..., c] = A @ coef
    sd = float(np.std((reg - bg)[~txt]))
    ink = np.percentile(reg[g > 150].reshape(-1, 3), 90, axis=0)
    print(b["box"], "sd", round(sd, 2), "ink", ink.round())
    m = cv2.GaussianBlur(txt.astype(np.float32), (0, 0), 1.5).clip(0, 1)[..., None]
    reg2 = reg * (1 - m) + (bg + rng.normal(0, sd, bg.shape)) * m
    w, h = x1 - x0, y1 - y0
    lay = Image.new("L", (w * SS, h * SS), 0)
    d = ImageDraw.Draw(lay)
    f = ImageFont.truetype(FONT, SIZE * SS)
    asc = f.getbbox("한")[1]
    for top, line in zip(b["tops"], b["lines"]):
        d.text(((b["x"] - x0) * SS, (top - y0) * SS - asc), line, font=f, fill=255)
    lay = lay.resize((w, h), Image.LANCZOS).filter(ImageFilter.GaussianBlur(0.6))
    a = np.array(lay).astype(np.float32) / 255
    if b.get("mosaic"):  # 원본처럼 한 글자 모자이크
        line = b["lines"][0]
        pre = f.getlength(line[:line.index(b["mosaic"])]) / SS
        cw = f.getlength(b["mosaic"]) / SS
        mx0 = int(b["x"] - x0 + pre) - 1; mx1 = int(mx0 + cw) + 3
        sub = a[:, mx0:mx1]
        sm = cv2.resize(sub, (max(1, (mx1 - mx0) // 5), max(1, h // 5)), interpolation=cv2.INTER_AREA)
        sub = cv2.resize(sm, (mx1 - mx0, h), interpolation=cv2.INTER_NEAREST)
        a[:, mx0:mx1] = cv2.GaussianBlur(sub, (0, 0), 0.8) * 0.85
    a = a[..., None]
    reg2 = reg2 * (1 - a) + ink[None, None] * a
    out[y0:y1, x0:x1] = reg2
o8 = np.clip(out, 0, 255).astype(np.uint8)
Image.fromarray(o8).save(os.path.join(HERE, "out/01_photo.jpg"), quality=93)
Image.fromarray(o8).crop((280, 370, 670, 800)).resize((780, 860)).save("/tmp/m2.png")
