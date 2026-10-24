#!/usr/bin/env python3
"""텔레그램 승인 루프.
1) 승인 대기(approved false, 게시 전) 게시물 중 아직 안 보낸 것 → 카드 앨범 + 본문 + ✅ 승인/❌ 거절 버튼 전송(jobs/<id>/tg.json 기록)
2) 버튼 응답을 받아 ✅ → post.json approved true(+approved_note), ❌ → rejected true. 바뀌면 커밋·푸시하고
   publish 워크플로를 실행(workflow_dispatch)한다. 게시는 publish 워크플로만 한다(중복 게시 방지).
3) 승인됐지만 publish_at 이 아직 안 된 건 그 시각까지 기다렸다가 publish 를 다시 실행한다.
대기할 게 없거나 --minutes 가 지나면 끝난다.
"""
import argparse
import datetime as dt
import glob
import json
import os
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import telegram as tg  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
KST = dt.timezone(dt.timedelta(hours=9))


def now():
    return dt.datetime.now(KST)


def sh(*cmd):
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)


def commit_push(msg):
    sh("git", "add", "jobs", "state")
    if sh("git", "diff", "--cached", "--quiet").returncode == 0:
        return
    sh("git", "-c", "user.name=humor-cards-bot", "-c", "user.email=actions@users.noreply.github.com", "commit", "-m", msg)
    for _ in range(3):
        sh("git", "pull", "--rebase", "-q")
        if sh("git", "push", "-q").returncode == 0:
            return
        time.sleep(5)


def dispatch_publish():
    r = sh("gh", "workflow", "run", "publish.yml", "-f", "mode=run")
    print("publish 실행 요청:", r.returncode, r.stderr.strip()[:200])


def jobs():
    sh("git", "pull", "--rebase", "-q")
    out = []
    for pj in sorted(glob.glob(os.path.join(ROOT, "jobs", "*", "post.json"))):
        jd = os.path.dirname(pj)
        if os.path.exists(os.path.join(jd, "published.json")):
            continue
        post = json.load(open(pj, encoding="utf-8"))
        if post.get("rejected"):
            continue
        if not post.get("approved") and when(post) < now() - dt.timedelta(hours=12):
            continue  # 12시간 넘게 승인 안 된 건 만료로 보고 기다리지 않는다
        out.append((os.path.basename(jd), jd, post))
    return out


def when(post):
    t = post.get("publish_at", "now")
    return now() if t == "now" else dt.datetime.fromisoformat(t)


def send_previews():
    sent = False
    for jid, jd, post in jobs():
        if post.get("approved") or os.path.exists(os.path.join(jd, "tg.json")):
            continue
        cards = sorted(glob.glob(os.path.join(jd, "out", "[0-9][0-9].jpg")))
        if not cards:
            continue
        tg.send_album(cards)
        t = when(post).strftime("%m/%d %H:%M")
        text = f"🛒 ㅋㅋ상회 게시 대기 ({t} 예정)\n\n{post['caption']}"
        msg = tg.send_text(text, buttons=[[{"text": "✅ 승인", "callback_data": f"ok:{jid}"},
                                           {"text": "❌ 거절", "callback_data": f"no:{jid}"}]])
        json.dump({"sent_at": now().isoformat(), "message_id": msg["message_id"]},
                  open(os.path.join(jd, "tg.json"), "w"), ensure_ascii=False)
        sent = True
        print("미리보기 보냄:", jid)
    if sent:
        commit_push("telegram: 미리보기 전송")


def handle(decisions):
    changed, approved_now = False, False
    for act, jid, cb in decisions:
        pj = os.path.join(ROOT, "jobs", jid, "post.json")
        if not os.path.exists(pj):
            tg.answer(cb, "이미 없는 게시물이에요")
            continue
        if os.path.exists(os.path.join(ROOT, "jobs", jid, "published.json")):
            tg.answer(cb, "이미 게시됐어요")
            continue
        post = json.load(open(pj, encoding="utf-8"))
        stamp = now().strftime("%Y-%m-%d %H:%M KST")
        if act == "ok":
            post.update(approved=True, approved_note=f"{stamp} 텔레그램 승인")
            t = when(post)
            msg = "바로 게시합니다" if t <= now() else f"{t.strftime('%H:%M')}에 게시합니다"
            tg.answer(cb, f"승인! {msg}")
            tg.send_text(f"✅ 승인됨: {jid}\n{msg}")
            approved_now = approved_now or t <= now()
        elif act == "no":
            post.update(rejected=True, rejected_note=f"{stamp} 텔레그램 거절")
            tg.answer(cb, "거절했어요")
            tg.send_text(f"❌ 거절됨: {jid}")
        else:
            continue
        json.dump(post, open(pj, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        changed = True
    if changed:
        commit_push("telegram: 승인·거절 반영")
    if approved_now:
        dispatch_publish()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--minutes", type=int, default=150)
    a = ap.parse_args()
    if not tg.enabled():
        print("TELEGRAM_BOT_TOKEN 없음 — 건너뜀")
        return
    deadline = time.time() + a.minutes * 60
    _, ups = tg.poll(timeout=0)
    if not tg.chat_id(ups):
        print("채팅 ID를 모름: 텔레그램에서 봇에게 아무 말이나 먼저 보내 주세요.")
        return
    commit_push("telegram: 채팅 정보")
    dispatched_for = set()
    while time.time() < deadline:
        send_previews()
        decisions, _ = tg.poll(timeout=25)
        if decisions:
            handle(decisions)
        pending = jobs()
        waiting = [p for p in pending if not p[2].get("approved")]
        scheduled = [p for p in pending if p[2].get("approved")]
        for jid, jd, post in scheduled:  # 승인됐고 시각이 됐으면 publish 실행(한 번만)
            if when(post) <= now() and jid not in dispatched_for:
                dispatch_publish()
                dispatched_for.add(jid)
        if not waiting and all(j in dispatched_for for j, _, _ in scheduled):
            break
    commit_push("telegram: 상태 저장")


if __name__ == "__main__":
    main()
