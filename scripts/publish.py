#!/usr/bin/env python3
"""예약·승인된 게시물을 인스타에 올린다.

jobs/<id>/post.json 형식:
  {"approved": true,                       # 사용자가 채팅에서 승인한 것만 올린다
   "publish_at": "2026-10-24T22:40:00+09:00",  # 이 시각이 지나면 게시("now"면 바로)
   "files": ["out/01.jpg", ...],           # 없으면 out/*.jpg 전부(이름순)
   "caption": "본문 전체"}
결과: jobs/<id>/published.json (media_id, permalink, published_at). 있으면 다시 올리지 않는다.
이미지 주소: MEDIA_BASE_URL(없으면 이 저장소 raw 주소)/jobs/<id>/<파일>. 인스타가 직접 받아가므로 공개 주소여야 한다.
사용: python3 scripts/publish.py [--dry-run] [--check]
"""
import argparse
import datetime as dt
import glob
import json
import os
import sys

import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import instagram  # noqa: E402
import telegram as tg  # noqa: E402


def notify(text):
    if tg.enabled():
        try:
            tg.send_text(text)
        except Exception as e:
            print("텔레그램 알림 실패:", e)

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
KST = dt.timezone(dt.timedelta(hours=9))


def base_url():
    b = os.environ.get("MEDIA_BASE_URL")
    if b:
        return b.rstrip("/")
    repo = os.environ.get("GITHUB_REPOSITORY", "evan-stock/humor-cards")
    return f"https://raw.githubusercontent.com/{repo}/main"


def due(post, now):
    if not post.get("approved"):
        return False
    t = post.get("publish_at", "now")
    if t == "now":
        return True
    return dt.datetime.fromisoformat(t) <= now


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="올리지 않고 무엇을 올릴지만 출력")
    ap.add_argument("--check", action="store_true", help="토큰이 어느 계정인지만 확인")
    a = ap.parse_args()
    if a.check:
        print("연결된 계정:", instagram.whoami())
        return
    now = dt.datetime.now(KST)
    for pj in sorted(glob.glob(os.path.join(ROOT, "jobs", "*", "post.json"))):
        jd = os.path.dirname(pj)
        jid = os.path.basename(jd)
        if os.path.exists(os.path.join(jd, "published.json")):
            continue
        post = json.load(open(pj, encoding="utf-8"))
        if not due(post, now):
            print(f"{jid}: 아직 아님(approved={post.get('approved')}, publish_at={post.get('publish_at')})")
            continue
        files = post.get("files") or sorted(os.path.relpath(p, jd) for p in glob.glob(os.path.join(jd, "out", "[0-9][0-9].jpg")))
        urls = [f"{base_url()}/jobs/{jid}/{f}" for f in files]
        print(f"{jid}: {len(urls)}장 게시 → {urls[0]} …")
        bad = [u for u in urls if requests.head(u, timeout=20).status_code != 200]
        if bad:  # 인스타가 못 받아가는 주소면 바로 멈춘다(비공개 저장소 등)
            result = {"status": "failed", "error": f"이미지 주소를 열 수 없음(공개 주소인지 확인): {bad[0]}", "at": now.isoformat()}
            json.dump(result, open(os.path.join(jd, "publish_error.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            print(result["error"])
            notify(f"⚠️ ㅋㅋ상회 게시 실패: {jid}\n{result['error']}")
            continue
        if a.dry_run:
            continue
        try:
            mid, link = instagram.publish_carousel(urls, post["caption"])
        except Exception as e:
            json.dump({"status": "failed", "error": str(e)[:800], "at": now.isoformat()},
                      open(os.path.join(jd, "publish_error.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            print("게시 실패:", e)
            notify(f"⚠️ ㅋㅋ상회 게시 실패: {jid}\n{str(e)[:300]}")
            continue
        json.dump({"media_id": mid, "permalink": link, "published_at": dt.datetime.now(KST).isoformat()},
                  open(os.path.join(jd, "published.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        err = os.path.join(jd, "publish_error.json")
        if os.path.exists(err):
            os.remove(err)
        print(f"게시 완료: {link}")
        notify(f"🎉 ㅋㅋ상회 게시 완료: {jid}\n{link}")


if __name__ == "__main__":
    main()
