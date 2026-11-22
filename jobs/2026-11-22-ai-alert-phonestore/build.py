"""ㅋㅋ상회 AI 짤: 수능 위급재난문자 × 휴대폰 매장 (2026-11-22).
소재: 펨코 '오늘자 재난문자 최고 피해자'(조회 58만) — 휴대폰 매장 직원 스레드 글.
위 = 아이폰 잠금화면 위급 재난 문자 알림(직접 그림, 문구는 교육부 실제 2차 문자), 아래 = 사진 src/01.png(ChatGPT 등). 4:5."""
import os, sys
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
W, H, TOP = 1080, 1350, 470
FB = '/home/claude/humor-cards/fonts/Pretendard-Bold.otf'; FM = '/home/claude/humor-cards/fonts/Pretendard-Medium.otf'
PSB = '/home/claude/cardnews/assets/fonts/Pretendard-SemiBold.otf'
cv = Image.new('RGB', (W, H), (12, 12, 14)); d = ImageDraw.Draw(cv)
d.text((W // 2, 46), '11월 19일 목요일', font=ImageFont.truetype(PSB, 34), fill=(225, 225, 230), anchor='mm')
d.text((W // 2, 140), '14:21', font=ImageFont.truetype(FB, 120), fill=(240, 240, 245), anchor='mm')
X0, X1, y = 34, W - 34, 230
d.rounded_rectangle((X0, y, X1, y + 214), 34, fill=(44, 44, 48))
# 경고 아이콘(빨간 삼각형 느낌표)
ix, iy = X0 + 30, y + 30
d.rounded_rectangle((ix, iy, ix + 62, iy + 62), 15, fill=(232, 58, 48))
d.polygon([(ix + 31, iy + 12), (ix + 52, iy + 50), (ix + 10, iy + 50)], fill='white')
d.rectangle((ix + 29, iy + 24, ix + 33, iy + 39), fill=(232, 58, 48)); d.rectangle((ix + 29, iy + 42, ix + 33, iy + 46), fill=(232, 58, 48))
tx = ix + 62 + 22
d.text((tx, iy - 2), '위급 재난 문자', font=ImageFont.truetype(FB, 34), fill='white')
d.text((X1 - 28, iy + 2), '지금', font=ImageFont.truetype(FM, 27), fill=(160, 160, 166), anchor='ra')
fb = ImageFont.truetype(FM, 31)
lines = ['(TEST ALERT) 수능 시험 부정 방지 문자입니다.', '국민들께서는 놀라지 마시고 일상생활 유지하시', '길 바랍니다. [교육부]']
for k, l in enumerate(lines):
    d.text((tx, iy + 46 + k * 42), l, font=fb, fill=(230, 230, 235))
src = os.path.join(HERE, 'src', '01.png')
if os.path.exists(src):
    im = Image.open(src).convert('RGB'); ph = H - TOP; s = max(W / im.width, ph / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    lx = (im.width - W) // 2; ty = (im.height - ph) // 2
    cv.paste(im.crop((lx, ty, lx + W, ty + ph)), (0, TOP))
cv.save(os.path.join(HERE, 'out', '01.jpg'), quality=93)
cv.crop((0, 0, W, TOP)).save(os.path.join(HERE, 'out', 'top.png'))
