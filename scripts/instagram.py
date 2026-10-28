"""인스타그램 API(Instagram 로그인 방식, graph.instagram.com)로 캐러셀·릴스 게시.
오늘의쓸모(evan-stock/cardnews)의 instagram.py를 바탕으로 했다(중복 게시 방지 확인 포함).
필요한 저장소 Secrets: IG_ACCESS_TOKEN, IG_USER_ID (ㅋㅋ상회 계정)."""
import os
import time

import requests

API = "https://graph.instagram.com/v25.0"


def env(name):
    v = os.environ.get(name)
    if not v:
        raise SystemExit(f"환경변수 {name} 가 없어요. GitHub 저장소 Settings → Secrets and variables → Actions 에 추가해 주세요.")
    return v


def _req(method, path, **params):
    r = requests.request(method, f"{API}/{path}", timeout=120,
                         headers={"Authorization": f"Bearer {env('IG_ACCESS_TOKEN')}"},
                         **({"json": params} if method == "POST" else {"params": params}))
    j = r.json()
    if r.status_code != 200 or "error" in j:
        raise RuntimeError(f"인스타 API 오류 {r.status_code}: {j}")
    return j


def whoami():
    return _req("GET", "me", fields="user_id,username")


def _wait_ready(cid, tries=10):
    for _ in range(tries):
        st = _req("GET", cid, fields="status_code").get("status_code")
        if st == "FINISHED":
            return
        if st in ("ERROR", "EXPIRED"):
            raise RuntimeError(f"컨테이너 {cid} 상태 {st}")
        time.sleep(20)
    raise RuntimeError(f"컨테이너 {cid} 준비 시간 초과")


def _already_published(cid, caption):
    """게시 응답이 오류여도 실제로는 올라갔을 수 있다 → 다시 보내기 전에 확인(중복 게시 방지)."""
    ig = env("IG_USER_ID")
    try:
        st = _req("GET", cid, fields="status_code").get("status_code")
    except Exception:
        st = None
    try:
        recent = _req("GET", f"{ig}/media", fields="id,caption", limit=10).get("data", [])
    except Exception:
        recent = []
    head = (caption or "")[:80]
    for m in recent:
        if head and (m.get("caption") or "")[:80] == head:
            return m["id"]
    if st == "PUBLISHED":
        return recent[0]["id"] if recent else "published"
    return None


def _publish(cid, caption, tries=6):
    ig = env("IG_USER_ID")
    for k in range(tries):
        try:
            return _req("POST", f"{ig}/media_publish", creation_id=cid)["id"]
        except Exception as e:
            time.sleep(15)
            done = _already_published(cid, caption)
            if done:
                print(f"게시 응답은 오류였지만 이미 올라가 있어 다시 보내지 않음: {done}")
                return done
            if "2207027" not in str(e) or k == tries - 1:  # 2207027 = 아직 준비 안 됨
                raise
            time.sleep(5)


def _permalink(mid):
    try:
        return _req("GET", mid, fields="permalink").get("permalink", "")
    except Exception:
        return ""


def publish_carousel(image_urls, caption):
    ig = env("IG_USER_ID")
    caption = caption[:2200]
    if len(image_urls) == 1:
        one = _req("POST", f"{ig}/media", image_url=image_urls[0], caption=caption)["id"]
        _wait_ready(one)
        mid = _publish(one, caption)
        return mid, _permalink(mid)
    children = [_req("POST", f"{ig}/media", image_url=u, is_carousel_item=True)["id"] for u in image_urls[:10]]
    for c in children:
        _wait_ready(c)
    car = _req("POST", f"{ig}/media", media_type="CAROUSEL", children=",".join(children), caption=caption)["id"]
    _wait_ready(car)
    time.sleep(5)
    mid = _publish(car, caption)
    return mid, _permalink(mid)


def publish_reel(video_url, caption, cover_url=None):
    """릴스 게시(피드에도 노출). 영상 처리에 몇 분 걸릴 수 있어 최대 약 15분 기다린다.
    API로 올린 릴스는 나중에 인스타 음악을 넣을 수 없다(원본 소리를 넣어 렌더할 것)."""
    ig = env("IG_USER_ID")
    caption = caption[:2200]
    params = {"media_type": "REELS", "video_url": video_url, "caption": caption, "share_to_feed": True}
    if cover_url:
        params["cover_url"] = cover_url
    cid = _req("POST", f"{ig}/media", **params)["id"]
    _wait_ready(cid, tries=45)
    time.sleep(5)
    mid = _publish(cid, caption)
    return mid, _permalink(mid)


def refresh_token():
    """장기 토큰(60일) 갱신 → 새 토큰 문자열."""
    r = requests.get("https://graph.instagram.com/refresh_access_token", timeout=60,
                     params={"grant_type": "ig_refresh_token", "access_token": env("IG_ACCESS_TOKEN")})
    j = r.json()
    if "access_token" not in j:
        raise RuntimeError(f"토큰 갱신 실패: {j}")
    return j["access_token"]
