"""'폰으로 바짝 붙여 찍은 카톡' 2판(다크 모드 + 키보드 + 반사 줄 + 먼지) — 사용자 참고: wamoyaaa·chatlogue·go_yang_e (2026-11-22 02:25).
AI 없음. 대화는 원문 그대로(이름 가상). 4:5 1080x1350."""
import os, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
HERE = os.path.dirname(os.path.abspath(__file__)); rng = np.random.default_rng(11)
NS = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'; NSM = '/usr/share/fonts/opentype/noto/NotoSansCJK-Medium.ttc'; NSB = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
EMO = '/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf'
def F(p, s): return ImageFont.truetype(p, s, index=1)
SW, SH = 1170, 2532
BG = (0, 0, 0); GRAY = (58, 58, 62); YEL = (254, 229, 0); TXT = (238, 238, 240); SUB = (140, 140, 148)
NAME = '지은'
MSGS = [('me_emoji', '👋', '오전 11:29'),
        ('me', '좀 이상하게 들릴 수 있지만 내가 맨날 일 끝나면 찾아가고 배고프다 하면 음식 사서 문 앞에 걸어두는 거 그런 게 싫은 거야? 아니면 너무 빠르다고 생각하는 거야?', '오전 11:31'),
        ('you', '아 아뇨! 전혀 안 이상해요 오빠! 다 설레는 행동인데 그냥 오빠가 찾아오는 게 싫고 오빠가 문 앞에 음식 걸어두는 게 싫고 빠르진 않지만 그냥 오빠가 싫은 거예요!', '오전 11:33')]

def wrap(d, text, font, maxw):
    out, line = [], ''
    for wd in text.split(' '):
        t = (line + ' ' + wd) if line else wd
        if d.textlength(t, font=font) > maxw and line: out.append(line); line = wd
        else: line = t
    return out + [line]

def screen():
    s = Image.new('RGB', (SW, SH), BG); d = ImageDraw.Draw(s)
    d.text((150, 75), '11:34', font=F(NSB, 52), fill='white', anchor='lm')
    for i, h in enumerate((16, 23, 30, 38)): d.rounded_rectangle((830 + i * 16, 95 - h, 841 + i * 16, 95), 3, fill='white')
    for r in (36, 24, 12): d.arc((950 - r, 100 - r, 950 + r, 100 + r), 225, 315, fill='white', width=7)
    d.rounded_rectangle((1000, 58, 1090, 96), 12, fill=(235, 235, 235)); d.text((1045, 77), '54', font=F(NSB, 30), fill='black', anchor='mm')
    # 머리
    d.rounded_rectangle((40, 160, 300, 262), 51, fill=(44, 44, 48)); d.line((100, 185, 76, 211), fill='white', width=8); d.line((76, 211, 100, 237), fill='white', width=8)
    d.text((125, 211), '128', font=F(NSB, 48), fill='white', anchor='lm')
    d.text((SW / 2, 211), NAME, font=F(NSB, 56), fill='white', anchor='mm')
    d.rounded_rectangle((870, 160, 1130, 262), 51, fill=(44, 44, 48))
    d.ellipse((920, 186, 960, 226), outline='white', width=6); d.line((955, 222, 975, 242), fill='white', width=7)
    for j in range(3): d.line((1040, 192 + j * 18, 1090, 192 + j * 18), fill='white', width=6)
    d.rounded_rectangle((330, 300, 840, 362), 31, fill=(40, 40, 44)); d.text((585, 331), '2026년 10월 6일 월요일 >', font=F(NSM, 34), fill=(225, 225, 230), anchor='mm')
    y = 410; f = F(NS, 46); lh = 64
    for kind, text, tm in MSGS:
        if kind == 'me_emoji':
            em = Image.new('RGBA', (160, 160), (0, 0, 0, 0)); ImageDraw.Draw(em).text((0, 0), text, font=ImageFont.truetype(EMO, 109), embedded_color=True)
            em = em.resize((230, 230), Image.LANCZOS); s.paste(em, (SW - 290, y), em); d.text((SW - 300, y + 225), tm, font=F(NS, 30), fill=SUB, anchor='rb'); y += 260; continue
        lines = wrap(d, text, f, 660); w = max(d.textlength(l, font=f) for l in lines) + 60; h = lh * len(lines) + 40
        if kind == 'me':
            x1 = SW - 46; x0 = x1 - w; d.rounded_rectangle((x0, y, x1, y + h), 30, fill=YEL); d.polygon([(x1 - 26, y), (x1 + 14, y + 2), (x1, y + 28)], fill=YEL)
            d.text((x0 - 14, y + h), tm, font=F(NS, 30), fill=SUB, anchor='rb')
            for k, l in enumerate(lines): d.text((x0 + 30, y + 20 + lh * k), l, font=f, fill=(15, 15, 15))
            y += h + 40
        else:
            d.rounded_rectangle((40, y, 146, y + 106), 40, fill=(90, 120, 150)); d.ellipse((75, y + 22, 111, y + 58), fill=(225, 235, 245)); d.chord((59, y + 58, 127, y + 114), 180, 360, fill=(225, 235, 245))
            d.text((172, y - 4), NAME, font=F(NS, 34), fill=(200, 200, 206), anchor='lt'); by = y + 50
            x0 = 172; d.rounded_rectangle((x0, by, x0 + w, by + h), 30, fill=GRAY); d.polygon([(x0 + 26, by), (x0 - 14, by + 2), (x0, by + 28)], fill=GRAY)
            d.text((x0 + w + 14, by + h), tm, font=F(NS, 30), fill=SUB, anchor='lb')
            for k, l in enumerate(lines): d.text((x0 + 30, by + 20 + lh * k), l, font=f, fill=TXT)
            y = by + h + 40
    # 입력창 + 키보드(아이폰 다크, 두벌식)
    ky = SH - 900
    d.rounded_rectangle((30, ky - 150, SW - 30, ky - 40), 55, fill=(30, 30, 33))
    d.ellipse((50, ky - 140, 140, ky - 50), fill=(52, 52, 56)); d.line((95, ky - 118, 95, ky - 72), fill='white', width=6); d.line((72, ky - 95, 118, ky - 95), fill='white', width=6)
    d.text((170, ky - 95), '메시지 입력', font=F(NS, 42), fill=(120, 120, 126), anchor='lm'); d.text((1000, ky - 95), '#', font=F(NSB, 58), fill=(200, 200, 205), anchor='mm')
    d.rectangle((0, ky, SW, SH), fill=(28, 28, 30))
    for i, t in enumerate(('나', '아', '나는')): d.text((SW * (i * 2 + 1) / 6, ky + 70), t, font=F(NS, 44), fill=(230, 230, 232), anchor='mm')
    rows = ['ㅂㅈㄷㄱㅅㅛㅕㅑㅐㅔ', 'ㅁㄴㅇㄹㅎㅗㅓㅏㅣ', 'ㅋㅌㅊㅍㅠㅜㅡ']
    kw, kh, gap = 103, 140, 13; y0 = ky + 150
    for r, row in enumerate(rows):
        n = len(row); x = (SW - (n * kw + (n - 1) * gap)) / 2 + (0 if r < 2 else 0)
        if r == 2: x = (SW - (7 * kw + 6 * gap)) / 2
        for ch in row:
            d.rounded_rectangle((x, y0 + r * (kh + 26), x + kw, y0 + r * (kh + 26) + kh), 14, fill=(72, 72, 76)); d.text((x + kw / 2, y0 + r * (kh + 26) + kh / 2), ch, font=F(NS, 54), fill='white', anchor='mm'); x += kw + gap
    r = 2; yy = y0 + r * (kh + 26)
    d.rounded_rectangle((20, yy, 150, yy + kh), 14, fill=(50, 50, 54)); d.text((85, yy + kh / 2), '⇧', font=F(NS, 56), fill='white', anchor='mm')
    d.rounded_rectangle((SW - 150, yy, SW - 20, yy + kh), 14, fill=(50, 50, 54)); d.text((SW - 85, yy + kh / 2), '⌫', font=F(NS, 50), fill='white', anchor='mm')
    yy += kh + 26
    d.rounded_rectangle((20, yy, 280, yy + kh), 14, fill=(50, 50, 54)); d.text((150, yy + kh / 2), '123', font=F(NS, 46), fill='white', anchor='mm')
    d.rounded_rectangle((300, yy, 870, yy + kh), 14, fill=(72, 72, 76)); d.text((585, yy + kh / 2), '스페이스', font=F(NS, 42), fill='white', anchor='mm')
    d.rounded_rectangle((890, yy, SW - 20, yy + kh), 14, fill=(50, 50, 54)); d.text((1020, yy + kh / 2), '⏎', font=F(NS, 52), fill='white', anchor='mm')
    return s

scr = screen().convert('RGBA')
# 폰: 검정 테두리, 위 가장자리만 살짝 보이게 바짝
B = 40; PW, PH = SW + 2 * B, SH + 2 * B
phone = Image.new('RGBA', (PW, PH), (0, 0, 0, 0)); pd = ImageDraw.Draw(phone)
pd.rounded_rectangle((0, 0, PW - 1, PH - 1), 170, fill=(14, 14, 16)); pd.rounded_rectangle((5, 5, PW - 6, PH - 6), 166, outline=(80, 80, 86), width=4)
m = Image.new('L', (SW, SH), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, SW - 1, SH - 1), 130, fill=255)
# 화면 찍은 티: 대비↓, 검정이 들뜸, 모아레, 먼지·지문, 반사 줄
a = np.asarray(scr.convert('RGB')).astype(float) * 0.88 + 18
yy, xx = np.mgrid[0:SH, 0:SW]
for c, p0 in enumerate((0, 2.1, 4.2)): a[..., c] += 6 * np.sin((xx * 0.95 + yy * 0.3) * 0.6 + p0) * np.sin((xx * 0.2 - yy * 0.9) * 0.5)
smudge = Image.fromarray((rng.random((SH // 40, SW // 40)) * 255).astype('uint8')).resize((SW, SH), Image.BICUBIC).filter(ImageFilter.GaussianBlur(40))
a += (np.asarray(smudge).astype(float) / 255 - 0.5)[..., None] * 22
s2 = Image.fromarray(np.clip(a, 0, 255).astype('uint8')).convert('RGBA'); dd = ImageDraw.Draw(s2)
for _ in range(260):
    x, y = rng.integers(0, SW), rng.integers(0, SH); r = rng.choice([1, 1, 2, 2, 3]); g = int(rng.integers(150, 230))
    dd.ellipse((x - r, y - r, x + r, y + r), fill=(g, g, g, int(rng.integers(90, 200))))
for _ in range(14):
    x, y = rng.integers(0, SW), rng.integers(0, SH); L = rng.integers(10, 40); ang = rng.random() * math.pi
    dd.line((x, y, x + L * math.cos(ang), y + L * math.sin(ang)), fill=(200, 200, 200, 120), width=2)
glare = Image.new('L', (SW, SH), 0); gd = ImageDraw.Draw(glare)
for off, wdt, val in ((0, 70, 150), (140, 26, 120), (-260, 40, 70)):
    gd.line((SW * 0.15 + off, SH * 0.98, SW * 0.98 + off, SH * 0.18), fill=val, width=wdt)
gd.ellipse((SW * 0.55, SH * 0.06, SW * 0.95, SH * 0.2), fill=60)
glare = glare.filter(ImageFilter.GaussianBlur(28))
s2 = Image.composite(Image.new('RGBA', (SW, SH), (255, 250, 235, 255)), s2, glare)
phone.paste(s2, (B, B), m)
# 바짝: 폰 폭을 캔버스보다 크게, 비스듬히, 원근
W, H = 1080, 1350
canvas = Image.new('RGBA', (W, H), (34, 30, 28, 255))
tw = 1130; sc = tw / PW; ph = phone.resize((tw, round(PH * sc)), Image.LANCZOS)
w0, h0 = ph.size
src = [(0, 0), (w0, 0), (w0, h0), (0, h0)]; dst = [(60, 0), (w0 - 20, 30), (w0 + 20, h0), (-30, h0 - 40)]
def coeffs(pa, pb):
    A = []
    for (x, y), (X, Y) in zip(pa, pb): A += [[X, Y, 1, 0, 0, 0, -x * X, -x * Y], [0, 0, 0, X, Y, 1, -y * X, -y * Y]]
    return np.linalg.solve(np.array(A, float), np.array(pa, float).reshape(8))
ph = ph.transform((w0 + 60, h0 + 40), Image.PERSPECTIVE, coeffs(src, dst), Image.BICUBIC).rotate(3.2, resample=Image.BICUBIC, expand=True)
# 보이는 부분: 머리 위 조금 ~ 키보드 위쪽 일부
oy = -int((B + 130) * sc)
canvas.alpha_composite(ph, (-70, oy))
img = canvas.convert('RGB')
r, g, b = img.split(); img = Image.merge('RGB', (ImageChops.offset(r, 2, 1), g, ImageChops.offset(b, -2, -1))).crop((6, 6, W - 6, H - 6)).resize((W, H), Image.BICUBIC)
soft = img.filter(ImageFilter.GaussianBlur(0.9)); blurry = img.filter(ImageFilter.GaussianBlur(2.6))
gradm = Image.fromarray((np.clip((np.mgrid[0:H, 0:W][0] - H * 0.6) / (H * 0.4), 0, 1) * 255).astype('uint8'))
img = Image.composite(blurry, soft, gradm).resize((W * 2 // 3, H * 2 // 3), Image.BILINEAR).resize((W, H), Image.BICUBIC)
a = np.asarray(img).astype(float) + rng.normal(0, 6, (H, W, 3))
yy, xx = np.mgrid[0:H, 0:W]; a *= (1 - 0.25 * (((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2))[..., None]
Image.fromarray(np.clip(a, 0, 255).astype('uint8')).save(os.path.join(HERE, 'out', '01_dark.jpg'), quality=80)
print('ok')
