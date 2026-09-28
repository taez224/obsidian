from typesafe_sdk import Choice, Noul, TypeSafeClient

client = TypeSafeClient()  # TYPESAFE_API_KEY 환경 변수를 읽는다
result = client.system_one(
    {"sentence": "다음 편에서는 외향성을 다룹니다."},
    {
        "preview": Noul(instructions="Does `sentence` only announce what the next part will cover?"),
        "tone": Choice(
            instructions="What is the tone of `sentence`?",
            criteria={
                "neutral": "Plain statement of fact or plan",
                "promotional": "Hypes or oversells",
                "none_of_the_above": "Neither fits",
            },
        ),
    },
)
print(result.nouls["preview"].noul)
print(result.choices["tone"].choice, result.choices["tone"].confidence, dict(result.choices["tone"].probabilities))
