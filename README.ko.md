# Persona Prompt Corpus (한국어)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23230144.svg)](https://doi.org/10.5281/zenodo.23230144)

English: [README.md](README.md)

GitHub 공개 저장소에서 수집한 **AI 에이전트 페르소나 프롬프트 281건**의 데이터셋입니다.
`SOUL.md`·`persona.md`·`IDENTITY.md` 처럼 에이전트의 정체성·가치·어조·행동 한계를 선언하는
파일을, 저장소·경로·커밋 SHA 를 고정해 모았습니다.

- **레코드 281건 / 저장소 168곳**
- **전 레코드 provenance 고정** (281/281) — 저장소·경로·수집 시점의 커밋 SHA
- 원문 수록 **179건**, 메타데이터만 **102건** (아래 "라이선스 게이트" 참고)
- **전 레코드에 두 평가자의 라벨** (v1.1) — 내용 facet 9개, 조건절 개수, 순서형 형태 척도.
  주석 가이드와 항목별 불일치 목록 포함

> 이 README 의 수치는 `scripts/build_public_bundle.py` 가 데이터에서 세어 적습니다.
> 손으로 적지 않으므로 데이터와 어긋나지 않습니다.

---

## 무엇이 들어 있나

```
data/
  records.jsonl          레코드 281건 (JSON Lines)
  content/               원문 179건 — 재배포가 허용된 것만
  dup_clusters.csv       저장소 간 근접 중복 군집 (코퍼스에 유지, 목록만 공개)
labels/
  rater1.csv             평가자 1 라벨 (레코드당 1행)
  rater2.csv             평가자 2 라벨 (독립 코딩)
  disagreements.csv      두 평가자가 다른 레코드×항목 (1017행)
schema/
  record.schema.json     레코드 스키마
docs/
  COLLECTION_METHOD.md   수집 방법 (국문: COLLECTION_METHOD.ko.md)
  ANNOTATION_GUIDE.md    판정 질문과 경계 사례 (영문)
  SCHEME_HISTORY.md      형태 척도가 3단이 된 경위 (영문, 파일럿 수치)
scripts/
  stats.py               코퍼스 통계 (라벨 무관)
  label_stats.py         라벨 의존 수치, 평가자별
  agreement.py           평가자 간 일치도 (Krippendorff α, Cohen κ)
  refetch_pinned.py      고정 커밋에서 다시 받아 대조
  license_gate.py        라이선스 게이트 감사, 선택 시 GitHub 에서 SPDX 재조회
  find_duplicates.py     근접 중복 탐지 (재실행은 수록 원문 범위)
requirements.txt
```

### 레코드 한 건의 모양

```json
{
  "id": "gh-000013",
  "source": {
    "repo": "ceciliomichael/echode",
    "path": "identity/ask.md",
    "commit_sha": "e1dc45961bf4ffebf7d8a3696c3bc2b5de7c180e",
    "url": "https://github.com/ceciliomichael/echode/blob/HEAD/identity/ask.md",
    "collected_at": "2026-08-09",
    "search_path": "identity"
  },
  "license": { "spdx": "MIT", "redistributable": true, "copyleft_review": false, "content_included": true },
  "full_text_ref": "content/gh-000013.md",
  "content_sha256": "…",
  "summary": "Excerpt of a coding-assistant app's 'Ask Mode' identity + communication-style prompt sections: …",
  "tags": ["coding-assistant", "documentation-excerpt"],
  "stats": { "chars": 937, "words": 125, "lang": "en", "format": "md",
             "headers_max_depth": 1, "has_code_block": true, "has_table": false },
  "refetch": "same",
  "refetched_at": "2026-09-06"
}
```

`full_text_ref` 가 `null` 이면 원문이 수록되지 않은 레코드입니다. 그 경우에도
`source.commit_sha` 가 있으므로 **상류 저장소가 남아 있는 한 원본을 직접 받아올 수 있습니다.**
수집 뒤 저장소가 삭제되거나 비공개로 바뀔 수 있고, 실제로 그런 곳이 있습니다. 그런 레코드는
메타데이터만 남습니다.

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

## 라벨

두 평가자가 281건 전부를 상의 없이, 기계 사전 채움 없이 독립적으로 코딩했습니다. 항목 정의와
경계 사례는 [docs/ANNOTATION_GUIDE.md](docs/ANNOTATION_GUIDE.md) 에 있습니다.

**쓰기 전에 신뢰도를 보세요.** `structure_form` 은 신뢰 기준을 넘었습니다(순서형
Krippendorff α = 0.84). 내용 facet 9개는 모두 α 0.667 미만이고, 불일치는 대부분 한쪽으로
쏠립니다 — 정체성·목표 같은 개념의 경계를 두 평가자가 다른 곳에 그었다는 뜻입니다. 그래서
합의한 단일 라벨 대신 두 평가자의 라벨과 불일치 목록을 그대로 공개합니다. facet 수치는
평가자 간 범위로 읽고, 두 평가자 모두에서 성립하는 패턴만 쓰세요.

```bash
pip install -r requirements.txt
python3 scripts/agreement.py        # α·κ·불일치 방향
python3 scripts/label_stats.py      # 내용 유형, 형태×내용, 경로별 수치
```

---

## 라이선스

- **이 프로젝트가 만든 메타데이터·라벨·스키마·문서**: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- **`scripts/` 의 스크립트**: MIT (`scripts/LICENSE`)
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
- 내용 facet 라벨은 통상의 신뢰 기준에 못 미칩니다(위 "라벨"). 이 판에서는 정의를 고치거나
  불일치를 재코딩하지 않았습니다.
- 두 평가자 모두 데이터셋 저자이며, 평가자 1은 `summary`·`tags` 도 썼습니다.
- 2026-09-06 재수집 이전 단계의 후보 수와 스크리닝 기록은 공개본에 없고, 포함 판정 자체의
  일치도는 재지 않았습니다.

---

## 인용

이 데이터셋을 쓰셨다면 Zenodo DOI 로 인용해 주세요.

> **10.5281/zenodo.23230144** — https://doi.org/10.5281/zenodo.23230144

이것은 *concept* DOI 로, 항상 최신 판을 가리킵니다. 특정 판을 인용하려면 Zenodo
레코드에서 그 릴리스의 DOI 를 쓰면 됩니다.

### 판

- **v1.1.0** — 두 평가자 라벨, 불일치 목록, 주석 가이드, 척도 경위 문서, 근접 중복 군집 목록,
  일치도·라벨 통계·재수집·라이선스 게이트·중복 탐지 스크립트 추가. 레코드와 원문은 그대로.
- **v1.0.0** — 레코드 281건, 원문 수록 179건.

## 문의

이슈로 남겨 주세요. 분류를 다시 하거나 확장한 결과를 공유해 주시면 반갑습니다.
