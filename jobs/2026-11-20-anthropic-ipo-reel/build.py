"""ㅋㅋ상회 영상 릴스: 앤트로픽 나스닥 상장식, 축하 영상이 '멸망 영화 도입부 같다'는 X 반응 (2026-11-20).
틀: jobs/2026-11-17-yoondy-reel3/build.py(주아체 흰색·기울임, 위 검정 띠, 움직임 없음, 원본 소리) — 원본 2개를 이어 붙이도록만 바꿈.
src/v01.mp4 = 나스닥 상장식 박수 장면(X @BillyM2k·@TicTocTick 첨부, cardnews media/20261120-anthreact),
src/v02.mp4 = 앤트로픽 공식 X 상장일 영상(2026-11-19, cardnews media/20261120-anthipo). 따옴표는 실제 문구 번역만.
"""
import os, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__)); S = os.path.join(HERE, 'src'); ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
F = os.path.join(ROOT, 'fonts'); SFX = os.path.join(ROOT, 'assets', 'sfx')
T = '/tmp/kkanthipo'; os.makedirs(T, exist_ok=True); os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
W, H, BAND = 1080, 1920, 440; VH = H - BAND
JUA = f'{F}/BMJUA.otf'; PB = f'{F}/Pretendard-Bold.otf'; PX = f'{F}/Pretendard-ExtraBold.otf'; LOGO = os.path.join(ROOT, 'brand', 'logo.png')
YEL = (255, 214, 10)
SRC = {'v01': ('crop=525:720:105:0', "영상: X @BillyM2k 공유"), 'v02': ('crop=788:1080:566:0', '영상: 앤트로픽 공식 X'), 'v02w': ('scale=1080:-2,pad=1080:1480:0:330:black,crop=1080:1480', '영상: 앤트로픽 공식 X')}
SC = [  # (자막, 원본, 시작 초, 길이)
    (["앤트로픽 나스닥 상장식"], 'v01', 0.0, 4.0),
    (["다들 웃으며 박수 치는데"], 'v01', 4.0, 4.0),
    (["X에선", "\"공포영화 같다\" 반응"], 'v01', 8.0, 4.0),
    (["행사장에 튼", "상장 축하 영상"], 'v02', 34.0, 3.6),
    (["인류 멸망 영화", "도입부 아님?"], 'v02', 37.0, 4.4),
    (["\"이 순간을 어떻게 만드느냐가", "이 순간을 만든다\""], 'v02w', 60.0, 6.4),
    (["축하 영상 vs 멸망 예고편", "댓글로 ㄱㄱ"], 'v01', 20.0, 4.0),
]
SFXS = []
TITLE = ["AI 회사 상장 축하 영상", "멸망 영화 도입부 실화냐"]
COVER = ["상장 축하 영상인데", "멸망 영화 같음ㅋㅋㅋ"]

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



TOTAL = sum(x[3] for x in SC)
starts = [sum(x[3] for x in SC[:i]) for i in range(len(SC))]; ends = starts[1:] + [TOTAL]
ENC = ['-c:v', 'libx264', '-crf', '18', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', '-r', '30', '-c:a', 'aac', '-ar', '44100', '-ac', '2', '-b:a', '160k']
clips = []
for i, (_, src, t0, dur) in enumerate(SC):
    out = f'{T}/s{i:02d}.mp4'; crop = SRC[src][0]
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t0:.3f}', '-t', f'{dur:.3f}', '-i', f'{S}/{src[:3]}.mp4', '-filter_complex',
                    f'[0:v]{crop},scale={W}:{VH}:flags=lanczos,fps=30,setsar=1[v];[0:a]aresample=44100,afade=t=in:d=0.05,afade=t=out:st={dur - 0.1:.3f}:d=0.1[a]',
                    '-map', '[v]', '-map', '[a]', '-t', f'{dur:.3f}', *ENC, out], check=True)
    clips.append(out)
open(f'{T}/list.txt', 'w').write(''.join(f"file '{c}'\n" for c in clips))
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'{T}/list.txt', '-c', 'copy', f'{T}/body.mp4'], check=True)

top = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(top).rectangle((0, 0, W, BAND), fill=(8, 8, 10, 255))
tl = Image.new('RGBA', (W, H), (0, 0, 0, 0))
jua_lines(tl, TITLE, 104, 285, lh=124, maxw=W - 90, shadow=False)
yc = 285 + 124 / 2 - 104 * 0.35; SH = 0.2
tl = tl.transform((W, H), Image.AFFINE, (1, SH, -SH * yc, 0, 1, 0), Image.BICUBIC)
top.alpha_composite(tl); tag(top)
top.save(f'{T}/top.png')
caps = []
for i, (rows, src, _, _) in enumerate(SC):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((W - 40, 500), SRC[src][1], font=ImageFont.truetype(PB, 28), fill=(235, 235, 235, 255), anchor='rs', stroke_width=2, stroke_fill=(0, 0, 0, 255))
    lh = 118; y = 1490 - lh * (len(rows) - 1) / 2 + 32
    cl = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    jua_lines(cl, rows, 94, y, lh=lh, maxw=W - 90, shadow=True)
    yc = y + lh * (len(rows) - 1) / 2 - 94 * 0.35
    im.alpha_composite(cl.transform((W, H), Image.AFFINE, (1, 0.2, -0.2 * yc, 0, 1, 0), Image.BICUBIC))
    p = f'{T}/cap{i}.png'; im.save(p); caps.append(p)

inputs = ['-i', f'{T}/body.mp4', '-i', f'{T}/top.png'] + sum((['-i', p] for p in caps), [])
fc = f'color=c=0x08080a:s={W}x{H}:r=30:d={TOTAL:.3f}[bg];[bg][0:v]overlay=0:{BAND}:shortest=1[s0];[s0][1:v]overlay=0:0[s1]'
last = 's1'
for i in range(len(SC)):
    a = 0 if i == 0 else starts[i] - 0.02; b = ends[i] - 0.02
    fc += f";[{last}][{i + 2}:v]overlay=0:0:enable='between(t,{a:.3f},{b:.3f})'[c{i}]"; last = f'c{i}'
fc += f";[{last}]setsar=1,format=yuv420p[vout]"
fc += f';[0:a]loudnorm=I=-15:TP=-1.5,atrim=0:{TOTAL:.3f}[aout]'
ains = []
out = os.path.join(HERE, 'out', 'reel.mp4')
subprocess.run(['ffmpeg', '-v', 'error', '-y', *inputs, *ains, '-filter_complex', fc, '-map', '[vout]', '-map', '[aout]', '-t', f'{TOTAL:.3f}',
                '-c:v', 'libx264', '-crf', '20', '-preset', 'veryfast', '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', out], check=True)

# 커버: 원본 화면(가로 그대로) + 큰 주아체 제목 + 딱지
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', '38.5', '-i', f'{S}/v02.mp4', '-frames:v', '1', '-vf', 'crop=1440:1080:240:0,scale=1080:810', f'{T}/cv.png'], check=True)
cv = Image.new('RGBA', (W, H), (8, 8, 10, 255))
im = Image.open(f'{T}/cv.png').convert('RGBA').resize((W, 810), Image.LANCZOS); cv.alpha_composite(im, (0, 660))
cl = Image.new('RGBA', (W, H), (0, 0, 0, 0))
jua_lines(cl, COVER, 150, 390, lh=190, maxw=W - 110)
cv.alpha_composite(cl.transform((W, H), Image.AFFINE, (1, 0.2, -0.2 * (390 + 95 - 150 * 0.35), 0, 1, 0), Image.BICUBIC)); tag(cv)
cv.convert('RGB').save(os.path.join(HERE, 'out', 'cover.jpg'), quality=92)
print('ok', round(TOTAL, 2))
