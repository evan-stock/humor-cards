"""소개팅녀 카톡(펨코 https://www.fmkorea.com/10229596769, 조회 38만)을 카카오톡(아이폰, 라이트 기본 테마) 화면으로.
색은 실제 카톡 캡처(펨코 트레이너 원본)에서 뽑음: 배경 (200,213,222), 노랑 (251,235,96), 흰 말풍선, 시간 글씨 회색.
머리(< 숫자 캡슐 · 가운데 이름 · 검색/메뉴 캡슐)와 날짜 알약은 chatlogue 실제 카톡 화면 구성을 따름."""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
SW, SH = 1170, 2532
BG = (200, 213, 222); YEL = (251, 235, 96); WHT = (255, 255, 255); INK = (25, 25, 25)
TIME = (110, 122, 132); PILL = (226, 233, 238); DATE = (166, 181, 192)
NOTO = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
NOTOM = "/usr/share/fonts/opentype/noto/NotoSansCJK-Medium.ttc"
NOTOB = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
PSB = "/home/claude/cardnews/assets/fonts/Pretendard-SemiBold.otf"
F = lambda p, s: ImageFont.truetype(p, s, index=1) if p.endswith("ttc") else ImageFont.truetype(p, s)
fmsg = F(NOTO, 47); ftime = F(NOTO, 29); fname = F(NOTO, 33); fdate = F(NOTOM, 31)
NAME = "사랑해따"

# (종류, 내용, 시간 표시) — 시간은 같은 분 묶음의 마지막에만
ORIG = Image.open(os.path.join(HERE, "src", "fmkorea_orig.webp")).convert("RGB")
CAT1 = ORIG.crop((257, 183, 466, 460)); CAT2 = ORIG.crop((257, 473, 466, 732))
CHAT = [
    ("date", "2026년 11월 15일 일요일"),
    ("me", "눈이 좋은 사슴은?", None),
    ("me", "굿아이디어ㅋㅋㅋㅋㅋㅋㅋ", None),
    ("me_img", CAT1, None),
    ("me_img", CAT2, "오후 1:27"),
    ("you", "연락 안하셨으면 좋겠어요", "오후 1:53"),
]


def wrap(d, text, maxw):
    out, line = [], ""
    for wd in text.split(" "):
        t = (line + " " + wd) if line else wd
        if d.textlength(t, font=fmsg) > maxw and line:
            out.append(line); line = wd
        else:
            line = t
    return out + [line]


def avatar(s, x, y, size=112):
    d = ImageDraw.Draw(s)
    d.rounded_rectangle((x, y, x + size, y + size), 44, fill=(170, 196, 214))
    c = x + size / 2
    d.ellipse((c - 20, y + 24, c + 20, y + 64), fill=WHT)
    d.chord((c - 38, y + 66, c + 38, y + 132), 180, 360, fill=WHT)


def screen():
    s = Image.new("RGB", (SW, SH), BG); d = ImageDraw.Draw(s)
    # 상태 표시줄
    d.text((165, 98), "1:54", font=F(PSB, 52), fill=INK, anchor="mm")
    d.rounded_rectangle((420, 34, 750, 140), 53, fill=(0, 0, 0))
    for i, h in enumerate((14, 21, 28, 35)):
        d.rounded_rectangle((858 + i * 15, 114 - h, 868 + i * 15, 114), 3, fill=INK)
    for r in (32, 21, 10):
        d.arc((962 - r, 116 - r, 962 + r, 116 + r), 225, 315, fill=INK, width=7)
    d.rounded_rectangle((1010, 80, 1094, 118), 12, outline=INK, width=4)
    d.rounded_rectangle((1015, 85, 1060, 113), 8, fill=INK)
    d.rounded_rectangle((1097, 92, 1103, 106), 2, fill=INK)
    # 머리
    hy = 262
    d.rounded_rectangle((38, hy - 60, 290, hy + 60), 60, fill=PILL)
    d.line([(108, hy - 25), (84, hy), (108, hy + 25)], fill=INK, width=7, joint="curve")
    d.text((134, hy), "999+", font=F(PSB, 46), fill=INK, anchor="lm")
    d.text((SW / 2, hy), NAME, font=F(NOTOB, 52), fill=INK, anchor="mm")
    d.rounded_rectangle((870, hy - 60, 1132, hy + 60), 60, fill=PILL)
    d.ellipse((925, hy - 26, 965, hy + 14), outline=INK, width=6)
    d.line((960, hy + 10, 980, hy + 30), fill=INK, width=7)
    for j in (-17, 0, 17):
        d.line((1040, hy + j, 1086, hy + j), fill=INK, width=6)

    y = 410
    maxw = 690; LH = 64; PX, PY = 30, 20; R = 36
    prev = None
    for item in CHAT:
        if item[0] == "date":
            y += 18
            tw = d.textlength(item[1] + " ›", font=fdate) + 60
            d.rounded_rectangle((SW / 2 - tw / 2, y, SW / 2 + tw / 2, y + 60), 30, fill=DATE)
            d.text((SW / 2, y + 30), item[1] + " ›", font=fdate, fill=WHT, anchor="mm")
            y += 60 + 34; prev = None
            continue
        kind, text, tm = item
        if kind == "me_img":
            pw = 515; ph = round(text.height * pw / text.width)
            img = text.resize((pw, ph), Image.LANCZOS)
            m = Image.new("L", (pw, ph), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, pw - 1, ph - 1), 36, fill=255)
            x1 = SW - 36; x0 = x1 - pw; y -= 22
            s.paste(img, (x0, y), m)
            if tm: d.text((x0 - 12, y + ph - 2), tm, font=ftime, fill=TIME, anchor="rb")
            y += ph + 34; prev = "me"
            continue
        lines = wrap(d, text, maxw - 2 * PX)
        bw = max(d.textlength(l, font=fmsg) for l in lines) + 2 * PX
        bh = LH * len(lines) + 2 * PY - 4
        first = prev != kind
        if kind == "me":
            x1 = SW - 36; x0 = x1 - bw
            if not first: y -= 22
            d.rounded_rectangle((x0, y, x1, y + bh), R, fill=YEL)
            if tm: d.text((x0 - 12, y + bh - 2), tm, font=ftime, fill=TIME, anchor="rb")
            for k, l in enumerate(lines):
                d.text((x0 + PX, y + PY + LH * k - 6), l, font=fmsg, fill=INK)
            y += bh + 34
        else:
            x0 = 172
            if first:
                avatar(s, 34, y)
                d.text((x0, y - 4), NAME, font=fname, fill=(70, 80, 90), anchor="lt")
                y += 50
            else:
                y -= 22
            d.rounded_rectangle((x0, y, x0 + bw, y + bh), R, fill=WHT)
            if tm: d.text((x0 + bw + 12, y + bh - 2), tm, font=ftime, fill=TIME, anchor="lb")
            for k, l in enumerate(lines):
                d.text((x0 + PX, y + PY + LH * k - 6), l, font=fmsg, fill=INK)
            y += bh + 34
        prev = kind
    # 입력창
    by = SH - 190
    d.ellipse((34, by, 134, by + 100), fill=PILL)
    d.line((84, by + 28, 84, by + 72), fill=INK, width=6); d.line((62, by + 50, 106, by + 50), fill=INK, width=6)
    d.rounded_rectangle((152, by, 1136, by + 100), 50, fill=PILL)
    d.text((196, by + 50), "메시지 입력", font=F(NOTO, 42), fill=(130, 140, 150), anchor="lm")
    d.ellipse((950, by + 26, 998, by + 74), outline=INK, width=5)
    d.ellipse((963, by + 40, 969, by + 46), fill=INK); d.ellipse((979, by + 40, 985, by + 46), fill=INK)
    d.arc((962, by + 44, 986, by + 64), 20, 160, fill=INK, width=4)
    d.text((1068, by + 50), "#", font=F(NOTOM, 50), fill=INK, anchor="mm")
    d.rounded_rectangle((SW / 2 - 140, SH - 30, SW / 2 + 140, SH - 18), 6, fill=INK)
    return s, y


if __name__ == "__main__":
    s, y = screen()
    print("content bottom", y, "input top", SH - 190)
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    s.save(os.path.join(HERE, "out", "kakao_screen.png"))
