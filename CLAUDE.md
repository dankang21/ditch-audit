# CLAUDE.md — ditch-audit 운영 규칙

종교철학 문헌의 실증 메타 연구. "외부 원인 → 니케아 유신론" 8스텝 사슬에 대해
문헌을 step × direction × claim strength × epistemic type × venue로 코딩한다.
정본 문서: `docs/` (outline v0.4 = 논문 설계, codebook-v1 (v1.1) = 코딩 도구,
gold-anchors-v1 = 진단용 골드셋, validation-battery-v1 = 제로휴먼 검증 배터리,
p0-sweep = 선행문헌 킬 스윕 보고). 지적 계보와 판정 이력: `CONTEXT.md`.

## 언어·컨벤션
- 대화·에이전트 정의: 한국어. 코드·커밋 메시지·연구 문서(docs/): 영어.
- git commit에 `Co-Authored-By` 라인 추가 금지.
- 페이즈 경계는 dk의 명시적 승인 없이 넘지 않는다 (HITL 게이트).

## 절대 규칙 (위반 = 즉시 중단 후 dk 보고)
1. **가설 방화벽.** 코더에게 전달되는 프롬프트는 `scripts/build_coder_prompt.py`의
   산출물(`pipeline/03_code/coder_prompt.txt`)만 사용한다. 수동 편집 금지.
   coder-runner 에이전트의 컨텍스트에 `CONTEXT.md`, `docs/outline-v*.md`,
   `docs/p0-sweep.md`, `docs/validation-battery-v1.md`, **`docs/codebook-v1.md`
   전체**의 내용을 절대 노출하지 않는다 (coder-runner는 빌드 프롬프트만 읽는다;
   금지 목록은 에이전트 정의와 항상 일치 유지). 이유: H1/H2를 아는 코더는
   예측 방향으로 드리프트한다.
2. **P3 freeze.** 사전등록(P3) 이후 수정 금지 대상: `docs/codebook-v1.md`, 빌드된
   프롬프트, `docs/validation-battery-v1.md`(임계값 표·실패 조치 §B10 포함),
   모델 스냅샷 핀 목록, 역할 배타 매트릭스, vault 합성 세트 해시.
   prereg-guardian이 SHA256 매니페스트로 기계 검증한다.
   freeze 이전의 codebook 수정은 반드시 §12 changelog에 기록.
3. **저작권 격리.** `data/raw|sanitized|coded`에는 저작권 있는 초록이 포함된다.
   .gitignore로 제외되어 있으며, 공개 원격 저장소에 push 금지. 논문·프리프린트에
   초록 원문을 재수록하지 않는다 (코드와 집계만 공개).
4. **시크릿.** API 키는 `.env`에만. 커밋 금지. 코더는 서로 다른 세 모델 패밀리
   (coder A = Anthropic, coder B = Google [`CODER_B_PROVIDER`], coder C = OpenAI
   [판정자]; 선택적 coder D = 오픈웨이트 아카이브. 역할 배타 매트릭스는
   validation-battery §B0).
5. **제로휴먼 룰 (dk 절대 결정, 2026-07-14).** 인간은 어떤 아이템도 코딩·판정하지
   않는다 — dk 포함. dk의 노동은 기기 설계(코드북 저술, 합성 criterion 스펙 작성·
   서명, 게이트 승인)에 한정. 불일치는 3패밀리 다수결로 자동 판정. 논문은
   "고정·사전등록된 다패밀리 LLM 기기의 측정"을 주장하며 인간 동등 어노테이션을
   주장하지 않는다 (초록에 무인 코딩 명시).

## 페이즈 게이트 (outline §10과 일치; 상세는 outline 참조)
| 페이즈 | 산출물 | 게이트 (dk 승인 + 조건) |
|---|---|---|
| P1 (현재) | 파일럿 코딩: RS 2015 (실측 35) + 골드 20 | **G1: 전 차원 Krippendorff α(A,B) ≥ 0.70 (3-way 병기)** |
| P2 | 코퍼스 수집 (T1 필터 + T2 2004–2024) | G2: 초록 커버리지 ≥ 90% |
| P3 | OSF 사전등록 freeze | 매니페스트 생성, 이후 수정 금지 |
| P4 | 본 코딩 (~1,500 × 3코더) + 검증 배터리 전체 (인간 검증 없음 — 절대 규칙 5) | 체크포인트·비용 로그 필수 |
| P5 | 분석 (H1/H2) | G5: 프레이밍 결정 (methods-forward vs results-forward) |
| P6 | 영어 초고 + AI 공시문 | venue 정책 확인 |

Kill criteria: G1 2회 실패 → D3를 3레벨로 축소 후 재게이트 ·
H1∧H2 null → 저널 투고 없이 프리프린트+에세이로 다운그레이드 (살라미 금지).

## 에이전트 오케스트레이션 (P1 시퀀스)
`harvester` → `sanitizer` → `coder-runner` (A/B/C 독립 3회) → `alpha-scorer`
→ 불일치는 `adjudication-logger`가 다수결 스크립트로 자동 판정·기록 (dk의
아이템 판정 없음 — 절대 규칙 5; dk HITL은 게이트 승인과 codebook 개정 승인만)
→ G1 보고 → dk 승인. `prereg-guardian`은 P3부터 모든 세션 시작 시 1회 실행.
에이전트 정의: `.claude/agents/`. 모델 기본 Opus (기계적 대량 작업은 정의 내
명시된 경우에만 다운그레이드 허용).

## P1 체크리스트 (2026-07-14 갱신)
- [x] `.env` 작성 (A/B 키 확인·검증 완료), `scripts/alpha.py selftest` PASS
- [x] `scripts/build_coder_prompt.py` → 프롬프트 + 매니페스트 (v1.1 재빌드 포함)
- [x] verify-at-pilot 서지 3건 확정 (A05/A07/A15 web-verified) + changelog
- [x] RS 2015 수집 (35편, 초록 100%) → `data/raw/pilot_rs2015.jsonl`
- [x] 골드 20편 수집 (초록 11 + 지면 초록 복원 3 + verbatim 발췌 6) → `data/raw/gold_anchors.jsonl`
- [x] sanitize 완료 (스크럽 로그, 55건) → `data/sanitized/`
- [ ] `.env`에 `OPENAI_API_KEY` 추가 (coder C) — dk
- [ ] 패밀리 E = **perplexity** 확정(dk) — `PERPLEXITY_API_KEY` 기입, 검색 비활성 검증 필수 (battery §B0)
- [ ] 코더 모델 스냅샷 핀 확정 (A/B/C[/D] + E) → cost_log에 기록
- [ ] 합성 criterion 스펙 초안 (dk 서명 대상) + dev/vault 분할·해시 (battery §B3)
- [ ] 트리플 코딩 → `data/coded/{pilot,gold}_{a,b,c}.jsonl`
- [ ] 배터리 P1 암: 인지 프로브 · cue-ablation 베이스라인 · 결정론 감사 · raw-vs-laundered 분기 측정 · dev-half 합성 정확도 (판별기 AUC 게이트 선행)
- [ ] `alpha.py rel` (A×B 게이트 + 3-way) + `alpha.py gold` (인지 점수 층화, 진단용) → G1 리포트
- [ ] S6 아이템 최초 발견 시 A21 승격 로그 (codebook §8)

## 환경
Python 3.10+. `scripts/`는 stdlib-only. fetch/sanitize/code 스텁은 이 시드
생성 환경(네트워크 제한 컨테이너)에서 미실행 — 로컬에서 엔드포인트 검증 필요.
