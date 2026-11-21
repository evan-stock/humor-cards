"""ㅋㅋ상회 영상 릴스: 추성훈 은퇴전(2026-11-21 블랙컴뱃17, 크리스 리벤에 1-2 판정패) 뒤 케이지 소감 (2026-11-22).
원본: 에펨코리아 포텐 https://www.fmkorea.com/best/10582557900 (조회 35만, 추천 757) 첨부 영상 19.8초(경기장 화면을 찍은 영상).
틀: jobs/2026-11-21-selfpark-reel/build.py(주아체 흰색·기울임, 위 검정 띠, 원본 소리) 복사.
바꾼 것: 위 180px 잘라 남의 워터마크('DAILY FASHION NEWS') 제거, 처음엔 관중석 가족 장면(4.3~6.75초)을 뺐으나 사용자 요청으로 다시 넣어 원본 전체 사용.
사실(기사): 리벤에 1-2 스플릿 판정패, 2010 UFC 116 이후 16년 만의 재대결, 22년 격투기 인생 마무리, 소감 "격투기 인생 XX 재밌었다"(스타뉴스).
"""
import os, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
F = os.path.join(ROOT, 'fonts'); SFX = os.path.join(ROOT, 'assets', 'sfx')
T = '/tmp/kkchoo'; os.makedirs(T, exist_ok=True); os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
W, H, BAND = 1080, 1920, 440; VH = H - BAND
JUA = f'{F}/BMJUA.otf'; PB = f'{F}/Pretendard-Bold.otf'; PX = f'{F}/Pretendard-ExtraBold.otf'; LOGO = os.path.join(ROOT, 'brand', 'logo.png')
YEL = (255, 214, 10)
VID = os.path.join(ROOT, 'jobs', '2026-11-22-choo-review', 'src', 'v01.mp4'); LABEL = '영상: 에펨코리아 (블랙컴뱃17 현장)'
CROP = 'crop=738:734:0:180'; VW = W; VHH = round(734 * W / 738); VY = BAND + 40
PARTS = [(0.0, 19.766)]   # 사용자 요청(11-22 00:50)으로 관중석 가족 장면 포함, 원본 전체
SC = [  # (자막, 시작 초(완성본 기준), 길이)
    (["어제 고척돔 은퇴전", "리벤한테 1-2 판정패"], 0.0, 4.3),
    (["관중석 가족들도", "끝까지 지켜봄"], 4.3, 2.45),
    (["16년 전 UFC에서 졌던", "바로 그 상대였음"], 6.75, 3.7),
    (["22년 격투기 인생", "마지막 경기 끝나고"], 10.45, 3.5),
    (["울컥하다가도", "끝까지 추성훈 그 자체"], 13.95, 3.0),
]
TITLE = ["은퇴전 끝난 추성훈 소감", "\"격투기 인생 ㅅㅂ 재밌었다\""]
COVER = ["추성훈 마지막 소감", "ㅅㅂ 재밌었다ㅠㅠ"]
LAST = (["추성훈다운 마무리 vs", "그래도 이기고 끝냈어야"], 16.95)
SFXS = [('swoosh_short', 6.75), ('dudung', 16.95)]

def runs(line):
    out, cur, on = [], '', False
    for ch in line:
        if ch in '[]':
            if cur: out.append((cur, on))
            cur, on = '', ch == '['; continue
        cur += ch
    if cur: out.append((cur, on))
    return out


def jua_lines(layer, lines, size, y_first, lh=None, maxw=W - 120, shadow=True):
    """ㅋㅋ상회 글씨: 주아체 흰색(강조 노랑) + 두꺼운 검정 외곽선 + 그림자. y_first = 첫 줄 글자 아래(baseline)"""
    d0 = ImageDraw.Draw(layer)
    while size > 40:
        f = ImageFont.truetype(JUA, size)
        if max(sum(d0.textlength(s, font=f) for s, _ in runs(l)) for l in lines) <= maxw: break
        size -= 2
    f = ImageFont.truetype(JUA, size); st = max(8, round(size * 0.12)); lh = lh or round(size * 1.28)
    def draw(d, dx, dy, color_fn, sw, sf):
        for k, l in enumerate(lines):
            rs = runs(l); w = sum(d.textlength(s, font=f) for s, _ in rs); x = (W - w) / 2 + dx
            for s, on in rs:
                d.text((x, y_first + lh * k + dy), s, font=f, fill=color_fn(on), anchor='ls', stroke_width=sw, stroke_fill=sf)
                x += d.textlength(s, font=f)
    if shadow:
        sh = Image.new('RGBA', layer.size, (0, 0, 0, 0))
        draw(ImageDraw.Draw(sh), 4, 8, lambda on: (0, 0, 0, 160), st + 4, (0, 0, 0, 160))
        layer.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)))
    d = ImageDraw.Draw(layer)
    draw(d, 0, 0, lambda on: (0, 0, 0, 255), st + 1, (0, 0, 0, 255))
    draw(d, 0, 0, lambda on: YEL if on else (255, 255, 255), 1, YEL)
    # 강조 아닌 글자의 1px 외곽선은 흰색이어야 해서 한 번 더
    draw(d, 0, 0, lambda on: YEL if on else (255, 255, 255), 0, (0, 0, 0))


def tag(layer):
    """왼쪽 위 채널 딱지(humor-cards render_reel.tag_layer와 같은 모양)"""
    d = ImageDraw.Draw(layer); f = ImageFont.truetype(PX, 34); t = '@kk.sanghoe'; r = 54; x0, y0 = 40, 120
    tw = d.textlength(t, font=f)
    d.rounded_rectangle((x0, y0, x0 + r + 30 + tw + 26, y0 + r + 12), radius=(r + 12) // 2, fill=(0, 0, 0, 150))
    av = Image.open(LOGO).convert('RGBA'); s = max(r / av.width, r / av.height)
    av = av.resize((round(av.width * s), round(av.height * s)), Image.LANCZOS)
    av = av.crop(((av.width - r) // 2, (av.height - r) // 2, (av.width - r) // 2 + r, (av.height - r) // 2 + r))
    m = Image.new('L', (r, r), 0); ImageDraw.Draw(m).ellipse((0, 0, r - 1, r - 1), fill=255)
    layer.paste(av, (x0 + 6, y0 + 6), m)
    d.text((x0 + r + 20, y0 + (r + 12) / 2), t, font=f, fill='white', anchor='lm')



TOTAL = sum(b - a for a, b in PARTS)
SC = SC + [(LAST[0], LAST[1], TOTAL - LAST[1])]
starts = [x[1] for x in SC]; ends = starts[1:] + [TOTAL]
segs = []
for i, (a, b) in enumerate(PARTS):
    o = f'{T}/p{i}.mp4'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{a:.3f}', '-t', f'{b - a:.3f}', '-i', VID, '-filter_complex',
                    f'[0:v]{CROP},scale={VW}:{VHH}:flags=lanczos,fps=30,setsar=1[v];[0:a]aresample=44100,afade=t=in:d=0.04,afade=t=out:st={b - a - 0.06:.3f}:d=0.06[a]',
                    '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-crf', '18', '-preset', 'veryfast', '-pix_fmt', 'yuv420p',
                    '-c:a', 'aac', '-ar', '44100', '-ac', '2', '-b:a', '160k', o], check=True)
    segs.append(o)
open(f'{T}/list.txt', 'w').write(''.join(f"file '{s}'\n" for s in segs))
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'{T}/list.txt', '-c', 'copy', f'{T}/body.mp4'], check=True)

top = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(top).rectangle((0, 0, W, BAND), fill=(8, 8, 10, 255))
tl = Image.new('RGBA', (W, H), (0, 0, 0, 0))
jua_lines(tl, TITLE, 104, 285, lh=124, maxw=W - 90, shadow=False)
yc = 285 + 124 / 2 - 104 * 0.35; SH = 0.2
tl = tl.transform((W, H), Image.AFFINE, (1, SH, -SH * yc, 0, 1, 0), Image.BICUBIC)
top.alpha_composite(tl); tag(top)
ImageDraw.Draw(top).text((W - 40, VY - 10), LABEL, font=ImageFont.truetype(PB, 28), fill=(235, 235, 235, 255), anchor='rs', stroke_width=2, stroke_fill=(0, 0, 0, 255))
top.save(f'{T}/top.png')
caps = []
for i, (rows, _, _) in enumerate(SC):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    lh = 118; y = 1640 - lh * (len(rows) - 1) / 2 + 32
    cl = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    jua_lines(cl, rows, 94, y, lh=lh, maxw=W - 90, shadow=True)
    yc = y + lh * (len(rows) - 1) / 2 - 94 * 0.35
    im.alpha_composite(cl.transform((W, H), Image.AFFINE, (1, 0.2, -0.2 * yc, 0, 1, 0), Image.BICUBIC))
    p = f'{T}/cap{i}.png'; im.save(p); caps.append(p)

inputs = ['-i', f'{T}/body.mp4', '-i', f'{T}/top.png'] + sum((['-i', p] for p in caps), [])
fc = f'color=c=0x08080a:s={W}x{H}:r=30:d={TOTAL:.3f}[bg];[bg][0:v]overlay=0:{VY}:shortest=1[s0];[s0][1:v]overlay=0:0[s1]'
last = 's1'
for i in range(len(SC)):
    a = 0 if i == 0 else starts[i] - 0.02; b = ends[i] - 0.02
    fc += f";[{last}][{i + 2}:v]overlay=0:0:enable='between(t,{a:.3f},{b:.3f})'[c{i}]"; last = f'c{i}'
fc += f";[{last}]setsar=1,format=yuv420p[vout]"
ains = sum((['-i', f'{SFX}/{n}.mp3'] for n, _ in SFXS), [])
k0 = 2 + len(caps)
fc += ';[0:a]loudnorm=I=-15:TP=-1.5,aresample=44100,aformat=channel_layouts=stereo,apad[orig]'
mix = ['[orig]']
for j, (_, t0) in enumerate(SFXS):
    fc += f';[{k0 + j}:a]aresample=44100,aformat=channel_layouts=stereo,volume=-8dB,adelay={int(t0 * 1000)}|{int(t0 * 1000)}[x{j}]'; mix.append(f'[x{j}]')
fc += f";{''.join(mix)}amix=inputs={len(mix)}:duration=longest:normalize=0,atrim=0:{TOTAL:.3f}[aout]"
out = os.path.join(HERE, 'out', 'reel.mp4')
subprocess.run(['ffmpeg', '-v', 'error', '-y', *inputs, *ains, '-filter_complex', fc, '-map', '[vout]', '-map', '[aout]', '-t', f'{TOTAL:.3f}',
                '-c:v', 'libx264', '-crf', '20', '-preset', 'veryfast', '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', out], check=True)

# 커버: 얼굴 크게 잡힌 장면(18.6초) + 큰 주아체 제목
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', '16.9', '-i', VID, '-frames:v', '1', '-vf', f'{CROP},scale={W}:{VHH}', f'{T}/cv.png'], check=True)
cv = Image.new('RGBA', (W, H), (8, 8, 10, 255))
im = Image.open(f'{T}/cv.png').convert('RGBA'); cv.alpha_composite(im, (0, 680))
cl = Image.new('RGBA', (W, H), (0, 0, 0, 0))
jua_lines(cl, COVER, 150, 390, lh=190, maxw=W - 110)
cv.alpha_composite(cl.transform((W, H), Image.AFFINE, (1, 0.2, -0.2 * (390 + 95 - 150 * 0.35), 0, 1, 0), Image.BICUBIC)); tag(cv)
cv.convert('RGB').save(os.path.join(HERE, 'out', 'cover.jpg'), quality=92)
print('ok', round(TOTAL, 2))
