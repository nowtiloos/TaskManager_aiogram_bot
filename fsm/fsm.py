from aiogram.fsm.state import StatesGroup, State


# Cоздаем класс, наследуемый от StatesGroup, для группы состояний нашей fsm
class FSMRegistration(StatesGroup):
    # Создаем экземпляры класса State, последовательно
    # перечисляя возможные состояния, в которых будет находиться
    # бот в разные моменты взаимодейтсвия с пользователем
    fill_name = State()  # Состояние ожидания ввода имени
    fill_role = State()  # Состояние ожидания ввода должности


class FSMEntry(StatesGroup):
    fill_code = State()
    successful_entry = State()


class FSMCreateTask(StatesGroup):
    fill_date = State()
    fill_task = State()
