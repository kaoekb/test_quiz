from __future__ import annotations

import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.config import settings
from app.quiz_data import QUIZ, resolve_result


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("tg-quiz-bot")


class QuizState(StatesGroup):
    in_quiz = State()


def kb_start_quiz():
    b = InlineKeyboardBuilder()
    b.button(text="🚀 Начать тест", callback_data="quiz:start")
    return b.as_markup()


def kb_question(q_index: int):
    q = QUIZ[q_index]
    b = InlineKeyboardBuilder()
    for opt_index, opt in enumerate(q.options):
        # callback: quiz:ans:<q_index>:<opt_index>
        b.button(text=opt.text, callback_data=f"quiz:ans:{q_index}:{opt_index}")
    b.adjust(1)
    return b.as_markup()


async def send_question(bot: Bot, chat_id: int, q_index: int):
    q = QUIZ[q_index]
    await bot.send_message(chat_id, q.text, reply_markup=kb_question(q_index))



async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Привет! Это бот-тестирование.\n"
        "Нажми «Начать тест», выбери ответы — и в конце получишь результат.",
        reply_markup=kb_start_quiz(),
    )


async def cmd_restart(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Окей, перезапускаю тест.", reply_markup=kb_start_quiz())


async def cb_quiz_start(call: CallbackQuery, state: FSMContext, bot: Bot):
    await call.answer()
    await state.set_state(QuizState.in_quiz)
    await state.update_data(q_index=0, score=0)

    # можно удалить “стартовое” сообщение, чтобы не захламлять
    try:
        await call.message.delete()
    except Exception:
        pass

    await send_question(bot, call.from_user.id, 0)


async def cb_quiz_answer(call: CallbackQuery, state: FSMContext, bot: Bot):
    await call.answer()

    data = await state.get_data()
    if not data:
        # если пользователь нажал кнопку после рестарта/таймаута
        await state.clear()
        await bot.send_message(call.from_user.id, "Сессия теста не найдена. Нажмите /start.")
        return

    try:
        _, _, q_index_s, opt_index_s = call.data.split(":")
        q_index = int(q_index_s)
        opt_index = int(opt_index_s)
    except Exception:
        await bot.send_message(call.from_user.id, "Некорректный ответ. Нажмите /start.")
        await state.clear()
        return

    current_q = data.get("q_index", 0)
    if q_index != current_q:
        # защита от “нажатий назад”/двойных кликов
        return

    # начисляем баллы
    option = QUIZ[q_index].options[opt_index]
    score = int(data.get("score", 0)) + option.score

    next_q = q_index + 1

    # можно аккуратно редактировать сообщение, чтобы “зафиксировать выбор”
    # (не обязательно; если хотите — можно заменить клавиатуру на None)
    try:
        await call.message.edit_reply_markup(reply_markup=None)
    except Exception:
        pass

    if next_q >= len(QUIZ):
        # конец теста
        result = resolve_result(score)
        await state.clear()

        await bot.send_message(
            call.from_user.id,
            "✅ Тест завершён!\n\n"
            f"**Результат:** {result['title']}\n"
            f"{result['desc']}\n\n"
            f"**Ваш счёт:** {score}/{len(QUIZ) * 2}\n\n"
            "Хочешь пройти ещё раз? /restart",
            parse_mode="Markdown",
        )
        return

    await state.update_data(q_index=next_q, score=score)
    await send_question(bot, call.from_user.id, next_q)


def build_dispatcher() -> Dispatcher:
    dp = Dispatcher(storage=MemoryStorage())
    dp.message.register(cmd_start, CommandStart())
    dp.message.register(cmd_restart, Command("restart"))

    dp.callback_query.register(cb_quiz_start, F.data == "quiz:start")
    dp.callback_query.register(cb_quiz_answer, F.data.startswith("quiz:ans:"))
    return dp


def main():
    bot = Bot(token=settings.bot_token)
    dp = build_dispatcher()
    logger.info("Bot started")
    dp.run_polling(bot)


if __name__ == "__main__":
    main()
