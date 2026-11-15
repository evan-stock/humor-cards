"""ㅋㅋ상회판: 더피드 '세무사 수석 부정행위 방법 펨코에 이미 있었다' TTS 릴스(politea media/20261115-feed-cheat/build2.py)를
같은 장면·내레이션·타이밍으로 다시 렌더하고, 로고·제목·자막 디자인만 ㅋㅋ상회 틀로 바꾼다.
- 왼쪽 위 채널 딱지(brand/logo.png + @kk.sanghoe), 하단 THE FEED 로고 삭제
- 제목·자막: 배민 주아체 흰 글씨 + 검정 외곽선, [대괄호] 강조는 노랑
- 펨코 댓글 캡처·참고 이미지 3장 장면은 원본 파일이 없어 게시된 더피드 릴스에서 그 장면만 잘라 씀(본문 영역만, 자막·로고 제외)
"""
import os, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__)); S = os.path.join(HERE, 'src')
T = '/tmp/kkcheat'; os.makedirs(T, exist_ok=True); os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
W, H, BAND = 1080, 1920, 440; VH = H - BAND; GAP = 0.1; INTRO = 0.2
JUA = f'{S}/BMJUA.otf'; PB = f'{S}/Pretendard-Bold.otf'; PX = f'{S}/Pretendard-ExtraBold.otf'
YEL = (255, 214, 10)

SC = [
    (["세무사 시험 수석", "결국 [경찰 자수]"], ('vid', 16.8)),
    (["160문제 중 [159개] 정답", "'AI 안경' 의혹 받던 사람"], ('img', 'note_cover.jpg')),
    (["안경이 아니라", "[초소형 카메라]"], ('vid', 40)),
    (["찍어서 [AI]로 보내고", "답은 [스마트폰]으로"], ('vid', 60)),
    (["그런데 이 방법", "이미 [펨코]에 있었다"], ('grab',)),
    (["셔츠 단추에 [초소형 카메라]", "귀에는 [초소형 이어폰]"], ('quote', ["초소형카메라(wifi됨)", "[셔츠단추] 뚫어서 달고", "초소형이어폰(쌀알만함)", "[귀속]에 넣은 다음에"])),
    (["사진 찍으면 [AI가 풀고]", "이어폰으로 [정답]"], ('quote', ["5초마다 사진찍어서", "[ai가 풀게]하고", "이어폰으로", "몇번에 [정답] 몇번", "이렇게 나옴."])),
    (["\"3분 뒤 삭제함\"", "다들 [구라]라고 넘겼는데"], ('quote', ["지금까지 비밀이었는데", "이제 그냥 밝힘ㅋ", "", "[3분있다 삭제함]"])),
    (["그게 [진짜]였다"], ('vid', 118)),
    (["쌀알만 한 [무선 이어폰]", "온라인에서 [6만 원대]"], ('grab',)),
    (["방송에서도", "[이 댓글] 그대로 소개"], ('grab',)),
    (["\"공무원 시험엔 [브로커]까지\"", "(커뮤니티 주장)"], ('grab',)),
    (["시험장 전자기기 검사", "[이대로 괜찮을까?]"], ('vid', 166)),
]
GRAB_T = {4: 13.5, 9: 28.0, 10: 31.5, 11: 34.3}
TITLE = ["세무사 수석 부정행위 방법", "[펨코에 이미 있었다]ㄷㄷ"]
COVER = ["세무사 수석 그 방법", "[펨코에 있었다]ㄷㄷ"]


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
    av = Image.open(f'{S}/logo.png').convert('RGBA'); s = max(r / av.width, r / av.height)
    av = av.resize((round(av.width * s), round(av.height * s)), Image.LANCZOS)
    av = av.crop(((av.width - r) // 2, (av.height - r) // 2, (av.width - r) // 2 + r, (av.height - r) // 2 + r))
    m = Image.new('L', (r, r), 0); ImageDraw.Draw(m).ellipse((0, 0, r - 1, r - 1), fill=255)
    layer.paste(av, (x0 + 6, y0 + 6), m)
    d.text((x0 + r + 20, y0 + (r + 12) / 2), t, font=f, fill='white', anchor='lm')


# 내레이션(더피드와 같은 Gemini Fenrir 파일, 같은 무음 정리) → 같은 타이밍
def trim(f, k):
    o = f'{T}/t{k:02d}.wav'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f, '-af',
                    'silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,apad=pad_dur=0.02', o], check=True)
    return o
TTS = [trim(f'{S}/tts4/l{i:02d}.wav', i) for i in range(1, 14)]
dur = [float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f], capture_output=True, text=True).stdout) for f in TTS]
starts = []; t = INTRO
for d_ in dur: starts.append(t); t += d_ + GAP
TOTAL = t + 0.5; ends = starts[1:] + [TOTAL]; seg = [ends[i] - (starts[i] if i else 0) for i in range(len(SC))]

PUNCH = "scale=w='2*trunc(540*max(1,1+0.07*exp(-t*14)))':h=-2:eval=frame,crop={W}:{VH},setsar=1"
ENC = ['-c:v', 'libx264', '-crf', '18', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', '-r', '30', '-an']


def quote_card(lines, i):
    bg = Image.new('RGB', (W, VH), (24, 24, 28)); d = ImageDraw.Draw(bg)
    f = ImageFont.truetype(PB, 64); lh = 92; h = lh * len(lines) + 90; y0 = (890 - h) // 2 + 30
    d.rounded_rectangle((60, y0, W - 60, y0 + h), 26, fill=(250, 250, 250))
    d.text((W / 2, y0 - 24), '펨코 댓글 원문', font=ImageFont.truetype(PB, 30), fill=(170, 170, 178), anchor='ms')
    for k, l in enumerate(lines):
        rs = runs(l); w = sum(d.textlength(s, font=f) for s, _ in rs); x = (W - w) / 2
        for s, on in rs:
            d.text((x, y0 + 95 + lh * k), s, font=f, fill=(230, 40, 30) if on else (20, 20, 22), anchor='ls'); x += d.textlength(s, font=f)
    p = f'{T}/q{i}.png'; bg.save(p); return p


def grab(i):
    """원본 이미지가 없는 장면: 더피드 릴스에서 그 장면 화면(본문 위쪽 890px)만 잘라 온다."""
    p = f'{T}/g{i}.png'  # 더피드 릴스는 장면이 자막보다 늦게 바뀌어(누적 밀림) 눈으로 확인한 시각을 쓴다
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(GRAB_T[i]), '-i', f'{S}/feed_reel.mp4', '-frames:v', '1', p], check=True)
    fr = Image.open(p).convert('RGB').crop((0, BAND, W, BAND + 890))
    bg = Image.new('RGB', (W, VH), (24, 24, 28)); bg.paste(fr, (0, 0)); bg.save(p); return p


# 원본에 박힌 노란 자막·'풀버전은' 딱지를 흐리게 덮는 띠: 가장자리를 부드럽게 해 상자처럼 안 보이게
MASK = f'{T}/mask.png'; _m = Image.new('L', (562, 300), 0); ImageDraw.Draw(_m).rectangle((-60, 70, 622, 245), fill=255)
_m.filter(ImageFilter.GaussianBlur(14)).save(MASK)
clips = []
for i, (_, sc) in enumerate(SC):
    out = f'{T}/s{i:02d}.mp4'; b0 = 0 if i == 0 else starts[i]
    nf = round(ends[i] * 30) - round(b0 * 30); d_ = nf / 30 + 0.2  # 프레임 수로 딱 맞춰 자막과 장면이 같이 바뀌게
    if sc[0] == 'vid':
        vf = f'crop=563:770:78:375,split[a][b];[b]format=rgba,crop=562:300:0:400,boxblur=30:3[bb];movie={MASK},format=gray[m];[bb][m]alphamerge[bm];[a][bm]overlay=0:400,scale={W}:{VH}:flags=lanczos,fps=30,{PUNCH.format(W=W, VH=VH)}'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(sc[1]), '-t', f'{d_:.3f}', '-i', f'{S}/v1.mp4', '-vf', vf, '-frames:v', str(nf), *ENC, out], check=True)
    else:
        if sc[0] == 'img':
            im = Image.open(f'{S}/{sc[1]}').convert('RGB'); r = max(W / im.width, VH / im.height)
            im = im.resize((int(im.width * r), int(im.height * r))); x = (im.width - W) // 2
            img = f'{T}/i{i}.png'; im.crop((x, 0, x + W, VH)).save(img)
        else:
            img = quote_card(sc[1], i) if sc[0] == 'quote' else grab(i)
        vf = (f"scale=2160:-1,zoompan=z='1+0.0008*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={W}x{VH}:fps=30,{PUNCH.format(W=W, VH=VH)}")
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-loop', '1', '-framerate', '30', '-t', f'{d_:.3f}', '-i', img, '-vf', vf, '-frames:v', str(nf), *ENC, out], check=True)
    clips.append(out)
open(f'{T}/list.txt', 'w').write(''.join(f"file '{c}'\n" for c in clips))
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'{T}/list.txt', '-t', f'{TOTAL:.3f}', *ENC, f'{T}/body.mp4'], check=True)

# 위 띠(제목 + 딱지)
top = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(top).rectangle((0, 0, W, BAND), fill=(8, 8, 10, 255))
tl = Image.new('RGBA', (W, H), (0, 0, 0, 0))  # 제목: 더 크게, 강조색 없이 흰색, 기울임(주아체에 이탤릭이 없어 기울여 만듦)
jua_lines(tl, [x.replace('[', '').replace(']', '') for x in TITLE], 104, 285, lh=124, maxw=W - 90, shadow=False)
yc = 285 + 124 / 2 - 104 * 0.35; SH = 0.2
tl = tl.transform((W, H), Image.AFFINE, (1, SH, -SH * yc, 0, 1, 0), Image.BICUBIC)
top.alpha_composite(tl); tag(top); top.save(f'{T}/top.png')
caps = []
for i, (rows, sc) in enumerate(SC):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if sc[0] == 'vid':
        d.text((W - 40, 500), "영상: 유튜브 '이돈호 변호사'", font=ImageFont.truetype(PB, 28), fill=(235, 235, 235, 255), anchor='rs', stroke_width=2, stroke_fill=(0, 0, 0, 255))
    lh = 118; y = 1490 - lh * (len(rows) - 1) / 2 + 32  # 자막: 더 크게, 검정 띠 없이 영상 위에, 흰색만, 기울임
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
fc += f";[{last}]scale=w='2*trunc(540*max(1,1+0.18*exp(-t*8)*cos(t*20)))':h=-2:eval=frame,crop={W}:{H},setsar=1,format=yuv420p[vout]"
n0 = 2 + len(SC); N = len(SC)
ains = sum((['-i', f] for f in TTS), []) + ['-i', f'{S}/boom.mp3', '-i', f'{S}/whoosh2.mp3', '-i', f'{S}/boom.mp3']
fc += ';' + ';'.join(f'[{n0 + i}:a]adelay={int(starts[i] * 1000)}|{int(starts[i] * 1000)}[a{i}]' for i in range(N))
w5 = int((starts[4] - 0.3) * 1000); b9 = int((starts[8] - 0.05) * 1000)
fc += f';[{n0 + N}:a]volume=1.3[x1];[{n0 + N + 1}:a]adelay={w5}|{w5},volume=1.1[x2];[{n0 + N + 2}:a]adelay={b9}|{b9},volume=1.2[x3]'
fc += ';' + ''.join(f'[a{i}]' for i in range(N)) + f'[x1][x2][x3]amix=inputs={N + 3}:normalize=0,apad,atrim=0:{TOTAL:.3f}[aout]'
out = os.path.join(HERE, 'out', 'reel.mp4')
subprocess.run(['ffmpeg', '-v', 'error', '-y', *inputs, *ains, '-filter_complex', fc, '-map', '[vout]', '-map', '[aout]', '-t', f'{TOTAL:.3f}',
                '-c:v', 'libx264', '-crf', '20', '-preset', 'veryfast', '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', out], check=True)

# 커버(ㅋㅋ상회 규칙): 원본 영상의 박힌 글씨(위 제목·아래 '풀버전은') 없는 부분만 + 큰 주아체 제목 + 딱지
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', '17.6', '-i', f'{S}/v1.mp4', '-frames:v', '1', '-vf', 'crop=720:560:0:385', f'{T}/cv.png'], check=True)
cv = Image.new('RGBA', (W, H), (8, 8, 10, 255))
im = Image.open(f'{T}/cv.png').convert('RGBA').resize((W, 840), Image.LANCZOS); cv.alpha_composite(im, (0, 640))
cl = Image.new('RGBA', (W, H), (0, 0, 0, 0))  # 커버 제목도 흰색만 + 기울임
jua_lines(cl, [x.replace('[', '').replace(']', '') for x in COVER], 150, 390, lh=190, maxw=W - 110)
cv.alpha_composite(cl.transform((W, H), Image.AFFINE, (1, 0.2, -0.2 * (390 + 95 - 150 * 0.35), 0, 1, 0), Image.BICUBIC)); tag(cv)
cv.convert('RGB').save(os.path.join(HERE, 'out', 'cover.jpg'), quality=92)
print('ok', round(TOTAL, 2))
