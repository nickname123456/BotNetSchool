from database.methods.get import get_student_by_telegram_id

from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram import Dispatcher

from ns import correction_mark, get_marks

from tg_bot.keyboards.inline import get_correction_lessons, kb_choice_mark
from tg_bot.states import CorrectionMark

import logging


async def chat_choice_lesson(callback: CallbackQuery):
    await callback.answer('❌Доступно только в л/с!')

async def private_choice_lesson(callback: CallbackQuery, state: FSMContext):
    logging.info(f'{callback.message.chat.id}: get private_choice_lesson command')
    message = callback.message
    user_id = message.chat.id
    student = get_student_by_telegram_id(user_id)

    await CorrectionMark.INLESSON.set()

    keyboard = get_correction_lessons((await get_marks( # Получаем уроки
        student.login,
        student.password,
        student.school,
        student.link,
        student.studentId,
        onlySubjects= True
    )))
    if 'EDIT' in callback.data:
        await message.edit_text('🤔Какой предмет хотите исправить?')
        await message.edit_reply_markup(reply_markup=keyboard)
    else:
        await message.answer('🤔Какой предмет хотите исправить?', reply_markup=keyboard)
    logging.info(f'{user_id}: I sent correction_mark_choice_lesson')

async def private_choice_mark(callback: CallbackQuery, state: FSMContext):
    logging.info(f'{callback.message.chat.id}: get private_choice_lesson command')
    message = callback.message
    user_id = message.chat.id

    lesson = int(callback.data.split('_')[3])
    await state.update_data(lesson=lesson)
    await CorrectionMark.INMARK.set()

    keyboard = kb_choice_mark

    await message.edit_text('👆🏻Какую оценку хотите?')
    await message.edit_reply_markup(reply_markup=keyboard)
    logging.info(f'{user_id}: I sent correction_mark_choice_mark')

async def private_finish(callback: CallbackQuery, state: FSMContext):
    logging.info(f'{callback.message.chat.id}: get private_choice_lesson command')
    message = callback.message
    user_id = message.chat.id
    student = get_student_by_telegram_id(user_id)

    numLesson = (await state.get_data())['lesson']
    mark = int(callback.data.split('_')[2])
    lesson = (await get_marks( # Получаем уроки
        student.login,
        student.password,
        student.school,
        student.link,
        student.studentId,
        onlySubjects=True
    ))[numLesson]

    await message.edit_text('🤔Высчитываю...')
    await message.edit_text(await correction_mark(
        student.login,
        student.password,
        student.school,
        student.link,
        student.studentId,
        lesson,
        mark
    ))
    await state.finish()

    logging.info(f'{user_id}: I sent correction_mark')


def register_handlers_correction_mark(dp: Dispatcher):
    dp.register_callback_query_handler(chat_choice_lesson, lambda callback: callback.data == 'correction_mark_choice_lesson', state='*', chat_type=['group', 'supergroup'])
    dp.register_callback_query_handler(private_choice_lesson, lambda callback: callback.data == 'correction_mark_choice_lesson', state='*', chat_type='private')
    dp.register_callback_query_handler(private_choice_lesson, lambda callback: callback.data == 'correction_mark_choice_lesson_EDIT', state='*', chat_type='private')
    dp.register_callback_query_handler(private_choice_mark, lambda callback: callback.data.startswith('correction_choice_mark_'), state=CorrectionMark.INLESSON)
    dp.register_callback_query_handler(private_finish, lambda callback: callback.data.startswith('choice_mark_'), state=CorrectionMark.INMARK)