"""고해상도 합성: Gemini 사진을 3배로 키운 뒤 문자 화면 렌더를 원해상도 그대로 원근 변환해 넣는다(글씨 선명).
그다음 대화 부분만 4:5로 크게 자른다(참고: wamoyaaa 확대 수준)."""
import numpy as np, cv2
from PIL import Image, ImageDraw
from composite import Hm  # 같은 기준점으로 구한 변환(원본 사진 좌표)

S = 3
R = np.array(Image.open("out/sms_screen.png").convert("RGB")).astype(np.float32)
Gs = Image.open("src/gemini_sms_phone.png").convert("RGB")
G = np.array(Gs.resize((Gs.width * S, Gs.height * S), Image.LANCZOS)).astype(np.float32)
h, w = G.shape[:2]
H3 = np.diag([S, S, 1]).astype(np.float64) @ Hm
warp = cv2.warpPerspective(R, H3, (w, h), flags=cv2.INTER_LINEAR)
m = Image.new("L", (R.shape[1], R.shape[0]), 0)
ImageDraw.Draw(m).rounded_rectangle((6, 6, R.shape[1] - 7, R.shape[0] - 7), 165, fill=255)
sm = cv2.warpPerspective(np.array(m), H3, (w, h)).astype(np.float32) / 255
sm = cv2.GaussianBlur(sm, (0, 0), 4)[..., None]
rng = np.random.default_rng(4)
warp = cv2.GaussianBlur(warp, (0, 0), 1.1) * 0.93
# 화면 픽셀 결(아주 옅은 모아레) + 노이즈
yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
moire = (np.sin((xx * 0.9 + yy * 0.35) * 0.55) * np.sin((yy * 0.9 - xx * 0.3) * 0.5)) * 4
warp += moire[..., None] * (warp.mean(2, keepdims=True) / 255 + 0.15)
warp += rng.normal(0, 4, warp.shape)
# 먼지·반사
dust = np.zeros((h, w), np.float32)
for _ in range(70):
    cx, cy = rng.integers(240 * S, 620 * S), rng.integers(200 * S, 990 * S)
    cv2.circle(dust, (int(cx), int(cy)), int(rng.integers(2, 6)), float(rng.uniform(20, 60)), -1)
dust = cv2.GaussianBlur(dust, (0, 0), 1.5)
glare = np.zeros((h, w), np.float32)
cv2.ellipse(glare, (500 * S, 420 * S), (320 * S, 55 * S), -38, 0, 360, 30, -1)
cv2.ellipse(glare, (330 * S, 760 * S), (200 * S, 30 * S), -38, 0, 360, 14, -1)
dust += cv2.GaussianBlur(glare, (0, 0), 40 * S)
out = G * (1 - sm) + (warp + dust[..., None]) * sm
out = np.clip(out, 0, 255).astype(np.uint8)
# 대화 부분 4:5 크게 + 살짝 기울임(손으로 든 느낌)
big = Image.fromarray(out)
cx, cy = 432 * S, 590 * S
big = big.rotate(-2.5, resample=Image.BICUBIC, center=(cx, cy))
cw = 470 * S; ch = int(cw * 1.25)
x0 = cx - cw // 2; y0 = 318 * S
crop = big.crop((x0, y0, x0 + cw, y0 + ch)).resize((1080, 1350), Image.LANCZOS)
crop.save("out/01_phone_zoom.jpg", quality=94)
print("bottom(orig)", (y0 + ch) / S)
