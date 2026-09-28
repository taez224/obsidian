import re
from typesafe_sdk import Choice, Noul, TypeSafeClient
t = open("/Users/taez/Projects/obsidian/20_Projects/blog/SLII 01 - 상황에 따른 맞춤형 리더십.md", encoding="utf-8").read()
body = re.sub(r"^---\n.*?\n---\n?", "", t, flags=re.S)  # 노트대로: 본문 원문을 그대로 자른다
TOPICS = {
    "AI": "Artificial intelligence: LLMs, AI agents, prompting, and how people and teams work with AI tools.",
    "개발": "Software development: languages, frameworks, infrastructure, design, code quality, engineering methods.",
    "커리어": "Career and self-development: growth, skills and learning, self-management, motivation, job changes, seniority.",
    "조직": "Organizations: delegation, hiring, team performance, leadership; principles that still hold without AI.",
    "심리": "Psychology and self-understanding, including personality tests such as HEXACO or MBTI.",
    "철학": "Philosophy and judgment: by what standard one weighs and chooses, values, ways of thinking.",
    "글쓰기": "Writing and communication: how to write, edit, and convey ideas.",
    "지식관리": "Personal knowledge management: Obsidian, PARA, Zettelkasten, note-taking systems.",
    "none_of_the_above": "The note fits none of the topics above.",
}
client = TypeSafeClient()
for run in (1, 2):
    result = client.system_one(
        {"title": "SLII®: 상황에 따른 맞춤형 리더십",
         "summary": "팀원의 역량과 몰입을 기준으로 개발 수준을 진단하고, 이에 맞는 리더십 행동을 선택하는 SLII 모델의 구조를 정리한다.",
         "body_excerpt": body[:2000]},
        {"topic": Choice(
            instructions="Which topic is this note's main claim about? "
                         "Judge by what the note argues, not by words it merely mentions.",
            criteria=TOPICS)},
    )
    a = result.choices["topic"]
    print(f"Choice run{run}:", a.choice, a.confidence, sorted(dict(a.probabilities).items(), key=lambda x: -x[1])[:3])
META = Noul(instructions=(
    "The Korean sentence `summary` is the one-line summary of a note or blog post. "
    "Does its main predicate describe what the note does (for example: introduces, explains, organizes, covers, "
    "looks at, proposes, reflects on, or is a record or post about X) instead of directly stating the question, "
    "the answer, the distinction, or the claim itself?"))
for s in ["@Constraint와 ConstraintValidator로 역할 티어 기반 사용자 조회·수정 권한을 DTO 검증으로 분리한 구현 기록.",
          "정직-겸손성이 신뢰와 공정성에 미치는 영향, 그리고 강점이 약점으로 바뀌는 조건을 살펴본다.",
          "환경변수로 주입한 Secret은 컨테이너 생성 시점에만 읽히므로, 값이 바뀌면 pod template을 바꿔 Pod를 새로 띄워야 한다."]:
    vals = [client.system_one({"summary": s}, {"meta": META}).nouls["meta"].noul for _ in range(2)]
    print("Noul:", vals, s[:30])
