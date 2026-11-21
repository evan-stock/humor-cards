"""ㅋㅋ상회 영상 릴스: 성시경 유튜브 채령(ITZY)편 반응 갈림 (2026-11-21, TTS 없음, 원본 소리).
틀: jobs/2026-11-21-selfpark-reel/build.py 복사(주아체 흰색·기울임, 위 검정 띠, 원본 소리). 바꾼 것: 영상 2개를 3구간으로 이어 붙임.
출처: X @jutingstar9999 2124097370573193463 (원 영상 유튜브 성시경 채널). 나이는 성시경 1979년생·채령 2001년생만 씀(트윗의 부모 나이는 미확인이라 안 씀).
"""
import os, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__)); S = os.path.join(HERE, 'src'); ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
F = os.path.join(ROOT, 'fonts'); SFX = os.path.join(ROOT, 'assets', 'sfx')
T = '/tmp/kkssk'; os.makedirs(T, exist_ok=True); os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
W, H, BAND = 1080, 1920, 440; VH = H - BAND
JUA = f'{F}/BMJUA.otf'; PB = f'{F}/Pretendard-Bold.otf'; PX = f'{F}/Pretendard-ExtraBold.otf'; LOGO = os.path.join(ROOT, 'brand', 'logo.png')
YEL = (255, 214, 10)
RV = os.path.join(ROOT, 'jobs', '2026-11-21-sungsikyung-chaeryeong-review', 'src'); LABEL = '영상: 유튜브 성시경 SUNG SI KYUNG'
VY = BAND + 50; VW, VHH = W, 900   # 영상 영역 1080x900 (v01은 가로 맞춤 후 위아래 45px 잘림, v02는 위아래 검정)
CUTS = [('v02', 0.0, 4.5), ('v02', 8.0, 12.5), ('v01', 0.5, 15.0)]   # (파일, 시작, 끝) — 원본 자막 경계에서 자름
SC = [  # (자막, 시작 초, 길이)
    (["79년생 선배가", "01년생 후배한테 한 말"], 0.0, 4.5),
    (["누가 좋아하냐 묻자", "본인이 좋아한다는 채령"], 4.5, 4.5),
    (["열애설 걱정 없어서", "매니저가 안심한다는 말"], 9.0, 4.0),
    (["결혼 안 한 나도", "속상하다는 성시경"], 13.0, 4.5),
    (["근데 채령 받아치는 게", "진짜 웃김"], 17.5, 3.0),
    (["선 넘었다 vs 그냥 예능", "댓글로 싸워주셈"], 20.5, 3.0),
]
SFXS = [('huh', 4.5), ('swoosh_short', 9.0), ('smack', 19.0)]
TITLE = ["성시경 유튜브 채령편", "반응 갈린 이유;;"]
COVER = ["성시경 채령편", "반응 갈림;;"]

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



TOTAL = SC[-1][1] + SC[-1][2]
starts = [x[1] for x in SC]; ends = starts[1:] + [TOTAL]
ins, fc = [], []
for k, (v, s0, s1) in enumerate(CUTS):
    ins += ['-ss', f'{s0}', '-t', f'{s1 - s0}', '-i', os.path.join(RV, v + '.mp4')]
    fc.append(f"[{k}:v]scale={VW}:-2:flags=lanczos,crop={VW}:min(ih\\,{VHH}),pad={VW}:{VHH}:0:(oh-ih)/2:color=0x08080a,fps=30,setsar=1,format=yuv420p[v{k}];"
              f"[{k}:a]aresample=44100,aformat=channel_layouts=stereo,asetpts=PTS-STARTPTS[a{k}]")
fc = ';'.join(fc) + ';' + ''.join(f'[v{k}][a{k}]' for k in range(len(CUTS))) + f'concat=n={len(CUTS)}:v=1:a=1[v][a]'
subprocess.run(['ffmpeg', '-v', 'error', '-y', *ins, '-filter_complex', fc, '-map', '[v]', '-map', '[a]', '-t', f'{TOTAL:.3f}',
                '-c:v', 'libx264', '-crf', '18', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-ar', '44100', '-ac', '2', '-b:a', '160k', f'{T}/body.mp4'], check=True)

top = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(top).rectangle((0, 0, W, BAND), fill=(8, 8, 10, 255))
tl = Image.new('RGBA', (W, H), (0, 0, 0, 0))
jua_lines(tl, TITLE, 104, 285, lh=124, maxw=W - 90, shadow=False)
yc = 285 + 124 / 2 - 104 * 0.35; SH = 0.2
tl = tl.transform((W, H), Image.AFFINE, (1, SH, -SH * yc, 0, 1, 0), Image.BICUBIC)
top.alpha_composite(tl); tag(top)
ImageDraw.Draw(top).text((W - 40, VY - 14), LABEL, font=ImageFont.truetype(PB, 28), fill=(235, 235, 235, 255), anchor='rs', stroke_width=2, stroke_fill=(0, 0, 0, 255))
top.save(f'{T}/top.png')
caps = []
for i, (rows, _, _) in enumerate(SC):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    lh = 118; y = 1490 - lh * (len(rows) - 1) / 2 + 32
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
fc += f';[0:a]loudnorm=I=-15:TP=-1.5[orig]'
mix = ['[orig]']
for j, (_, t0) in enumerate(SFXS):
    fc += f';[{k0 + j}:a]aresample=44100,aformat=channel_layouts=stereo,volume=-8dB,adelay={int(t0 * 1000)}|{int(t0 * 1000)}[x{j}]'; mix.append(f'[x{j}]')
fc += f";{''.join(mix)}amix=inputs={len(mix)}:duration=first:normalize=0,atrim=0:{TOTAL:.3f}[aout]"
out = os.path.join(HERE, 'out', 'reel.mp4')
subprocess.run(['ffmpeg', '-v', 'error', '-y', *inputs, *ains, '-filter_complex', fc, '-map', '[vout]', '-map', '[aout]', '-t', f'{TOTAL:.3f}',
                '-c:v', 'libx264', '-crf', '20', '-preset', 'veryfast', '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', out], check=True)

# 커버: 두 사람이 같이 보이는 장면(v02 9.0초) + 큰 주아체 제목 + 딱지
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', '9.0', '-i', os.path.join(RV, 'v02.mp4'), '-frames:v', '1', '-vf', f'scale={W}:-2', f'{T}/cv.png'], check=True)
cv = Image.new('RGBA', (W, H), (8, 8, 10, 255))
im = Image.open(f'{T}/cv.png').convert('RGBA'); cv.alpha_composite(im, (0, 760))
cl = Image.new('RGBA', (W, H), (0, 0, 0, 0))
jua_lines(cl, COVER, 150, 450, lh=190, maxw=W - 110)
cv.alpha_composite(cl.transform((W, H), Image.AFFINE, (1, 0.2, -0.2 * (450 + 95 - 150 * 0.35), 0, 1, 0), Image.BICUBIC)); tag(cv)
cv.convert('RGB').save(os.path.join(HERE, 'out', 'cover.jpg'), quality=92)
print('ok', round(TOTAL, 2))
