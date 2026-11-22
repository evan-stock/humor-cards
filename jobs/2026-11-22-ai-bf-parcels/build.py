"""ㅋㅋ상회 AI 짤: 블프 택배 (2026-11-22). 위 = 잠금화면 택배 알림 + 엄마 카톡(직접 그림), 아래 = Gemini 사진 src/01.png. 4:5."""
import os
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
W, H, TOP = 1080, 1350, 596
FB = '/home/claude/humor-cards/fonts/Pretendard-Bold.otf'
FM = '/home/claude/humor-cards/fonts/Pretendard-Medium.otf'
ft = ImageFont.truetype(FB, 31); fb = ImageFont.truetype(FM, 31); fs = ImageFont.truetype(FM, 25)
cv = Image.new('RGB', (W, H), (12, 12, 14)); d = ImageDraw.Draw(cv)
X0, X1, R = 34, W - 34, 30
def icon(x, y, kind):
    if kind == 'box':
        d.rounded_rectangle((x, y, x + 62, y + 62), 15, fill=(196, 140, 82))
        d.polygon([(x + 16, y + 24), (x + 31, y + 16), (x + 46, y + 24), (x + 31, y + 32)], fill=(245, 225, 196))
        d.polygon([(x + 16, y + 24), (x + 31, y + 32), (x + 31, y + 48), (x + 16, y + 40)], fill=(232, 204, 166))
        d.polygon([(x + 46, y + 24), (x + 31, y + 32), (x + 31, y + 48), (x + 46, y + 40)], fill=(214, 182, 140))
    else:  # 카톡
        d.rounded_rectangle((x, y, x + 62, y + 62), 15, fill=(254, 229, 0))
        d.ellipse((x + 12, y + 15, x + 50, y + 43), fill=(60, 30, 30))
        d.polygon([(x + 20, y + 38), (x + 17, y + 50), (x + 29, y + 41)], fill=(60, 30, 30))
def card(y, kind, app, title, body, h=106, when='지금'):
    d.rounded_rectangle((X0, y, X1, y + h), R, fill=(40, 40, 44))
    icon(X0 + 24, y + (h - 62) // 2, kind)
    tx = X0 + 24 + 62 + 22
    d.text((tx, y + 17), title, font=ft, fill='white')
    d.text((X1 - 26, y + 19), when, font=fs, fill=(150, 150, 156), anchor='ra')
    d.text((tx, y + 58), body, font=fb, fill=(225, 225, 230))
    return y + h + 14
d.text((W // 2, 30), '알림 센터', font=fs, fill=(150, 150, 156), anchor='mt')
y = 72
y = card(y, 'box', '택배', '배송 완료', '문 앞에 놓아두었습니다 (롱패딩 외 2건)', when='2시간 전')
y = card(y, 'box', '택배', '배송 완료', '문 앞에 놓아두었습니다 (전기요 외 4건)', when='1시간 전')
# 뒤에 쌓인 알림 3장
for k in (2, 1):
    d.rounded_rectangle((X0 + 22 * k, y + 106 - 6 + 9 * k, X1 - 22 * k, y + 106 + 9 * k + 4), R, fill=(40 - 8 * k, 40 - 8 * k, 44 - 8 * k))
y = card(y, 'box', '택배', '배송 완료 외 6개', '문 앞에 놓아두었습니다 (공기청정기 외 1건)', when='30분 전')
y += 22
y = card(y, 'kakao', '카카오톡', '엄마', '현관에 이거 다 니꺼냐', when='지금')
print('top used', y)
im = Image.open(os.path.join(HERE, 'src', '01.png')).convert('RGB'); s = W / im.width
im = im.resize((W, round(im.height * s)), Image.LANCZOS)
ph = H - TOP; top = max(0, (im.height - ph) // 2 + 20)
cv.paste(im.crop((0, top, W, top + ph)), (0, TOP))
cv.save(os.path.join(HERE, 'out', '01.jpg'), quality=93)
