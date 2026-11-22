"""Gemini 손폰 사진(src/gemini_sms_phone.png)의 깨진 화면 글씨를 → 내 문자 화면 렌더(out/sms_screen.png)로 바꿔 끼움.
초록 말풍선 3개 모서리 + 프로필·홈바 위치로 원근 변환을 맞추고, 흐림·밝기·노이즈·먼지를 사진에 맞춘다."""
import numpy as np, cv2
from PIL import Image

def boxes(im):
    m = ((im[..., 1] > 140) & (im[..., 1] - im[..., 0] > 60) & (im[..., 1] - im[..., 2] > 40)).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    n, l, st, c = cv2.connectedComponentsWithStats(m)
    return sorted([tuple(s[:4]) for s in st[1:] if s[4] > 200], key=lambda b: b[1])

R = np.array(Image.open("out/sms_screen.png").convert("RGB")).astype(np.float32)
G = np.array(Image.open("src/gemini_sms_phone.png").convert("RGB")).astype(np.float32)
src, dst = [], []
for (x, y, w, h), (X, Y, Wd, Hd) in zip(boxes(R.astype(int)), boxes(G.astype(int))):
    src += [(x, y), (x + w, y), (x, y + h), (x + w, y + h)]
    dst += [(X, Y), (X + Wd, Y), (X, Y + Hd), (X + Wd, Y + Hd)]
src += [(603, 275), (603, 2588), (185, 98), (201, 251)]
dst += [(432, 268), (421, 990), (308, 217), (311, 264)]
Hm, inl = cv2.findHomography(np.float32(src), np.float32(dst), cv2.RANSAC, 6)
print("inliers", int(inl.sum()), "/", len(src))
h, w = G.shape[:2]
warp = cv2.warpPerspective(R, Hm, (w, h), flags=cv2.INTER_AREA)
# 화면 영역 마스크(렌더 전체 사각형을 둥근 모서리로)
from PIL import ImageDraw
_m = Image.new("L", (R.shape[1], R.shape[0]), 0)
ImageDraw.Draw(_m).rounded_rectangle((6, 6, R.shape[1] - 7, R.shape[0] - 7), 165, fill=255)
rm = np.array(_m)
sm = cv2.warpPerspective(rm, Hm, (w, h)).astype(np.float32) / 255
sm = cv2.GaussianBlur(sm, (0, 0), 2.0)[..., None]
np.save("/tmp/H.npy", Hm)
# 사진처럼: 살짝 흐림 + 밝기 맞춤 + 노이즈
warp = cv2.GaussianBlur(warp, (0, 0), 0.9)
gm = (sm[..., 0] > .9)
bright = (G[gm].reshape(-1, 3).max(1) > 120)
ratio = np.median(G[gm][bright], 0) / max(1, 1)
# 초록 말풍선 색 기준으로 밝기·색 맞춤
Gg = G[boxes(G.astype(int))[0][1] + 10, boxes(G.astype(int))[0][0] + 10]
Rg = np.array([52, 199, 89], np.float32)
gain = Gg / Rg
warp = warp * 0.93
warp += np.random.default_rng(2).normal(0, 3.5, warp.shape)
# 원래 사진의 먼지·반사(밝은 점) 조금 살리기: 원본 화면의 고주파 성분 더함
hp = G - cv2.GaussianBlur(G, (0, 0), 3)
rng = np.random.default_rng(9)
dust = np.zeros((h, w), np.float32)  # 액정 먼지 점 몇 개(새로 뿌림)
for _ in range(45):
    cx, cy = rng.integers(240, 620), rng.integers(200, 990)
    cv2.circle(dust, (int(cx), int(cy)), int(rng.integers(1, 3)), float(rng.uniform(25, 70)), -1)
dust = cv2.GaussianBlur(dust, (0, 0), 0.8)[..., None]
glare = np.zeros((h, w), np.float32)
cv2.ellipse(glare, (520, 330), (260, 60), -35, 0, 360, 18, -1)
dust += cv2.GaussianBlur(glare, (0, 0), 40)[..., None]
out = G * (1 - sm) + (warp + dust) * sm
out = np.clip(out, 0, 255).astype(np.uint8)
Image.fromarray(out).save("out/01_phone.jpg", quality=93)
Image.fromarray(out).crop((230, 180, 640, 1010)).resize((820, 1660)).save("/tmp/scr.png")
print("gain", gain.round(2))
