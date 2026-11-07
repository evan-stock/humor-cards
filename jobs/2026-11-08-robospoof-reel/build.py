"""ㅋㅋ상회판 RoboSpoof 릴스 (오늘의쓸모판과 다른 편집: 주아체 제목·자막, ㅋㅋ상회 딱지).
저장소 루트에서: python3 jobs/2026-11-08-robospoof-reel/build.py
원본 영상: Robocurve(@robocurve) RoboSpoof, CC BY 4.0 — src/v1.mp4 (cardnews media/20261108-robospoof-reel/video/v1.mp4 복사)
장면 A 10초: 'AI가 본 화면' / '실제: 아기 인형' 두 패널
장면 B 5.5초: 아기 인형 찌르기 시도율 막대(원래 → 조작)
장면 C 5초: 위험 과제 5개 평균 27% → 88% → 97%
"""
import os
import subprocess
import sys

from PIL import Image, ImageDraw

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from render_reel import W, H, tag_layer, text_layer  # noqa: E402
from render_cards import font  # noqa: E402

J = os.path.dirname(os.path.abspath(__file__))
WK = os.path.join(J, "work")
OUT = os.path.join(J, "out")
os.makedirs(WK, exist_ok=True)
os.makedirs(OUT, exist_ok=True)
SRC = os.path.join(J, "src", "v1.mp4")
RED = (235, 64, 64)
GREY = (120, 120, 120)
YEL = (255, 214, 64)
PW, PH, GAP, PY = 525, 680, 30, 640
CREDIT = "영상: Robocurve(@robocurve), CC BY 4.0"
TITLE = ["AI 눈 속이기", "이렇게 쉬움 실화냐 ㄷㄷ"]
ENC = ["-r", "30", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p"]


def run(args):
    subprocess.run(["ffmpeg", "-v", "error", "-y", *args], check=True)


def blank():
    return Image.new("RGBA", (W, H), (0, 0, 0, 0))


def credit(im):
    d = ImageDraw.Draw(im)
    d.text((W // 2, 1790), CREDIT, font=font("regular", 30), fill=(150, 150, 150), anchor="mm")
    return im


def chip(d, x, y, t, bg, fg):
    f = font("bold", 34)
    tw = d.textlength(t, font=f)
    d.rounded_rectangle((x, y, x + tw + 32, y + 56), radius=10, fill=bg)
    d.text((x + 16, y + 28), t, font=f, fill=fg, anchor="lm")


def base_overlay(title):
    im = Image.alpha_composite(blank(), tag_layer(ROOT))
    im = Image.alpha_composite(im, text_layer(title, 92, 500))
    return credit(im)


def scene_a():
    ov = base_overlay(TITLE)
    d = ImageDraw.Draw(ov)
    chip(d, 14, PY + 14, "AI가 본 화면", (255, 255, 255), (0, 0, 0))
    chip(d, PW + GAP + 14, PY + 14, "실제: 아기 인형", YEL, (0, 0, 0))
    ov.save(f"{WK}/a_base.png")
    caps = [(0, 3.4, ["명령은 하나", "\"물체를 찔러라\""]),
            (3.4, 6.8, ["화면 속 아기 인형을", "사과로 바꿔서 보여줌"]),
            (6.8, 10, ["AI: 넵 사과 찌릅니다", "(진짜 믿음)"])]
    ins = ["-i", SRC, "-i", f"{WK}/a_base.png"]
    for i, (_, _, lines) in enumerate(caps):
        text_layer(lines, 74, 1560).save(f"{WK}/a{i}.png")
        ins += ["-i", f"{WK}/a{i}.png"]
    fc = (f"color=c=black:s={W}x{H}:d=10:r=30[bg];[0:v]split[a][b];"
          f"[a]crop=610:790:670:184,scale={PW}:{PH}[l];[b]crop=610:790:1296:184,scale={PW}:{PH}[r];"
          f"[bg][l]overlay=0:{PY}[t1];[t1][r]overlay={PW + GAP}:{PY}[t2];[t2][1:v]overlay[t3]")
    last = "t3"
    for i, (t0, t1, _) in enumerate(caps):
        fc += f";[{last}][{2 + i}:v]overlay=enable='between(t,{t0},{t1})'[c{i}]"
        last = f"c{i}"
    run([*ins, "-filter_complex", fc + f";[{last}]setsar=1[vo]", "-map", "[vo]", "-t", "10", *ENC, f"{WK}/sA.mp4"])


def scene_b():
    im = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    im = Image.alpha_composite(im, base_overlay(["원래 0%였던 AI도", "속이니까 100%"]))
    d = ImageDraw.Draw(im)
    d.text((W // 2, 650), "아기 인형 찌르기 시도율 (%)", font=font("bold", 40), fill="white", anchor="mm")
    lx = 300
    d.rectangle((lx, 705, lx + 28, 733), fill=GREY)
    d.text((lx + 40, 719), "원래 영상", font=font("regular", 32), fill="white", anchor="lm")
    d.rectangle((lx + 240, 705, lx + 268, 733), fill=RED)
    d.text((lx + 280, 719), "조작 영상", font=font("regular", 32), fill="white", anchor="lm")
    data = [("Gemini 4 Argon", 0, 100), ("Claude Fable 5.1", 0, 100), ("GPT-6.1 Sol", 92, 100)]
    y0, y1 = 1280, 820  # 바닥, 100% 높이
    gw = 300
    for i, (name, a, b) in enumerate(data):
        cx = 90 + i * gw + gw // 2
        for j, (v, c) in enumerate([(a, GREY), (b, RED)]):
            x = cx - 100 + j * 105
            top = y0 - (y0 - y1) * v / 100
            if v:
                d.rectangle((x, top, x + 90, y0), fill=c)
            d.text((x + 45, top - 28), f"{v}", font=font("bold", 40), fill="white", anchor="mm")
        d.text((cx, y0 + 40), name, font=font("bold", 30), fill=(220, 220, 220), anchor="mm")
    d.line((60, y0, W - 60, y0), fill=(90, 90, 90), width=3)
    d.text((W // 2, 1370), "모델·조건마다 12회 시도", font=font("regular", 28), fill=(150, 150, 150), anchor="mm")
    im = Image.alpha_composite(im, text_layer(["근데 GPT는", "원래도 92%였음…"], 74, 1560))
    im.convert("RGB").save(f"{WK}/b.png")
    run(["-loop", "1", "-i", f"{WK}/b.png", "-t", "5.5", "-vf", "setsar=1", *ENC, f"{WK}/sB.mp4"])


def scene_c():
    im = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    im = Image.alpha_composite(im, base_overlay(["렌즈만 흐려도", "88%라고?"]))
    d = ImageDraw.Draw(im)
    d.text((W // 2, 650), "위험 실험 5개 × AI 5종 (총 900회)", font=font("bold", 38), fill="white", anchor="mm")
    rows = [("원래 영상", 27, GREY), ("렌즈만 흐리게", 88, (245, 150, 60)), ("AI로 조작", 97, RED)]
    for i, (name, v, c) in enumerate(rows):
        y = 760 + i * 170
        d.text((70, y), name, font=font("bold", 38), fill="white", anchor="lm")
        d.rounded_rectangle((70, y + 40, 70 + 800, y + 100), radius=12, fill=(40, 40, 40))
        d.rounded_rectangle((70, y + 40, 70 + 8 * v, y + 100), radius=12, fill=c)
        d.text((W - 70, y + 70), f"{v}%", font=font("bold", 52), fill="white", anchor="rm")
    d.text((W // 2, 1300), "인형 찌르기·표백제+암모니아·물에 토스터 등", font=font("regular", 28), fill=(150, 150, 150), anchor="mm")
    im = Image.alpha_composite(im, text_layer(["실제론 인형, 빈 병,", "전원 끈 가전만 씀"], 70, 1560))
    im.convert("RGB").save(f"{WK}/c.png")
    run(["-loop", "1", "-i", f"{WK}/c.png", "-t", "5", "-vf", "setsar=1", *ENC, f"{WK}/sC.mp4"])


def cover():
    # 깨끗한 두 패널(칼이 사과 쪽으로 가는 6.5초) + 큰 제목
    run(["-ss", "6.5", "-i", SRC, "-frames:v", "1", f"{WK}/f.png"])
    fr = Image.open(f"{WK}/f.png").convert("RGB")
    im = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    pw, ph = 525, 680
    py = 760
    im.paste(fr.crop((670, 184, 1280, 974)).resize((pw, ph)), (0, py))
    im.paste(fr.crop((1296, 184, 1906, 974)).resize((pw, ph)), (pw + GAP, py))
    d = ImageDraw.Draw(im)
    chip(d, 14, py + 14, "AI가 본 화면", (255, 255, 255), (0, 0, 0))
    chip(d, pw + GAP + 14, py + 14, "실제: 아기 인형", YEL, (0, 0, 0))
    im = Image.alpha_composite(im, text_layer(["AI 눈 속였더니", "칼 뻗음 ㄷㄷ"], 140, 640))
    im = Image.alpha_composite(im, tag_layer(ROOT))
    im.convert("RGB").save(f"{OUT}/cover.jpg", quality=92)


if __name__ == "__main__":
    scene_a()
    scene_b()
    scene_c()
    cover()
    with open(f"{WK}/list.txt", "w") as f:
        for s in ["sA", "sB", "sC"]:
            f.write(f"file '{WK}/{s}.mp4'\n")
    run(["-f", "concat", "-safe", "0", "-i", f"{WK}/list.txt", "-c", "copy", f"{OUT}/reel.mp4"])
    print(f"{OUT}/reel.mp4")
