"""ㅋㅋ상회 '폰으로 찍은 레전드 카톡' 짤: 썸녀와 밀당 카톡 (2026-11-22).
원본: 에펨코리아 포텐 https://www.fmkorea.com/index.php?mid=best&document_srl=10416394299 (조회 104만, 추천 2,625). 대화 문장은 원본 그대로, 이름은 가상('지은').
AI 그림 없이: 카톡풍 화면을 직접 그리고 → 폰 테두리 → 기울기·원근 → 반사·모아레·노이즈로 '다른 폰으로 찍은' 느낌. 4:5(1080x1350)."""
import os, random, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
HERE = os.path.dirname(os.path.abspath(__file__)); random.seed(7)
NS = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
NSM = '/usr/share/fonts/opentype/noto/NotoSansCJK-Medium.ttc'
EMO = '/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf'
def F(p, s): return ImageFont.truetype(p, s, index=1)
SW, SH = 1170, 1900                      # 폰 화면(아이폰 폭)
BG = (178, 199, 217); YEL = (254, 229, 0); WHT = (255, 255, 255)
NAME = '지은'

def wrap(d, text, font, maxw):
    out = []
    for para in text.split('\n'):
        line = ''
        for wd in para.split(' '):
            t = (line + ' ' + wd) if line else wd
            if d.textlength(t, font=font) > maxw and line: out.append(line); line = wd
            else: line = t
        out.append(line)
    return out

def screen():
    """2026 카톡 화면(사용자 참고 사진 '미정이' 카톡 기준): 이름 가운데, 오른쪽 둥근 캡슐 안 아이콘 3개, 날짜는 글자만, 둥근 사각 프로필, 떠 있는 입력창."""
    s = Image.new('RGB', (SW, SH), BG); d = ImageDraw.Draw(s); ink = (25, 25, 28)
    # 상태 표시줄: 시간 + 무음 종, 신호·와이파이·배터리(숫자)
    d.text((120, 70), '11:34', font=F(NSM, 50), fill=ink, anchor='lm')
    for i, h in enumerate((14, 21, 28, 35)): d.rounded_rectangle((820 + i * 15, 88 - h, 830 + i * 15, 88), 3, fill=ink)
    for r in (34, 23, 12): d.arc((925 - r, 92 - r, 925 + r, 92 + r), 225, 315, fill=ink, width=6)
    d.rounded_rectangle((975, 52, 1065, 92), 12, fill=(60, 62, 66)); d.text((1020, 72), '50', font=F(NSM, 30), fill='white', anchor='mm'); d.rounded_rectangle((1067, 64, 1073, 80), 2, fill=(60, 62, 66))
    # 머리: 뒤로 < , 가운데 이름, 오른쪽 캡슐(검색·전화·메뉴)
    d.line((118, 172, 92, 200), fill=ink, width=7); d.line((92, 200, 118, 228), fill=ink, width=7)
    d.text((SW / 2 - 40, 200), NAME, font=F(NSM, 56), fill=ink, anchor='mm')
    d.rounded_rectangle((760, 150, 1120, 250), 50, fill=(204, 217, 229))
    cx = 820; d.ellipse((cx - 24, 176, cx + 16, 216), outline=ink, width=5); d.line((cx + 12, 212, cx + 30, 230), fill=ink, width=6)
    cx = 940  # 전화기
    d.arc((cx - 30, 172, cx + 30, 232), 100, 250, fill=ink, width=7); d.rounded_rectangle((cx - 30, 170, cx - 12, 186), 6, fill=ink); d.rounded_rectangle((cx - 22, 214, cx - 2, 230), 6, fill=ink)
    cx = 1050
    for j in range(3): d.line((cx - 26, 182 + j * 17, cx + 26, 182 + j * 17), fill=ink, width=5)
    d.text((SW / 2, 310), '2026년 10월 6일 월요일 >', font=F(NS, 36), fill=(55, 60, 68), anchor='mm')
    y = 380
    em = Image.new('RGBA', (160, 160), (0, 0, 0, 0)); ImageDraw.Draw(em).text((0, 0), '👋', font=ImageFont.truetype(EMO, 109), embedded_color=True)
    em = em.resize((250, 250), Image.LANCZOS); s.paste(em, (SW - 310, y), em); y += 250
    d.text((SW - 320, y - 10), '오전 11:29', font=F(NS, 30), fill=(70, 78, 90), anchor='rb')
    f = F(NS, 45); lh = 64
    def bubble(y, text, me, tm):
        lines = wrap(d, text, f, 660); w = max(d.textlength(l, font=f) for l in lines) + 60; h = lh * len(lines) + 40
        if me:
            x1 = SW - 46; x0 = x1 - w
            d.rounded_rectangle((x0, y, x1, y + h), 28, fill=YEL); d.polygon([(x1 - 24, y), (x1 + 14, y + 2), (x1, y + 26)], fill=YEL)
            d.text((x0 - 14, y + h), tm, font=F(NS, 30), fill=(70, 78, 90), anchor='rb'); tx = x0 + 30; ty = y
        else:
            d.rounded_rectangle((44, y - 52, 150, y + 54), 40, fill=(160, 195, 222)); d.ellipse((79, y - 30, 115, y + 6), fill=WHT); d.chord((63, y + 6, 131, y + 62), 180, 360, fill=WHT)
            d.text((176, y - 56), NAME, font=F(NS, 34), fill=(50, 56, 66), anchor='lt')
            x0 = 176; x1 = x0 + w; by = y - 8
            d.rounded_rectangle((x0, by, x1, by + h), 28, fill=WHT); d.polygon([(x0 + 24, by), (x0 - 14, by + 2), (x0, by + 26)], fill=WHT)
            d.text((x1 + 14, by + h), tm, font=F(NS, 30), fill=(70, 78, 90), anchor='lb'); tx = x0 + 30; ty = by; y = by
        for k, l in enumerate(lines): d.text((tx, ty + 20 + lh * k), l, font=f, fill=(20, 20, 22), anchor='la')
        return y + h
    y = bubble(y + 30, '좀 이상하게 들릴 수 있지만 내가 맨날 일 끝나면 찾아가고 배고프다 하면 음식 사서 문 앞에 걸어두는 거 그런 게 싫은 거야? 아니면 너무 빠르다고 생각하는 거야?', True, '오전 11:31')
    y = bubble(y + 130, '아 아뇨! 전혀 안 이상해요 오빠! 다 설레는 행동인데 그냥 오빠가 찾아오는 게 싫고 오빠가 문 앞에 음식 걸어두는 게 싫고 빠르진 않지만 그냥 오빠가 싫은 거예요!', False, '오전 11:33')
    # 떠 있는 입력창: 왼쪽 + 동그라미, 가운데 글자, 오른쪽 이모티콘·#
    d.rounded_rectangle((40, SH - 175, SW - 40, SH - 55), 60, fill=(222, 230, 238))
    d.ellipse((62, SH - 160, 152, SH - 70), fill=(240, 244, 248)); d.line((107, SH - 140, 107, SH - 90), fill=(70, 70, 75), width=6); d.line((82, SH - 115, 132, SH - 115), fill=(70, 70, 75), width=6)
    d.text((185, SH - 115), '메시지 입력', font=F(NS, 42), fill=(150, 156, 165), anchor='lm')
    d.ellipse((930, SH - 145, 990, SH - 85), outline=(70, 70, 75), width=5); d.ellipse((947, SH - 125, 955, SH - 117), fill=(70, 70, 75)); d.ellipse((965, SH - 125, 973, SH - 117), fill=(70, 70, 75)); d.arc((945, SH - 122, 975, SH - 98), 20, 160, fill=(70, 70, 75), width=4)
    d.text((1060, SH - 115), '#', font=F(NSM, 64), fill=(70, 70, 75), anchor='mm')
    return s, y

scr, endy = screen()
# 폰(검정 테두리 + 둥근 모서리)
B = 46; PW, PH = SW + 2 * B, SH + 2 * B
phone = Image.new('RGBA', (PW, PH), (0, 0, 0, 0)); pd = ImageDraw.Draw(phone)
pd.rounded_rectangle((0, 0, PW - 1, PH - 1), 150, fill=(18, 18, 20)); pd.rounded_rectangle((6, 6, PW - 7, PH - 7), 146, outline=(70, 70, 76), width=4)
m = Image.new('L', (SW, SH), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, SW - 1, SH - 1), 110, fill=255)
# 화면을 찍은 티: 대비·밝기 낮춤, 색 있는 모아레, 천장 조명 반사, 대각 반사
arr = np.asarray(scr).astype(float) * 0.9 + 14
yy, xx = np.mgrid[0:SH, 0:SW]
for c, ph0 in enumerate((0, 2.1, 4.2)):
    arr[..., c] += 9 * np.sin((xx * 0.97 + yy * 0.26) * 0.62 + ph0) * np.sin((xx * 0.18 - yy * 0.93) * 0.51)
s2 = Image.fromarray(np.clip(arr, 0, 255).astype('uint8')).convert('RGBA')
glare = Image.new('L', (SW, SH), 0); gd = ImageDraw.Draw(glare)
gd.polygon([(SW * 0.5, 0), (SW, 0), (SW, SH * 0.42), (SW * 0.05, SH)], fill=46); gd.ellipse((SW * 0.62, SH * 0.07, SW * 0.92, SH * 0.2), fill=120)
glare = glare.filter(ImageFilter.GaussianBlur(120))
s2 = Image.composite(Image.new('RGBA', (SW, SH), (255, 252, 240, 255)), s2, glare)
phone.paste(s2, (B, B), m)
# 배경(어두운 책상) + 원근·기울기
W, H = 1080, 1350
bg = np.zeros((H, W, 3), float); bg[:] = (92, 70, 52)
yy0, xx0 = np.mgrid[0:H, 0:W]; grain = np.sin(yy0 * 0.045 + np.sin(xx0 * 0.004) * 6) * 9 + np.sin(yy0 * 0.21 + xx0 * 0.002) * 4
bg += grain[..., None] * np.array([1.0, 0.8, 0.6]); bg += np.random.default_rng(1).normal(0, 5, (H, W, 3))
canvas = Image.fromarray(np.clip(bg, 0, 255).astype('uint8')).filter(ImageFilter.GaussianBlur(3)).convert('RGBA')
# 보이는 부분: 머리~말풍선 아래 조금(폰 위아래는 화면 밖으로 잘림)
top_crop = 0; bot = PH   # 11-22 02:19 사용자: 조금 위에서 떨어져서 찍은 느낌 → 폰 전체
ph = phone.crop((0, top_crop, PW, bot))
# 화면이 거의 꽉 차게 → 원근 변형(위쪽이 살짝 좁게, 왼쪽으로 살짝 기울게)
tw = 860; s = tw / ph.width; ph = ph.resize((tw, round(ph.height * s)), Image.LANCZOS)
w0, h0 = ph.size
src = [(0, 0), (w0, 0), (w0, h0), (0, h0)]
dst = [(70, 10), (w0 - 40, 0), (w0 + 18, h0), (-14, h0 - 24)]
def coeffs(pa, pb):
    A = []
    for (x, y), (X, Y) in zip(pa, pb):
        A.append([X, Y, 1, 0, 0, 0, -x * X, -x * Y]); A.append([0, 0, 0, X, Y, 1, -y * X, -y * Y])
    A = np.array(A, float); b = np.array(pa, float).reshape(8)
    return np.linalg.solve(A, b)
ph = ph.transform((w0 + 40, h0 + 20), Image.PERSPECTIVE, coeffs(src, dst), Image.BICUBIC).rotate(-2.4, resample=Image.BICUBIC, expand=False)
ox = (W - ph.width) // 2; oy = 70
# 폰 그림자
sh = Image.new('RGBA', canvas.size, (0, 0, 0, 0)); sh.alpha_composite(Image.new('RGBA', ph.size, (0, 0, 0, 150)), (ox + 18, oy + 26)); shm = ph.split()[3]
shadow = Image.new('RGBA', canvas.size, (0, 0, 0, 0)); shadow.paste(Image.new('RGBA', ph.size, (0, 0, 0, 140)), (ox + 16, oy + 24), shm); canvas.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(22)))
canvas.alpha_composite(ph, (ox, oy))
img = canvas.convert('RGB')
r, g, b2 = img.split(); r = ImageChops.offset(r, 2, 1); b2 = ImageChops.offset(b2, -2, -1); img = Image.merge('RGB', (r, g, b2)).crop((4, 4, W - 4, H - 4)).resize((W, H), Image.BICUBIC)
soft = img.filter(ImageFilter.GaussianBlur(1.0)); blurry = img.filter(ImageFilter.GaussianBlur(3.2))
grad = Image.fromarray((np.clip((np.mgrid[0:H, 0:W][0] - H * 0.55) / (H * 0.45), 0, 1) * 255).astype('uint8'))
img = Image.composite(blurry, soft, grad)
img = img.resize((W // 2, H // 2), Image.BILINEAR).resize((W, H), Image.BICUBIC)
a = np.asarray(img).astype(float); a += np.random.default_rng(2).normal(0, 7, a.shape)
yy, xx = np.mgrid[0:H, 0:W]; v = 1 - 0.32 * (((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2); a *= v[..., None]
a[..., 0] *= 1.04; a[..., 2] *= 0.95
Image.fromarray(np.clip(a, 0, 255).astype('uint8')).save(os.path.join(HERE, 'out', '01.jpg'), quality=78)
print('ok', endy, ph.size)
