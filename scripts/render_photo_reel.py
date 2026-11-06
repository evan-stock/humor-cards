#!/usr/bin/env python3
"""밈 사진 릴스 렌더: 사진 한 장 + 주아체 제목·자막·채널 딱지 → 1080x1920 이미지.

사용: python3 scripts/render_photo_reel.py jobs/<id>/photo.json → jobs/<id>/out/photo.jpg
photo.json:
{
  "image": "../<id>-review/src/01.jpg",
  "crop": [x0, y0, x1, y1],        # 선택, 0~1
  "title": "첫 줄\\n둘째 줄",        # 위쪽 큰 제목(영상 릴스와 같은 위치)
  "size": 96, "bottom": 0.27,       # 제목 크기·마지막 줄 위치(0~1)
  "caption": "아래 자막",           # 선택
  "caption_size": 72, "caption_y": 0.76,
  "photo_box": [0.08, 0.31, 0.92, 0.69],  # 사진이 들어갈 영역(x0,y0,x1,y1 0~1)
  "photo_scale": 1.0                # 작은 캡처를 영역 안에서 키울 최대 배율 제한 없음(영역에 맞춤)
}
인스타 앱에서 이 이미지 한 장으로 릴스를 만들고 음원을 넣는다(API로는 음원 불가).
"""
import json
import os
import sys

from PIL import Image, ImageDraw, ImageOps

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render_reel import W, H, tag_layer, text_layer  # noqa: E402


def tweet_card(src, text, time_text="", width=1000):
    """캡처형: 트윗 화면 모양(어두운 테마) — 프로필 사진·닉네임·아이디는 회색 블록으로 가리고 X 로고는 넣지 않는다."""
    from render_cards import font
    pad = 40
    ft = font("regular", 44)
    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    lines = []
    for para in text.split("\n"):
        cur = ""
        for ch in para:
            if probe.textlength(cur + ch, font=ft) > width - 2 * pad:
                lines.append(cur)
                cur = ch
            else:
                cur += ch
        lines.append(cur)
    lh = 62
    iw = width - 2 * pad
    img = None
    if src is not None:
        img = src.copy()
        img.thumbnail((iw, 900), Image.LANCZOS)
    head = 140
    h = pad + head + len(lines) * lh + 24 + (img.height + 24 if img else 0) + (60 if time_text else 0) + pad
    card = Image.new("RGB", (width, h), (0, 0, 0))
    d = ImageDraw.Draw(card)
    d.ellipse((pad, pad, pad + 100, pad + 100), fill=(70, 70, 75))           # 프로필 사진 자리(가림)
    d.rounded_rectangle((pad + 124, pad + 14, pad + 124 + 260, pad + 50), radius=10, fill=(70, 70, 75))  # 닉네임 가림
    d.rounded_rectangle((pad + 124, pad + 62, pad + 124 + 190, pad + 90), radius=10, fill=(50, 50, 55))  # 아이디 가림
    y = pad + head
    for l in lines:
        d.text((pad, y), l, font=ft, fill=(231, 233, 234))
        y += lh
    y += 24
    if img:
        m = Image.new("L", img.size, 0)
        ImageDraw.Draw(m).rounded_rectangle((0, 0, img.width - 1, img.height - 1), radius=28, fill=255)
        card.paste(img, (pad, y), m)
        d.rounded_rectangle((pad, y, pad + img.width - 1, y + img.height - 1), radius=28, outline=(60, 60, 65), width=2)
        y += img.height + 24
    if time_text:
        d.text((pad, y + 6), time_text, font=font("regular", 34), fill=(113, 118, 123))
    return card


def main(spec_path):
    spec = json.load(open(spec_path, encoding="utf-8"))
    base = os.path.dirname(os.path.abspath(spec_path))
    src = Image.open(os.path.join(base, spec["image"])).convert("RGB") if spec.get("image") else None
    if src is not None and spec.get("crop"):
        x0, y0, x1, y1 = spec["crop"]
        src = src.crop((round(x0 * src.width), round(y0 * src.height), round(x1 * src.width), round(y1 * src.height)))
    if spec.get("tweet"):  # 캡처형: {"text": "트윗 글", "time": "오후 2:04 · 2026년 11월 5일"}
        src = tweet_card(src, spec["tweet"]["text"], spec["tweet"].get("time", ""))
        spec.setdefault("radius", 0)
    bx0, by0, bx1, by1 = spec.get("photo_box", [0.06, 0.31, 0.94, 0.69])
    box = (round((bx1 - bx0) * W), round((by1 - by0) * H))
    fg = ImageOps.contain(src, box, Image.LANCZOS)
    img = Image.new("RGB", (W, H), (0, 0, 0)).convert("RGBA")
    px = round(bx0 * W) + (box[0] - fg.width) // 2
    py = round(by0 * H) + (box[1] - fg.height) // 2
    if spec.get("radius", 24):
        m = Image.new("L", fg.size, 0)
        ImageDraw.Draw(m).rounded_rectangle((0, 0, fg.width - 1, fg.height - 1), radius=spec.get("radius", 24), fill=255)
        img.paste(fg, (px, py), m)
    else:
        img.paste(fg, (px, py))
    img = Image.alpha_composite(img, text_layer(spec["title"].split("\n"), spec.get("size", 96), round(spec.get("bottom", 0.27) * H)))
    if spec.get("caption"):
        img = Image.alpha_composite(img, text_layer(spec["caption"].split("\n"), spec.get("caption_size", 72),
                                                    round(spec.get("caption_y", 0.76) * H)))
    img = Image.alpha_composite(img, tag_layer(base))
    out = os.path.join(base, spec.get("out", "out/photo.jpg"))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    img.convert("RGB").save(out, quality=92)
    print(out)


if __name__ == "__main__":
    main(sys.argv[1])
