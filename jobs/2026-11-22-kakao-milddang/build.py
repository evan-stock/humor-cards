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
        for ch in para:
            if d.textlength(line + ch, font=font) > maxw: out.append(line); line = ch
            else: line += ch
        out.append(line)
    return out

def screen():
    s = Image.new('RGB', (SW, SH), BG); d = ImageDraw.Draw(s)
    # 상태 표시줄
    d.text((90, 62), '11:34', font=F(NSM, 46), fill=(20, 20, 20), anchor='lm')
    for i, h in enumerate((14, 20, 27, 34)): d.rounded_rectangle((900 + i * 16, 78 - h, 910 + i * 16, 78), 3, fill=(20, 20, 20))
    d.rounded_rectangle((990, 50, 1062, 80), 9, outline=(20, 20, 20), width=3); d.rounded_rectangle((995, 55, 1040, 75), 5, fill=(20, 20, 20))
    # 대화방 머리
    d.text((70, 170), '‹', font=F(NS, 90), fill=(30, 30, 30), anchor='lm')
    d.text((150, 170), NAME, font=F(NSM, 52), fill=(20, 20, 20), anchor='lm')
    for k, x in enumerate((900, 990, 1080)):
        if k == 0: d.ellipse((x - 22, 148, x + 14, 184), outline=(30, 30, 30), width=5); d.line((x + 10, 180, x + 26, 196), fill=(30, 30, 30), width=5)
        elif k == 2:
            for j in range(3): d.line((x - 24, 156 + j * 14, x + 24, 156 + j * 14), fill=(30, 30, 30), width=5)
        else: d.text((x, 170), '☏', font=F(NS, 56), fill=(30, 30, 30), anchor='mm')
    d.rounded_rectangle((385, 245, 785, 297), 26, fill=(160, 180, 199)); d.text((585, 271), '2026년 10월 6일 월요일 >', font=F(NS, 30), fill=(255, 255, 255), anchor='mm')
    y = 340
    # 손 흔드는 이모티콘(내가 보냄)
    em = Image.new('RGBA', (160, 160), (0, 0, 0, 0)); ImageDraw.Draw(em).text((0, 0), '👋', font=ImageFont.truetype(EMO, 109), embedded_color=True)
    em = em.resize((260, 260), Image.LANCZOS); s.paste(em, (SW - 330, y), em); y += 270
    d.text((SW - 330 - 14, y - 22), '오전 11:29', font=F(NS, 28), fill=(80, 90, 100), anchor='rb')
    f = F(NS, 44); lh = 62
    def bubble(y, text, me, tm):
        maxw = 700; lines = wrap(d, text, f, maxw); w = max(d.textlength(l, font=f) for l in lines) + 64; h = lh * len(lines) + 44
        if me:
            x1 = SW - 50; x0 = x1 - w; d.rounded_rectangle((x0, y, x1, y + h), 34, fill=YEL); d.polygon([(x1 - 6, y + 22), (x1 + 18, y + 14), (x1 - 4, y + 44)], fill=YEL)
            d.text((x0 - 16, y + h), tm, font=F(NS, 28), fill=(80, 90, 100), anchor='rb')
        else:
            d.ellipse((40, y - 60, 148, y + 48), fill=(155, 196, 223)); d.ellipse((76, y - 38, 112, y - 2), fill=WHT); d.chord((62, y + 2, 126, y + 50), 180, 360, fill=WHT)
            d.text((170, y - 46), NAME, font=F(NS, 32), fill=(60, 70, 80), anchor='ls')
            x0 = 170; x1 = x0 + w; d.rounded_rectangle((x0, y - 20, x1, y - 20 + h), 34, fill=WHT); d.polygon([(x0 + 6, y + 2), (x0 - 18, y - 6), (x0 + 4, y + 24)], fill=WHT)
            d.text((x1 + 16, y - 20 + h), tm, font=F(NS, 28), fill=(80, 90, 100), anchor='lb'); y -= 20
        for k, l in enumerate(lines): d.text(((SW - 50 - w + 32) if me else 202, y + 22 + lh * k), l, font=f, fill=(20, 20, 20), anchor='la')
        return y + h
    y = bubble(y + 20, '좀 이상하게 들릴 수 있지만 내가 맨날 일 끝나면 찾아가고 배고프다 하면 음식 사서 문 앞에 걸어두는 거 그런 게 싫은 거야? 아니면 너무 빠르다고 생각하는 거야?', True, '오전 11:31')
    y = bubble(y + 130, '아 아뇨! 전혀 안 이상해요 오빠! 다 설레는 행동인데 그냥 오빠가 찾아오는 게 싫고 오빠가 문 앞에 음식 걸어두는 게 싫고 빠르진 않지만 그냥 오빠가 싫은 거예요!', False, '오전 11:33')
    # 입력창
    d.rectangle((0, SH - 150, SW, SH), fill=(255, 255, 255)); d.rounded_rectangle((150, SH - 125, SW - 150, SH - 35), 45, fill=(242, 242, 242))
    d.text((60, SH - 80), '+', font=F(NS, 70), fill=(120, 120, 120), anchor='mm'); d.text((200, SH - 80), '메시지 입력', font=F(NS, 38), fill=(170, 170, 170), anchor='lm')
    return s, y

scr, endy = screen()
# 폰(검정 테두리 + 둥근 모서리)
B = 46; PW, PH = SW + 2 * B, SH + 2 * B
phone = Image.new('RGBA', (PW, PH), (0, 0, 0, 0)); pd = ImageDraw.Draw(phone)
pd.rounded_rectangle((0, 0, PW - 1, PH - 1), 150, fill=(18, 18, 20)); pd.rounded_rectangle((6, 6, PW - 7, PH - 7), 146, outline=(70, 70, 76), width=4)
m = Image.new('L', (SW, SH), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, SW - 1, SH - 1), 110, fill=255)
# 화면 반사·모아레
s2 = scr.convert('RGBA')
yy, xx = np.mgrid[0:SH, 0:SW]
moire = (np.sin((xx * 0.9 + yy * 0.35) * 0.55) * np.sin((xx * 0.2 - yy * 0.95) * 0.48))
mo = Image.fromarray(((moire * 0.5 + 0.5) * 255).astype('uint8')).convert('L')
s2 = Image.composite(Image.blend(s2, Image.merge('RGBA', (mo, mo, mo, Image.new('L', (SW, SH), 255))), 0.05), s2, Image.new('L', (SW, SH), 255))
glare = Image.new('L', (SW, SH), 0); gd = ImageDraw.Draw(glare); gd.polygon([(SW * 0.55, 0), (SW, 0), (SW, SH * 0.5), (SW * 0.1, SH)], fill=38); glare = glare.filter(ImageFilter.GaussianBlur(160))
s2 = Image.composite(Image.new('RGBA', (SW, SH), (255, 255, 255, 255)), s2, glare)
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
dst = [(34, 0), (w0 - 6, 18), (w0 + 14, h0), (-8, h0 - 12)]
def coeffs(pa, pb):
    A = []
    for (x, y), (X, Y) in zip(pa, pb):
        A.append([X, Y, 1, 0, 0, 0, -x * X, -x * Y]); A.append([0, 0, 0, X, Y, 1, -y * X, -y * Y])
    A = np.array(A, float); b = np.array(pa, float).reshape(8)
    return np.linalg.solve(A, b)
ph = ph.transform((w0 + 40, h0 + 20), Image.PERSPECTIVE, coeffs(src, dst), Image.BICUBIC).rotate(-1.6, resample=Image.BICUBIC, expand=False)
ox = (W - ph.width) // 2; oy = 70
# 폰 그림자
sh = Image.new('RGBA', canvas.size, (0, 0, 0, 0)); sh.alpha_composite(Image.new('RGBA', ph.size, (0, 0, 0, 150)), (ox + 18, oy + 26)); shm = ph.split()[3]
shadow = Image.new('RGBA', canvas.size, (0, 0, 0, 0)); shadow.paste(Image.new('RGBA', ph.size, (0, 0, 0, 140)), (ox + 16, oy + 24), shm); canvas.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(22)))
canvas.alpha_composite(ph, (ox, oy))
img = canvas.convert('RGB').filter(ImageFilter.GaussianBlur(0.7))
# 노이즈·비네팅·살짝 따뜻한 색
a = np.asarray(img).astype(float); a += np.random.default_rng(2).normal(0, 4.5, a.shape)
yy, xx = np.mgrid[0:H, 0:W]; v = 1 - 0.28 * (((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2); a *= v[..., None]
a[..., 0] *= 1.03; a[..., 2] *= 0.97
Image.fromarray(np.clip(a, 0, 255).astype('uint8')).save(os.path.join(HERE, 'out', '01.jpg'), quality=86)
print('ok', endy, ph.size)
