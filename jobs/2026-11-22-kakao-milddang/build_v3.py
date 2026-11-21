"""'폰으로 찍은 카톡' 3판 — 실제 2026 카톡(아이폰) 화면에 맞춤: 참고 chatlogue '형' 릴스(10.3만) 프레임.
연보라빛 배경, 왼쪽 '< 128' 캡슐, 가운데 굵은 이름, 오른쪽 검색·전화·메뉴 캡슐, 날짜 알약, 꼬리 없는 둥근 말풍선, 둥근 사각 프로필.
글꼴은 아이폰 기본(애플 SD 고딕 Neo)과 가장 가까운 Pretendard. 덜 바짝: 폰 위쪽 끝과 양옆 테두리가 보이게. AI 없음."""
import os, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..')); rng = np.random.default_rng(5)
FD = os.path.join(ROOT, 'fonts')
def P(w, s): return ImageFont.truetype({'L': '/tmp/Pretendard-Light.otf', 'M': f'{FD}/Pretendard-Medium.otf', 'S': '/tmp/Pretendard-SemiBold.otf', 'B': f'{FD}/Pretendard-Bold.otf'}[w], s)
EMO = '/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf'
SW, SH = 1170, 2532
BG = (176, 186, 222); PILL = (226, 230, 244); DATE = (160, 170, 208); WHT = (255, 255, 255); YEL = (254, 229, 0); INK = (17, 17, 19); SUB = (92, 98, 118)
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

def icons(d, cx, cy, kind, col=INK, w=6):
    if kind == 'search': d.ellipse((cx - 26, cy - 26, cx + 14, cy + 14), outline=col, width=w); d.line((cx + 10, cy + 10, cx + 30, cy + 30), fill=col, width=w + 1)
    if kind == 'menu':
        for j in (-18, 0, 18): d.line((cx - 26, cy + j, cx + 26, cy + j), fill=col, width=w)
    if kind == 'phone':
        d.arc((cx - 28, cy - 28, cx + 28, cy + 28), 110, 250, fill=col, width=w)
        d.line((cx - 18, cy - 26, cx - 6, cy - 14), fill=col, width=w); d.line((cx + 4, cy + 10, cx + 18, cy + 22), fill=col, width=w)

def screen():
    s = Image.new('RGB', (SW, SH), BG); d = ImageDraw.Draw(s)
    # 상태 표시줄 + 다이내믹 아일랜드
    d.text((170, 100), '11:34', font=P('S', 54), fill=INK, anchor='mm')
    d.rounded_rectangle((398, 36, 772, 146), 55, fill=(0, 0, 0))
    for i, h in enumerate((15, 22, 29, 36)): d.rounded_rectangle((850 + i * 15, 116 - h, 860 + i * 15, 116), 3, fill=INK)
    for r in (34, 23, 12): d.arc((958 - r, 118 - r, 958 + r, 118 + r), 225, 315, fill=INK, width=7)
    d.rounded_rectangle((1008, 82, 1098, 122), 13, fill=INK); d.text((1053, 102), '53', font=P('B', 31), fill=WHT, anchor='mm'); d.rounded_rectangle((1100, 94, 1106, 110), 2, fill=INK)
    # 머리
    hy = 262
    d.rounded_rectangle((40, hy - 62, 300, hy + 62), 62, fill=PILL); d.line((112, hy - 26, 88, hy), fill=INK, width=7); d.line((88, hy, 112, hy + 26), fill=INK, width=7)
    d.text((140, hy), '128', font=P('M', 52), fill=INK, anchor='lm')
    d.text((SW / 2, hy), NAME, font=P('B', 58), fill=INK, anchor='mm')
    d.rounded_rectangle((780, hy - 62, 1130, hy + 62), 62, fill=PILL)
    icons(d, 850, hy, 'search'); icons(d, 955, hy, 'phone'); icons(d, 1060, hy, 'menu')
    d.rounded_rectangle((322, 380, 848, 446), 33, fill=DATE); d.text((585, 413), '2026년 10월 6일 월요일 >', font=P('M', 36), fill=(48, 52, 70), anchor='mm')
    y = 500; f = P('M', 50); lh = 68
    for kind, text, tm in MSGS:
        if kind == 'me_emoji':
            em = Image.new('RGBA', (160, 160), (0, 0, 0, 0)); ImageDraw.Draw(em).text((0, 0), text, font=ImageFont.truetype(EMO, 109), embedded_color=True)
            em = em.resize((220, 220), Image.LANCZOS); s.paste(em, (SW - 270, y), em); d.text((SW - 280, y + 218), tm, font=P('M', 32), fill=SUB, anchor='rb'); y += 250; continue
        lines = wrap(d, text, f, 700); w = max(d.textlength(l, font=f) for l in lines) + 64; h = lh * len(lines) + 46
        if kind == 'me':
            x1 = SW - 40; x0 = x1 - w; d.rounded_rectangle((x0, y, x1, y + h), 42, fill=YEL)
            d.text((x0 - 16, y + h - 4), tm, font=P('M', 32), fill=SUB, anchor='rb')
            for k, l in enumerate(lines): d.text((x0 + 32, y + 23 + lh * k), l, font=f, fill=INK)
            y += h + 46
        else:
            d.rounded_rectangle((38, y, 158, y + 120), 46, fill=(143, 186, 178)); d.ellipse((79, y + 26, 117, y + 64), fill=WHT); d.chord((61, y + 64, 135, y + 124), 180, 360, fill=WHT)
            d.text((182, y - 2), NAME, font=P('M', 36), fill=(48, 52, 70), anchor='lt'); by = y + 54; x0 = 182
            d.rounded_rectangle((x0, by, x0 + w, by + h), 42, fill=WHT)
            d.text((x0 + w + 16, by + h - 4), tm, font=P('M', 32), fill=SUB, anchor='lb')
            for k, l in enumerate(lines): d.text((x0 + 32, by + 23 + lh * k), l, font=f, fill=INK)
            y = by + h + 46
    return s, y

scr, endy = screen()
B = 42; PW, PH = SW + 2 * B, SH + 2 * B
phone = Image.new('RGBA', (PW, PH), (0, 0, 0, 0)); pd = ImageDraw.Draw(phone)
pd.rounded_rectangle((0, 0, PW - 1, PH - 1), 175, fill=(16, 16, 18)); pd.rounded_rectangle((4, 4, PW - 5, PH - 5), 171, outline=(96, 96, 104), width=5)
m = Image.new('L', (SW, SH), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, SW - 1, SH - 1), 135, fill=255)
# 찍은 티(적당히): 대비 약간↓, 옅은 모아레, 반사 줄 2개, 먼지 조금
a = np.asarray(scr).astype(float) * 0.93 + 10
yy, xx = np.mgrid[0:SH, 0:SW]
for c, p0 in enumerate((0, 2.1, 4.2)): a[..., c] += 4 * np.sin((xx * 0.95 + yy * 0.3) * 0.6 + p0) * np.sin((xx * 0.2 - yy * 0.9) * 0.5)
s2 = Image.fromarray(np.clip(a, 0, 255).astype('uint8')).convert('RGBA'); dd = ImageDraw.Draw(s2)
for _ in range(90):
    x, y = rng.integers(0, SW), rng.integers(0, SH); r = rng.choice([1, 2, 2, 3]); g = int(rng.integers(200, 250))
    dd.ellipse((x - r, y - r, x + r, y + r), fill=(g, g, g, int(rng.integers(70, 160))))
glare = Image.new('L', (SW, SH), 0); gd = ImageDraw.Draw(glare)
gd.line((SW * 0.05, SH * 0.55, SW * 0.9, SH * 0.02), fill=110, width=34); gd.line((SW * 0.3, SH * 0.62, SW * 1.05, SH * 0.18), fill=70, width=18)
glare = glare.filter(ImageFilter.GaussianBlur(14))
s2 = Image.composite(Image.new('RGBA', (SW, SH), (255, 252, 240, 255)), s2, glare)
phone.paste(s2, (B, B), m)
W, H = 1080, 1350
# 배경: 흐린 이불(밝은 회갈색 주름)
bg = np.zeros((H, W, 3), float); bg[:] = (196, 188, 178); yy2, xx2 = np.mgrid[0:H, 0:W]
bg += (np.sin(xx2 * 0.012 + np.sin(yy2 * 0.006) * 3) * 10 + np.sin(yy2 * 0.02 + xx2 * 0.004) * 6)[..., None]
canvas = Image.fromarray(np.clip(bg, 0, 255).astype('uint8')).filter(ImageFilter.GaussianBlur(6)).convert('RGBA')
# 보이는 부분: 폰 위 끝 ~ 마지막 말풍선 아래 조금
visible = phone.crop((0, 0, PW, min(PH, endy + B + 420)))
tw = 900; sc = tw / PW; ph = visible.resize((tw, round(visible.height * sc)), Image.LANCZOS)
w0, h0 = ph.size
src = [(0, 0), (w0, 0), (w0, h0), (0, h0)]; dst = [(26, 0), (w0 - 4, 14), (w0 + 10, h0), (-6, h0 - 8)]
def coeffs(pa, pb):
    A = []
    for (x, y), (X, Y) in zip(pa, pb): A += [[X, Y, 1, 0, 0, 0, -x * X, -x * Y], [0, 0, 0, X, Y, 1, -y * X, -y * Y]]
    return np.linalg.solve(np.array(A, float), np.array(pa, float).reshape(8))
ph = ph.transform((w0 + 20, h0 + 10), Image.PERSPECTIVE, coeffs(src, dst), Image.BICUBIC).rotate(-1.8, resample=Image.BICUBIC, expand=True)
ox, oy = (W - ph.width) // 2, 14
sh = Image.new('RGBA', canvas.size, (0, 0, 0, 0)); sh.paste(Image.new('RGBA', ph.size, (0, 0, 0, 110)), (ox + 10, oy + 16), ph.split()[3]); canvas.alpha_composite(sh.filter(ImageFilter.GaussianBlur(18)))
canvas.alpha_composite(ph, (ox, oy))
img = canvas.convert('RGB')
r, g, b = img.split(); img = Image.merge('RGB', (ImageChops.offset(r, 1, 0), g, ImageChops.offset(b, -1, 0))).crop((3, 3, W - 3, H - 3)).resize((W, H), Image.BICUBIC)
img = img.filter(ImageFilter.GaussianBlur(0.6)).resize((W * 3 // 4, H * 3 // 4), Image.BILINEAR).resize((W, H), Image.BICUBIC)
a = np.asarray(img).astype(float) + rng.normal(0, 4, (H, W, 3))
yy, xx = np.mgrid[0:H, 0:W]; a *= (1 - 0.18 * (((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2))[..., None]
a[..., 0] *= 1.02; a[..., 2] *= 0.98
Image.fromarray(np.clip(a, 0, 255).astype('uint8')).save(os.path.join(HERE, 'out', '01_v3.jpg'), quality=84)
print('ok', endy)
