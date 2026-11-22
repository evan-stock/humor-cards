"""ChatGPT 손폰 사진 글씨 고침: '젊으로'→'첨으로', '헛|지않도록.'→'헛되지않도록.'
깨진 글자 자리를 말풍선 바탕색으로 지우고, 기울기·크기·흐림을 맞춰 다시 씀."""
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter
SRC = "src/chatgpt_photo.png"
im = np.array(Image.open(SRC).convert("RGB")).astype(np.float32)
NOTO = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
INK = np.array([50, 38, 74], np.float32)
INKY = np.array([45, 33, 10], np.float32)


def erase(poly, pad=1, thr=188, bgthr=175):
    """다각형 안의 글씨(어두운 픽셀)를 주변 바탕으로 메움(평면 맞춤)."""
    h, w = im.shape[:2]
    m = np.zeros((h, w), np.uint8); cv2.fillPoly(m, [np.int32(poly)], 1)
    ys, xs = np.where(m > 0); y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    reg = im[y0:y1, x0:x1]; mm = m[y0:y1, x0:x1] > 0
    g = reg.mean(2); txt = cv2.dilate((g < thr).astype(np.uint8), np.ones((5, 5), np.uint8)) > 0
    bgm = (~txt) & (g > bgthr)
    yy, xx = np.mgrid[0:y1 - y0, 0:x1 - x0].astype(np.float32)
    A = np.stack([np.ones_like(xx), xx, yy], -1)
    out = reg.copy()
    for c in range(3):
        coef, *_ = np.linalg.lstsq(A[bgm], reg[..., c][bgm], rcond=None)
        out[..., c] = A @ coef
    out += np.random.default_rng(0).normal(0, 2.0, out.shape)
    sel = (mm & txt)[..., None]
    soft = cv2.GaussianBlur(sel.astype(np.float32)[..., 0], (0, 0), 0.8)[..., None]
    im[y0:y1, x0:x1] = reg * (1 - soft) + out * soft


def draw(text, x, yb, width, angle, size_guess=24, ink=None):
    """왼쪽 아래(x,yb)에서 시작해 글자 폭 width가 되게, angle(도, +는 오른쪽이 올라감)만큼 기울여 씀."""
    S = 8
    f = ImageFont.truetype(NOTO, size_guess * S, index=1)
    bb = f.getbbox(text)
    lay = Image.new("L", (bb[2] + 40 * S, bb[3] + 40 * S), 0)
    ImageDraw.Draw(lay).text((20 * S, 20 * S), text, font=f, fill=255)
    lay = lay.crop(lay.getbbox())
    sc = width / (lay.width / S)
    nw, nh = max(1, round(lay.width / S * sc * S)), max(1, round(lay.height / S * sc * S))
    lay = lay.resize((nw, nh), Image.LANCZOS)
    rot = lay.rotate(angle, resample=Image.BICUBIC, expand=True)
    # 회전 후 원래 왼쪽 아래 모서리 위치 계산
    import math
    a = math.radians(angle); cx, cy = lay.width / 2, lay.height / 2
    px, py = 0 - cx, lay.height - cy
    rx = px * math.cos(a) + py * math.sin(a) + rot.width / 2
    ry = -px * math.sin(a) + py * math.cos(a) + rot.height / 2
    small = rot.resize((max(1, round(rot.width / S)), max(1, round(rot.height / S))), Image.LANCZOS).filter(ImageFilter.GaussianBlur(0.45))
    al = np.array(small).astype(np.float32)[..., None] / 255
    al = np.clip(al * 1.3, 0, 1)
    ox, oy = round(x - rx / S), round(yb - ry / S)
    h, w = al.shape[:2]
    reg = im[oy:oy + h, ox:ox + w]
    im[oy:oy + h, ox:ox + w] = reg * (1 - al) + (INK if ink is None else ink) * al


# 1) 마지막 말풍선: '조건감사해헛|지않도록.' 다시 쓰기('무'는 원본 유지)
erase([(457, 1250), (457, 1212), (730, 1180), (730, 1218)])
draw("무조건감사해헛되지않도록.", 461, 1240, 263, 6.6)
# 3) '그걸로 빗 먼저 갚아'의 '갚' 다시 쓰기(노란 말풍선)
erase([(805, 230), (805, 199), (830, 197), (830, 228)], thr=120, bgthr=140)
draw("갚", 810, 229, 21, 7.0, ink=INKY)
# 2) '젊' → '첨'
erase([(519, 607), (519, 569), (543, 566), (543, 604)])
draw("첨", 520, 600, 20, 6.0)

out = Image.fromarray(np.clip(im, 0, 255).astype(np.uint8))
out.save("out/01_chatgpt_fixed.png")
out.crop((440, 1170, 760, 1250)).resize((1280, 320), Image.LANCZOS).save("/tmp/c2.png")
out.crop((640, 190, 870, 250)).resize((920, 240), Image.LANCZOS).save("/tmp/a1.png")
out.crop((360, 540, 760, 640)).resize((1200, 300), Image.LANCZOS).save("/tmp/c1.png")
