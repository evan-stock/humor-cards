"""Gemini가 만든 '손에 든 폰' 사진의 깨진 말풍선 글씨를 원문으로 다시 써 넣는다.
입력: src/gemini_base.png  출력: out/01_photo.jpg
"""
import os
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.environ.get("FONT", "/home/claude/humor-cards/fonts/Pretendard-Medium.otf")
SS = 4  # 슈퍼샘플

base = np.array(Image.open(os.path.join(HERE, "src/gemini_base.png")).convert("RGB")).astype(np.float32)
H, W, _ = base.shape
# 흰 말풍선을 한 줄(26px) 줄인다: 아랫부분(+시간)을 위로 올리고 빈 곳은 아래 배경으로 채움
X0, X1, D = 272, 702, 26
strip = base[764:810, X0:X1].copy()
fill = base[810:836, X0:X1].copy()
base[738:784, X0:X1] = strip
base[784:810, X0:X1] = fill
rng = np.random.default_rng(7)

BUBBLES = [
    # 영역(글씨 지울 곳), 첫 줄 왼쪽 x, 줄 윗선 y들, 줄 글
    dict(box=(372, 436, 676, 572), x=377, tops=[441, 466, 492, 518, 544], lines=[
        "좀 이상하게 들릴 수 있지만",
        "내가 맨날 일 끝나면 찾아가고 배고프다",
        "하면 음식사서 문앞에 걸어두는거 그런",
        "게 싫은거야? 아니면 너무 빠르다고 생",
        "각하는거야?",
    ]),
    dict(box=(287, 641, 598, 751), x=292, tops=[646, 672, 698, 724], lines=[
        "아 아뇨! 전혀 안 이상해요 오빠! 다 설레",
        "는 행동인데 그냥 오빠가 찾아오는 게 싫",
        "고 오빠가 문 앞에 음식 걸어두는 게 싫고",
        "빠르진 않지만 그냥 오빠가 싫은 거예요!",
    ]),
]


def fit_size(text, width):
    for s in range(14, 30):
        f = ImageFont.truetype(FONT, s * SS)
        if f.getlength(text) / SS > width:
            return s - 1
    return 29


# 기준: 젬니 사진 첫 줄 실제 폭(292~589)
SIZE = fit_size("아 아뇨! 전혀 안이상해요 오빠! 다 설레", 589 - 292)
print("font size", SIZE)

out = base.copy()
gray = cv2.cvtColor(base.astype(np.uint8), cv2.COLOR_RGB2GRAY)

for b in BUBBLES:
    x0, y0, x1, y1 = b["box"]
    reg = base[y0:y1, x0:x1]
    g = gray[y0:y1, x0:x1]
    txt = cv2.dilate((g < 170).astype(np.uint8), np.ones((5, 5), np.uint8)) > 0
    # 글씨 아닌 픽셀로 2차 평면 맞추기(채널별)
    yy, xx = np.mgrid[0:y1 - y0, 0:x1 - x0].astype(np.float32)
    A = np.stack([np.ones_like(xx), xx, yy, xx * xx, yy * yy, xx * yy], -1)
    m = ~txt
    bg = np.zeros_like(reg)
    for c in range(3):
        coef, *_ = np.linalg.lstsq(A[m], reg[..., c][m], rcond=None)
        bg[..., c] = A @ coef
    resid = (reg - bg)[m]
    sd = float(np.std(resid))
    ink = np.median(reg[g < 90], axis=0) if (g < 90).any() else np.array([40, 40, 40])
    print("box", b["box"], "noise sd", round(sd, 2), "ink", ink.round())
    # 지울 곳: 글씨 영역만(가장자리 둥근 부분은 안 건드림) -> 부드럽게 섞음
    mask = cv2.GaussianBlur(txt.astype(np.float32), (0, 0), 1.5)
    mask = np.clip(mask * 1.5, 0, 1)[..., None]
    clean = bg + rng.normal(0, sd * 0.9, bg.shape).astype(np.float32)
    reg2 = reg * (1 - mask) + clean * mask

    # 글씨 그리기
    w, h = x1 - x0, y1 - y0
    lay = Image.new("L", (w * SS, h * SS), 0)
    d = ImageDraw.Draw(lay)
    f = ImageFont.truetype(FONT, SIZE * SS)
    asc = f.getbbox("한")[1]
    for top, line in zip(b["tops"], b["lines"]):
        if not line:
            continue
        d.text(((b["x"] - x0) * SS, (top - y0) * SS - asc + 1 * SS), line, font=f, fill=255)
    lay = lay.resize((w, h), Image.LANCZOS).filter(ImageFilter.GaussianBlur(0.55))
    a = (np.array(lay).astype(np.float32) / 255.0)[..., None]
    reg2 = reg2 * (1 - a) + ink[None, None, :] * a
    reg2 += rng.normal(0, sd * 0.5, reg2.shape).astype(np.float32) * a
    out[y0:y1, x0:x1] = reg2

# 젬니 별 워터마크 지우기(오른쪽 아래)
o8 = np.clip(out, 0, 255).astype(np.uint8)
wm = np.zeros((H, W), np.uint8)
cv2.circle(wm, (807, 1033), 30, 255, -1)
o8 = cv2.inpaint(o8, wm, 9, cv2.INPAINT_TELEA)
patch = o8[1000:1068, 774:842].astype(np.float32)
patch += rng.normal(0, 3, patch.shape)
o8[1000:1068, 774:842] = np.clip(patch, 0, 255).astype(np.uint8)

os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
Image.fromarray(o8).save(os.path.join(HERE, "out/01_photo.jpg"), quality=93)
Image.fromarray(o8).crop((240, 400, 720, 800)).resize((960, 800)).save("/tmp/fix_zoom.png")
print("ok")

# '오친 11:33' -> 11:31 라벨의 '오전' 픽셀을 옮겨 붙임
o = np.array(Image.open(os.path.join(HERE, "out/01_photo.jpg"))).astype(np.float32)
sx0, sy0, sx1, sy1 = 301, 569, 325, 586
dx, dy = 309, 172
src = o[sy0:sy1, sx0:sx1].copy()
dst = o[sy0 + dy:sy1 + dy, sx0 + dx:sx1 + dx]
gs = cv2.cvtColor(src.astype(np.uint8), cv2.COLOR_RGB2GRAY) > 140
gd = cv2.cvtColor(dst.astype(np.uint8), cv2.COLOR_RGB2GRAY) > 140
src += dst[gd].mean(0) - src[gs].mean(0)  # 배경색 맞춤
hh, ww = src.shape[:2]
fm = np.zeros((hh, ww), np.float32); fm[2:-2, 2:-2] = 1
fm = cv2.GaussianBlur(fm, (0, 0), 1.2)[..., None]
o[sy0 + dy:sy1 + dy, sx0 + dx:sx1 + dx] = dst * (1 - fm) + src * fm
Image.fromarray(np.clip(o, 0, 255).astype(np.uint8)).save(os.path.join(HERE, "out/01_photo.jpg"), quality=93)
Image.fromarray(np.clip(o, 0, 255).astype(np.uint8)).crop((560, 700, 720, 800)).resize((640, 400)).save("/tmp/t.png")

# 상단 '단톡방' 지우고 이름 자리를 빨간 낙서로 가림(말풍선 위 이름 가림과 같은 낙서 복사)
o = np.array(Image.open(os.path.join(HERE, "out/01_photo.jpg"))).astype(np.float32)
x0, y0, x1, y1 = 420, 176, 492, 210
reg = o[y0:y1, x0:x1]
g = reg.mean(2)
txt = cv2.dilate((g < 170).astype(np.uint8), np.ones((5, 5), np.uint8)) > 0
yy, xx = np.mgrid[0:y1 - y0, 0:x1 - x0].astype(np.float32)
A = np.stack([np.ones_like(xx), xx, yy, xx * yy], -1)
bg = np.zeros_like(reg)
for c in range(3):
    coef, *_ = np.linalg.lstsq(A[~txt], reg[..., c][~txt], rcond=None)
    bg[..., c] = A @ coef
sd = float(np.std((reg - bg)[~txt]))
m = cv2.GaussianBlur(txt.astype(np.float32), (0, 0), 1.5)[..., None].clip(0, 1)
o[y0:y1, x0:x1] = reg * (1 - m) + (bg + rng.normal(0, sd, bg.shape)) * m
sx0, sy0, sx1, sy1 = 262, 598, 344, 636
sc = o[sy0:sy1, sx0:sx1].copy()  # 원래 낙서(복사본 기준은 바뀌기 전 값)
src0 = np.array(Image.open(os.path.join(HERE, "out/01_photo.jpg"))).astype(np.float32)[sy0:sy1, sx0:sx1]
red = ((src0[..., 0] - src0[..., 1:].mean(2)) / 120.0).clip(0, 1)
red = cv2.GaussianBlur(red, (0, 0), 0.7)[..., None]
hh, ww = red.shape[:2]
cx, cy = 456, 193
tx, ty = cx - ww // 2, cy - hh // 2
dst = o[ty:ty + hh, tx:tx + ww]
o[ty:ty + hh, tx:tx + ww] = dst * (1 - red) + src0 * red
Image.fromarray(np.clip(o, 0, 255).astype(np.uint8)).save(os.path.join(HERE, "out/01_photo.jpg"), quality=93)
Image.fromarray(np.clip(o, 0, 255).astype(np.uint8)).crop((200, 100, 728, 300)).resize((1056, 400)).save("/tmp/h.png")
