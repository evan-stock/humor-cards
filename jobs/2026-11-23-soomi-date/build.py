"""수민버스형 연애 '세대 비교 데이트' 2단 (2026-11-23). 그림 = Gemini 1장(src/01.png, 수민버스 27살 게시물 그림체 참고), 글씨·말풍선 직접."""
import os
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
FX = '/home/claude/humor-cards/fonts/Pretendard-ExtraBold.otf'
FM = '/home/claude/humor-cards/fonts/Pretendard-Medium.otf'
W, H = 1080, 1350; BG = (250, 248, 244); INK = (28, 28, 30)
src = Image.open(os.path.join(HERE, 'src/01.png')).convert('RGB')
p1 = src.crop((60, 44, 840, 548)); p2 = src.crop((60, 628, 840, 1106))
cv = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(cv)
PW = 900; X = (W - PW) // 2

def paste(p, y):
    p = p.resize((PW, round(p.height * PW / p.width)), Image.LANCZOS)
    cv.paste(p, (X, y)); d.rectangle((X, y, X + PW - 1, y + p.height - 1), outline=(120, 120, 120), width=2)
    return y + p.height

def title(t, y):
    d.text((W // 2, y), t, font=ImageFont.truetype(FX, 58), fill=INK, anchor='mm')

def bubble(lines, cx, cy, tail, size=44, sub=None):
    f = ImageFont.truetype(FX, size)
    tw = max(d.textlength(l, font=f) for l in lines); lh = size + 12
    bw, bh = tw + 70, lh * len(lines) + 40 + (40 if sub else 0)
    x0, y0 = cx - bw / 2, cy - bh / 2
    d.polygon([(cx + tail[0] * 0.15 - 18, y0 + bh - 8), (cx + tail[0] * 0.15 + 18, y0 + bh - 8), (cx + tail[0], cy + tail[1])], fill='white', outline=INK)
    d.ellipse((x0, y0, x0 + bw, y0 + bh), fill='white', outline=INK, width=4)
    d.polygon([(cx + tail[0] * 0.15 - 15, y0 + bh - 12), (cx + tail[0] * 0.15 + 15, y0 + bh - 12), (cx + tail[0] - 3, cy + tail[1] - 6)], fill='white')
    ty = cy - (lh * len(lines) + (40 if sub else 0)) / 2 + lh / 2
    for i, l in enumerate(lines):
        d.text((cx, ty + i * lh), l, font=f, fill=INK, anchor='mm')
    if sub:
        d.text((cx, ty + len(lines) * lh - 6), sub, font=ImageFont.truetype(FM, 26), fill=(90, 90, 95), anchor='mm')

title("우리 부모님 데이트할 때", 50)
y = paste(p1, 94)
title("우리 데이트할 때", y + 46)
y2 = paste(p2, y + 90)
print('bottom', y2)
# 위 칸 말풍선 (패널 좌표 → 캔버스: x*1000/780+40, y*1000/780+98)
s1 = PW / p1.width
def P1(x, yy): return X + (x - 60) * s1, 94 + (yy - 44) * s1
def P2(x, yy): return X + (x - 60) * s1, y + 90 + (yy - 628) * s1
bubble(['3시간 기다렸어.'], 330, 148, (95, 52), size=40)
bubble(['미안!! 삐삐가 늦게 와서!!'], 790, 140, (-60, 50), size=36)
cx, cy = P2(250, 660); bubble(['오늘 뭐 먹을래?'], cx + 30, cy + 20, (10, 76), size=38, sub='(카톡으로)')
cx, cy = P2(640, 660); bubble(['아무거나ㅋㅋ'], cx + 30, cy + 20, (-10, 76), size=38, sub='(카톡으로)')
cv.save(os.path.join(HERE, 'out/01.jpg'), quality=94)
