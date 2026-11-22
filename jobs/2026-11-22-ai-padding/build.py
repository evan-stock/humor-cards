"""ㅋㅋ상회 AI 짤: 패딩 옷장 (사용자 선택) (2026-11-22). 그림 = Gemini(글씨 없음) src/01.png, 대화는 직접 그림.
양식: soominiverse 좋아요 2위('키 186 신발') — 위 대화 + 아래 실사 사진, 4:5."""
import os
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
W, H, TOP = 1080, 1350, 455
NS = '/usr/share/fonts/opentype/noto/NotoSansCJK-Medium.ttc'
f = ImageFont.truetype(NS, 38, index=1); fs = ImageFont.truetype(NS, 26, index=1)
cv = Image.new('RGB', (W, H), (12, 12, 14)); d = ImageDraw.Draw(cv)
def bub(y, text, right=False):
    tw = d.textlength(text, font=f); pw, ph = 30, 20; bw = tw + pw * 2; bh = 38 + ph * 2
    x0 = W - 50 - bw if right else 110
    d.rounded_rectangle((x0, y, x0 + bw, y + bh), radius=bh // 2, fill=(47, 124, 246) if right else (58, 58, 62))
    d.text((x0 + pw, y + bh / 2), text, font=f, fill='white', anchor='lm')
    if right and text.startswith('옷장'): d.text((x0 - 14, y + bh - 6), '읽음', font=fs, fill=(140, 140, 146), anchor='rb')
    return y + bh + 14
d.ellipse((40, 62, 92, 114), fill=(90, 90, 96)); d.text((66, 88), '지', font=fs, fill='white', anchor='mm')
d.text((110, 70), '지훈', font=fs, fill=(170, 170, 176), anchor='lm')
y = bub(96, '이번 주말에 패딩 보러 갈래?')
y = bub(y + 26, 'ㄴㄴ 올해는 있는 거 입음', right=False if False else True)
y = bub(y, '옷장에 비슷한 거 많아서', right=True)
im = Image.open(os.path.join(HERE, 'src', '01.png')).convert('RGB')
ph = H - TOP; s = max(W / im.width, ph / im.height)
im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
lx = (im.width - W) // 2; ty = (im.height - ph) // 2
cv.paste(im.crop((lx, ty, lx + W, ty + ph)), (0, TOP))
cv.save(os.path.join(HERE, 'out', '01.jpg'), quality=93); print('ok', y)
