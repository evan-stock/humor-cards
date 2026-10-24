"""ㅋㅋ상회 전용 텔레그램 봇: 미리보기(카드 앨범 + 본문 + ✅/❌ 버튼) 보내기, 버튼 응답 받기.
Secrets: TELEGRAM_BOT_TOKEN(필수), TELEGRAM_CHAT_ID(선택 — 없으면 봇에게 처음 말 건 사람의 채팅으로 정해 state/telegram_chat.json에 저장).
오늘의쓸모 봇과 같은 봇을 쓰면 getUpdates 응답을 서로 가져가므로 반드시 전용 봇을 쓴다."""
import json
import os

import requests

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
STATE = os.path.join(ROOT, "state")
OFFSET_FILE = os.path.join(STATE, "telegram_offset.txt")
CHAT_FILE = os.path.join(STATE, "telegram_chat.json")


def enabled():
    return bool(os.environ.get("TELEGRAM_BOT_TOKEN"))


def _api(method, files=None, **data):
    url = f"https://api.telegram.org/bot{os.environ['TELEGRAM_BOT_TOKEN']}/{method}"
    r = requests.post(url, data=data if files else None, json=None if files else data, files=files, timeout=60)
    j = r.json()
    if not j.get("ok"):
        raise RuntimeError(f"텔레그램 {method} 실패: {j.get('description')}")
    return j["result"]


def _offset():
    try:
        return int(open(OFFSET_FILE).read().strip())
    except Exception:
        return 0


def _save_offset(v):
    os.makedirs(STATE, exist_ok=True)
    open(OFFSET_FILE, "w").write(str(v))


def chat_id(updates=None):
    if os.environ.get("TELEGRAM_CHAT_ID"):
        return os.environ["TELEGRAM_CHAT_ID"]
    try:
        return json.load(open(CHAT_FILE))["chat_id"]
    except Exception:
        pass
    for u in reversed(updates or []):
        m = u.get("message") or {}
        if m.get("chat", {}).get("type") == "private":
            os.makedirs(STATE, exist_ok=True)
            json.dump({"chat_id": m["chat"]["id"]}, open(CHAT_FILE, "w"))
            return m["chat"]["id"]
    return None


def send_text(text, buttons=None, chat=None):
    data = {"chat_id": chat or chat_id(), "text": text[:4000], "disable_web_page_preview": True}
    if buttons:
        data["reply_markup"] = {"inline_keyboard": buttons}
    return _api("sendMessage", **data)


def send_album(paths, chat=None):
    media, files = [], {}
    for i, p in enumerate(paths[:10]):
        files[f"f{i}"] = open(p, "rb")
        media.append({"type": "photo", "media": f"attach://f{i}"})
    return _api("sendMediaGroup", files=files, chat_id=chat or chat_id(), media=json.dumps(media))


def poll(timeout=25):
    """새 업데이트를 받아 (결정 목록, 원본 업데이트) 반환. 결정 = (\"ok\"|\"no\", job_id, callback_id)."""
    ups = _api("getUpdates", offset=_offset() + 1 if _offset() else 0, timeout=timeout,
               allowed_updates=["message", "callback_query"])
    out = []
    for u in ups:
        _save_offset(u["update_id"])
        cq = u.get("callback_query")
        if cq and ":" in (cq.get("data") or ""):
            act, jid = cq["data"].split(":", 1)
            out.append((act, jid, cq["id"]))
    return out, ups


def answer(callback_id, text):
    try:
        _api("answerCallbackQuery", callback_query_id=callback_id, text=text[:190])
    except Exception as e:
        print("answerCallbackQuery 실패:", e)
