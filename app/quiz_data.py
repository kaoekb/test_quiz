from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict


@dataclass(frozen=True)
class AnswerOption:
    text: str
    score: int  # сколько баллов даёт ответ


@dataclass(frozen=True)
class Question:
    text: str
    options: List[AnswerOption]


QUIZ: List[Question] = [
    Question(
        text="1) Как вы предпочитаете решать проблему?",
        options=[
            AnswerOption("Через логи и метрики", 2),
            AnswerOption("Сразу перезапустить всё (классика)", 0),
            AnswerOption("Постепенно, гипотезами и тестами", 1),
        ],
    ),
    Question(
        text="2) Ваше отношение к документации?",
        options=[
            AnswerOption("Пишу и обновляю регулярно", 2),
            AnswerOption("Читаю, но не пишу", 1),
            AnswerOption("Документация — это миф", 0),
        ],
    ),
    Question(
        text="3) Как вы относитесь к автоматизации?",
        options=[
            AnswerOption("Если руками — значит ещё не автоматизировано", 2),
            AnswerOption("Иногда можно и руками", 1),
            AnswerOption("Автоматизация ломает магию", 0),
        ],
    ),
]

# Результаты по диапазонам баллов
RESULTS: List[Dict[str, object]] = [
    {
        "min": 0,
        "max": 2,
        "title": "Экспериментатор",
        "desc": "Вы действуете смело и быстро. Добавьте чуть больше системности — и будет идеально.",
    },
    {
        "min": 3,
        "max": 4,
        "title": "Практик",
        "desc": "Здоровый баланс. Вы умеете и думать, и делать — отличный режим для продакшена.",
    },
    {
        "min": 5,
        "max": 6,
        "title": "Инженер порядка",
        "desc": "Логи, метрики, автоматизация — вы звучите как человек, у которого всё работает (и не только случайно).",
    },
]


def resolve_result(total_score: int) -> Dict[str, object]:
    for r in RESULTS:
        if r["min"] <= total_score <= r["max"]:
            return r
    # на случай, если расширите квиз и забудете обновить диапазоны
    return {"title": "Неопределённо", "desc": f"Счёт: {total_score}. Обновите диапазоны результатов."}
