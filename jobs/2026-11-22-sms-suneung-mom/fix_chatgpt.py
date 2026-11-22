"""ChatGPT 손폰 사진의 오타 '많은증이야' → '많은중이야'.
'증'의 ㅇ을 4px 아래로 내리고 ㅡ 가운데에 세로획(ㅜ)을 그려 '중'으로 만든다."""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
im = np.array(Image.open("src/chatgpt_photo.png").convert("RGB")).astype(np.float32)
x0, x1 = 606, 635
bgpatch = im[1176:1186, x0:x1].reshape(-1, 3)
bg = np.median(bgpatch, 0)
old = im[1166:1178, x0:x1].copy()
im[1166:1182, x0:x1] = bg
im[1169:1181, x0:x1] = old
# ㅇ 위 남은 경계 부드럽게
# 세로획(ㅜ): ㅡ 가운데(x≈621~622, y 1165) 아래로
S = 8
lay = Image.new("L", ((x1 - x0) * S, 20 * S), 0)
d = ImageDraw.Draw(lay)
cx = (621.5 - x0) * S
d.line([(cx, 1 * S), (cx + 0.3 * S, 4.8 * S)], fill=255, width=int(2.4 * S))
lay = lay.resize((x1 - x0, 20), Image.LANCZOS).filter(ImageFilter.GaussianBlur(0.35))
a = (np.array(lay).astype(np.float32) / 255)[..., None]
ink = np.array([67, 55, 83], np.float32)
reg = im[1164:1184, x0:x1]
im[1164:1184, x0:x1] = reg * (1 - a) + ink * a
# 노이즈 맞춤
rng = np.random.default_rng(1)
im[1164:1184, x0:x1] += rng.normal(0, 2.5, im[1164:1184, x0:x1].shape)
out = Image.fromarray(np.clip(im, 0, 255).astype(np.uint8))
out.save("out/01_chatgpt_fixed.png")
out.crop((300, 1120, 720, 1200)).resize((1260, 240), Image.LANCZOS).save("/tmp/z1.png")
