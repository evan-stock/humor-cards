"""ㅋㅋ상회 AI 짤: 주식 폭락 '쏙쏙인가 쏙슬인가' 엄마 카톡 (2026-11-22). 그림 = Gemini(글씨 없음) src/01.png, 대화는 직접 그림.
양식: soominiverse 좋아요 2위('키 186 신발') — 위 대화 + 아래 실사 사진, 4:5."""
import os
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
W, H, TOP = 1080, 1350, 545
NS = '/usr/share/fonts/opentype/noto/NotoSansCJK-Medium.ttc'
f = ImageFont.truetype(NS, 38, index=1); fs = ImageFont.truetype(NS, 26, index=1)
cv = Image.new('RGB', (W, H), (12, 12, 14)); d = ImageDraw.Draw(cv)
def bub(y, text, right=False):
    tw = d.textlength(text, font=f); pw, ph = 30, 20; bw = tw + pw * 2; bh = 38 + ph * 2
    x0 = W - 50 - bw if right else 110
    d.rounded_rectangle((x0, y, x0 + bw, y + bh), radius=bh // 2, fill=(47, 124, 246) if right else (58, 58, 62))
    d.text((x0 + pw, y + bh / 2), text, font=f, fill='white', anchor='lm')
    if right: d.text((x0 - 14, y + bh - 6), '읽음', font=fs, fill=(140, 140, 146), anchor='rb')
    return y + bh + 14
d.ellipse((40, 62, 92, 114), fill=(90, 90, 96)); d.text((66, 88), '엄', font=fs, fill='white', anchor='mm')
d.text((110, 70), '엄마', font=fs, fill=(170, 170, 176), anchor='lm')
y = bub(96, '아들, 뉴스 보니까 쏙쏙인가 쏙슬인가')
y = bub(y, '그거 폭락했다던데')
y = bub(y, '너도 산 거 아니지?')
y = bub(y + 26, '엄마 김장은 언제 해?', right=True)
im = Image.open(os.path.join(HERE, 'src', '01.png')).convert('RGB'); s = W / im.width
im = im.resize((W, round(im.height * s)), Image.LANCZOS)
ph = H - TOP; top = 330; cv.paste(im.crop((0, top, W, top + ph)), (0, TOP))
cv.save(os.path.join(HERE, 'out', '01.jpg'), quality=93); print('ok', y)
