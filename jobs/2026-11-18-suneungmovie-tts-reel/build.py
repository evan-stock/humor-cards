"""ㅋㅋ상회: '2028 영화 <수능>' 가상 캐스팅 짤 사진 + TTS 릴스.
사진 7장(X @thsozvi 2122570361015583151 첨부, cardnews media/20261117-thsozvi/video) + 내레이션 1개(src/a01.mp3, Gemini Fenrir)를
무음 기준으로 9문장으로 나눠 장면마다 붙인다. 디자인은 kangsungtae-tts-reel/build.py(= cheat-tts-reel/build_kk.py 틀) 그대로.
2026-11-17 사용자: 릴스는 움직임·깜박임 없이 → 확대·펀치·첫 프레임 흔들림 없음(컷만).
커뮤니티 글쓴이 닉네임은 흐리게 가린다.
"""
import os, subprocess, json, re
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
S = os.path.join(HERE, 'src'); R = S; SFX = os.path.join(ROOT, 'assets', 'sfx')
T = '/tmp/kkcast'; os.makedirs(T, exist_ok=True); os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
W, H, BAND = 1080, 1920, 440; VH = H - BAND; INTRO = 0.15
JUA = f'{ROOT}/fonts/BMJUA.otf'; PB = f'{ROOT}/fonts/Pretendard-Bold.otf'; PX = f'{ROOT}/fonts/Pretendard-ExtraBold.otf'
YEL = (255, 214, 10)

# (자막 줄들, 사진 번호, 자르기 [x0,y0,x1,y1] 0~1)
SC = [
    (["AI 부정행위 난리에", "영화 캐스팅 짜옴ㅋㅋ"], 1, [0, 0, 1, 0.8]),
    (["부정행위 쫓는 형사", "황정민"], 1, [0, 0.3, 1, 1]),
    (["매일 배웅해주는 딸", "예승이"], 2, [0, 0, 1, 1]),
    (["냉혈한 수사관", "김혜수"], 3, [0, 0, 1, 1]),
    (["수능 밀어붙이는 정치인", "이경영"], 4, [0, 0, 1, 1]),
    (["아들 입학에 진심인 친구", "정석용"], 5, [0, 0, 1, 1]),
    (["직접 봤다는 감독위원", "조우진"], 6, [0, 0, 1, 0.9]),
    (["그리고 정체불명의 인물", "임시완"], 7, [0, 0, 1, 1]),
    (["본다 vs 안 본다", "댓글로 ㄱㄱ"], 1, [0, 0, 1, 0.8]),
]
NARR_LINES = ["요즘 AI 부정행위 난리에, 누가 영화 캐스팅을 짜왔습니다.", "수능 부정행위를 쫓는 강력팀 형사, 황정민.", "매일 아침 배웅해주는 딸, 예승이.",
              "이성으로 판단하는 냉혈한 수사관, 김혜수.", "수능을 예정대로 밀어붙이는 정치인, 이경영.", "아들 입학이라면 뭐든 하는 친구, 정석용.",
              "시험장에서 직접 봤다는 감독위원, 조우진.", "그리고, 정체를 알 수 없는 인물, 임시완.", "이 영화, 본다 안 본다, 댓글로 골라주세요."]
TITLE = ["2028년 개봉 영화 수능", "캐스팅 벌써 떴음ㅋㅋㅋ"]
COVER = ["영화 수능", "캐스팅 떴음ㅋㅋㅋ"]
BLUR1 = [(30, 95, 245, 145)]  # 1번 사진: 글쓴이 닉네임
SFXS = [('bell', 0, -9), ('dudung', 7, -7)]  # (이름, 장면 번호, dB)
BOUNDS = None  # 눈으로 고친 경계가 있으면 여기에


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
    draw(d, 0, 0, lambda on: YEL if on else (255, 255, 255), 0, (0, 0, 0))


def tag(layer):
    d = ImageDraw.Draw(layer); f = ImageFont.truetype(PX, 34); t = '@kk.sanghoe'; r = 54; x0, y0 = 40, 120
    tw = d.textlength(t, font=f)
    d.rounded_rectangle((x0, y0, x0 + r + 30 + tw + 26, y0 + r + 12), radius=(r + 12) // 2, fill=(0, 0, 0, 150))
    av = Image.open(f'{ROOT}/brand/logo.png').convert('RGBA'); s = max(r / av.width, r / av.height)
    av = av.resize((round(av.width * s), round(av.height * s)), Image.LANCZOS)
    av = av.crop(((av.width - r) // 2, (av.height - r) // 2, (av.width - r) // 2 + r, (av.height - r) // 2 + r))
    m = Image.new('L', (r, r), 0); ImageDraw.Draw(m).ellipse((0, 0, r - 1, r - 1), fill=255)
    layer.paste(av, (x0 + 6, y0 + 6), m)
    d.text((x0 + r + 20, y0 + (r + 12) / 2), t, font=f, fill='white', anchor='lm')


def photo(n):
    im = Image.open(f'{R}/{n:02d}.jpg').convert('RGB')
    if n == 1:
        for b in BLUR1:
            im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(9)), b[:2])
    return im


# 1) 내레이션을 무음으로 8문장으로 나누기
NARR = f'{S}/a01.mp3'
wav = f'{T}/n.wav'
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', NARR, '-ac', '1', '-ar', '44100', wav], check=True)
# 한 번에 읽은 내레이션이라 문장 사이 무음이 짧다 → 50ms 에너지로 찾은 틈(-32dB 아래) 중 글자 수 비율에 맞는 7곳을 경계로(눈으로 확인)
TOT_A = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', wav], capture_output=True, text=True).stdout)
def auto_bounds():
    r = subprocess.run(['ffmpeg', '-i', wav, '-af', 'silencedetect=n=-35dB:d=0.08', '-f', 'null', '-'], capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', r)]; en = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', r)]
    gaps = [((a + b) / 2, b - a) for a, b in zip(st, en) if a > 0.3 and b < TOT_A - 0.3]
    n = [len(x.replace(' ', '')) for x in NARR_LINES]; cum = 0; out = [0.0]
    for k in n[:-1]:
        cum += k; exp = TOT_A * cum / sum(n)
        c = [g for g in gaps if abs(g[0] - exp) < 1.6 and g[0] > out[-1] + 0.8]
        g = max(c, key=lambda g: g[1] - 0.25 * abs(g[0] - exp)) if c else (exp, 0)
        out.append(round(g[0], 2))
    print('gaps', [(round(a, 2), round(b, 2)) for a, b in gaps])
    return out + [TOT_A]
bounds = BOUNDS + [TOT_A] if BOUNDS else auto_bounds()
print('bounds', bounds)
GAP = 0.1  # 문장 간격(사용자 11-15: 0.1초)
SPEED = float(os.environ.get('SPEED', '1.35'))  # Gemini Fenrir는 원래 빠르게 읽어 2배속 대신 길이 20초 안팎에 맞춤
pieces, starts, t = [], [], INTRO
for i in range(len(SC)):
    a, b = bounds[i], bounds[i + 1]
    p = f'{T}/p{i}.wav'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{a:.3f}', '-to', f'{b:.3f}', '-i', wav, '-af',
                    f'silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,atempo={SPEED}', p], check=True)
    d_ = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p], capture_output=True, text=True).stdout)
    pieces.append(p); starts.append(t); t += d_ + GAP
TOTAL = t + 0.6; ends = starts[1:] + [TOTAL]
print('길이', round(TOTAL, 2), [round(x, 2) for x in starts])

# 2) 장면(사진 + 천천히 확대 + 펀치 인)
PUNCH = "scale=w='2*trunc(540*max(1,1+0.06*exp(-t*14)))':h=-2:eval=frame,crop={W}:{VH},setsar=1"
ENC = ['-c:v', 'libx264', '-crf', '18', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', '-r', '30', '-an']
clips = []
for i, (_, n, cr) in enumerate(SC):
    im = photo(n); x0, y0, x1, y1 = cr
    im = im.crop((round(x0 * im.width), round(y0 * im.height), round(x1 * im.width), round(y1 * im.height)))
    bg = Image.new('RGB', (W, VH), (14, 14, 16))
    # 흐린 배경 + 가운데 사진(폭 1000, 위아래는 자막 자리 남김)
    blur = im.resize((W, VH)).filter(ImageFilter.GaussianBlur(40)); bg.paste(blur, (0, 0))
    bg = Image.blend(bg, Image.new('RGB', (W, VH), (0, 0, 0)), 0.55)
    box_w, box_h = 1000, 860; s = min(box_w / im.width, box_h / im.height)
    ph = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    m = Image.new('L', ph.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, ph.width - 1, ph.height - 1), 22, fill=255)
    px, py = (W - ph.width) // 2, 60 + (box_h - ph.height) // 2
    bg.paste(ph, (px, py), m)
    img = f'{T}/i{i}.png'; bg.save(img)
    b0 = 0 if i == 0 else starts[i]; nf = round(ends[i] * 30) - round(b0 * 30)
    vf = f"scale={W}:{VH},fps=30,setsar=1"  # 움직임 없음(사용자 11-17)
    out = f'{T}/s{i:02d}.mp4'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-loop', '1', '-framerate', '30', '-t', f'{nf / 30 + 0.2:.3f}', '-i', img, '-vf', vf, '-frames:v', str(nf), *ENC, out], check=True)
    clips.append(out)
open(f'{T}/list.txt', 'w').write(''.join(f"file '{c}'\n" for c in clips))
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'{T}/list.txt', '-t', f'{TOTAL:.3f}', *ENC, f'{T}/body.mp4'], check=True)

# 3) 위 띠(제목 + 딱지), 장면별 자막
top = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(top).rectangle((0, 0, W, BAND), fill=(8, 8, 10, 255))
tl = Image.new('RGBA', (W, H), (0, 0, 0, 0))  # 제목: 강조색 없이 흰색, 기울임(cheat-tts-reel과 같게)
jua_lines(tl, [x.replace('[', '').replace(']', '') for x in TITLE], 104, 285, lh=124, maxw=W - 90, shadow=False)
yc = 285 + 124 / 2 - 104 * 0.35; SH = 0.2
top.alpha_composite(tl.transform((W, H), Image.AFFINE, (1, SH, -SH * yc, 0, 1, 0), Image.BICUBIC)); tag(top); top.save(f'{T}/top.png')
caps = []
for i, (rows, n, _) in enumerate(SC):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    src = "사진: X @thsozvi"
    d.text((W - 40, BAND + 40), src, font=ImageFont.truetype(PB, 26), fill=(225, 225, 225, 255), anchor='rs', stroke_width=2, stroke_fill=(0, 0, 0, 255))
    lh = 118; y = 1560 - lh * (len(rows) - 1) / 2 + 32  # 자막: 흰색만, 기울임(cheat-tts-reel과 같게)
    cl = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    jua_lines(cl, [x.replace('[', '').replace(']', '') for x in rows], 94, y, lh=lh, maxw=W - 90, shadow=True)
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
n0 = 2 + len(SC); N = len(SC)
ains = sum((['-i', p] for p in pieces), []) + sum((['-i', f'{SFX}/{n}.mp3'] for n, _, _ in SFXS), [])
fc += ';' + ';'.join(f'[{n0 + i}:a]adelay={int(starts[i] * 1000)}|{int(starts[i] * 1000)}[a{i}]' for i in range(N))
fc += ';' + ''.join(f'[a{i}]' for i in range(N)) + f'amix=inputs={N}:normalize=0,loudnorm=I=-15:TP=-1.5[narr]'
for k, (n, sc_i, db) in enumerate(SFXS):
    ms = int(starts[sc_i] * 1000) if sc_i else 0
    fc += f';[{n0 + N + k}:a]volume={db}dB,adelay={ms}|{ms}[x{k}]'
fc += ';[narr]' + ''.join(f'[x{k}]' for k in range(len(SFXS))) + f'amix=inputs={1 + len(SFXS)}:normalize=0,alimiter=limit=0.95,apad,atrim=0:{TOTAL:.3f}[aout]'
out = os.path.join(HERE, 'out', 'reel.mp4')
subprocess.run(['ffmpeg', '-v', 'error', '-y', *inputs, *ains, '-filter_complex', fc, '-map', '[vout]', '-map', '[aout]', '-t', f'{TOTAL:.3f}',
                '-c:v', 'libx264', '-crf', '20', '-preset', 'veryfast', '-c:a', 'aac', '-b:a', '160k', '-ar', '44100', '-movflags', '+faststart', out], check=True)

# 4) 커버: 5번 사진(AI 안경 은퇴) + 큰 주아체 제목 + 딱지
cv = Image.new('RGBA', (W, H), (8, 8, 10, 255))
im = photo(1); s = W / im.width; im = im.resize((W, round(im.height * s)), Image.LANCZOS).convert('RGBA')
cv.alpha_composite(im, (0, 820))
cl = Image.new('RGBA', (W, H), (0, 0, 0, 0))
jua_lines(cl, [x.replace('[', '').replace(']', '') for x in COVER], 150, 470, lh=185, maxw=W - 110)
cv.alpha_composite(cl.transform((W, H), Image.AFFINE, (1, 0.2, -0.2 * (470 + 92 - 150 * 0.35), 0, 1, 0), Image.BICUBIC)); tag(cv)
cv.convert('RGB').save(os.path.join(HERE, 'out', 'cover.jpg'), quality=92)
json.dump({'total': round(TOTAL, 2), 'starts': [round(x, 2) for x in starts]}, open(os.path.join(HERE, 'out', 'timing.json'), 'w'))
print('ok', round(TOTAL, 2))
