#!/usr/bin/env python3
"""원글 이미지 수집: jobs/<id>/collect.json을 읽어 jobs/<id>/src/에 이미지를 받는다.

collect.json 형식:
  {"pages": ["원글 주소", ...], "image_urls": ["이미지 직접 주소", ...]}
결과:
  src/01.jpg, 02.jpg ...  (gif·webp는 첫 장면을 jpg로, 원본은 src/raw/에 보관)
  src/candidates.jpg      (번호가 붙은 한눈에 보기)
  src/index.json          (번호 → 원래 주소·크기)
collect.json 내용이 바뀌지 않았으면 다시 받지 않는다. 사용: python3 scripts/collect.py [job_id ...]
"""
import glob
import hashlib
import io
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont, ImageOps

from fetch_util import get, read_post

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
FONT = os.path.join(ROOT, "fonts", "Pretendard-Black.otf")


def sheet(paths, out):
    if not paths:
        return
    cell, cols = 360, 4
    rows = (len(paths) + cols - 1) // cols
    sh = Image.new("RGB", (cols * cell, rows * cell), (30, 30, 30))
    f = ImageFont.truetype(FONT, 44) if os.path.exists(FONT) else ImageFont.load_default()
    for i, p in enumerate(paths):
        im = ImageOps.contain(Image.open(p).convert("RGB"), (cell - 8, cell - 8))
        x, y = (i % cols) * cell, (i // cols) * cell
        sh.paste(im, (x + (cell - im.width) // 2, y + (cell - im.height) // 2))
        d = ImageDraw.Draw(sh)
        d.rectangle((x + 4, y + 4, x + 70, y + 58), fill=(255, 214, 0))
        d.text((x + 37, y + 31), f"{i+1:02d}", font=f, fill="black", anchor="mm")
    sh.save(out, quality=88)


def run(job_dir):
    cfg_p = os.path.join(job_dir, "collect.json")
    raw_cfg = open(cfg_p, "rb").read()
    h = hashlib.sha1(raw_cfg).hexdigest()
    src = os.path.join(job_dir, "src")
    hp = os.path.join(src, ".hash")
    if os.path.exists(hp) and open(hp).read().strip() == h:
        print(f"{job_dir}: 이미 받음, 건너뜀")
        return
    cfg = json.loads(raw_cfg)
    os.makedirs(os.path.join(src, "raw"), exist_ok=True)

    targets = []  # (이미지 주소, referer)
    for page in cfg.get("pages", []):
        post = read_post(page)
        if not post:
            print(f"  원글을 못 읽음: {page}")
            continue
        print(f"  원글 '{post['title'][:30]}' 이미지 {len(post['images'])}개")
        targets += [(u, page) for u in post["images"]]
        open(os.path.join(src, "post.txt"), "a", encoding="utf-8").write(
            f"# {post['title']}\n{page}\n\n{post['text']}\n\n")
    targets += [(u, cfg.get("referer")) for u in cfg.get("image_urls", [])]

    index, saved, n = [], [], 0
    for url, ref in targets:
        r = get(url, referer=ref)
        if not r or not r.content:
            index.append({"url": url, "error": "다운로드 실패"})
            continue
        try:
            im = Image.open(io.BytesIO(r.content))
            fmt = (im.format or "bin").lower()
            im.seek(0)
            rgb = im.convert("RGB")
        except Exception:
            index.append({"url": url, "error": "이미지가 아님"})
            continue
        if min(rgb.size) < 120:  # 아이콘·이모티콘
            continue
        n += 1
        name = f"{n:02d}.jpg"
        open(os.path.join(src, "raw", f"{n:02d}.{fmt}"), "wb").write(r.content)
        rgb.save(os.path.join(src, name), quality=95)
        saved.append(os.path.join(src, name))
        index.append({"no": n, "file": f"src/{name}", "url": url, "size": list(rgb.size), "format": fmt})
        print(f"  {name} {rgb.size} {fmt}")

    json.dump(index, open(os.path.join(src, "index.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    sheet(saved, os.path.join(src, "candidates.jpg"))
    open(hp, "w").write(h)
    print(f"{job_dir}: {n}장 저장")


def main():
    jobs = sys.argv[1:] or sorted(os.path.dirname(p) for p in glob.glob(os.path.join(ROOT, "jobs", "*", "collect.json")))
    for j in jobs:
        j = j if os.path.isabs(j) else os.path.join(ROOT, "jobs", os.path.basename(j.rstrip("/")))
        run(j)


if __name__ == "__main__":
    main()
