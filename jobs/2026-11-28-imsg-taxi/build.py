"""ㅋㅋ상회: 아이폰 메시지(iMessage) 다크모드 + 키보드 올라온 화면 — '택시비 5천 원 더 내기' 계산 싸움.
벤치마크: @love._.zip__ '10만 원 더 내기로 했다면 30만 vs 35만'(댓글 390) 구조를 우리 사연으로.
UI 기준: 사용자 아이폰 문자 캡처 src/ios_sms_ui_ref.png(상태바·키보드·입력창을 그대로 떼어 씀).
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ref = Image.open(os.path.join(HERE, "src/ios_sms_ui_ref.png")).convert("RGB")
W, H = ref.size  # 1206 x 2622
NOTO = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
NOTOB = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
NOTOM = "/usr/share/fonts/opentype/noto/NotoSansCJK-Medium.ttc"
PSB = "/home/claude/cardnews/assets/fonts/Pretendard-SemiBold.otf"
F = lambda p, s: ImageFont.truetype(p, s, index=1)
f = F(NOTO, 46); fts = F(NOTO, 33); ftsb = F(NOTOB, 33)
ftime = ImageFont.truetype(PSB, 47); fname = F(NOTOM, 34); fbadge = ImageFont.truetype(PSB, 36)
GRAY = (38, 38, 41); BLUE = (10, 132, 255); SUB = (142, 142, 147)
NAME, INITIAL, CLOCK = "민지", "민", "11:48"
KB_TOP = 1400  # 이 아래는 원본 캡처의 입력창+키보드

CHAT = [
    ("stamp", "iMessage", "(오늘) 오후 11:42"),
    ("me", "택시비 2만 원 나왔어"),
    ("me", "너네 집 더 머니까 5천 원 더 내기로 했지?"),
    ("you", "응응 그니까 12,500원 보낼게"),
    ("me", "?"),
    ("me", "1만 원 + 5천 원 = 15,000원이지"),
    ("you", "아니 둘이 5천 원 차이 나면 되잖아"),
    ("you", "12,500 - 7,500 = 5,000 맞는데?"),
]

MAXW = 860
PADX, PADY, LH, RAD = 36, 20, 60, 42


def layout(d):
    """말풍선 높이를 먼저 재서, 마지막 말풍선이 입력창 바로 위에 오게 시작 y를 정한다."""
    items = []
    for i, it in enumerate(CHAT):
        if it[0] == "stamp":
            items.append((it, 14 + 50 + 44 + 18)); continue
        last = i + 1 >= len(CHAT) or CHAT[i + 1][0] != it[0]
        lines = wrap(d, it[1])
        bh = len(lines) * LH + 2 * PADY - 6
        items.append((it, bh + (26 if last else 8)))
    return items


def wrap(d, text):
    lines, cur = [], ""
    for ch in text:
        if d.textlength(cur + ch, font=f) > MAXW - 2 * PADX:
            if " " in cur:
                cut = cur.rfind(" "); lines.append(cur[:cut]); cur = cur[cut + 1:] + ch
            else:
                lines.append(cur); cur = ch
        else:
            cur += ch
    return lines + [cur]


cv = Image.new("RGB", (W, H), (0, 0, 0)); d = ImageDraw.Draw(cv)


def tail(x, yb, right, color):
    if right:
        d.ellipse((x - 46, yb - 56, x + 16, yb + 1), fill=color)
        d.ellipse((x + 2, yb - 70, x + 64, yb - 8), fill=(0, 0, 0))
        d.rectangle((x + 16, yb - 60, x + 70, yb + 4), fill=(0, 0, 0))
    else:
        d.ellipse((x - 16, yb - 56, x + 46, yb + 1), fill=color)
        d.ellipse((x - 64, yb - 70, x - 2, yb - 8), fill=(0, 0, 0))
        d.rectangle((x - 70, yb - 60, x - 16, yb + 4), fill=(0, 0, 0))


items = layout(d)
y = KB_TOP - 22 - sum(h for _, h in items)
assert y >= 455, ('넘침', y)
for i, (it, h) in enumerate(items):
    if it[0] == "stamp":
        d.text((W / 2, y + 36), it[1], font=ftsb, fill=SUB, anchor="mm")
        d.text((W / 2, y + 80), it[2], font=fts, fill=SUB, anchor="mm")
        y += h; continue
    right = it[0] == "me"
    last = i + 1 >= len(CHAT) or CHAT[i + 1][0] != it[0]
    lines = wrap(d, it[1])
    tw = max(d.textlength(l, font=f) for l in lines)
    bw, bh = tw + 2 * PADX, len(lines) * LH + 2 * PADY - 6
    x0 = W - 40 - bw if right else 40
    col = BLUE if right else GRAY
    d.rounded_rectangle((x0, y, x0 + bw, y + bh), RAD, fill=col)
    if last:
        tail(x0 + bw if right else x0, y + bh, right, col)
    for k, l in enumerate(lines):
        d.text((x0 + PADX, y + PADY + k * LH - 4), l, font=f, fill="white")
    y += h
print("content bottom", y, "kb top", KB_TOP)

# ---------- 위쪽(상태바·헤더) ----------
g = Image.linear_gradient("L").resize((W, 450)).point(lambda v: 255 - int(v * 0.55))
cv.paste(Image.new("RGB", (W, 450), (0, 0, 0)), (0, 0), g)
d = ImageDraw.Draw(cv)
d.text((140, 98), CLOCK, font=ftime, fill="white", anchor="lm")
st_im = ref.crop((860, 68, 1110, 128))
for xx in range(14):
    for yy in range(60):
        if st_im.getpixel((xx, yy))[0] < 200: st_im.putpixel((xx, yy), (0, 0, 0))
cv.paste(st_im, (860, 68))
d.rounded_rectangle((50, 188, 270, 312), 62, fill=(30, 30, 32), outline=(58, 58, 60), width=2)
d.line([(118, 222), (92, 250), (118, 278)], fill="white", width=7, joint="curve")
d.rounded_rectangle((150, 222, 230, 280), 29, fill=(236, 239, 245))
d.text((190, 251), "37", font=fbadge, fill=(20, 20, 22), anchor="mm")
# 이니셜 아바타(회색 원 + 글자)
d.ellipse((513, 185, 693, 365), fill=(142, 142, 147))
d.text((603, 275), INITIAL, font=F(NOTOM, 84), fill="white", anchor="mm")
d.text((603 - 10, 400), NAME, font=fname, fill="white", anchor="mm")
d.text((603 + d.textlength(NAME, font=fname) / 2 + 8, 400), "›", font=fname, fill=SUB, anchor="mm")

# ---------- 아래: 원본 캡처의 입력창 + 한글 키보드, 자리표시 글씨만 iMessage로 ----------
cv.paste(ref.crop((0, KB_TOP, W, H)), (0, KB_TOP))
d.rectangle((243, 1458, 1040, 1540), fill=(24, 24, 24))
d.line((252, 1468, 252, 1526), fill=BLUE, width=5)  # 커서
d.text((264, 1497), "iMessage", font=F(NOTO, 44), fill=(110, 110, 115), anchor="lm")

cv.save(os.path.join(HERE, "out/imsg_screen.png"))
