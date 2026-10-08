# Persona Prompt Corpus (한국어)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23230144.svg)](https://doi.org/10.5281/zenodo.23230144)

English: [README.md](README.md)

GitHub 공개 저장소에서 수집한 **AI 에이전트 페르소나 프롬프트 281건**의 데이터셋입니다.
`SOUL.md`·`persona.md`·`IDENTITY.md` 처럼 에이전트의 정체성·가치·어조·행동 한계를 선언하는
파일을, 저장소·경로·커밋 SHA 를 고정해 모았습니다.

- **레코드 281건 / 저장소 168곳**
- **전 레코드 provenance 고정** (281/281) — 저장소·경로·수집 시점의 커밋 SHA
- 원문 수록 **179건**, 메타데이터만 **102건** (아래 "라이선스 게이트" 참고)

> 이 README 의 수치는 `scripts/build_public_bundle.py` 가 데이터에서 세어 적습니다.
> 손으로 적지 않으므로 데이터와 어긋나지 않습니다.

---

## 무엇이 들어 있나

```
data/
  records.jsonl        레코드 281건 (JSON Lines)
  content/             원문 179건 — 재배포가 허용된 것만
schema/
  record.schema.json   레코드 스키마
docs/
  COLLECTION_METHOD.md 수집 방법
scripts/
  stats.py             코퍼스 통계 재생성
```

### 레코드 한 건의 모양

```json
{
  "id": "gh-000001",
  "source": {
    "repo": "HLR/DomiKnowS",
    "path": "Agent.md",
    "commit_sha": "d3fb1904b602f69e654986d6add27cc18db7312f",
    "url": "https://github.com/HLR/DomiKnowS/blob/HEAD/Agent.md",
    "collected_at": "2026-08-09"
  },
  "license": { "spdx": "MIT", "redistributable": true, "content_included": true },
  "full_text_ref": "content/gh-000001.md",
  "content_sha256": "…",
  "summary": "Two-phase DomiKnowS graph-builder agent: …",
  "tags": ["coding-assistant", "domain-expert", "structured-output"],
  "refetch": "same",
  "refetched_at": "2026-09-06",
  "stats": { "chars": 7335, "words": 980, "lang": "en", "format": "md",
             "headers_max_depth": 3, "has_code_block": true, "has_table": true }
}
```

`full_text_ref` 가 `null` 이면 원문이 수록되지 않은 레코드입니다. 그 경우에도
`source.commit_sha` 가 있으므로 **원본을 직접 받아올 수 있습니다.**

---

## 라이선스 게이트 — 왜 102건은 원문이 없나

원문을 다시 배포하는 것은 **저작물의 재출판**입니다. 그래서 수집한 저장소 전수의 SPDX 를
확인하고, 재배포가 허용되는 레코드의 원문만 수록했습니다.

| | 레코드 |
|---|---|
| 원문 수록 | **179** |
| 메타데이터만 | **102** |

수록분의 라이선스 분포: MIT 138 · Apache-2.0 31 · CC-BY-4.0 7 · BSD-3-Clause 2 · CC0-1.0 1

빠진 102건의 대부분은 **라이선스가 명시되지 않은 저장소**입니다. 라이선스가 없다는 것은
"써도 된다"가 아니라 저작권이 그대로 살아 있다는 뜻이므로 원문을 수록하지 않았습니다.
나머지는 카피레프트 저장소로, 아카이브 라이선스를 단순하게 유지하기 위해 메타만 남겼습니다.

이 판정은 글이 아니라 **데이터에 들어 있습니다** — `license.redistributable` 과
`license.content_included` 두 필드로, 레코드 하나하나를 감사할 수 있습니다.
배포본은 빌드 스크립트가 그 필드를 읽어 매번 새로 만듭니다. 사람이 파일을 골라
복사하지 않습니다.

---

## 라이선스

- **이 저장소가 만든 것** — 메타데이터, 스키마, 문서, 스크립트: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- **`data/content/` 의 원문** — 각 원저작자의 라이선스를 그대로 따릅니다.
  레코드별 SPDX 는 `records.jsonl` 의 `license.spdx` 에 있습니다.

원문을 이용할 때는 해당 레코드의 라이선스와 원저작자 표기를 확인해 주세요.

---

## 쓰는 법

```python
import json, pathlib

recs = [json.loads(l) for l in open("data/records.jsonl", encoding="utf-8")]

with_text = [r for r in recs if r["full_text_ref"]]          # 원문이 있는 레코드
text = pathlib.Path("data", with_text[0]["full_text_ref"]).read_text(encoding="utf-8")
```

통계 재생성:

```bash
python3 scripts/stats.py
```

---

## 한계

- GitHub 한정 수집이라 개발자가 쓴 페르소나로 치우쳐 있습니다.
- 경로 기반 검색은 **관습적 명명도 놓칩니다.** 같은 모집단을 스캔했을 때 `.agents/` 관습을
  쓰는 저장소 3곳이 이 코퍼스에 들어오지 않았습니다.
- 단일 시점 스냅샷입니다(수집 마감 2026-09-30).
- 거의 전부 영어입니다(281건 중 280건 — 문자 기반 판정이라 근사치입니다).
- `summary` 와 `tags` 는 **데이터셋 작성자가 수집 과정에서 직접 쓴 것**입니다. 원문에서 자동
  추출한 것이 아니며, 탐색과 필터 편의를 위한 것입니다.
- 평가자 간 일치도를 재는 **분류 라벨은 아직 포함되지 않았습니다.** 평가가 끝나고 일치도를
  보고할 수 있게 되면 별도 릴리스로 추가합니다.

---

## 인용

이 데이터셋을 쓰셨다면 Zenodo DOI 로 인용해 주세요.

> **10.5281/zenodo.23230144** — https://doi.org/10.5281/zenodo.23230144

이것은 *concept* DOI 로, 항상 최신 판을 가리킵니다. 특정 판을 인용하려면 Zenodo
레코드에서 그 릴리스의 DOI 를 쓰면 됩니다.

## 문의

이슈로 남겨 주세요. 분류를 다시 하거나 확장한 결과를 공유해 주시면 반갑습니다.
