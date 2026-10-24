#!/usr/bin/env python3
"""운영판 연동: jobs/<id>/post.json ↔ state/posts/<id>.json

- 운영판(통합 운영판·운영판 앱)은 오늘의쓸모(cardnews)와 같은 형식의 state/posts/<id>.json 을 읽는다.
- 운영판에서 승인/거절하면 state/posts/<id>.json 의 status 를 "approved"/"rejected" 로 바꿔 커밋한다
  → 이 스크립트가 jobs/<id>/post.json 에 반영(approved/rejected)하고, publish 가 게시한다.
- 반대로 채팅 승인·게시 결과는 이 스크립트가 state/posts 에 써서 운영판에 보이게 한다.
status: pending(승인 대기) → approved(승인, publish_at 에 게시) → published / failed / rejected / expired
사용: python3 scripts/sync_state.py
"""
import datetime as dt
import glob
import json
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
KST = dt.timezone(dt.timedelta(hours=9))
SLOTS = {"noon": ("lunch", "점심"), "night": ("evening", "저녁")}


def load(p):
    try:
        return json.load(open(p, encoding="utf-8"))
    except Exception:
        return None


def save(p, d):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def topic_of(jd, post):
    if post.get("topic"):
        return post["topic"]
    spec = load(os.path.join(jd, "spec.json")) or {}
    for s in spec.get("slides", []):
        if s.get("type") == "cover" and s.get("title"):
            return s["title"].replace("\n", " ")
    return (post.get("caption") or "").split("\n")[0][:80]


def main():
    now = dt.datetime.now(KST)
    changed = []
    for pj in sorted(glob.glob(os.path.join(ROOT, "jobs", "*", "post.json"))):
        jd = os.path.dirname(pj)
        jid = os.path.basename(jd)
        post = load(pj)
        if post is None:
            continue
        sp = os.path.join(ROOT, "state", "posts", f"{jid}.json")
        st = load(sp) or {}
        pub = load(os.path.join(jd, "published.json"))
        err = load(os.path.join(jd, "publish_error.json"))

        # 1) 운영판 결정 → post.json
        if not pub and st.get("status") == "approved" and not post.get("approved") and not post.get("rejected"):
            post.update(approved=True, approved_note=f"{st.get('decided_at') or now.isoformat()} 운영판 승인")
            save(pj, post)
            changed.append(f"{jid}: 운영판 승인 반영")
        if not pub and st.get("status") == "rejected" and not post.get("rejected"):
            post.update(rejected=True, approved=False, rejected_note=f"{st.get('decided_at') or now.isoformat()} 운영판 거절")
            save(pj, post)
            changed.append(f"{jid}: 운영판 거절 반영")

        # 2) post.json·게시 결과 → state/posts
        t = post.get("publish_at", "now")
        if t == "now":
            when = dt.datetime.fromisoformat(pub["published_at"]) if pub and pub.get("published_at") else now
        else:
            when = dt.datetime.fromisoformat(t)
        if pub:
            status = "published"
        elif post.get("rejected"):
            status = "rejected"
        elif err and post.get("approved"):
            status = "failed"
        elif post.get("approved"):
            status = "approved"
        elif when < now - dt.timedelta(hours=12):
            status = "expired"
        else:
            status = "pending"
        slot = next((v for k, v in SLOTS.items() if f"-{k}-" in jid), None) or \
            (SLOTS["noon"] if when.astimezone(KST).hour < 17 else SLOTS["night"])
        files = sorted(os.path.relpath(p, ROOT) for p in glob.glob(os.path.join(jd, "out", "[0-9][0-9].jpg")))
        new = {
            "id": jid,
            "channel": "kksanghoe",
            "account": "@kk.sanghoe",
            "slot": slot[0],
            "slot_label": slot[1],
            "status": status,
            "created_at": st.get("created_at") or post.get("created_at") or now.isoformat(),
            "publish_at": when.isoformat(),
            "topic": topic_of(jd, post),
            "category": post.get("category", "커뮤 유머"),
            "source": post.get("source", ""),
            "caption_full": post.get("caption", ""),
            "files": files,
            "preview": f"jobs/{jid}/out/preview.jpg" if os.path.exists(os.path.join(jd, "out", "preview.jpg")) else "",
        }
        if post.get("approved_note") or post.get("rejected_note"):
            new["decided_note"] = post.get("approved_note") or post.get("rejected_note")
            new["decided_at"] = st.get("decided_at") or now.isoformat()
        if pub:
            new.update(ig_media_id=pub.get("media_id"), permalink=pub.get("permalink"), published_at=pub.get("published_at"))
        if err and status == "failed":
            new["error"] = err.get("error", "")[:500]
        keep = {k: v for k, v in st.items() if k not in new}  # 운영판이 덧붙인 값(곡 추천 등)은 보존
        merged = {**keep, **new}
        if merged != st:
            save(sp, merged)
            changed.append(f"{jid}: state {st.get('status')} → {status}")
    print("\n".join(changed) or "변경 없음")


if __name__ == "__main__":
    main()
