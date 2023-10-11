from aiogram import Router
from aiogram.filters import StateFilter, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message
from aiogram import F

from filters.filters import ValidatorID
from fsm.fsm import FSMCreateTask
from keyboards.inline_keyboard import keyboard, day_markup
from lexicon.lexicon import LEXICON_RU

router = Router()
# Хэндлеры работают если выполнен вход
router.message.filter(ValidatorID())


# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['welcome'], reply_markup=keyboard)


# Этот хэндлер будет срабатывать на апдейт типа CallbackQuery
@router.callback_query(F.data == 'add_task_pressed')
async def process_add_task_press(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text='Выберите день месяца',
        reply_markup=day_markup())
    await state.set_state(FSMCreateTask.fill_date)


@router.callback_query(StateFilter(FSMCreateTask.fill_date))
async def select_day(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text='Введите задачу')
    await state.update_data(date=callback.data)
    await state.set_state(FSMCreateTask.fill_task)


@router.message(StateFilter(FSMCreateTask.fill_task))
async def select_task(message: Message, state: FSMContext):
    await message.answer(text='Возврат', reply_markup=keyboard )
    await state.update_data(task=message.text)
    await state.clear()


# Этот хэндлер будет срабатывать на апдейт типа CallbackQuery
@router.callback_query(F.data == 'show_tasks_today_pressed')
async def process_show_tasks_today_press(callback: CallbackQuery):
    await callback.message.answer(text='Список задач на сегодня')
