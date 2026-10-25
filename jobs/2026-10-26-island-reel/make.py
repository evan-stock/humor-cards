#!/usr/bin/env python3
"""무인도 지급품 릴스: 원본 영상 없이 직접 그린 섬 배경 + 주아체 자막 + 이모지 아이템.
사용: python3 jobs/2026-10-26-island-reel/make.py → out/reel.mp4, out/cover.jpg"""
import math, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "scripts"))
from render_reel import text_layer, tag_layer, W, H, ffmpeg  # noqa

FPS = 30
EMOJI = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf", 109)

SCENES = [  # (초, 이모지, 큰 글씨, 작은 글씨)
    (2.6, "🏝️", "무인도에 떨어졌는데\n지급품이 딱 하나", None),
    (2.4, "🧾", "니가 마지막으로\n결제한 물건임", None),
    (2.4, "🍙", "편의점 삼각김밥", "생존 1일 ㅋㅋㅋ"),
    (2.4, "🧻", "물티슈 100매", "깨끗하게 굶음;;"),
    (2.4, "🍜", "마라탕 2단계", "국물로 3일 버팀"),
    (2.4, "🔥", "라이터 하나", "생존왕 확정 ㄷㄷ"),
    (3.4, "👇", "니 마지막 결제템\n댓글로 ㄱㄱ", "생존 확률 판정해줌"),
]


def background():
    bg = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(bg)
    for y in range(H):  # 하늘 → 바다
        if y < 1050:
            t = y / 1050
            c = (int(120 + 90 * t), int(200 + 40 * t), int(255 - 10 * t))
        else:
            t = (y - 1050) / (H - 1050)
            c = (int(30 + 20 * t), int(150 - 60 * t), int(200 - 60 * t))
        d.line((0, y, W, y), fill=c)
    d.ellipse((760, 150, 940, 330), fill=(255, 236, 140))  # 해
    d.ellipse((140, 1220, 940, 1520), fill=(240, 214, 150))  # 섬
    d.ellipse((200, 1240, 880, 1440), fill=(250, 228, 170))
    d.polygon([(250, 1340), (272, 1340), (300, 990), (280, 985)], fill=(130, 85, 45))  # 야자수 줄기
    for ang in (-150, -110, -60, -20, 20):
        a = math.radians(ang)
        tip = (290 + 230 * math.cos(a), 990 + 230 * math.sin(a) + 60)
        mid = (290 + 120 * math.cos(a), 990 + 120 * math.sin(a) - 25)
        d.polygon([(290, 990), mid, tip, (mid[0], mid[1] + 50)], fill=(60, 160, 80))
    return bg


def emoji_img(ch, size):
    im = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((80, 80), ch, font=EMOJI, embedded_color=True, anchor="mm")
    return im.resize((size, size), Image.LANCZOS)


def pop(t):  # 0→1 튀어나오는 크기
    if t >= 0.35:
        return 1.0
    x = t / 0.35
    return 0.55 + 0.55 * math.sin(x * math.pi * 0.62) / math.sin(math.pi * 0.62) * (1.0 if x < 0.8 else 1.0) - 0.1 * max(0, x - 0.7) / 0.3


def main():
    out_dir = os.path.join(HERE, "out")
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, "reel.mp4")
    bg0, tag = background(), tag_layer(HERE)
    proc = subprocess.Popen([ffmpeg(), "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                             "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
                             "-shortest", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
                             "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    frame_no = 0
    for si, (dur, emo, big, small) in enumerate(SCENES):
        big_l = text_layer(big.split("\n"), 118, 560 if "\n" in big else 520)
        small_l = text_layer([small], 92, 760) if small else None
        if small_l:  # 판정 글씨는 노랑
            r, g, b, a = small_l.split()
            yellow = Image.merge("RGBA", (r, g, Image.eval(b, lambda v: int(v * 0.25)), a))
            small_l = yellow
        em = emoji_img(emo, 480)
        n = round(dur * FPS)
        for k in range(n):
            t = k / FPS
            fr = bg0.copy().convert("RGBA")
            d = ImageDraw.Draw(fr)
            for i in range(3):  # 움직이는 물결
                y = 1110 + i * 150
                pts = [(x, y + 12 * math.sin((x / 90) + frame_no / 8 + i)) for x in range(0, W + 30, 30)]
                d.line(pts, fill=(255, 255, 255, 110), width=6)
            s = pop(t)
            bob = 14 * math.sin(frame_no / 7)
            e = em.resize((max(1, int(480 * s)), max(1, int(480 * s))))
            fr.alpha_composite(e, (W // 2 - e.width // 2, int(1180 - e.height / 2 + bob)))
            for layer, delay in ((big_l, 0), (small_l, 0.45)):
                if layer is None or t < delay:
                    continue
                ss = pop(t - delay)
                box = layer.getbbox()
                crop = layer.crop(box)
                cw, chh = max(1, int(crop.width * ss)), max(1, int(crop.height * ss))
                crop = crop.resize((cw, chh))
                cx, cy = (box[0] + box[2]) // 2, (box[1] + box[3]) // 2
                fr.alpha_composite(crop, (cx - cw // 2, cy - chh // 2))
            fr.alpha_composite(tag)
            rgb = fr.convert("RGB")
            if si == 0 and k == n - 1:
                rgb.save(os.path.join(out_dir, "cover.jpg"), quality=92)
            proc.stdin.write(rgb.tobytes())
            frame_no += 1
    proc.stdin.close()
    proc.wait()
    print(out)


if __name__ == "__main__":
    main()
