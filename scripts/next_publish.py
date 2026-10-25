#!/usr/bin/env python3
"""승인됐지만 아직 안 올라간 게시물 중 가장 이른 것의 "게시시각(epoch) id" 를 출력한다(없으면 빈 출력).

승인: jobs/<id>/post.json approved true, 또는 운영판 승인(state/posts/<id>.json status approved).
제외: published.json 있음, rejected, 운영판 status rejected/published, 인자로 준 id(이번 대기에서 이미 실행 요청한 것).
publish-wait 워크플로가 쓴다.
"""
import datetime as dt
import glob
import json
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
skip = set(sys.argv[1:])
best = None
for pj in glob.glob(os.path.join(ROOT, "jobs", "*", "post.json")):
    jd = os.path.dirname(pj)
    jid = os.path.basename(jd)
    if jid in skip or os.path.exists(os.path.join(jd, "published.json")):
        continue
    try:
        post = json.load(open(pj, encoding="utf-8"))
    except Exception:
        continue
    state = {}
    sp = os.path.join(ROOT, "state", "posts", jid + ".json")
    if os.path.exists(sp):
        try:
            state = json.load(open(sp, encoding="utf-8"))
        except Exception:
            pass
    status = state.get("status")
    if post.get("rejected") or status in ("rejected", "published"):
        continue
    if not (post.get("approved") or status == "approved"):
        continue
    t = post.get("publish_at", "now")
    ts = dt.datetime.now().timestamp() if t == "now" else dt.datetime.fromisoformat(t).timestamp()
    if best is None or ts < best[0]:
        best = (ts, jid)
if best:
    print(int(best[0]), best[1])
