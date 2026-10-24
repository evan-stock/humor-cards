#!/usr/bin/env python3
"""인기글 서칭: 디시 실시간 베스트 + 개드립 목록을 읽어 scout/<날짜>.json·.md로 저장한다.

각 글의 제목·추천수·본문 앞부분·이미지 수를 모아, Claude가 채널 기준(일상·반전·실존인물 없음)으로
후보를 고를 수 있게 한다. 사용: python3 scripts/scout.py [--limit 25]
"""
import argparse
import datetime as dt
import json
import os
import re
import time
from urllib.parse import urljoin

from fetch_util import read_post, soup

KST = dt.timezone(dt.timedelta(hours=9))
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")


def dc_best(limit):
    url = "https://gall.dcinside.com/board/lists/?id=dcbest"
    sp, raw = soup(url)
    items = []
    if not sp:
        return items, raw
    for tr in sp.select("tr.ub-content"):
        num = tr.select_one("td.gall_num")
        if not num or not num.get_text(strip=True).isdigit():
            continue  # 공지·광고
        a = tr.select_one("td.gall_tit a")
        if not a:
            continue
        rec = tr.select_one("td.gall_recommend")
        views = tr.select_one("td.gall_count")
        items.append({
            "site": "디시 실베",
            "title": a.get_text(" ", strip=True),
            "url": urljoin(url, a.get("href", "")),
            "recommend": rec.get_text(strip=True) if rec else "",
            "views": views.get_text(strip=True) if views else "",
        })
        if len(items) >= limit:
            break
    return items, raw


def dogdrip(limit):
    url = "https://www.dogdrip.net/dogdrip"
    sp, raw = soup(url)
    items, seen = [], set()
    if not sp:
        return items, raw
    for a in sp.find_all("a", href=True):
        m = re.search(r"(?:/dogdrip/|document_srl=)(\d{6,})", a["href"])
        t = a.get_text(" ", strip=True)
        if not m or len(t) < 4 or m.group(1) in seen:
            continue
        seen.add(m.group(1))
        t = re.sub(r"\s*\[?\d+\]?$", "", t)  # 끝의 댓글 수 제거
        items.append({"site": "개드립", "title": t,
                      "url": f"https://www.dogdrip.net/dogdrip/{m.group(1)}"})
        if len(items) >= limit:
            break
    return items, raw


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=25)
    args = ap.parse_args()
    now = dt.datetime.now(KST)
    day = now.strftime("%Y-%m-%d")
    outdir = os.path.join(ROOT, "scout")
    os.makedirs(outdir, exist_ok=True)

    all_items = []
    for fn in (dc_best, dogdrip):
        items, raw = fn(args.limit)
        print(f"{fn.__name__}: {len(items)}개")
        if not items and raw:  # 구조가 바뀌었을 때 고칠 수 있게 원본 저장
            os.makedirs(os.path.join(outdir, "_debug"), exist_ok=True)
            open(os.path.join(outdir, "_debug", f"{fn.__name__}.html"), "w", encoding="utf-8").write(raw)
        all_items += items

    for i, it in enumerate(all_items):
        time.sleep(1.0)
        post = read_post(it["url"])
        if not post:
            it["error"] = "본문을 못 읽음"
            continue
        it["text"] = post["text"][:1500]
        it["images"] = post["images"][:15]
        it["image_count"] = len(post["images"])
        print(f"  [{i+1}/{len(all_items)}] {it['title'][:30]} · 글 {len(post['text'])}자 · 이미지 {len(post['images'])}")

    data = {"date": day, "fetched_at": now.isoformat(timespec="minutes"), "items": all_items}
    json.dump(data, open(os.path.join(outdir, f"{day}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    md = [f"# 인기글 서칭 {day} ({now.strftime('%H:%M')} KST)", ""]
    for i, it in enumerate(all_items, 1):
        head = f"## {i}. [{it['site']}] {it['title']}"
        info = " · ".join(x for x in [
            f"추천 {it['recommend']}" if it.get("recommend") else "",
            f"조회 {it['views']}" if it.get("views") else "",
            f"이미지 {it.get('image_count', '?')}장"] if x)
        prev = (it.get("text") or it.get("error") or "").replace("\n", " ")[:220]
        md += [head, f"{info} · {it['url']}", "", f"> {prev}", ""]
    open(os.path.join(outdir, f"{day}.md"), "w", encoding="utf-8").write("\n".join(md))
    print(f"저장: scout/{day}.json, .md ({len(all_items)}개)")


if __name__ == "__main__":
    main()
