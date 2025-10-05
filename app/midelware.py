from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


class AddTask(StatesGroup):
    title = State()
    des = State()
    

class AddTime(StatesGroup):
    time = State()
    