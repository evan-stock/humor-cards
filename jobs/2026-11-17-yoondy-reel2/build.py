"""ㅋㅋ상회 영상 릴스: 과학 일타강사 윤도영 'AI 커닝 기댓값이 양수' (2026-11-17).
틀: jobs/2026-11-15-cheat-tts-reel/build_kk.py 그대로(주아체 흰색·기울임 제목/자막, 위 검정 띠 440, 딱지, 펀치 전환).
재게시판(reel2): 화면 움직임 효과 전부 뺌(사용자 요청).
TTS 대신 원본 소리. 원본: 유튜브 윤도영통합과학시스템 'AI 부정행위에 대해'(2026-11-16), cardnews 맥북 도우미로 받음(720p).
대사는 cardnews transcribe(faster-whisper) 단어 시각으로 맞춤. 정치 언급 구간은 쓰지 않음.
"""
import os, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__)); S = os.path.join(HERE, 'src'); ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
F = os.path.join(ROOT, 'fonts'); SFX = os.path.join(ROOT, 'assets', 'sfx')
T = '/tmp/kkyoondy2'; os.makedirs(T, exist_ok=True); os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
W, H, BAND = 1080, 1920, 440; VH = H - BAND
JUA = f'{F}/BMJUA.otf'; PB = f'{F}/Pretendard-Bold.otf'; PX = f'{F}/Pretendard-ExtraBold.otf'; LOGO = os.path.join(ROOT, 'brand', 'logo.png')
YEL = (255, 214, 10)
SS = 80.7  # 원본 시작 초
SC = [  # (자막, 원본 기준 시작 초) — 장면 = 자막 하나, 바뀔 때 펀치
    (["성공해서 의대 가면"], 80.7),
    (["남은 일생이 보장"], 83.6),
    (["실패해도 처벌은", "솜방망이"], 86.3),
    (["도덕적 기준 없는 사람은"], 90.9),
    (["시도 안 할 이유가 없다"], 94.2),
    (["수학으로 말하면"], 98.5),
    (["기댓값이 양수"], 99.8),
]
END = 101.4
SFXS = [('bell', 0.0, -8), ('smack', 86.3, -7), ('huh', 94.2, -9), ('dudung', 99.8, -6)]
TITLE = ["과학 일타강사가 계산한", "AI 커닝 기댓값ㅋㅋㅋ"]
COVER = ["일타강사가 계산한", "커닝 기댓값ㅋㅋㅋ"]
CROP = 'crop=540:720:430:0'  # 1280x720 원본에서 인물 중심 세로 자르기(1080x1480 비율)

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



TOTAL = END - SS
starts = [t - SS for _, t in SC]; ends = starts[1:] + [TOTAL]
PUNCH = "setsar=1"  # 2026-11-17 사용자 요청: 문장마다 화면 움직임(펀치) 없앰
ENC = ['-c:v', 'libx264', '-crf', '18', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', '-r', '30', '-an']
clips = []
for i, (_, t0) in enumerate(SC):
    out = f'{T}/s{i:02d}.mp4'; nf = round(ends[i] * 30) - round(starts[i] * 30)
    vf = f'{CROP},scale={W}:{VH}:flags=lanczos,fps=30,{PUNCH.format(W=W, VH=VH)}'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t0:.3f}', '-t', f'{nf / 30 + 0.2:.3f}', '-i', f'{S}/v01.mp4', '-vf', vf, '-frames:v', str(nf), *ENC, out], check=True)
    clips.append(out)
open(f'{T}/list.txt', 'w').write(''.join(f"file '{c}'\n" for c in clips))
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'{T}/list.txt', '-t', f'{TOTAL:.3f}', *ENC, f'{T}/body.mp4'], check=True)

top = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(top).rectangle((0, 0, W, BAND), fill=(8, 8, 10, 255))
tl = Image.new('RGBA', (W, H), (0, 0, 0, 0))
jua_lines(tl, TITLE, 104, 285, lh=124, maxw=W - 90, shadow=False)
yc = 285 + 124 / 2 - 104 * 0.35; SH = 0.2
tl = tl.transform((W, H), Image.AFFINE, (1, SH, -SH * yc, 0, 1, 0), Image.BICUBIC)
top.alpha_composite(tl); tag(top)
ImageDraw.Draw(top).text((W - 40, 500), "영상: 유튜브 '윤도영통합과학시스템'", font=ImageFont.truetype(PB, 28), fill=(235, 235, 235, 255), anchor='rs', stroke_width=2, stroke_fill=(0, 0, 0, 255))
top.save(f'{T}/top.png')
caps = []
for i, (rows, _) in enumerate(SC):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
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
n0 = 2 + len(SC)
ains = ['-ss', f'{SS:.3f}', '-t', f'{TOTAL:.3f}', '-i', f'{S}/v01.mp4'] + sum((['-i', f'{SFX}/{n}.mp3'] for n, _, _ in SFXS), [])
fc += f';[{n0}:a]afade=t=in:d=0.05,afade=t=out:st={TOTAL - 0.15:.3f}:d=0.15[orig]'
for k, (n, t, db) in enumerate(SFXS):
    ms = int(max(0, t - SS) * 1000); fc += f';[{n0 + 1 + k}:a]adelay={ms}|{ms},volume={db}dB[x{k}]'
fc += ';[orig]' + ''.join(f'[x{k}]' for k in range(len(SFXS))) + f'amix=inputs={1 + len(SFXS)}:normalize=0,alimiter=limit=0.95,apad,atrim=0:{TOTAL:.3f}[aout]'
out = os.path.join(HERE, 'out', 'reel.mp4')
subprocess.run(['ffmpeg', '-v', 'error', '-y', *inputs, *ains, '-filter_complex', fc, '-map', '[vout]', '-map', '[aout]', '-t', f'{TOTAL:.3f}',
                '-c:v', 'libx264', '-crf', '20', '-preset', 'veryfast', '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', out], check=True)

# 커버: 원본 화면(가로 그대로) + 큰 주아체 제목 + 딱지
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', '99.6', '-i', f'{S}/v01.mp4', '-frames:v', '1', '-vf', 'crop=900:700:240:20', f'{T}/cv.png'], check=True)
cv = Image.new('RGBA', (W, H), (8, 8, 10, 255))
im = Image.open(f'{T}/cv.png').convert('RGBA').resize((W, 840), Image.LANCZOS); cv.alpha_composite(im, (0, 640))
cl = Image.new('RGBA', (W, H), (0, 0, 0, 0))
jua_lines(cl, COVER, 150, 390, lh=190, maxw=W - 110)
cv.alpha_composite(cl.transform((W, H), Image.AFFINE, (1, 0.2, -0.2 * (390 + 95 - 150 * 0.35), 0, 1, 0), Image.BICUBIC)); tag(cv)
cv.convert('RGB').save(os.path.join(HERE, 'out', 'cover.jpg'), quality=92)
print('ok', round(TOTAL, 2))
