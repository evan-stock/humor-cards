"""Gemini 실사본(kk_menhera_real): 아래에 한 번 더 찍힌 마지막 말풍선을 지운다."""
import numpy as np, cv2
from PIL import Image
im = np.array(Image.open("src/gemini_real.png").convert("RGB")).astype(np.float32)
H, W, _ = im.shape
Y = 1020
band = im[980:Y].copy()                 # 말풍선 사이 빈 배경 줄
fill = np.concatenate([band, band[::-1]] * 4, 0)[:H - Y]
fill = cv2.GaussianBlur(fill, (0, 0), 6)
fill += np.random.default_rng(1).normal(0, 2.5, fill.shape)
# 오른쪽 하트 배경은 원본 아랫부분을 살린다(말풍선이 없는 x>620 영역)
keep = np.zeros((H - Y, W, 1), np.float32); keep[:, 640:] = 1
keep = cv2.GaussianBlur(keep, (0, 0), 25)[..., None] if keep.ndim == 2 else cv2.GaussianBlur(keep[..., 0], (0, 0), 25)[..., None]
out = im.copy()
out[Y:] = fill * (1 - keep) + im[Y:] * keep
# 이음매 부드럽게
a = np.linspace(0, 1, 12)[:, None, None]
out[Y - 6:Y + 6] = im[Y - 6:Y + 6] * (1 - a) + out[Y - 6:Y + 6] * a
Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).save("out/01_real.jpg", quality=93)
