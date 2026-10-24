# humor-cards

유머채널 썰 카드 파이프라인: 인기글 서칭 → 원글 이미지 수집 → 카드 렌더.

| 단계 | 하는 곳 | 방법 |
|---|---|---|
| 1. 서칭 | GitHub Actions `scout` | 매일 19:00 KST 자동. 즉시 돌리려면 `requests/scout.txt` 내용을 바꿔 푸시. 결과 `scout/<날짜>.md`·`.json` |
| 2. 고르기·원고 | Claude 채팅 | 서칭 결과에서 후보를 골라 원고 작성, `jobs/<날짜-소재>/spec.json` |
| 3. 이미지 수집 | GitHub Actions `collect` | `jobs/<id>/collect.json`(`pages`·`image_urls`) 푸시 → `jobs/<id>/src/`에 저장, `candidates.jpg`로 번호 확인 |
| 4. 렌더 | Claude 채팅(로컬) | `python3 scripts/render_cards.py jobs/<id>/spec.json` → `jobs/<id>/out/` |

- 글꼴: `fonts/BMJUA.otf`(배민 주아체, 표지), `fonts/Pretendard-*.otf`(썰 카드). 둘 다 상업 무료.
- 렌더러 옵션과 디자인 규칙은 Claude 스킬 `humor-sseol-cards`에 있다.
