"""01_real.jpg를 조금 멀리서 찍은 것처럼: 둥근 화면+검은 폰 몸체+어두운 방(무료 합성)."""
import numpy as np, cv2
from PIL import Image, ImageDraw
rng = np.random.default_rng(5)
scr = np.array(Image.open("out/01_real.jpg").convert("RGB")).astype(np.float32)
sh, sw = scr.shape[:2]
B, R = 40, 95                     # 몸체 두께, 화면 모서리 반지름
PW, PH = sw + 2 * B, sh + 2 * B + 260   # 아래로 폰이 이어지게(프레임 밖으로 잘림)
def rr(w, h, r, off=(0, 0), size=None):
    im = Image.new("L", size or (w, h), 0)
    ImageDraw.Draw(im).rounded_rectangle((off[0], off[1], off[0] + w - 1, off[1] + h - 1), r, fill=255)
    return np.array(im).astype(np.float32) / 255
phone = np.zeros((PH, PW, 3), np.float32) + np.array([16, 14, 18])
body_a = rr(PW, PH, R + B)
scr_a = rr(sw, sh + 260, R, (B, B), (PW, PH))
canvas = np.zeros((PH, PW, 3), np.float32)
canvas[B:B + sh, B:B + sw] = scr
canvas[B + sh:, B:B + sw] = scr[-1:, :, :] * 0.9   # 화면 아래쪽 이어짐(어두운 배경)
canvas[B + sh:] = cv2.GaussianBlur(canvas[B + sh:], (0, 0), 8)
phone = phone * (1 - scr_a[..., None]) + canvas * scr_a[..., None]
# 몸체 가장자리 하이라이트
ring = cv2.dilate((body_a > .5).astype(np.uint8), np.ones((3, 3))) - cv2.erode((body_a > .5).astype(np.uint8), np.ones((7, 7)))
phone += cv2.GaussianBlur(ring.astype(np.float32), (0, 0), 1.5)[..., None] * 60
W, H = 1080, 1350
bg = cv2.GaussianBlur(cv2.resize(scr, (W, H)), (0, 0), 70) * 0.15
bg += np.linspace(4, 22, H)[:, None, None] * np.array([1, .85, .75])
src = np.float32([[0, 0], [PW, 0], [PW, PH], [0, PH]])
sc = 0.86
w2, h2 = PW * sc, PH * sc
x0, y0 = 95, 70
dst = np.float32([[x0 + 30, y0], [x0 + w2 + 10, y0 + 40], [x0 + w2 - 40, y0 + h2 + 20], [x0 - 20, y0 + h2 - 10]])
M = cv2.getPerspectiveTransform(src, dst)
wp = cv2.warpPerspective(phone, M, (W, H))
wa = cv2.warpPerspective(body_a, M, (W, H))
wa = cv2.GaussianBlur(wa, (0, 0), 1.0)[..., None]
out = bg * (1 - wa) + wp * wa
out = cv2.GaussianBlur(out, (0, 0), 0.8) + rng.normal(0, 4, out.shape)
Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).save("out/01_real_zoomout.jpg", quality=92)
