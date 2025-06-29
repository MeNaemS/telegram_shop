from aiogram.fsm.state import State, StatesGroup


class CartState(StatesGroup):
    waiting_quantity = State()


class OrderState(StatesGroup):
    waiting_name = State()
    waiting_address = State()
    waiting_phone = State()
    waiting_payment = State()