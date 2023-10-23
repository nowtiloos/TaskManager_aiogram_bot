from aiogram import Router
from aiogram.filters import StateFilter, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message
from aiogram import F

from filters import Authorized
from fsm import FSMCreateTask
from keyboards.inline_keyboard import keyboard, days_keyboard
from lexicon import lexicon
from services.db_interface import insert

router = Router()
# Хэндлеры работают если выполнен вход
router.message.filter(Authorized())


# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    await message.answer(text=lexicon["welcome"], reply_markup=keyboard)


@router.callback_query(F.data == "/abort")
async def process_abort(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=lexicon["welcome"], reply_markup=keyboard)
    await state.clear()


@router.message(F.text == "/abort")
async def process_abort(message: Message, state: FSMContext):
    await message.answer(text=lexicon["welcome"], reply_markup=keyboard)
    await state.clear()


# Этот хэндлер будет срабатывать на апдейт типа CallbackQuery
@router.callback_query(F.data == "add_task_pressed")
async def process_add_task_press(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text=lexicon["select_date"], reply_markup=days_keyboard()
    )
    await state.update_data(users_tg_id=callback.from_user.id)
    await state.set_state(FSMCreateTask.fill_date)


@router.callback_query(StateFilter(FSMCreateTask.fill_date))
async def select_day(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=lexicon["write_task_text"])
    await state.update_data(due_date=callback.data)
    await state.set_state(FSMCreateTask.fill_task)


@router.message(StateFilter(FSMCreateTask.fill_task))
async def select_task(message: Message, state: FSMContext):
    await message.answer(text=lexicon["task_added"], reply_markup=keyboard)
    await state.update_data(task_text=message.text)
    insert(table="tasks", data_dict=await state.get_data())
    await state.clear()


# Запрос задач на текущий день
@router.callback_query(F.data == "show_tasks_today_pressed")
async def process_show_tasks_today_press(callback: CallbackQuery):
    from services.services import get_table

    await callback.message.answer(text="Список задач на сегодня")
    table = get_table()
    await callback.message.answer(
        text=f"```{table}```", parse_mode="MarkdownV2"
    )  # форматируем markdown
