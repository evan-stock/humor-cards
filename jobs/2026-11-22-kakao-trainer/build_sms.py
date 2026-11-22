"""ㅋㅋ상회 레전드 카톡 → iOS 문자(SMS) 다크모드 화면으로 다시 그림.
원문: 펨코 '헬스장 트레이너와의 카톡' https://www.fmkorea.com/10542177794 (조회 95만)
UI 기준: 사용자 아이폰 문자 캡처 src/ios_sms_ui_ref.png (상태바 아이콘·프로필·입력창을 그대로 떼어 씀)
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ref = Image.open(os.path.join(HERE, "src/ios_sms_ui_ref.png")).convert("RGB")
orig = Image.open(os.path.join(HERE, "src/fmkorea_orig.png")).convert("RGB")
W, H = ref.size  # 1206 x 2622
NOTO = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
NOTOB = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
PSB = "/home/claude/cardnews/assets/fonts/Pretendard-SemiBold.otf"
f = ImageFont.truetype(NOTO, 49, index=1)
fts = ImageFont.truetype(NOTO, 33, index=1)
ftsb = ImageFont.truetype(NOTOB, 33, index=1)
ftime = ImageFont.truetype(PSB, 47)
fname = ImageFont.truetype(NOTOB, 38, index=1)
fbadge = ImageFont.truetype(PSB, 36)

GRAY = (38, 38, 41)
GREEN = (52, 199, 89)
SUB = (142, 142, 147)

cv = Image.new("RGB", (W, H), (0, 0, 0))
d = ImageDraw.Draw(cv)

# ---------- 대화 ----------
MAXW = 800
PADX, PADY, LH, RAD = 38, 22, 64, 44
y = 470


def wrap(text):
    lines, cur = [], ""
    for ch in text:
        if d.textlength(cur + ch, font=f) > MAXW - 2 * PADX:
            # 띄어쓰기 단위로 끊기
            if " " in cur:
                cut = cur.rfind(" ")
                lines.append(cur[:cut]); cur = cur[cut + 1:] + ch
            else:
                lines.append(cur); cur = ch
        else:
            cur += ch
    lines.append(cur)
    return lines


def stamp(day, t):
    global y
    y += 30
    w1 = d.textlength(day + " ", font=ftsb); w2 = d.textlength(t, font=fts)
    x = (W - w1 - w2) / 2
    d.text((x, y), day + " ", font=ftsb, fill=SUB)
    d.text((x + w1, y), t, font=fts, fill=SUB)
    y += 62


def tail(x, yb, right, color):
    # 아이폰 말풍선 꼬리: 색 원 위에 배경색 원으로 깎아 갈고리 모양
    if right:
        d.ellipse((x - 46, yb - 56, x + 16, yb + 1), fill=color)
        d.ellipse((x + 2, yb - 70, x + 64, yb - 8), fill=(0, 0, 0))
        d.rectangle((x + 16, yb - 60, x + 70, yb + 4), fill=(0, 0, 0))
    else:
        d.ellipse((x - 16, yb - 56, x + 46, yb + 1), fill=color)
        d.ellipse((x - 64, yb - 70, x - 2, yb - 8), fill=(0, 0, 0))
        d.rectangle((x - 70, yb - 60, x - 16, yb + 4), fill=(0, 0, 0))


def bubble(text, right, last=True):
    global y
    lines = wrap(text)
    tw = max(d.textlength(l, font=f) for l in lines)
    bw, bh = tw + 2 * PADX, len(lines) * LH + 2 * PADY - 6
    x0 = W - 40 - bw if right else 40
    col = GREEN if right else GRAY
    d.rounded_rectangle((x0, y, x0 + bw, y + bh), RAD, fill=col)
    if last:
        if right:
            tail(x0 + bw, y + bh, True, col)
        else:
            tail(x0, y + bh, False, col)
    for i, l in enumerate(lines):
        d.text((x0 + PADX, y + PADY + i * LH - 4), l, font=f, fill="white")
    y += bh + (26 if last else 8)


def photo_bubble(img, right=True, w=600):
    global y
    h = round(img.height * w / img.width)
    img = img.resize((w, h), Image.LANCZOS)
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), 40, fill=255)
    x0 = W - 40 - w if right else 40
    cv.paste(img, (x0, y), m)
    y += h + 26


gym = orig.crop((302, 170, 782, 490))  # 원본 속 헬스장 문 사진

stamp("오늘", "오전 6:58")
bubble("쌤 저 도착했는데 문 잠겨있어요 오늘 7시 맞죠?", True, last=False)
photo_bubble(gym)
stamp("오늘", "오전 7:12")
bubble("아 죄송해요 알람을 못들었어요 지금 바로 나갈게요", False)
bubble("몇분쯤 걸리세요? 저 8시에 회사로 출발해야돼요", True)
bubble("20분정도요 일단 앞에서 조금만 기다려주세요", False)
bubble("그럼 운동하고 씻을시간도 없어요 오늘은 그냥 갈게요", True)
bubble("근데 당일 취소는 1회 차감인데 괜찮으세요?", False)
print("content bottom", y)

# ---------- 위쪽(상태바·헤더) : 대화 위에 덮이는 어두운 띠 ----------
top = Image.new("RGBA", (W, 450), (0, 0, 0, 0))
g = Image.linear_gradient("L").resize((W, 450)).point(lambda v: 255 - int(v * 0.55))
top.putalpha(g)
cv.paste(Image.new("RGB", (W, 450), (0, 0, 0)), (0, 0), g)
d = ImageDraw.Draw(cv)
d.text((140, 98), "7:16", font=ftime, fill="white", anchor="lm")
st = ref.crop((860, 68, 1110, 128)).load()
st_im = ref.crop((860, 68, 1110, 128))
for xx in range(0, 14):
    for yy in range(60):
        r_, g_, b_ = st_im.getpixel((xx, yy))
        if r_ < 200: st_im.putpixel((xx, yy), (0, 0, 0))
cv.paste(st_im, (860, 68))  # 신호·5G·배터리
# 뒤로 가기
d.rounded_rectangle((50, 188, 300, 312), 62, fill=(30, 30, 32), outline=(58, 58, 60), width=2)
d.line([(118, 222), (92, 250), (118, 278)], fill="white", width=7, joint="curve")
d.rounded_rectangle((150, 222, 252, 280), 29, fill=(236, 239, 245))
d.text((201, 251), "621", font=fbadge, fill=(20, 20, 22), anchor="mm")
# 프로필(원형 그대로)
av = ref.crop((513, 185, 693, 365))
m = Image.new("L", av.size, 0); ImageDraw.Draw(m).ellipse((1, 1, 178, 178), fill=255)
cv.paste(av, (513, 185), m)
# 이름 알약
name = "트레이너쌤"
nw = d.textlength(name, font=fname) + 90
d.rounded_rectangle((603 - nw / 2, 352, 603 + nw / 2, 428), 38, fill=(30, 30, 32), outline=(58, 58, 60), width=2)
d.text((603 - 14, 390), name, font=fname, fill="white", anchor="mm")
d.text((603 + nw / 2 - 34, 390), "›", font=fname, fill=SUB, anchor="mm")

# ---------- 아래 입력창·홈바 ----------
inp = ref.crop((0, 1408, W, 1562))
cv.paste(inp, (0, H - 270))
d.rounded_rectangle((W / 2 - 140, H - 40, W / 2 + 140, H - 28), 6, fill="white")

cv.save(os.path.join(HERE, "out/sms_screen.png"))
cv.resize((W // 3, H // 3)).save("/tmp/sms_small.png")
