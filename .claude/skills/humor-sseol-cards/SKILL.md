---
name: "humor-sseol-cards"
description: "유머채널(썰 재구성) 인스타 카드를 원고 작성·렌더·검수할 때 사용. 배민 주아체 흰 외곽선 제목 표지와 흰 바탕 썰 카드 틀을 따른다."
---

# 유머채널 썰 카드 제작법

채널 운영 원칙은 프로젝트 문서 `claude/유머채널_운영가이드.md`에 있다. 작업 시작 시 그 문서를 읽고 따른다. 이 스킬은 그 원칙 위에 **카드 디자인과 제작 순서**를 정한다. 이 스킬 원본 사본은 프로젝트 `claude/skill/humor-sseol-cards_SKILL.md`에도 있다.

## 지킬 것 (운영 가이드 요약)
- 커뮤니티 인기글은 **상황·전개·반전 세 줄 메모**로만 받는다. 원문 문장, 캡처, 원본 짤, 닉네임은 쓰지 않는다. 사용자가 원문을 통째로 붙여 넣으면 세 줄로 줄인 뒤 그 메모만 보고 새로 쓴다.
- 등장인물 관계·장소·물건·대사를 우리 버전으로 바꾼다.
- 실존 인물(연예인, 유튜버, 정치인), 특정 가능한 회사·지인, 혐오·비하·성적 소재는 쓰지 않는다.
- 이미지는 AI 생성, 직접 만든 것, 무료 라이선스 사진만 쓴다. 연예인 사진, 다른 계정·언론사 로고, 인증 배지가 든 이미지는 쓰지 않는다.

## 디자인 (2026.10.23 사용자 지정, 참고 피드 실측)
참고한 것은 **배치와 글자 스타일**이다. 다른 계정의 로고·이름·인증 배지·사진은 가져오지 않고, 헤더와 워터마크는 우리 채널 것만 쓴다.

**공통**: 1080x1350(4:5). 프로필 격자에서 좌우가 약 34px 잘리므로 글자는 좌우 48px 안쪽.

**1장 표지 (`type: cover`)**
- 사진을 카드 전체에 꽉 채운다(그라데이션 없음).
- 제목 2줄, 가운데 정렬, **배민 주아체(참고 피드와 같은 동글동글한 글씨체)**를 살짝 두꺼게(글자 크기의 약 1.2%) 한 흰 글씨 + 두꺼운 검정 외곽선(약 12%) + 흐린 그림자. 자간을 좁게(-4%) 붙여 쓴다.
- 마지막 줄 중심이 카드 높이 약 80%. 제목 블록은 사진 아래쪽 1/3에 놓인다.
- 줄당 한글 8~11자. 길면 렌더러가 글자를 줄여 맞춘다. 끝에 `ㄷㄷ`, `ㅋㅋ`를 붙이면 커뮤 느낌이 산다.
- 제목 틀 예: "~하는 나라 ㄷㄷ", "~해서 ~한 능력자 직원", "~하자마자 던진 황당한 질문", "~하다가 ~된 썰", "요즘 ~ 근황".

**2장~ 썰 카드 (`type: story`)**
- 흰 바탕. 맨 위 헤더: 둥근 사각 프로필 사진 + 채널 이름(굵게) + @아이디(회색).
- 굵은 검정 헤드라인 한 줄(그 장의 요약 또는 다음 궁금증). 헤드라인은 주아체가 아니라 각진 고딕 Black.
- 가로 사진 박스(약 1.8:1, 얇은 테두리), 우하단에 초록 점 + 채널 이름 워터마크.
- 아래 본문: 짧은 줄 끊기, 문단 사이 띄움. 핵심 문단(반전, 결정적 한 줄)은 `bold: true`.
- 본문이 넘치면 렌더러가 글자를 줄이고, 그래도 넘치면 경고를 낸다 → 글을 줄인다.

**장 구성 (기본 3장, 길면 4~5장)**
| 장 | 내용 |
|---|---|
| 1 | 표지: 사진 + 2줄 후킹 제목 |
| 2 | 상황·전개. 헤드라인은 "그래서 어떻게 됐냐면" 류로 넘김 유도 |
| 3 | 반전(굵게) + 마지막 줄 댓글 유도("너네도 ~ 있으면 댓글 ㄱㄱ") |
- 반전은 반드시 장을 넘겨야 보이게 둔다. 표지와 2장 헤드라인에 반전을 쓰지 않는다.
- 말투는 커뮤 반말체(~함, ~했음, ~임). 이모지는 쓰지 않거나 장당 1개.

## 작업 순서
1. **세 줄 메모 확인**: 소재 기준(가이드 2번)에 걸리면 이유를 한 줄로 말하고 다른 소재를 청한다.
2. **원고**: 표지 제목 후보 3개(하나 추천) + 장별 헤드라인·본문을 채팅에 먼저 보여준다.
3. **이미지 프롬프트**: 장마다 AI 이미지 프롬프트를 코드 블록으로 준다(한국어, 복사 한 번에).
   - 표지: `세로 4:5, 실제 사진처럼 보이는 극사실적 장면, 등장인물의 과장된 표정이 화면 위쪽 2/3에 크게, 아래쪽 1/3은 단순하게 비워 글자 자리`.
   - 썰 카드 사진: `가로 16:9, 일상 스냅 사진 느낌, 그 장면 한 컷`.
   - 실존 인물·브랜드 로고를 넣지 않는다. 등장인물은 평범한 한국인 일반인으로 묘사한다.
   - 사용자가 Higgsfield 생성을 원하면 그 도구로 만든다(크레딧이 드니 먼저 묻는다).
4. **렌더**: 아래 렌더러를 작업 폴더에 `render_cards.py`로 저장하고 spec.json을 만들어 실행한다. 이미지가 아직 없으면 자리표시로 먼저 렌더해 배치를 확인한다.
5. **검수**: 결과 장들을 한 장으로 이어 붙여 직접 보고 확인한다(줄 넘침, 얼굴이 제목에 가림, 워터마크 겹침). 사진이 제목과 겹치면 `fy`(0~1, 세로 초점)로 조정한다.
6. **전달**: 카드 이미지 파일들 + 캡션(가이드 6번 틀, 해시태그 5개 이내) + AI 이미지면 캡션 끝에 "이미지: AI 생성"을 붙인다.

## spec.json 형식
```json
{
  "out_dir": "out/<소재id>",
  "channel": {"name": "채널이름", "handle": "@아이디", "avatar": "avatar.png"},
  "slides": [
    {"type": "cover", "image": "cover.jpg", "title": "줄1\n줄2 ㄷㄷ", "fy": 0.35},
    {"type": "story", "headline": "헤드라인", "image": "s2.jpg",
     "paras": [{"text": "문단\n둘째 줄"}, {"text": "핵심 문단", "bold": true}]}
  ]
}
```
선택 값: cover `size`(제목 최대 글자 크기, 기본 140, 줄이 길면 자동 축소), `track`(자간 좁힘 비율, 기본 0.04), `embolden`(제목 두꺼게 비율, 기본 0.012), `bottom`(마지막 줄 위치, 기본 0.80); story `image_h`(사진 높이, 기본 540), `headline_size`(58), `body_size`(46), `fx`/`fy`(사진 초점).

## 글꼴 (2026.10.23 사용자 지시: 보내준 피드와 같은 글씨체)
- **표지 제목 = 배민 주아체** `fonts/BMJUA.otf`(우아한형제들, 상업 무료). 참고 피드 제목과 글자 모양을 나란히 비교해 확인했다. 원본은 주아체를 살짝 두꺼게 쓴 형태라 렌더러가 `embolden`으로 두께를 더한다.
- 작업 폴더에 없으면 GitHub에서 받는다(작업공간에서 git은 통한다, curl은 막힘):
  `git clone --depth 1 https://github.com/fonts-archive/BMJua.git /tmp/bmjua && mkdir -p fonts && cp /tmp/bmjua/BMJUA.otf fonts/`
- 주아체를 못 받으면 잘난체(`fonts-archive/Jalnan`, `Jalnan.otf`)로, 그것도 없으면 Noto Black으로 대체되며 그때는 사용자에게 한 줄로 알린다.
- 썰 카드 헤드라인·본문은 Pretendard(`fonts/Pretendard-*.otf`)가 있으면 쓰고, 없으면 Noto Sans CJK KR(Black/Bold/Medium).

## 렌더러 (`render_cards.py`)
```python
#!/usr/bin/env python3
"""유머채널 카드 렌더러 (1080x1350, 4:5)

사용법: python3 render_cards.py spec.json
- 이미지가 없거나 경로가 틀리면 회색 자리표시 이미지가 들어간다.
- 글꼴: 표지 제목은 fonts/BMJUA.otf(배민 주아체, 참고 피드와 같은 글씨체)를 살짝 두꺼게. 썰 카드 헤드라인·본문은 Pretendard가 fonts/에 있으면 쓰고, 없으면 Noto Sans CJK KR.
"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

W, H = 1080, 1350
HERE = os.path.dirname(os.path.abspath(__file__))
NOTO = "/usr/share/fonts/opentype/noto/NotoSansCJK-{}.ttc"


def font(kind, size):
    cands = {
        "title": ["BMJUA.otf", "BMJUA.ttf", "Jalnan.otf"],
        "headline": ["Pretendard-Black.otf", "Pretendard-ExtraBold.otf"],
        "bold": ["Pretendard-ExtraBold.otf", "Pretendard-Bold.otf"],
        "regular": ["Pretendard-Medium.otf", "Pretendard-Regular.otf"],
    }[kind]
    for d in (os.path.join(HERE, "fonts"), os.path.join(os.getcwd(), "fonts")):
        for c in cands:
            p = os.path.join(d, c)
            if os.path.exists(p):
                return ImageFont.truetype(p, size)
    weight = {"title": "Black", "headline": "Black", "bold": "Bold", "regular": "Medium"}[kind]
    return ImageFont.truetype(NOTO.format(weight), size, index=1)  # index 1 = KR


def load_img(path, base):
    if path:
        p = path if os.path.isabs(path) else os.path.join(base, path)
        if os.path.exists(p):
            return Image.open(p).convert("RGB")
    ph = Image.new("RGB", (1080, 1350), (70, 74, 82))
    d = ImageDraw.Draw(ph)
    d.text((540, 675), "이미지 자리", font=font("bold", 60), fill=(150, 154, 162), anchor="mm")
    return ph


def cover_fit(img, w, h, fx=0.5, fy=0.4):
    return ImageOps.fit(img, (w, h), Image.LANCZOS, centering=(fx, fy))


def wrap(text, f, maxw, draw):
    out = []
    for raw in text.split("\n"):
        line = ""
        for word in raw.split(" "):
            t = (line + " " + word).strip()
            if draw.textlength(t, font=f) <= maxw or not line:
                line = t
            else:
                out.append(line)
                line = word
        out.append(line)
    return out


# ---------- 1장: 표지 ----------
def tracked_width(text, f, track, draw):
    return sum(draw.textlength(c, font=f) for c in text) + track * (len(text) - 1)


def draw_tracked(draw, cx, cy, text, f, track, **kw):
    """글자 사이를 좁혀(자간 음수) 가운데 정렬로 그린다."""
    x = cx - tracked_width(text, f, track, draw) / 2
    for c in text:
        draw.text((x, cy), c, font=f, anchor="lm", **kw)
        x += draw.textlength(c, font=f) + track


def render_cover(s, ch, base):
    img = cover_fit(load_img(s.get("image"), base), W, H, s.get("fx", 0.5), s.get("fy", 0.4))
    lines = s["title"].split("\n")
    probe = ImageDraw.Draw(img)
    size = s.get("size", 140)
    while size > 70:
        f = font("title", size)
        tr = -size * s.get("track", 0.04)
        if max(tracked_width(l, f, tr, probe) for l in lines) <= W - 2 * 56:
            break
        size -= 2
    f = font("title", size)
    tr = -size * s.get("track", 0.04)
    stroke = max(10, round(size * 0.12))
    bold = max(1, round(size * s.get("embolden", 0.012)))  # 주아체를 원본처럼 살짝 두꺼게
    lh = round(size * 1.32)
    # 제목 블록: 마지막 줄 중심이 카드 높이 약 80% (참고 디자인 실측)
    last_cy = round(H * s.get("bottom", 0.80))
    first_cy = last_cy - lh * (len(lines) - 1)

    # 은은한 그림자
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    for i, l in enumerate(lines):
        draw_tracked(sd, W // 2 + 4, first_cy + i * lh + 8, l, f, tr, fill=(0, 0, 0, 170),
                     stroke_width=stroke + 4, stroke_fill=(0, 0, 0, 170))
    shadow = shadow.filter(ImageFilter.GaussianBlur(10))
    img = Image.alpha_composite(img.convert("RGBA"), shadow)

    # 외곽선을 먼저 전부 그리고, 흰 글자를 위에 얹는다(자간이 좁아도 외곽선이 글자를 덮지 않게)
    d = ImageDraw.Draw(img)
    for i, l in enumerate(lines):
        draw_tracked(d, W // 2, first_cy + i * lh, l, f, tr, fill="black",
                     stroke_width=stroke + bold, stroke_fill="black")
    for i, l in enumerate(lines):
        draw_tracked(d, W // 2, first_cy + i * lh, l, f, tr, fill="white",
                     stroke_width=bold, stroke_fill="white")
    return img.convert("RGB")


# ---------- 2장~: 흰 바탕 썰 카드 ----------
def render_story(s, ch, base):
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    X = 48
    # 헤더: 프로필 + 채널 이름 + 아이디
    av_r = 58
    av = load_img(ch.get("avatar"), base) if ch.get("avatar") else Image.new("RGB", (av_r, av_r), (255, 214, 0))
    av = cover_fit(av, av_r, av_r, 0.5, 0.5)
    m = Image.new("L", (av_r, av_r), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, av_r - 1, av_r - 1), radius=12, fill=255)
    img.paste(av, (X, 26), m)
    d.text((X + av_r + 14, 28), ch.get("name", "채널이름"), font=font("bold", 27), fill=(20, 20, 20))
    d.text((X + av_r + 14, 60), ch.get("handle", "@channel"), font=font("regular", 22), fill=(110, 110, 110))

    # 굵은 헤드라인
    hf = font("headline", s.get("headline_size", 58))
    y = 112
    for l in wrap(s["headline"], hf, W - 2 * X, d):
        d.text((X, y), l, font=hf, fill=(15, 15, 15))
        y += round(hf.size * 1.25)
    y += 10

    # 사진 박스 (테두리 + 우하단 채널 워터마크)
    bw = W - 2 * X
    bh = s.get("image_h", 540)
    ph = cover_fit(load_img(s.get("image"), base), bw, bh, s.get("fx", 0.5), s.get("fy", 0.4))
    img.paste(ph, (X, y))
    d.rectangle((X, y, X + bw - 1, y + bh - 1), outline=(60, 60, 60), width=2)
    wf = font("bold", 26)
    wm = ch.get("name", "채널이름")
    tw = d.textlength(wm, font=wf)
    wx, wy = X + bw - 24 - tw, y + bh - 50
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sdd = ImageDraw.Draw(sh)
    sdd.text((wx + 2, wy + 2), wm, font=wf, fill=(0, 0, 0, 200))
    sdd.ellipse((wx - 28, wy + 9, wx - 12, wy + 25), fill=(0, 0, 0, 200))
    sh = sh.filter(ImageFilter.GaussianBlur(2))
    img = Image.alpha_composite(img.convert("RGBA"), sh).convert("RGB")
    d = ImageDraw.Draw(img)
    d.ellipse((wx - 30, wy + 7, wx - 14, wy + 23), fill=(52, 199, 89))
    d.text((wx, wy), wm, font=wf, fill="white")
    y += bh + 22

    # 본문 문단
    size = s.get("body_size", 46)
    paras = s.get("paras", [])
    while True:
        rf, bf = font("regular", size), font("bold", size)
        lh, gap = round(size * 1.5), round(size * 0.55)
        total = sum(len(wrap(p["text"], bf if p.get("bold") else rf, W - 2 * X, d)) * lh + gap for p in paras)
        if y + total <= H - 40 or size <= 30:
            break
        size -= 2
    for p in paras:
        f = bf if p.get("bold") else rf
        for l in wrap(p["text"], f, W - 2 * X, d):
            d.text((X, y), l, font=f, fill=(15, 15, 15))
            y += lh
        y += gap
    if y > H - 20:
        print(f"  ! 본문이 넘침: 글을 줄이세요 ({s['headline'][:12]}…)")
    return img


def main(spec_path):
    spec = json.load(open(spec_path, encoding="utf-8"))
    base = os.path.dirname(os.path.abspath(spec_path))
    out = spec.get("out_dir", "out")
    out = out if os.path.isabs(out) else os.path.join(base, out)
    os.makedirs(out, exist_ok=True)
    ch = spec.get("channel", {})
    files = []
    for i, s in enumerate(spec["slides"], 1):
        r = render_cover if s.get("type") == "cover" else render_story
        p = os.path.join(out, f"{i:02d}.jpg")
        r(s, ch, base).save(p, quality=93)
        files.append(p)
        print(p)
    return files


if __name__ == "__main__":
    main(sys.argv[1])
```