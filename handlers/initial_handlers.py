from aiogram import Router, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message

from keyboards.inline_keyboard import buttons, name_button, create_inline_kb
from lexicon.lexicon import LEXICON_RU
from keyboards.standart_keyboard import start_kb, register_kb
from fsm.fsm import FSMRegistration, FSMEntry
from services.services import get_access, to_database, multi_delete
from filters.filters import ValidatorCode, ValidatorName

# Инициализируем роутер уровня модуля
router = Router()
# Хэндлеры работают до тех пор, пока не выполнен вход
router.message.filter(~StateFilter(FSMEntry.successful_entry))


# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    await multi_delete(message)
    await message.answer(text=LEXICON_RU['/start'], reply_markup=start_kb)


# Этот хэндлер будет срабатывать на команду "/cancel" в состоянии
# по умолчанию и сообщать, что эта команда работает внутри машины состояний
@router.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(text='Отменять нечего.')


# Этот хэндлер будет срабатывать на команду "/cancel" в любых состояниях,
# кроме состояния по умолчанию, и отключать машину состояний
@router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await multi_delete(message)
    await message.answer(text='Команда отменена', reply_markup=start_kb)
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()


# Этот хэндлер срабатывает на кнопку "Регистрация"
@router.message(F.text == LEXICON_RU['register'], StateFilter(default_state))
async def process_register(message: Message, state: FSMContext):
    await multi_delete(message, 2)
    await message.answer(text=LEXICON_RU['input_reg'])
    # Устанавливаем состояние ожидания выбора фамилии
    await state.set_state(FSMRegistration.fill_name)


# Этот хэндлер срабатывает на ввод фамилии и инициалов
@router.message(StateFilter(FSMRegistration.fill_name), ValidatorName())
async def process_input_name(message: Message, state: FSMContext):
    await multi_delete(message, 2)
    await message.answer(text=LEXICON_RU['input_name'], reply_markup=register_kb)
    # Сохраняем введенное имя в хранилище по ключу "name"
    await state.update_data(name=message.text)
    await state.update_data(tg_id=message.from_user.id)
    # Устанавливаем состояние ожидания выбора роли
    await state.set_state(FSMRegistration.fill_role)


# Хэндлер на неверное имя
@router.message(StateFilter(FSMRegistration.fill_name))
async def invalid_name(message: Message):
    await message.answer(
        text='То, что вы отправили не похоже на имя\n\n'
             'Пожалуйста, введите ваше имя\n\n'
             'Если вы хотите прервать заполнение анкеты - '
             'отправьте команду /cancel')


# Этот хэндлер срабатывает на кнопку "Мастер-приемщик"
@router.message(StateFilter(FSMRegistration.fill_role), F.text == LEXICON_RU['manager'])
async def process_manager(message: Message, state: FSMContext):
    await multi_delete(message, 2)
    code = get_access('manager')
    # Передает данные в БД
    await to_database(message, state, code)


# Этот хэндлер срабатывает на кнопку "Мастер рем-зоны"
@router.message(StateFilter(FSMRegistration.fill_role), F.text == LEXICON_RU['master'])
async def process_master(message: Message, state: FSMContext):
    await multi_delete(message, 2)
    code = get_access('master')
    # Передает данные в БД
    await to_database(message, state, code)


# Этот хэндлер срабатывает на кнопку "Сотрудник"
@router.message(StateFilter(FSMRegistration.fill_role), F.text == LEXICON_RU['staff'])
async def process_staff(message: Message, state: FSMContext):
    await multi_delete(message, 2)
    code = get_access('staff')
    # Передает данные в БД
    await to_database(message, state, code)


# ------------Ветка входа----------------
# Этот хэндлер срабатывает на кнопку "Вход"
@router.message(F.text == LEXICON_RU['sign_in'], StateFilter(default_state))
async def choice_sign_in(message: Message, state: FSMContext):
    await multi_delete(message, 3)
    await message.answer(text=LEXICON_RU['input_uid'])
    await state.set_state(FSMEntry.fill_code)


# Успешный вход
@router.message(StateFilter(FSMEntry.fill_code), ValidatorCode())
async def enter_code(message: Message, state: FSMContext):
    await multi_delete(message, 2)
    keyboard = create_inline_kb(2, 'button', 'cott', 'sdf', last_btn='quit')
    await message.answer(text=LEXICON_RU['welcome'], reply_markup=keyboard)
    await state.set_state(FSMEntry.successful_entry)


# Неверный код доступа
@router.message(StateFilter(FSMEntry.fill_code))
async def enter_bad_code(message: Message):
    await message.answer(text=LEXICON_RU['invalid_code'])
