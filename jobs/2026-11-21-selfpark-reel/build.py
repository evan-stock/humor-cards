"""ㅋㅋ상회 영상 릴스: 중국 안후이 지하주차장, 빈 전기차가 밤새 혼자 868번 주차 시도 (2026-11-21).
틀: jobs/2026-11-20-anthropic-ipo-reel/build.py(주아체 흰색·기울임, 위 검정 띠, 움직임 없음, 원본 소리) 복사.
바꾼 것: 원본 1개(가로 1280x1100)를 위 240px 잘라(남의 영어 제목 상자 제거) 가로 맞춤, 'ANHUI PROVINCE' 딱지 흐림 패치, 장면 전환 효과음 3개.
사실: 868번 = NEXTA(X @nexta_tv) 게시글. 배경 = CarNewsChina(2026-11) — 화웨이 첸쿤 주차 부문 대회(10/31~11/13, 성공 횟수 순위),
차주들이 순위 올리려 반복했다는 SNS 글, 새벽(22시~6시)은 집계 제외. 이 차가 대회 참가 차인지는 확인 안 됨 → 자막은 '~하던 중'으로만.
"""
import os, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__)); S = os.path.join(HERE, 'src'); ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
F = os.path.join(ROOT, 'fonts'); SFX = os.path.join(ROOT, 'assets', 'sfx')
T = '/tmp/kkselfpark'; os.makedirs(T, exist_ok=True); os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
W, H, BAND = 1080, 1920, 440; VH = H - BAND
JUA = f'{F}/BMJUA.otf'; PB = f'{F}/Pretendard-Bold.otf'; PX = f'{F}/Pretendard-ExtraBold.otf'; LOGO = os.path.join(ROOT, 'brand', 'logo.png')
YEL = (255, 214, 10)
VID = os.path.join(ROOT, 'jobs', '2026-11-21-selfpark-review', 'src', 'v01.mp4'); LABEL = '영상: X @nexta_tv'
VY = BAND + 70; VW, VHH = W, round(860 * W / 1280)   # 영상 놓는 위치·크기(위 240px 잘라 1280x860 → 1080x726)
SC = [  # (자막, 시작 초, 길이)
    (["주인은 자는 새벽 3시", "빈 차가 혼자 움직임"], 0.0, 3.0),
    (["넣었다 뺐다 넣었다 뺐다", "밤새 868번"], 3.0, 3.0),
    (["알고 보니 그때 화웨이가", "주차 횟수 대회 하던 중"], 6.0, 3.2),
    (["근데 새벽 주차는", "점수에도 안 들어감ㅋㅋㅋ"], 9.2, 3.0),
    (["차 고장 vs 주인 욕심", "댓글로 ㄱㄱ"], 12.2, 3.05),
]
SFXS = [('dudung', 3.0), ('tiring', 6.0), ('buzz_wrong', 9.2)]   # (파일, 시각) — 원본 소리보다 -8dB 안팎
TITLE = ["주인 자는 동안 전기차가", "혼자 868번 주차함ㅋㅋㅋ"]
COVER = ["빈 차가 밤새", "868번 주차함ㅋㅋㅋ"]

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
# 영상: 위 240px(남의 제목 상자·천장) 잘라 가로 맞춤, 'ANHUI PROVINCE, CHINA' 딱지(7.0~11.05초)는 부드러운 흐림 패치로 지움
MASK = f'{T}/mask.png'; _m = Image.new('L', (620, 380), 0); ImageDraw.Draw(_m).rounded_rectangle((22, 22, 598, 358), 70, fill=255)
_m.filter(ImageFilter.GaussianBlur(10)).save(MASK)
vf = (f"[0:v]split[a][b];[b]crop=620:380:330:485,boxblur=45:5[bb];movie={MASK},format=gray[m];[bb]format=rgba[bb2];[bb2][m]alphamerge[bm];"
      f"[a][bm]overlay=330:485:enable='between(t,7.0,11.05)',crop=1280:860:0:240,"
      f"scale={VW}:{VHH}:flags=lanczos,fps=30,setsar=1[v]")
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', VID, '-filter_complex', vf + f';[0:a]aresample=44100,atrim=0:{TOTAL:.3f}[a]',
                '-map', '[v]', '-map', '[a]', '-t', f'{TOTAL:.3f}', '-c:v', 'libx264', '-crf', '18', '-preset', 'veryfast', '-pix_fmt', 'yuv420p',
                '-c:a', 'aac', '-ar', '44100', '-ac', '2', '-b:a', '160k', f'{T}/body.mp4'], check=True)

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

# 커버: 차가 크게 보이는 장면(4.6초, 위 240 잘라 가로) + 큰 주아체 제목 + 딱지
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', '4.6', '-i', VID, '-frames:v', '1', '-vf', f'crop=1280:860:0:240,scale={W}:{VHH}', f'{T}/cv.png'], check=True)
cv = Image.new('RGBA', (W, H), (8, 8, 10, 255))
im = Image.open(f'{T}/cv.png').convert('RGBA'); cv.alpha_composite(im, (0, 700))
cl = Image.new('RGBA', (W, H), (0, 0, 0, 0))
jua_lines(cl, COVER, 150, 390, lh=190, maxw=W - 110)
cv.alpha_composite(cl.transform((W, H), Image.AFFINE, (1, 0.2, -0.2 * (390 + 95 - 150 * 0.35), 0, 1, 0), Image.BICUBIC)); tag(cv)
cv.convert('RGB').save(os.path.join(HERE, 'out', 'cover.jpg'), quality=92)
print('ok', round(TOTAL, 2))
