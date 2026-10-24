"""커뮤니티 페이지 읽기 공통 함수 (디시인사이드, 개드립, 그 밖의 일반 페이지)."""
import re
import time
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36")
S = requests.Session()
S.headers.update({"User-Agent": UA, "Accept-Language": "ko-KR,ko;q=0.9",
                  "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"})
LOG = []  # 진단용: (상태, 주소) — 액션 로그를 못 볼 때 저장소에 남긴다
LAST_HTML = {}  # 주소 → 마지막으로 받은 HTML(실패 분석용)

# 사이트별 본문 영역 (앞에서부터 찾는다)
CONTENT_SEL = [
    "div.write_div",            # 디시인사이드
    "div.rhymix_content",       # 개드립
    "div.xe_content",           # 개드립(구버전)·XE 계열
    "article",
    "div#content", "div.content",
]


def get(url, referer=None, tries=3):
    for i in range(tries):
        try:
            r = S.get(url, timeout=20, headers={"Referer": referer or f"{urlparse(url).scheme}://{urlparse(url).netloc}/"})
            LOG.append(f"{r.status_code} {len(r.content)}B {url}")
            if r.status_code == 200:
                return r
            print(f"  {r.status_code} {url}")
            LAST_HTML[url] = r.text[:200000]
        except requests.RequestException as e:
            LOG.append(f"오류 {type(e).__name__} {url}")
            print(f"  오류 {e} {url}")
        time.sleep(1.5 * (i + 1))
    return None


def soup(url):
    r = get(url)
    if not r:
        return None, None
    r.encoding = r.apparent_encoding if not r.encoding or r.encoding.lower() == "iso-8859-1" else r.encoding
    return BeautifulSoup(r.text, "html.parser"), r.text


def meta(sp, prop):
    m = sp.find("meta", property=prop) or sp.find("meta", attrs={"name": prop})
    return (m.get("content") or "").strip() if m else ""


def content_node(sp):
    for sel in CONTENT_SEL:
        n = sp.select_one(sel)
        if n and (n.get_text(strip=True) or n.find("img")):
            return n
    # 마지막 수단: 글자가 가장 많은 div
    best, best_len = None, 0
    for d in sp.find_all("div"):
        t = len(d.get_text(strip=True))
        if 200 < t and (best is None or t < best_len * 3) and d.find("img"):
            best, best_len = d, t
    return best


def img_urls(node, page_url):
    out = []
    if not node:
        return out
    for im in node.find_all(["img", "video", "source"]):
        src = im.get("data-original") or im.get("data-src") or im.get("src") or ""
        if not src or src.startswith("data:"):
            continue
        u = urljoin(page_url, src)
        if re.search(r"(emoticon|icon|btn_|/common/|spacer|blank\.gif|dccon)", u, re.I):
            continue
        if u not in out:
            out.append(u)
    return out


def read_post(url):
    """글 하나: 제목, 본문 글(앞부분), 이미지 주소 목록."""
    sp, raw = soup(url)
    if not sp:
        return None
    LAST_HTML[url] = raw
    title = ""
    for sel in ("span.title_subject", "h1", "h2.title", "h4", ".ed.title"):
        n = sp.select_one(sel)
        if n and n.get_text(strip=True):
            title = n.get_text(" ", strip=True)
            break
    title = meta(sp, "og:title") or title
    node = content_node(sp)
    text = node.get_text("\n", strip=True) if node else ""
    imgs = img_urls(node, url)
    if not imgs and meta(sp, "og:image"):
        imgs = [urljoin(url, meta(sp, "og:image"))]
    return {"url": url, "title": title, "text": text, "images": imgs}
