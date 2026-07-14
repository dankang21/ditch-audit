# CLAUDE.md — ditch-audit 운영 규칙

종교철학 문헌의 실증 메타 연구. "외부 원인 → 니케아 유신론" 8스텝 사슬에 대해
문헌을 step × direction × claim strength × epistemic type × venue로 코딩한다.
정본 문서: `docs/` (outline v0.3 = 논문 설계, codebook-v1 = 코딩 도구,
gold-anchors-v1 = 검증 골드셋, p0-sweep = 선행문헌 킬 스윕 보고).
지적 계보와 판정 이력: `CONTEXT.md`.

## 언어·컨벤션
- 대화·에이전트 정의: 한국어. 코드·커밋 메시지·연구 문서(docs/): 영어.
- git commit에 `Co-Authored-By` 라인 추가 금지.
- 페이즈 경계는 dk의 명시적 승인 없이 넘지 않는다 (HITL 게이트).

## 절대 규칙 (위반 = 즉시 중단 후 dk 보고)
1. **가설 방화벽.** 코더에게 전달되는 프롬프트는 `scripts/build_coder_prompt.py`의
   산출물(`pipeline/03_code/coder_prompt.txt`)만 사용한다. 수동 편집 금지.
   coder-runner 에이전트의 컨텍스트에 `CONTEXT.md`, `docs/outline-v0.3.md`,
   `docs/p0-sweep.md`의 내용을 절대 노출하지 않는다 (읽기 금지 목록은 에이전트
   정의에 명시). 이유: H1/H2를 아는 코더는 예측 방향으로 드리프트한다.
2. **P3 freeze.** 사전등록(P3) 이후 `docs/codebook-v1.md` 및 빌드된 프롬프트의
   수정 금지. prereg-guardian이 SHA256 매니페스트로 기계 검증한다.
   freeze 이전의 codebook 수정은 반드시 §12 changelog에 기록.
3. **저작권 격리.** `data/raw|sanitized|coded`에는 저작권 있는 초록이 포함된다.
   .gitignore로 제외되어 있으며, 공개 원격 저장소에 push 금지. 논문·프리프린트에
   초록 원문을 재수록하지 않는다 (코드와 집계만 공개).
4. **시크릿.** API 키는 `.env`에만. 커밋 금지. 두 코더는 서로 다른 모델 패밀리
   (coder A = Anthropic, coder B = `CODER_B_PROVIDER` 지정 타사).

## 페이즈 게이트 (outline §10과 일치; 상세는 outline 참조)
| 페이즈 | 산출물 | 게이트 (dk 승인 + 조건) |
|---|---|---|
| P1 (현재) | 파일럿 코딩: RS 2015 (~50) + 골드 20 | **G1: 전 차원 Krippendorff α ≥ 0.70** |
| P2 | 코퍼스 수집 (T1 필터 + T2 2004–2024) | G2: 초록 커버리지 ≥ 90% |
| P3 | OSF 사전등록 freeze | 매니페스트 생성, 이후 수정 금지 |
| P4 | 본 코딩 (~1,500 × 2코더) + 인간 검증 150 | 체크포인트·비용 로그 필수 |
| P5 | 분석 (H1/H2) | G5: 프레이밍 결정 (methods-forward vs results-forward) |
| P6 | 영어 초고 + AI 공시문 | venue 정책 확인 |

Kill criteria: G1 2회 실패 → D3를 3레벨로 축소 후 재게이트 ·
H1∧H2 null → 저널 투고 없이 프리프린트+에세이로 다운그레이드 (살라미 금지).

## 에이전트 오케스트레이션 (P1 시퀀스)
`harvester` → `sanitizer` → `coder-runner` (A/B 독립 2회) → `alpha-scorer`
→ 불일치 발생 시 `adjudication-logger` (dk HITL) → G1 보고 → dk 승인.
`prereg-guardian`은 P3부터 모든 세션 시작 시 1회 실행.
에이전트 정의: `.claude/agents/`. 모델 기본 Opus (기계적 대량 작업은 정의 내
명시된 경우에만 다운그레이드 허용).

## P1 체크리스트 (다음 액션)
- [ ] `.env` 작성 (두 패밀리 키), `scripts/alpha.py selftest` 통과 확인
- [ ] `scripts/build_coder_prompt.py` 실행 → 프롬프트 + 매니페스트 생성 확인
- [ ] verify-at-pilot 서지 3건 확정: A05 (Schellenberg RS 2005 파트 구조),
      A07 (Swinburne 1968, Philosophy 43 서지), A15 (Plantinga 1981, Noûs 15 서지)
      → `docs/gold-anchors-v1.json` 갱신 + changelog
- [ ] RS 2015 연간 논문 목록·초록 수집 (harvester) → `data/raw/pilot_rs2015.jsonl`
- [ ] 골드 앵커 20편 초록 수집 → `data/raw/gold_anchors.jsonl`
- [ ] sanitize (스크럽 로그 포함) → `data/sanitized/`
- [ ] 듀얼 코딩 → `data/coded/pilot_a.jsonl`, `pilot_b.jsonl`, `gold_a.jsonl`, `gold_b.jsonl`
- [ ] dk 수기 코딩 (파일럿 연도, 코더 산출물 열람 전에)
- [ ] `alpha.py rel` (코더 간) + `alpha.py gold` (골드 정확도) → G1 리포트
- [ ] S6 아이템 최초 발견 시 A21 승격 로그 (codebook §8)

## 환경
Python 3.10+. `scripts/`는 stdlib-only. fetch/sanitize/code 스텁은 이 시드
생성 환경(네트워크 제한 컨테이너)에서 미실행 — 로컬에서 엔드포인트 검증 필요.
