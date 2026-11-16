"""ㅋㅋ상회판: 더피드 '6개월 전 세무사 갤러리 너무 순수했다' TTS 릴스(politea media/20261116-feed-sagal/build.py, src/feed_build.py)를
같은 장면 순서·장면 길이·내레이션(Gemini Fenrir, 더피드와 같은 무음 정리)·효과음 타이밍으로 다시 렌더하고,
디자인·자막만 ㅋㅋ상회 틀(jobs/2026-11-15-cheat-tts-reel/build_kk.py)로 바꾼다.
- 하단 THE FEED 로고·빨간 강조 삭제, 왼쪽 위 @kk.sanghoe 딱지
- 제목·자막·커버: 배민 주아체 흰색만 + 검정 외곽선, 기울임 0.2 (제목 104 / 자막 94 / 커버 150)
- 영상 장면은 build_kk.py와 같은 처리(원본 노란 자막 자리 부드럽게 흐림)
소스: src/v1.mp4(이돈호 변호사 유튜브 쇼츠, cardnews media/20261115-brk/video), src/p1_1·p1_2.jpg(X @zzal_cat 게시 세무사 갤러리 캡처),
src/tts/l01~l10.wav(더피드와 같은 파일), src/boom.mp3·whoosh2.mp3(politea assets/sfx)."""
import os, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..')); S = os.path.join(HERE, 'src')
T = '/tmp/kksagal'; os.makedirs(T, exist_ok=True); os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
W, H, BAND = 1080, 1920, 440; VH = H - BAND; GAP = 0.1; INTRO = 0.2  # 더피드와 같은 값(장면 길이 그대로)
JUA = f'{ROOT}/fonts/BMJUA.otf'; PB = f'{ROOT}/fonts/Pretendard-Bold.otf'; PX = f'{ROOT}/fonts/Pretendard-ExtraBold.otf'
k = 2.05  # 캡처 화면좌표 → 원본(더피드와 같음)

SC = [  # (화면 자막: ㅋㅋ상회 말투, 장면: 더피드와 같은 순서·소스)
    (["올해 5월 세무사 갤러리", "\"왜 갑자기 다들 잘함?\""], ('cmt', 'p1_1.jpg', (0, 0, 2652, round(560 * k)), '세무사 갤러리 캡처 (2026.05.28)')),
    (["합격 난이도가", "코스피처럼 떡상함"], ('quote', ["합격 체감난이도가", "불과 2~3년만에", "코스피마냥 급상승"], '세무사 갤러리 원문')),
    (["새로 온 사람들", "다 허수인 줄 알았대"], ('quote', ["진입하는 인간들", "다 허수라며", "정신승리했잖아"], '세무사 갤러리 원문')),
    (["\"고이다 못해", "석유 됨\" ㅋㅋㅋ"], ('cmt', 'p1_2.jpg', (0, round(190 * k), 3151, round(860 * k)), '댓글 캡처')),
    (["알고 보니 신입들이", "괴물이었다고"], ('quote', ["까고보니", "원래 하던놈들보다", "괴수들이었다 이거네?"], '댓글 원문')),
    (["근데 6개월 뒤", "올해 세무사 수석이"], ('vid', 16.8)),
    (["AI 부정행위", "직접 자백함;;"], ('vid', 118)),
    (["초소형 카메라로 찍고", "AI한테 답 받음"], ('vid', 40)),
    (["그것도 모르고", "다들 자기 탓만 함ㅠㅠ"], ('quote', ["매일 진입글 5개씩", "올라오는거 볼 때마다", "솔직히 섬뜩했어"], '세무사 갤러리 원문')),
    (["너네라면", "눈치챘을 것 같음?"], ('vid', 166)),
]
TITLE = ["6개월 전 세무사 갤러리", "다들 너무 순수했음ㅠㅠ"]
COVER = ["6개월 전 세무갤", "너무 순수했음ㅠㅠ"]


def jua_lines(layer, lines, size, y_first, lh=None, maxw=W - 120, shadow=True):
    """ㅋㅋ상회 글씨(build_kk.py와 같음): 주아체 흰색 + 두꺼운 검정 외곽선 + 그림자. y_first = 첫 줄 baseline"""
    d0 = ImageDraw.Draw(layer)
    while size > 40:
        f = ImageFont.truetype(JUA, size)
        if max(d0.textlength(l, font=f) for l in lines) <= maxw: break
        size -= 2
    f = ImageFont.truetype(JUA, size); st = max(8, round(size * 0.12)); lh = lh or round(size * 1.28)
    def draw(d, dx, dy, fill, sw, sf):
        for n, l in enumerate(lines):
            d.text(((W - d.textlength(l, font=f)) / 2 + dx, y_first + lh * n + dy), l, font=f, fill=fill, anchor='ls', stroke_width=sw, stroke_fill=sf)
    if shadow:
        sh = Image.new('RGBA', layer.size, (0, 0, 0, 0))
        draw(ImageDraw.Draw(sh), 4, 8, (0, 0, 0, 160), st + 4, (0, 0, 0, 160))
        layer.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)))
    d = ImageDraw.Draw(layer)
    draw(d, 0, 0, (0, 0, 0, 255), st + 1, (0, 0, 0, 255))
    draw(d, 0, 0, (255, 255, 255, 255), 0, (0, 0, 0))


def italic(layer, yc, sh=0.2):
    return layer.transform((W, H), Image.AFFINE, (1, sh, -sh * yc, 0, 1, 0), Image.BICUBIC)


def tag(layer):
    """왼쪽 위 채널 딱지(build_kk.py와 같음)"""
    d = ImageDraw.Draw(layer); f = ImageFont.truetype(PX, 34); t = '@kk.sanghoe'; r = 54; x0, y0 = 40, 120
    tw = d.textlength(t, font=f)
    d.rounded_rectangle((x0, y0, x0 + r + 30 + tw + 26, y0 + r + 12), radius=(r + 12) // 2, fill=(0, 0, 0, 150))
    av = Image.open(f'{ROOT}/brand/logo.png').convert('RGBA'); s = max(r / av.width, r / av.height)
    av = av.resize((round(av.width * s), round(av.height * s)), Image.LANCZOS)
    av = av.crop(((av.width - r) // 2, (av.height - r) // 2, (av.width - r) // 2 + r, (av.height - r) // 2 + r))
    m = Image.new('L', (r, r), 0); ImageDraw.Draw(m).ellipse((0, 0, r - 1, r - 1), fill=255)
    layer.paste(av, (x0 + 6, y0 + 6), m)
    d.text((x0 + r + 20, y0 + (r + 12) / 2), t, font=f, fill='white', anchor='lm')


# 내레이션: 더피드와 같은 파일·같은 무음 정리 → 같은 타이밍
def trim(f, n):
    o = f'{T}/t{n:02d}.wav'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f, '-af',
                    'silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,apad=pad_dur=0.02', o], check=True)
    return o
TTS = [trim(f'{S}/tts/l{i:02d}.wav', i) for i in range(1, 11)]
dur = [float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f], capture_output=True, text=True).stdout) for f in TTS]
starts = []; t = INTRO
for d_ in dur: starts.append(t); t += d_ + GAP
TOTAL = t + 0.5; ends = starts[1:] + [TOTAL]

PUNCH = "scale=w='2*trunc(540*max(1,1+0.07*exp(-t*14)))':h=-2:eval=frame,crop={W}:{VH},setsar=1"
ENC = ['-c:v', 'libx264', '-crf', '18', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', '-r', '30', '-an']


def quote_card(lines, i, label):
    """원문 카드(더피드와 같은 배치, 빨간 강조 없이 검정 글씨)"""
    bg = Image.new('RGB', (W, VH), (24, 24, 28)); d = ImageDraw.Draw(bg)
    f = ImageFont.truetype(PB, 64); lh = 92; h = lh * len(lines) + 90; y0 = (890 - h) // 2 + 30
    d.rounded_rectangle((60, y0, W - 60, y0 + h), 26, fill=(250, 250, 250))
    d.text((W / 2, y0 - 24), label, font=ImageFont.truetype(PB, 30), fill=(170, 170, 178), anchor='ms')
    for n, l in enumerate(lines):
        d.text((W / 2, y0 + 95 + lh * n), l, font=f, fill=(20, 20, 22), anchor='ms')
    p = f'{T}/q{i}.png'; bg.save(p); return p


def comment_card(name, box, label, i):
    c = Image.open(f'{S}/{name}').convert('RGB').crop(box)
    s = 1000 / c.width; c = c.resize((1000, int(c.height * s)), Image.LANCZOS)
    if c.height > 780:
        c = c.resize((int(c.width * 780 / c.height), 780), Image.LANCZOS)
    bg = Image.new('RGB', (W, VH), (24, 24, 28)); y = (890 - c.height) // 2 + 25
    bg.paste(c, ((W - c.width) // 2, y)); d = ImageDraw.Draw(bg)
    d.text((W / 2, y - 26), label, font=ImageFont.truetype(PB, 30), fill=(170, 170, 178), anchor='ms')
    p = f'{T}/c{i}.png'; bg.save(p); return p


# 원본에 박힌 노란 자막·'풀버전은' 딱지를 흐리게 덮는 띠(build_kk.py와 같음)
MASK = f'{T}/mask.png'; _m = Image.new('L', (562, 300), 0); ImageDraw.Draw(_m).rectangle((-60, 70, 622, 245), fill=255)
_m.filter(ImageFilter.GaussianBlur(14)).save(MASK)

clips = []
for i, (_, sc) in enumerate(SC):
    out = f'{T}/s{i:02d}.mp4'; b0 = 0 if i == 0 else starts[i]
    nf = round(ends[i] * 30) - round(b0 * 30); d_ = nf / 30 + 0.2  # 프레임 수로 맞춰 자막과 장면이 같이 바뀌게
    if sc[0] == 'vid':
        vf = f'crop=563:770:78:375,split[a][b];[b]format=rgba,crop=562:300:0:400,boxblur=30:3[bb];movie={MASK},format=gray[m];[bb][m]alphamerge[bm];[a][bm]overlay=0:400,scale={W}:{VH}:flags=lanczos,fps=30,{PUNCH.format(W=W, VH=VH)}'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(sc[1]), '-t', f'{d_:.3f}', '-i', f'{S}/v1.mp4', '-vf', vf, '-frames:v', str(nf), *ENC, out], check=True)
    else:
        img = quote_card(sc[1], i, sc[2]) if sc[0] == 'quote' else comment_card(sc[1], sc[2], sc[3], i)
        vf = f"scale=2160:-1,zoompan=z='1+0.0008*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={W}x{VH}:fps=30,{PUNCH.format(W=W, VH=VH)}"
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-loop', '1', '-framerate', '30', '-t', f'{d_:.3f}', '-i', img, '-vf', vf, '-frames:v', str(nf), *ENC, out], check=True)
    clips.append(out)
open(f'{T}/list.txt', 'w').write(''.join(f"file '{c}'\n" for c in clips))
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'{T}/list.txt', '-t', f'{TOTAL:.3f}', *ENC, f'{T}/body.mp4'], check=True)

# 위 띠(제목 + 딱지)
top = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(top).rectangle((0, 0, W, BAND), fill=(8, 8, 10, 255))
tl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); jua_lines(tl, TITLE, 104, 285, lh=124, maxw=W - 90, shadow=False)
top.alpha_composite(italic(tl, 285 + 124 / 2 - 104 * 0.35)); tag(top); top.save(f'{T}/top.png')
caps = []
for i, (rows, sc) in enumerate(SC):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if sc[0] == 'vid':
        d.text((W - 40, 500), "영상: 유튜브 '이돈호 변호사'", font=ImageFont.truetype(PB, 28), fill=(235, 235, 235, 255), anchor='rs', stroke_width=2, stroke_fill=(0, 0, 0, 255))
    lh = 118; y = 1490 - lh * (len(rows) - 1) / 2 + 32
    cl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); jua_lines(cl, rows, 94, y, lh=lh, maxw=W - 90, shadow=True)
    im.alpha_composite(italic(cl, y + lh * (len(rows) - 1) / 2 - 94 * 0.35))
    p = f'{T}/cap{i}.png'; im.save(p); caps.append(p)

inputs = ['-i', f'{T}/body.mp4', '-i', f'{T}/top.png'] + sum((['-i', p] for p in caps), [])
fc = f'color=c=0x08080a:s={W}x{H}:r=30:d={TOTAL:.3f}[bg];[bg][0:v]overlay=0:{BAND}:shortest=1[s0];[s0][1:v]overlay=0:0[s1]'
last = 's1'
for i in range(len(SC)):
    a = 0 if i == 0 else starts[i] - 0.02; b = ends[i] - 0.02
    fc += f";[{last}][{i + 2}:v]overlay=0:0:enable='between(t,{a:.3f},{b:.3f})'[c{i}]"; last = f'c{i}'
fc += f";[{last}]scale=w='2*trunc(540*max(1,1+0.18*exp(-t*8)*cos(t*20)))':h=-2:eval=frame,crop={W}:{H},setsar=1,format=yuv420p[vout]"
n0 = 2 + len(SC); N = len(SC)
ains = sum((['-i', f] for f in TTS), []) + ['-i', f'{S}/boom.mp3', '-i', f'{S}/whoosh2.mp3', '-i', f'{S}/boom.mp3']
fc += ';' + ';'.join(f'[{n0 + i}:a]adelay={int(starts[i] * 1000)}|{int(starts[i] * 1000)}[a{i}]' for i in range(N))
w5 = int((starts[5] - 0.3) * 1000); b9 = int((starts[6] - 0.05) * 1000)  # 효과음 타이밍 더피드와 같음
fc += f';[{n0 + N}:a]volume=1.3[x1];[{n0 + N + 1}:a]adelay={w5}|{w5},volume=1.1[x2];[{n0 + N + 2}:a]adelay={b9}|{b9},volume=1.2[x3]'
fc += ';' + ''.join(f'[a{i}]' for i in range(N)) + f'[x1][x2][x3]amix=inputs={N + 3}:normalize=0,apad,atrim=0:{TOTAL:.3f}[aout]'
out = os.path.join(HERE, 'out', 'reel.mp4')
subprocess.run(['ffmpeg', '-v', 'error', '-y', *inputs, *ains, '-filter_complex', fc, '-map', '[vout]', '-map', '[aout]', '-t', f'{TOTAL:.3f}',
                '-c:v', 'libx264', '-crf', '20', '-preset', 'veryfast', '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', out], check=True)

# 커버(build_kk.py와 같은 틀): 원본 영상의 박힌 글씨 없는 부분 + 큰 주아체 제목(흰색·기울임) + 딱지
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', '17.6', '-i', f'{S}/v1.mp4', '-frames:v', '1', '-vf', 'crop=720:560:0:385', f'{T}/cv.png'], check=True)
cv = Image.new('RGBA', (W, H), (8, 8, 10, 255))
cv.alpha_composite(Image.open(f'{T}/cv.png').convert('RGBA').resize((W, 840), Image.LANCZOS), (0, 640))
cl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); jua_lines(cl, COVER, 150, 390, lh=190, maxw=W - 110)
cv.alpha_composite(italic(cl, 390 + 95 - 150 * 0.35)); tag(cv)
cv.convert('RGB').save(os.path.join(HERE, 'out', 'cover.jpg'), quality=92)
print('ok', round(TOTAL, 2), [round(x, 2) for x in starts])
