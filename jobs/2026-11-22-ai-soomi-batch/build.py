"""ㅋㅋ상회 AI 공감짤 5개 — soominiverse 양식(사진 게시물 4:5, 글씨가 그림 안에) 첫 시험 (2026-11-22).
그림: cardnews gemini-image(gemini-2.5-flash-image, 글씨 없이) → src/kk_s0N_*.png
글씨: 여기서 직접 얹는다(AI 한글은 깨짐). 시험지형 = 본고딕 명조(Noto Serif CJK KR), 말풍선 = Pretendard ExtraBold.
결과: jobs/2026-11-22-ai-s0N-<이름>/out/01.jpg + post.json(approved false, 승인하면 사진 한 장 게시물로 올라감)
"""
import os, json
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__)); S = os.path.join(HERE, 'src'); ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
W, H = 1080, 1350
SERIF_B = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc', 40, index=1)
def serif(size, bold=False):
    return ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSerifCJK-%s.ttc' % ('Bold' if bold else 'Medium'), size, index=1)
def pxb(size):
    return ImageFont.truetype(os.path.join(ROOT, 'fonts', 'Pretendard-ExtraBold.otf'), size)
TAGLINE = '\n\n🎨 ㅋㅋ상회 제작 (AI 그림)\n\n'


def bubble(d, box, lines, font, tail=None, cloud=False, fill='white', line_gap=1.25):
    """둥근 말풍선(또는 생각 풍선) + 가운데 정렬 글씨. tail=(x,y) 꼬리 끝."""
    x0, y0, x1, y1 = box
    if cloud:
        d.ellipse(box, fill=fill, outline='black', width=4)
        if tail:  # 생각 풍선 작은 동그라미 3개
            tx, ty = tail; cx, cy = (x0 + x1) / 2, y1
            for k, r in enumerate((22, 15, 9)):
                px = cx + (tx - cx) * (k + 1) / 4; py = cy + (ty - cy) * (k + 1) / 4
                d.ellipse((px - r, py - r, px + r, py + r), fill=fill, outline='black', width=3)
    else:
        if tail:  # 짧은 꼬리: 풍선 가장자리에서 대상 쪽으로 60px만
            tx, ty = tail; bx = min(max(tx, x0 + 70), x1 - 70)
            base_y = y1 if ty > y1 else y0; sgn = 1 if ty > y1 else -1
            dx = max(-50, min(50, (tx - bx) * 0.25)); tip = (bx + dx, base_y + sgn * 62)
            d.polygon([(bx - 24, base_y), (bx + 24, base_y), tip], fill=fill, outline='black')
            d.line([(bx - 24, base_y), tip, (bx + 24, base_y)], fill='black', width=4)
        d.rounded_rectangle(box, radius=min(60, (y1 - y0) // 2), fill=fill, outline='black', width=4)
        if tail:  # 꼬리와 풍선 이음새 지우기
            d.line([(bx - 22, base_y), (bx + 22, base_y)], fill=fill, width=6)
    lh = font.size * line_gap; ty0 = (y0 + y1) / 2 - lh * (len(lines) - 1) / 2
    for k, l in enumerate(lines):
        d.text(((x0 + x1) / 2, ty0 + lh * k), l, font=font, fill='black', anchor='mm')


def exam(img, no, situation, said, bubble_box, tail, options):
    cv = Image.new('RGB', (W, H), 'white'); d = ImageDraw.Draw(cv)
    d.text((70, 70), f'문제 {no}.', font=serif(50, True), fill='black')
    d.text((70, 140), '다음 상황에 알맞은 답변을 고르시오.', font=serif(40, True), fill='black')
    d.text((70, 200), situation, font=serif(32), fill=(40, 40, 40))
    im = Image.open(img).convert('RGB'); bw = W - 140; bh = round(im.height * bw / im.width)
    im = im.resize((bw, bh), Image.LANCZOS); top = 262
    cv.paste(im, (70, top)); d.rectangle((70, top, 70 + bw, top + bh), outline='black', width=3)
    bx0, by0, bx1, by1 = bubble_box
    bubble(d, (70 + bx0, top + by0, 70 + bx1, top + by1), said, serif(36), tail=(70 + tail[0], top + tail[1]))
    y = top + bh + 56
    for k, o in enumerate(options):
        d.text((80, y + k * 80), f'{"①②③④"[k]} {o}', font=serif(40), fill='black', anchor='lm')
    return cv


def full(img):
    im = Image.open(img).convert('RGB'); s = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = (im.width - W) // 2; y = (im.height - H) // 2
    return im.crop((x, y, x + W, y + H))


posts = []
# 1. 시험지형: 셀카 100장
cv = exam(f'{S}/kk_s01_selfie.png', 3, '친구가 셀카 100장을 찍더니 말했다.', ['건질 게 하나도 없네…'],
          (20, 24, 470, 124), (300, 300), ['원래 재료가 중요하지', '카메라를 바꿔 봐', '101번째도 똑같을 거야', '그래도 배경은 잘 나왔네'])
posts.append(('s01-selfie', cv, '정답은?!' + TAGLINE + '#ㅋㅋ상회 #친구 #셀카 #공감짤 #웃긴짤'))
# 2. 시험지형: 월급 3일
cv = exam(f'{S}/kk_s02_payday.png', 7, '월급 들어온 지 3일 만에 친구가 말했다.', ['내 돈 다 어디 갔지…'],
          (16, 22, 420, 122), (395, 365), ['다음 달엔 아껴 쓰자', '원래 월급은 스쳐 가는 거야', '네 통장도 너 손절했대', '택배 상자한테 물어봐'])
posts.append(('s02-payday', cv, '정답은?!' + TAGLINE + '#ㅋㅋ상회 #월급 #월급날 #직장인공감 #공감짤'))
# 3. 대사형: 만두 둘
cv = full(f'{S}/kk_s03_mandu.png'); d = ImageDraw.Draw(cv)
bubble(d, (40, 520, 560, 650), ['우리 진짜 친하지?'], pxb(54), tail=(300, 900))
bubble(d, (440, 700, 1050, 880), ['응. 그러니까', '돈 얘기는 하지 말자'], pxb(52), tail=(800, 1000))
posts.append(('s03-mandu', cv, '생각나는 친구한테 조용히 보내셈' + TAGLINE + '#ㅋㅋ상회 #친구 #돈 #공감짤 #웃긴짤'))
# 4. 생각 풍선형: 단톡방 ㅋ 하나
cv = full(f'{S}/kk_s04_groupchat.png'); d = ImageDraw.Draw(cv)
d.rounded_rectangle((60, 60, 1020, 200), radius=30, fill='white', outline='black', width=4)
d.text((540, 130), "단톡에 보낸 내 말에 'ㅋ' 하나 달렸을 때", font=pxb(46), fill='black', anchor='mm')
bubble(d, (90, 250, 760, 560), ['아… 나 지금', '손절당하는 중이구나', '이민 가야겠다'], pxb(52), tail=(760, 760), cloud=True)
posts.append(('s04-groupchat', cv, '이거 나만 그래? 아니라고 해줘' + TAGLINE + '#ㅋㅋ상회 #단톡방 #카톡 #공감짤 #INFP'))
# 5. 감성 반전형: 펭귄
cv = full(f'{S}/kk_s05_penguin.png'); d = ImageDraw.Draw(cv)
bubble(d, (40, 560, 600, 710), ['추운데 왜 자꾸', '옆에 붙어 있어?'], pxb(50), tail=(330, 900))
bubble(d, (420, 330, 1040, 470), ['너 혼자 추울까 봐.'], pxb(56), tail=(800, 620))
posts.append(('s05-penguin', cv, '혼자 버티는 게 익숙했던 작은 펭귄에게 처음으로 바람막이가 생긴 이야기\n옆에 있어 준 사람한테 보내세요' + TAGLINE + '#ㅋㅋ상회 #펭귄 #사랑 #감성 #공감짤'))

for name, cv, cap in posts:
    jd = os.path.join(ROOT, 'jobs', f'2026-11-22-ai-{name}'); os.makedirs(os.path.join(jd, 'out'), exist_ok=True)
    cv.save(os.path.join(jd, 'out', '01.jpg'), quality=93)
    json.dump({'approved': False, 'publish_at': None, 'format': 'photo', 'caption': cap,
               'source': 'Gemini 이미지 생성(gemini-2.5-flash-image, 글씨 없이) + 글씨는 직접 얹음. jobs/2026-11-22-ai-soomi-batch/build.py. 벤치마크 @soominiverse 양식.'},
              open(os.path.join(jd, 'post.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(name, 'ok')
