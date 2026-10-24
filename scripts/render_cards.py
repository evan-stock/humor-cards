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
- 표지에 "fit": "contain"을 주면 캡처·가로 사진을 흐린 배경 위에 원본 비율로 얹는다(contain_h, contain_top로 크기·위치).
- 썰 카드에 "watermark": false를 주면 사진 위 채널 워터마크를 뺀다(캡처 사진용).
- 뉴스형 틀: "news_cover"(흰 액자 + 줄별 색 제목 colors:["red","blue","black"] + 사진), "photo"(사진 크게 + caption 검정 자막, fit "contain"/"fill").
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
    src_img = slide_img(s, base)
    if s.get("fit") == "contain":
        # 캡처·가로 사진용: 흐린 배경 위에 원본 비율 그대로 위쪽에 크게 얹는다
        img = cover_fit(src_img, W, H).filter(ImageFilter.GaussianBlur(40))
        img = Image.blend(img, Image.new("RGB", (W, H), (0, 0, 0)), 0.45)
        box_h = round(H * s.get("contain_h", 0.62))
        fg = ImageOps.contain(src_img, (W - 2 * 40, box_h), Image.LANCZOS)
        top = round(H * s.get("contain_top", 0.06))
        img.paste(fg, ((W - fg.width) // 2, top))
    else:
        img = cover_fit(src_img, W, H, s.get("fx", 0.5), s.get("fy", 0.4))
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
    if s.get("watermark", True) is False:  # 캡처처럼 글자가 꽉 찬 사진은 워터마크를 빼서 가리지 않게
        y += bh + 22
        return _story_body(s, img, y, X)
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
    return _story_body(s, img, y, X)


def _story_body(s, img, y, X):
    d = ImageDraw.Draw(img)
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


# ---------- 뉴스형(이슈 카드) 틀: type "news_cover" / "photo" ----------
# 흰 바탕 테두리 액자 + 줄마다 색이 다른 굵은 제목 + 아래 사진 / 안쪽 장은 사진 크게 + 아래 검정 한 줄 자막
NEWS_COLORS = {"red": (226, 32, 40), "blue": (24, 52, 190), "black": (12, 12, 12)}


def news_font(size):
    for d in (os.path.join(HERE, "..", "fonts"), os.path.join(HERE, "fonts"), os.path.join(os.getcwd(), "fonts")):
        p = os.path.join(d, "GmarketSansBold.otf")
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return font("headline", size)


def render_news_cover(s, ch, base):
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    M, R, BW = 34, 22, 7                       # 바깥 여백, 모서리, 테두리 두께
    fx0, fy0, fx1, fy1 = M, M, W - M, H - M
    lines = s["title"].split("\n")
    colors = s.get("colors") or ["red", "blue", "black"][-len(lines):] if len(lines) <= 3 else ["black"] * len(lines)
    if len(colors) < len(lines):
        colors = colors + ["black"] * (len(lines) - len(colors))
    size = s.get("size", 92)
    maxw = fx1 - fx0 - 60
    while size > 50:
        f = news_font(size)
        if max(d.textlength(l, font=f) for l in lines) <= maxw:
            break
        size -= 2
    f = news_font(size)
    lh = round(size * 1.18)
    y = fy0 + 46
    for l, c in zip(lines, colors):
        d.text((W // 2, y), l, font=f, fill=NEWS_COLORS.get(c, c), anchor="mt")
        y += lh
    top = y + 18
    # 사진: 제목 아래부터 액자 바닥까지
    pw, ph = fx1 - fx0 - 2 * BW, fy1 - top - BW
    photo = cover_fit(slide_img(s, base), pw, ph, s.get("fx", 0.5), s.get("fy", 0.4))
    mask = Image.new("L", (pw, ph), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, -R, pw - 1, ph - 1), radius=R - BW, fill=255)
    img.paste(photo, (fx0 + BW, top), mask)
    d.rounded_rectangle((fx0, fy0, fx1, fy1), radius=R, outline=(10, 10, 10), width=BW)
    return img


def caption_bar(img, text, size=40):
    """사진 아래쪽 가운데 검정 자막 상자."""
    if not text:
        return img
    d = ImageDraw.Draw(img)
    f = font("bold", size)
    lines = wrap(text, f, W - 160, d)
    lh = round(size * 1.35)
    tw = max(d.textlength(l, font=f) for l in lines)
    bw, bh = tw + 56, lh * len(lines) + 30
    x0, y1 = (W - bw) / 2, H - 70
    y0 = y1 - bh
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(ov).rounded_rectangle((x0, y0, x0 + bw, y1), radius=10, fill=(0, 0, 0, 225))
    img = Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")
    d = ImageDraw.Draw(img)
    for i, l in enumerate(lines):
        d.text((W / 2, y0 + 15 + i * lh + lh / 2), l, font=f, fill="white", anchor="mm")
    return img


def render_photo(s, ch, base):
    src = slide_img(s, base)
    if s.get("fit", "contain") == "fill":
        img = cover_fit(src, W, H, s.get("fx", 0.5), s.get("fy", 0.4))
    else:  # 원본 비율 그대로, 남는 곳은 같은 사진을 흐리고 어둡게
        img = cover_fit(src, W, H).filter(ImageFilter.GaussianBlur(40))
        img = Image.blend(img, Image.new("RGB", (W, H), (20, 20, 20)), 0.6)
        fg = ImageOps.contain(src, (W, H - s.get("reserve", 0)), Image.LANCZOS)
        img.paste(fg, ((W - fg.width) // 2, (H - s.get("reserve", 0) - fg.height) // 2))
    img = caption_bar(img, s.get("caption", ""), s.get("caption_size", 40))
    return channel_tag(img, ch, base) if s.get("tag", True) else img


DEFAULT_CHANNEL = {"name": "ㅋㅋ상회", "handle": "@kk.sanghoe", "avatar": "brand/logo.png"}


def channel_tag(img, ch, base):
    """사진 장 왼쪽 위에 작은 채널 딱지(로고 + 아이디)."""
    d = ImageDraw.Draw(img)
    f = font("bold", 30)
    t = ch.get("handle", "")
    r = 46
    tw = d.textlength(t, font=f)
    x0, y0 = 36, 36
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(ov).rounded_rectangle((x0, y0, x0 + r + 26 + tw + 24, y0 + r + 12), radius=(r + 12) // 2, fill=(0, 0, 0, 150))
    img = Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")
    av = load_img(ch.get("avatar"), base)
    av = cover_fit(av, r, r, 0.5, 0.5)
    m = Image.new("L", (r, r), 0)
    ImageDraw.Draw(m).ellipse((0, 0, r - 1, r - 1), fill=255)
    img.paste(av, (x0 + 6, y0 + 6), m)
    ImageDraw.Draw(img).text((x0 + r + 18, y0 + (r + 12) / 2), t, font=f, fill="white", anchor="lm")
    return img


RENDERERS = {"cover": None, "story": None, "news_cover": render_news_cover, "photo": render_photo}


def main(spec_path):
    spec = json.load(open(spec_path, encoding="utf-8"))
    base = os.path.dirname(os.path.abspath(spec_path))
    out = spec.get("out_dir", "out")
    out = out if os.path.isabs(out) else os.path.join(base, out)
    os.makedirs(out, exist_ok=True)
    ch = {**DEFAULT_CHANNEL, **spec.get("channel", {})}
    if not os.path.isabs(ch.get("avatar", "")):
        ch["avatar"] = os.path.relpath(os.path.join(HERE, "..", ch["avatar"]), base) if ch.get("avatar") == DEFAULT_CHANNEL["avatar"] else ch.get("avatar")
    files = []
    for i, s in enumerate(spec["slides"], 1):
        r = RENDERERS.get(s.get("type")) or (render_cover if s.get("type") == "cover" else render_story)
        p = os.path.join(out, f"{i:02d}.jpg")
        r(s, ch, base).save(p, quality=93)
        files.append(p)
        print(p)
    return files


if __name__ == "__main__":
    main(sys.argv[1])
