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

class ConnectCodeStates(StatesGroup):
    INCODE = State()

class HomeworkStates(StatesGroup):
    INLESSON = State()
    INHOMEWORK = State()

class UpdScheduleStates(StatesGroup):
    INPHOTO = State()
    INCLASS = State()
    END = State()

class CorrectionMark(StatesGroup):
    INLESSON = State()
    INMARK = State()