Jev(TypeSafe System One, jev-1.13.0) 실험 기록 - 2026-09-24 ~ 2026-09-25

개념 노트 「Jev와 System One 모델」와 DevLog 2026-09-24의 수치를 다시 계산하기 위한 원자료다.
외부로 보낸 것은 공개 노트와 발행 글뿐이다. 초안 summary(exp5_drafts.json)는 로컬에서 정규식으로만 채점했다.
예외로, exp6(성숙도)에는 당시 커밋되지 않은 Slipbox 초안 한 편이 포함돼 전송됐다.

판정 방법
- 태그 실험(exp0)의 정답은 사람이 붙여 둔 기존 태그다. 그래서 수치는 정확도가 아니라 일치율이다.
- 나머지 실험은 Jev를 돌리기 전에 표본을 읽고 라벨을 붙여 *_labels.json으로 고정했다. 라벨은 한 사람(Claude)이 붙였다.
- exp5의 검증용 표본(exp5_holdout.json)은 정규식을 만들 때 쓰지 않은 문장이며, 라벨을 먼저 붙인 뒤 정규식과 Jev를 한 번씩만 채점했다.
- 각 판단은 한 번씩만 실행했다. note_examples_rerun.py로 노트의 예시만 두 번 다시 돌려 같은 결과를 확인했다.

실험과 파일
- exp0 태그 분류: jev_tag_eval.py -> jev_results.json (공개 노트 74개, 주제 8개·첫 태그 13개 Choice)
- exp1 양분법("X가 아니라 Y"): exp_prepare.py, exp_run.py -> exp1_occurrences.json, exp1_sample_ids.json, exp1_labels.json, exp1_results.json
- exp2 summary 꼬리: 같은 스크립트 -> exp2_summaries.json, exp2_labels.json, exp2_results.json
- exp3 링크 후보 관계: 같은 스크립트 -> exp3_links.json, exp3_results.json
- exp4 예고·되짚기·용어 정의: exp4_prepare.py, exp4_run.py -> exp4_sample.json, exp4_labels.json, exp4_results.json
- exp5 과적합 검증: exp5_prepare.py, exp5_run.py, exp5_score_regex.mjs, exp5_regex_all.mjs -> exp5_holdout.json, exp5_labels.json, exp5_holdout_jev.json, exp5_unseen.json, exp5_unseen_jev.json, exp5_unseen_regex.json, exp5_drafts.json
- 정규식 설계 점검: pv_test.mjs, pv2_test.mjs (이미 본 데이터로 돌린 점검이라 검증 결과가 아니다)
- exp6 성숙도 Score: exp6_maturity.py -> exp6_results.json (영구 노트 33개)
- exp7 AI 첫 태그: exp7_ai_tag.py -> exp7_results.json (커밋된 공개 노트 19개)
- 노트 예시 확인: snippet.py, note_examples_rerun.py

다시 실행하기
- 키는 macOS 키체인에 있다: export TYPESAFE_API_KEY="$(security find-generic-password -a "$USER" -s TYPESAFE_API_KEY -w)"
- uv run --with typesafe-sdk python <스크립트>.py
- 스크립트는 같은 폴더의 JSON을 읽고 쓴다. 노트가 그 뒤에 바뀌었으면 입력도 달라진다.

lint-decisions.csv
- 새 글에서 blog-slop-lint의 preview-sentence, vault-lint의 summary 꼬리 후보를 채택했는지 기각했는지 적는다.
- 두 정규식은 검증용 문장을 본 뒤 다시 썼으므로, 공정한 채점은 이 기록으로만 할 수 있다.
