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
    """수민버스식 말풍선: 4배로 그려 줄여 매끈하게. 타원 + 짧은 꼬리, 얇은 검정 선."""
    S = 4
    f = ImageFont.truetype(FX, size * S); fs_ = ImageFont.truetype(FM, 24 * S)
    tmp = ImageDraw.Draw(Image.new('L', (1, 1)))
    tw = max(tmp.textlength(l, font=f) for l in lines); lh = (size + 10) * S
    th = lh * len(lines) + (34 * S if sub else 0)
    bw, bh = tw + 64 * S, th + 46 * S
    tx, ty = tail[0] * S, tail[1] * S
    pad = 40 * S
    Wl = int(bw + abs(tx) * 2 + pad * 2); Hl = int(bh + abs(ty) + pad * 2)
    lay = Image.new('RGBA', (Wl, Hl), (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
    ox, oy = Wl / 2 - bw / 2, pad
    LW = 3 * S
    box = (ox, oy, ox + bw, oy + bh)
    tip = (Wl / 2 + tx, oy + bh / 2 + ty)
    bx = Wl / 2 + tx * 0.25
    base = [(bx - 16 * S, oy + bh - 14 * S), (bx + 16 * S, oy + bh - 14 * S)]
    # 바깥선: 검정으로 크게 그린 뒤 흰색으로 안쪽 채움
    dl.ellipse((box[0] - LW, box[1] - LW, box[2] + LW, box[3] + LW), fill=INK)
    dl.polygon([(base[0][0] - LW, base[0][1]), (base[1][0] + LW, base[1][1]), (tip[0], tip[1] + LW * 0.8)], fill=INK)
    dl.ellipse(box, fill='white')
    dl.polygon([base[0], base[1], tip], fill='white')
    yy = oy + (bh - th) / 2 + lh / 2
    for i, l in enumerate(lines):
        dl.text((Wl / 2, yy + i * lh), l, font=f, fill=INK, anchor='mm')
    if sub:
        dl.text((Wl / 2, yy + len(lines) * lh - 8 * S), sub, font=fs_, fill=(95, 95, 100), anchor='mm')
    lay = lay.resize((Wl // S, Hl // S), Image.LANCZOS)
    cv.paste(lay, (int(cx - Wl / S / 2), int(cy - (oy + bh / 2) / S)), lay)


title("우리 부모님 데이트할 때", 50)
y = paste(p1, 94)
title("우리 데이트할 때", y + 46)
y2 = paste(p2, y + 90)
print('bottom', y2)
# 위 칸 말풍선 (패널 좌표 → 캔버스: x*1000/780+40, y*1000/780+98)
s1 = PW / p1.width
def P1(x, yy): return X + (x - 60) * s1, 94 + (yy - 44) * s1
def P2(x, yy): return X + (x - 60) * s1, y + 90 + (yy - 628) * s1
bubble(['3시간', '기다렸어.'], 300, 175, (70, 70), size=38)
bubble(['미안!!', '삐삐가 늦게 와서!!'], 820, 175, (-90, 70), size=36)
cx, cy = P2(250, 660); bubble(['오늘 뭐 먹을래?'], cx + 30, cy + 20, (10, 76), size=38, sub='(카톡으로)')
cx, cy = P2(640, 660); bubble(['아무거나ㅋㅋ'], cx + 30, cy + 20, (-10, 76), size=38, sub='(카톡으로)')
cv.save(os.path.join(HERE, 'out/01.jpg'), quality=94)
