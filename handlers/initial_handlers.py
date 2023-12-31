import uuid

from aiogram import Router, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery

from keyboards.inline_keyboard import keyboard, create_inline_kb
from lexicon import lexicon
from fsm import FSMRegistration, FSMEntry
from services.db_interface import update_auth, insert
from services.services import multi_delete
from filters import ValidatorCode, ValidatorName

# Инициализируем роутер уровня модуля
router = Router()


# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    await multi_delete(message)
    markup = create_inline_kb("register", "sign_in")
    await message.answer(text=lexicon["/start"], reply_markup=markup)


# Этот хэндлер будет срабатывать на команду "/cancel" в состоянии
# по умолчанию и сообщать, что эта команда работает внутри машины состояний
@router.message(Command(commands="cancel"), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(text="Нет запущенных процессов")


# Этот хэндлер будет срабатывать на команду "/cancel" в любых состояниях,
# кроме состояния по умолчанию, и отключать машину состояний
@router.message(Command(commands="cancel"), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await multi_delete(message, 2)
    await message.answer(text="Команда отменена")
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()


# Этот хэндлер срабатывает на кнопку "Регистрация"
@router.callback_query(F.data == "register", StateFilter(default_state))
async def process_register(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=lexicon["input_reg"])
    # Устанавливаем состояние ожидания выбора фамилии
    await state.set_state(FSMRegistration.fill_name)


# Этот хэндлер срабатывает на ввод фамилии и инициалов
@router.message(StateFilter(FSMRegistration.fill_name), ValidatorName())
async def process_input_name(message: Message, state: FSMContext):
    await multi_delete(message, 2)
    markup = create_inline_kb("manager", "master", "staff", "/cancel")
    await message.answer(text=lexicon["input_name"], reply_markup=markup)
    # Сохраняем введенное имя в хранилище по ключу "name"
    await state.update_data(name=message.text)
    await state.update_data(tg_id=message.from_user.id)
    # Устанавливаем состояние ожидания выбора роли
    await state.set_state(FSMRegistration.fill_role)


# Хэндлер на неверное имя
@router.message(StateFilter(FSMRegistration.fill_name))
async def invalid_name(message: Message):
    await message.answer(
        text="То, что вы отправили не похоже на имя\n\n"
        "Пожалуйста, введите ваше имя\n\n"
        "Если вы хотите прервать заполнение анкеты - "
        "отправьте команду /cancel"
    )


# собирает оставшиеся данные и отправляет в БД
@router.callback_query(StateFilter(FSMRegistration.fill_role))
async def process_get_role(callback: CallbackQuery, state: FSMContext):
    code = uuid.uuid4().hex  # генерируем код доступа
    await callback.message.edit_text(
        text=f'{lexicon["your_code_is"]}\n`{code}`', parse_mode="MarkdownV2"
    )
    await state.update_data(role=lexicon[callback.data])
    await state.update_data(code=code)
    insert(table="users", data_dict=await state.get_data())
    await state.clear()
    markup = create_inline_kb("register", "sign_in")
    await callback.message.answer(text=lexicon["final_reg"], reply_markup=markup)


# ------------Ветка входа----------------
# Этот хэндлер срабатывает на кнопку "Вход"
@router.callback_query(F.data == "sign_in", StateFilter(default_state))
async def choice_sign_in(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete_reply_markup()
    await multi_delete(callback.message, 2)
    await callback.message.answer(text=lexicon["input_uid"])
    await state.set_state(FSMEntry.fill_code)


# Успешный вход
@router.message(StateFilter(FSMEntry.fill_code), ValidatorCode())
async def enter_code(message: Message, state: FSMContext):
    await multi_delete(message, 10)
    await update_auth(tg_id=message.from_user.id, value=1)
    await message.answer(text=lexicon["welcome"], reply_markup=keyboard)
    await state.set_state(FSMEntry.successful_entry)


# Неверный код доступа
@router.message(StateFilter(FSMEntry.fill_code))
async def enter_bad_code(message: Message):
    await message.answer(text=lexicon["invalid_code"])
