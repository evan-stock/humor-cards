#!/usr/bin/env python3
"""유머채널 카드 렌더러 (1080x1350, 4:5)

사용법: python3 render_cards.py spec.json
spec.json 예시:
{
  "out_dir": "out/subway",
  "channel": {"name": "채널이름", "handle": "@channel_id", "avatar": "avatar.png"},
  "slides": [
    {"type": "cover", "image": "cover.jpg", "title": "지하철에서 졸다가\n인생 꼬인 썰 ㄷㄷ"},
    {"type": "story", "headline": "옆사람 어깨에 기댔는데", "image": "s2.jpg",
     "paras": [{"text": "출근길 지하철에서 졸다가\n옆사람 어깨에 기댐"},
               {"text": "근데 그 사람도 나한테 기대서 자고 있었음", "bold": true}]}
  ]
}
- 이미지가 없거나 경로가 틀리면 회색 자리표시 이미지가 들어간다.
- 슬라이드에 "crop": [x0, y0, x1, y1](0~1 비율)을 주면 사진의 그 부분만 쓴다(반전을 숨기는 부분 컷 등).
- 글꼴: 표지 제목은 fonts/BMJUA.otf(배민 주아체, 참고 피드와 같은 글씨체)를 살짝 두껍게. 썰 카드 헤드라인·본문은 Pretendard가 fonts/에 있으면 쓰고, 없으면 Noto Sans CJK KR.
"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

W, H = 1080, 1350
HERE = os.path.dirname(os.path.abspath(__file__))
NOTO = "/usr/share/fonts/opentype/noto/NotoSansCJK-{}.ttc"


def font(kind, size):
    cands = {
        "title": ["BMJUA.otf", "BMJUA.ttf", "Jalnan.otf"],
        "headline": ["Pretendard-Black.otf", "Pretendard-ExtraBold.otf"],
        "bold": ["Pretendard-ExtraBold.otf", "Pretendard-Bold.otf"],
        "regular": ["Pretendard-Medium.otf", "Pretendard-Regular.otf"],
    }[kind]
    for d in (os.path.join(HERE, "fonts"), os.path.join(HERE, "..", "fonts"), os.path.join(os.getcwd(), "fonts")):
        for c in cands:
            p = os.path.join(d, c)
            if os.path.exists(p):
                return ImageFont.truetype(p, size)
    weight = {"title": "Black", "headline": "Black", "bold": "Bold", "regular": "Medium"}[kind]
    return ImageFont.truetype(NOTO.format(weight), size, index=1)  # index 1 = KR


def load_img(path, base):
    if path:
        p = path if os.path.isabs(path) else os.path.join(base, path)
        if os.path.exists(p):
            return Image.open(p).convert("RGB")
    ph = Image.new("RGB", (1080, 1350), (70, 74, 82))
    d = ImageDraw.Draw(ph)
    d.text((540, 675), "이미지 자리", font=font("bold", 60), fill=(150, 154, 162), anchor="mm")
    return ph


def slide_img(s, base):
    """슬라이드 사진을 불러오고, "crop": [x0, y0, x1, y1](0~1 비율)이 있으면 그 부분만 잘라 쓴다."""
    img = load_img(s.get("image"), base)
    c = s.get("crop")
    if c:
        w, h = img.size
        img = img.crop((round(c[0] * w), round(c[1] * h), round(c[2] * w), round(c[3] * h)))
    return img


def cover_fit(img, w, h, fx=0.5, fy=0.4):
    return ImageOps.fit(img, (w, h), Image.LANCZOS, centering=(fx, fy))


def wrap(text, f, maxw, draw):
    out = []
    for raw in text.split("\n"):
        line = ""
        for word in raw.split(" "):
            t = (line + " " + word).strip()
            if draw.textlength(t, font=f) <= maxw or not line:
                line = t
            else:
                out.append(line)
                line = word
        out.append(line)
    return out


# ---------- 1장: 표지 ----------
def tracked_width(text, f, track, draw):
    return sum(draw.textlength(c, font=f) for c in text) + track * (len(text) - 1)


def draw_tracked(draw, cx, cy, text, f, track, **kw):
    """글자 사이를 좁혀(자간 음수) 가운데 정렬로 그린다."""
    x = cx - tracked_width(text, f, track, draw) / 2
    for c in text:
        draw.text((x, cy), c, font=f, anchor="lm", **kw)
        x += draw.textlength(c, font=f) + track


def render_cover(s, ch, base):
    img = cover_fit(slide_img(s, base), W, H, s.get("fx", 0.5), s.get("fy", 0.4))
    lines = s["title"].split("\n")
    probe = ImageDraw.Draw(img)
    size = s.get("size", 140)
    while size > 70:
        f = font("title", size)
        tr = -size * s.get("track", 0.04)
        if max(tracked_width(l, f, tr, probe) for l in lines) <= W - 2 * 56:
            break
        size -= 2
    f = font("title", size)
    tr = -size * s.get("track", 0.04)
    stroke = max(10, round(size * 0.12))
    bold = max(1, round(size * s.get("embolden", 0.012)))  # 주아체를 원본처럼 살짝 두껍게
    lh = round(size * 1.32)
    # 제목 블록: 마지막 줄 중심이 카드 높이 약 80% (참고 디자인 실측)
    last_cy = round(H * s.get("bottom", 0.80))
    first_cy = last_cy - lh * (len(lines) - 1)

    # 은은한 그림자
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    for i, l in enumerate(lines):
        draw_tracked(sd, W // 2 + 4, first_cy + i * lh + 8, l, f, tr, fill=(0, 0, 0, 170),
                     stroke_width=stroke + 4, stroke_fill=(0, 0, 0, 170))
    shadow = shadow.filter(ImageFilter.GaussianBlur(10))
    img = Image.alpha_composite(img.convert("RGBA"), shadow)

    # 외곽선을 먼저 전부 그리고, 흰 글자를 위에 얹는다(자간이 좁아도 외곽선이 글자를 덮지 않게)
    d = ImageDraw.Draw(img)
    for i, l in enumerate(lines):
        draw_tracked(d, W // 2, first_cy + i * lh, l, f, tr, fill="black",
                     stroke_width=stroke + bold, stroke_fill="black")
    for i, l in enumerate(lines):
        draw_tracked(d, W // 2, first_cy + i * lh, l, f, tr, fill="white",
                     stroke_width=bold, stroke_fill="white")
    return img.convert("RGB")


# ---------- 2장~: 흰 바탕 썰 카드 ----------
def render_story(s, ch, base):
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    X = 48
    # 헤더: 프로필 원 + 채널 이름 + 아이디
    av_r = 58
    av = load_img(ch.get("avatar"), base) if ch.get("avatar") else Image.new("RGB", (av_r, av_r), (255, 214, 0))
    av = cover_fit(av, av_r, av_r, 0.5, 0.5)
    m = Image.new("L", (av_r, av_r), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, av_r - 1, av_r - 1), radius=12, fill=255)
    img.paste(av, (X, 26), m)
    d.text((X + av_r + 14, 28), ch.get("name", "채널이름"), font=font("bold", 27), fill=(20, 20, 20))
    d.text((X + av_r + 14, 60), ch.get("handle", "@channel"), font=font("regular", 22), fill=(110, 110, 110))

    # 굵은 헤드라인
    hf = font("headline", s.get("headline_size", 58))
    y = 112
    for l in wrap(s["headline"], hf, W - 2 * X, d):
        d.text((X, y), l, font=hf, fill=(15, 15, 15))
        y += round(hf.size * 1.25)
    y += 10

    # 사진 박스 (테두리 + 우하단 채널 워터마크)
    bw = W - 2 * X
    bh = s.get("image_h", 540)
    ph = cover_fit(slide_img(s, base), bw, bh, s.get("fx", 0.5), s.get("fy", 0.4))
    img.paste(ph, (X, y))
    d.rectangle((X, y, X + bw - 1, y + bh - 1), outline=(60, 60, 60), width=2)
    wf = font("bold", 26)
    wm = ch.get("name", "채널이름")
    tw = d.textlength(wm, font=wf)
    wx, wy = X + bw - 24 - tw, y + bh - 50
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sdd = ImageDraw.Draw(sh)
    sdd.text((wx + 2, wy + 2), wm, font=wf, fill=(0, 0, 0, 200))
    sdd.ellipse((wx - 28, wy + 9, wx - 12, wy + 25), fill=(0, 0, 0, 200))
    sh = sh.filter(ImageFilter.GaussianBlur(2))
    img = Image.alpha_composite(img.convert("RGBA"), sh).convert("RGB")
    d = ImageDraw.Draw(img)
    d.ellipse((wx - 30, wy + 7, wx - 14, wy + 23), fill=(52, 199, 89))
    d.text((wx, wy), wm, font=wf, fill="white")
    y += bh + 22

    # 본문 문단
    size = s.get("body_size", 46)
    paras = s.get("paras", [])
    while True:
        rf, bf = font("regular", size), font("bold", size)
        lh, gap = round(size * 1.5), round(size * 0.55)
        total = sum(len(wrap(p["text"], bf if p.get("bold") else rf, W - 2 * X, d)) * lh + gap for p in paras)
        if y + total <= H - 40 or size <= 30:
            break
        size -= 2
    for p in paras:
        f = bf if p.get("bold") else rf
        for l in wrap(p["text"], f, W - 2 * X, d):
            d.text((X, y), l, font=f, fill=(15, 15, 15))
            y += lh
        y += gap
    if y > H - 20:
        print(f"  ! 본문이 넘침: 글을 줄이세요 ({s['headline'][:12]}…)")
    return img


def main(spec_path):
    spec = json.load(open(spec_path, encoding="utf-8"))
    base = os.path.dirname(os.path.abspath(spec_path))
    out = spec.get("out_dir", "out")
    out = out if os.path.isabs(out) else os.path.join(base, out)
    os.makedirs(out, exist_ok=True)
    ch = spec.get("channel", {})
    files = []
    for i, s in enumerate(spec["slides"], 1):
        r = render_cover if s.get("type") == "cover" else render_story
        p = os.path.join(out, f"{i:02d}.jpg")
        r(s, ch, base).save(p, quality=93)
        files.append(p)
        print(p)
    return files


if __name__ == "__main__":
    main(sys.argv[1])
