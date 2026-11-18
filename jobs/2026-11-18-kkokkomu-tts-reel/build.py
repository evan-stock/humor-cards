"""ㅋㅋ상회: 꼬꼬무 스타일 패러디 '2026년 이O우 사건 편'(가상 시나리오) 사진 + TTS 릴스(2026-11-18).
원작: 인스타 @history.me_me 캐러셀(13장, 사용자 제공 화면 캡처)을 사용자 요청으로 릴스로. 장면은 원작 속 SBS '꼬리에 꼬리를 무는 그날 이야기' 장면(src/*.jpg),
인스타 화면 아이콘·장 번호는 잘라냄. 실존 인물 AI 조커 합성 장(11번)과 흐린 시험지 장(5번)은 쓰지 않음. 실명은 원작처럼 이O우.
내레이션: Gemini TTS Fenrir(꼬꼬무 이야기꾼 반말), 무음 기준 10문장, 2배속. 틀: 2026-11-15-kangsungtae-tts-reel/build.py.
움직임: 사용자 11/17 'ㅋㅋ상회 움직임 빼기' 반영(펀치·확대·첫 흔들림 없음), 바탕 pad(깜박임 방지)."""
import os, subprocess, json
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
S = os.path.join(HERE, 'src'); R = S
T = '/tmp/kkkkm'; os.makedirs(T, exist_ok=True); os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
W, H, BAND = 1080, 1920, 440; VH = H - BAND; INTRO = 0.15
JUA = f'{ROOT}/fonts/BMJUA.otf'; PB = f'{ROOT}/fonts/Pretendard-Bold.otf'; PX = f'{ROOT}/fonts/Pretendard-ExtraBold.otf'
YEL = (255, 214, 10)

# (자막 줄들, 사진 파일, 자르기 [x0,y0,x1,y1] 0~1)
SC = [
    (["그렇게...", "11월 19일이 됐어"], 's02', [0, 0, 1, 1]),
    (["전 국민이 지켜보는", "생중계 시작"], 's04', [0, 0, 1, 1]),
    (["주인공은", "리트 만점자 이O우"], 's02', [0.1, 0, 0.9, 1]),
    (["리트 역사상 만점자", "단 한 명도 없었거든"], 's03a', [0, 0, 1, 1]),
    (["공개한 시험지 보니", "밑줄 하나 없이 풀었대"], 's06', [0, 0, 1, 1]),
    (["수능 국어", "몇 점 나왔을 것 같아?"], 's08', [0, 0, 1, 1]),
    (["65분 만에 전부 맞혀서", "126점!"], 's09', [0, 0, 1, 1]),
    (["그러더니 갑자기", "웃음을 터뜨렸어"], 's10', [0, 0, 1, 1]),
    (["카메라가 꺼지자", "바람처럼 사라졌대"], 's13', [0, 0, 1, 1]),
    (["물론 내일을 상상한 패러디", "진짜 결과는 내일 공개!"], 's03b', [0, 0, 1, 1]),
]
TITLE = ["꼬꼬무 이O우 사건 편", "가상 미리보기ㅋㅋㅋ"]
COVER = ["꼬꼬무", "이O우 사건 편ㅋㅋㅋ"]
SFXS = [('chills', 0, -10), ('dudung', 3, -9), ('huh', 5, -9), ('explosion', 6, -10), ('chills', 8, -9), ('bell', 9, -10)]  # (효과음, 장면, dB)


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
    return Image.open(f'{R}/{n}.jpg').convert('RGB')


# 1) 내레이션을 무음으로 8문장으로 나누기
NARR = f'{S}/a01.mp3'
wav = f'{T}/n.wav'
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', NARR, '-ac', '1', '-ar', '44100', wav], check=True)
# 한 번에 읽은 내레이션이라 문장 사이 무음이 짧다 → 50ms 에너지로 찾은 틈(-32dB 아래) 중 글자 수 비율에 맞는 7곳을 경계로(눈으로 확인)
TOT_A = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', wav], capture_output=True, text=True).stdout)
bounds = [0.0, 3.17, 6.41, 10.09, 14.0, 18.72, 22.93, 27.41, 31.73, 36.53, TOT_A]
GAP = 0.1  # 문장 간격(사용자 11-15: 0.1초)
SPEED = 2.0  # 목소리 2배속(사용자 11-15)
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
PUNCH = "scale={W}:{VH},setsar=1"  # 움직임 없음
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
    vf = f"scale={W}:{VH},fps=30,setsar=1"  # 천천히 확대 없음
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
    src = "원작: 인스타 @history.me_me / SBS 꼬꼬무 장면"
    d.text((W - 40, BAND + 40), src, font=ImageFont.truetype(PB, 26), fill=(225, 225, 225, 255), anchor='rs', stroke_width=2, stroke_fill=(0, 0, 0, 255))
    lh = 118; y = 1560 - lh * (len(rows) - 1) / 2 + 32  # 자막: 흰색만, 기울임(cheat-tts-reel과 같게)
    cl = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    jua_lines(cl, [x.replace('[', '').replace(']', '') for x in rows], 94, y, lh=lh, maxw=W - 90, shadow=True)
    yc = y + lh * (len(rows) - 1) / 2 - 94 * 0.35
    im.alpha_composite(cl.transform((W, H), Image.AFFINE, (1, 0.2, -0.2 * yc, 0, 1, 0), Image.BICUBIC))
    p = f'{T}/cap{i}.png'; im.save(p); caps.append(p)

inputs = ['-i', f'{T}/body.mp4', '-i', f'{T}/top.png'] + sum((['-i', p] for p in caps), [])
fc = f'[0:v]pad={W}:{H}:0:{BAND}:color=0x08080a[s0];[s0][1:v]overlay=0:0[s1]'
last = 's1'
for i in range(len(SC)):
    a = 0 if i == 0 else starts[i] - 0.02; b = ends[i] - 0.02
    fc += f";[{last}][{i + 2}:v]overlay=0:0:enable='between(t,{a:.3f},{b:.3f})'[c{i}]"; last = f'c{i}'
fc += f";[{last}]setsar=1,format=yuv420p[vout]"
n0 = 2 + len(SC); N = len(SC)
SFXD = os.path.join(ROOT, 'assets', 'sfx')
ains = sum((['-i', p] for p in pieces), []) + sum((['-i', f'{SFXD}/{n}.mp3'] for n, _, _ in SFXS), [])
fc += ';' + ';'.join(f'[{n0 + i}:a]adelay={int(starts[i] * 1000)}|{int(starts[i] * 1000)}[a{i}]' for i in range(N))
fc += ';' + ''.join(f'[a{i}]' for i in range(N)) + f'amix=inputs={N}:normalize=0,apad=pad_dur=3,loudnorm=I=-15:TP=-1.5[vo]'
for k, (n, sci, db) in enumerate(SFXS):
    ms = int(max(0, starts[sci] - 0.05) * 1000); fc += f';[{n0 + N + k}:a]adelay={ms}|{ms},volume={db}dB[x{k}]'
fc += ';[vo]' + ''.join(f'[x{k}]' for k in range(len(SFXS))) + f'amix=inputs={1 + len(SFXS)}:normalize=0,alimiter=limit=0.95,apad,atrim=0:{TOTAL:.3f}[aout]'
out = os.path.join(HERE, 'out', 'reel.mp4')
subprocess.run(['ffmpeg', '-v', 'error', '-y', *inputs, *ains, '-filter_complex', fc, '-map', '[vout]', '-map', '[aout]', '-t', f'{TOTAL:.3f}',
                '-c:v', 'libx264', '-crf', '20', '-preset', 'veryfast', '-c:a', 'aac', '-b:a', '160k', '-ar', '44100', '-movflags', '+faststart', out], check=True)

# 4) 커버: 탕탕탕 장면 + 큰 주아체 제목 + 딱지
cv = Image.new('RGBA', (W, H), (8, 8, 10, 255))
im = photo('s09'); s = W / im.width; im = im.resize((W, round(im.height * s)), Image.LANCZOS).convert('RGBA')
cv.alpha_composite(im, (0, 820))
cl = Image.new('RGBA', (W, H), (0, 0, 0, 0))
jua_lines(cl, [x.replace('[', '').replace(']', '') for x in COVER], 150, 470, lh=185, maxw=W - 110)
cv.alpha_composite(cl.transform((W, H), Image.AFFINE, (1, 0.2, -0.2 * (470 + 92 - 150 * 0.35), 0, 1, 0), Image.BICUBIC)); tag(cv)
cv.convert('RGB').save(os.path.join(HERE, 'out', 'cover.jpg'), quality=92)
json.dump({'total': round(TOTAL, 2), 'starts': [round(x, 2) for x in starts]}, open(os.path.join(HERE, 'out', 'timing.json'), 'w'))
print('ok', round(TOTAL, 2))
