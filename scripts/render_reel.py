#!/usr/bin/env python3
"""릴스 렌더: 원글 영상 구간을 이어 붙이고 주아체 제목·자막·채널 딱지를 얹는다.

사용: python3 scripts/render_reel.py jobs/<id>/reel.json  → jobs/<id>/out/reel.mp4 (+ cover.jpg)
reel.json:
{
  "out": "out/reel.mp4",
  "mute": true,                     # 원본 소리 빼기(무음 트랙을 넣음)
  "segments": [
    {"video": "src/v01.mp4", "start": 3.0, "end": 6.0,
     "title": "첫 줄\\n둘째 줄"},     # title = 표지형 큰 제목(마지막 줄이 화면 높이 bottom 위치)
    {"video": "src/v02.mp4", "start": 0, "end": 4, "caption": "자막 한두 줄"}
  ]
}
선택: 구간별 "fx"/"fy"(세로 영상이 아닐 때 자를 위치), "bottom"(제목 위치 0~1, 기본 0.72),
      "caption_y"(자막 중심 0~1, 기본 0.78), "size"(제목 130, 자막 84), "speed"(1.0).
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render_cards import cover_fit, draw_tracked, font, load_img, tracked_width  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
W, H = 1080, 1920


def ffmpeg():
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def text_layer(lines, size, center_last_y, maxw=W - 2 * 60):
    """흰 글씨 + 두꺼운 검정 외곽선 + 그림자(주아체)를 투명 판에 그린다."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    probe = ImageDraw.Draw(layer)
    while size > 50:
        f = font("title", size)
        tr = -size * 0.04
        if max(tracked_width(l, f, tr, probe) for l in lines) <= maxw:
            break
        size -= 2
    f = font("title", size)
    tr = -size * 0.04
    stroke = max(8, round(size * 0.12))
    bold = max(1, round(size * 0.012))
    lh = round(size * 1.3)
    first = center_last_y - lh * (len(lines) - 1)
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sh)
    for i, l in enumerate(lines):
        draw_tracked(sd, W // 2 + 4, first + i * lh + 8, l, f, tr, fill=(0, 0, 0, 160),
                     stroke_width=stroke + 4, stroke_fill=(0, 0, 0, 160))
    layer = Image.alpha_composite(layer, sh.filter(ImageFilter.GaussianBlur(10)))
    d = ImageDraw.Draw(layer)
    for i, l in enumerate(lines):
        draw_tracked(d, W // 2, first + i * lh, l, f, tr, fill="black", stroke_width=stroke + bold, stroke_fill="black")
    for i, l in enumerate(lines):
        draw_tracked(d, W // 2, first + i * lh, l, f, tr, fill="white", stroke_width=bold, stroke_fill="white")
    return layer


def tag_layer(base):
    """왼쪽 위 채널 딱지(로고 + @kk.sanghoe), 투명 판."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    f = font("bold", 34)
    t = "@kk.sanghoe"
    r = 54
    tw = d.textlength(t, font=f)
    x0, y0 = 40, 120  # 인스타 릴스 상단 UI를 피해 조금 내림
    d.rounded_rectangle((x0, y0, x0 + r + 30 + tw + 26, y0 + r + 12), radius=(r + 12) // 2, fill=(0, 0, 0, 150))
    av = cover_fit(load_img("brand/logo.png", ROOT), r, r, 0.5, 0.5).convert("RGBA")
    m = Image.new("L", (r, r), 0)
    ImageDraw.Draw(m).ellipse((0, 0, r - 1, r - 1), fill=255)
    layer.paste(av, (x0 + 6, y0 + 6), m)
    d.text((x0 + r + 20, y0 + (r + 12) / 2), t, font=f, fill="white", anchor="lm")
    return layer


def main(spec_path):
    spec_path = os.path.abspath(spec_path)
    base = os.path.dirname(spec_path)
    spec = json.load(open(spec_path, encoding="utf-8"))
    out = os.path.join(base, spec.get("out", "out/reel.mp4"))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    ff = ffmpeg()
    tmp = tempfile.mkdtemp()
    tag = tag_layer(base)
    parts = []
    for i, s in enumerate(spec["segments"]):
        ov = tag.copy()
        if s.get("title"):
            ov = Image.alpha_composite(ov, text_layer(s["title"].split("\n"), s.get("size", 130), round(H * s.get("bottom", 0.72))))
        if s.get("caption"):
            ov = Image.alpha_composite(ov, text_layer(s["caption"].split("\n"), s.get("size", 84), round(H * s.get("caption_y", 0.78))))
        png = os.path.join(tmp, f"ov{i}.png")
        ov.save(png)
        seg = os.path.join(tmp, f"seg{i}.mp4")
        speed = s.get("speed", 1.0)
        fx, fy = s.get("fx", 0.5), s.get("fy", 0.5)
        vf = (f"[0:v]trim={s['start']}:{s['end']},setpts=(PTS-STARTPTS)/{speed},"
              f"scale={W}:{H}:force_original_aspect_ratio=increase,"
              f"crop={W}:{H}:(iw-{W})*{fx}:(ih-{H})*{fy},fps=30,setsar=1[v];[v][1:v]overlay=0:0,format=yuv420p[o]")
        subprocess.run([ff, "-y", "-loglevel", "error", "-i", os.path.join(base, s["video"]), "-i", png,
                        "-filter_complex", vf, "-map", "[o]", "-an",
                        "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", seg], check=True)
        parts.append(seg)
        if i == 0:  # 첫 장면을 커버 이미지로
            subprocess.run([ff, "-y", "-loglevel", "error", "-ss", "0.5", "-i", seg, "-frames:v", "1",
                            os.path.join(os.path.dirname(out), "cover.jpg")], check=True)
    lst = os.path.join(tmp, "list.txt")
    open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
    subprocess.run([ff, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst,
                    "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-shortest",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart", out], check=True)
    shutil.rmtree(tmp)
    print(out)


if __name__ == "__main__":
    main(sys.argv[1])
