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


def main(spec_path):
    spec = json.load(open(spec_path, encoding="utf-8"))
    base = os.path.dirname(os.path.abspath(spec_path))
    src = Image.open(os.path.join(base, spec["image"])).convert("RGB")
    if spec.get("crop"):
        x0, y0, x1, y1 = spec["crop"]
        src = src.crop((round(x0 * src.width), round(y0 * src.height), round(x1 * src.width), round(y1 * src.height)))
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
