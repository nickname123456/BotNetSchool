from aiogram.dispatcher.filters.state import State, StatesGroup


class StartStates(StatesGroup):
    INLINK = State()
    INCOUNTRIES = State()
    INPROVINCES = State()
    INCITIES = State()
    INSCHOOL = State()
    INCLASS = State()
    INLOGIN = State()
    INPASSWORD = State()