Jev 1단계 실험 기록 - 2026-09-25 (조정용까지 진행하고 중단)

질문: 문단 하나에 작성자가 실제로 해 본 일과 그 뒤 관찰한 결과가 함께 적혀 있는가? (question.json v1)
결과 요약과 중단 이유는 DevLog 2026-09-25에 있다.

표본
- 게시판 origin/main(a507ca5)의 공개 노트 12개에서 산문 문단 48개. 조정용·최종 평가용 24개씩, 노트 단위로 나눔
- 이전 실험(exp1·exp4·exp5)에서 라벨을 붙이며 읽은 문장이 든 문단 53개 제외
- 최종 평가용 보강 16개는 뽑기만 하고 라벨·모델 호출 없음

정답
- labels_before_aug.json: 사용자 라벨. 조정용은 한 번 다시 붙인 판, 최종 평가용은 처음 판
- labels.json: 같은 시점의 내려받기 파일
- 조정용을 다시 붙일 때 Claude의 설명을 참고했다. 비교 모델도 Claude 계열이라 두 결과가 겹칠 수 있다

모델 결과 (조정용만)
- runs/tune_v1_jev.json: jev-1.13.0 Noul, 24건, 1.26초, $0.000422
- runs/tune_v1_sonnet.json: claude-sonnet-5 하위 에이전트, 한 번에 24문단
- frozen.json: 최종 평가 전에 고정한 문턱(0.4)과 통과 기준. 최종 평가는 실행하지 않음

다시 실행하기
- python3 prepare.py (같은 커밋·seed면 같은 표본, 보강 전 48개), python3 augment.py (보강 16개)
- export TYPESAFE_API_KEY="$(security find-generic-password -a "$USER" -s TYPESAFE_API_KEY -w)"
- uv run --with typesafe-sdk python run_tune.py
- review.html: 로컬 검토 화면, 네트워크 호출 없음
