from aiogram import types, Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from UI.get_buttons import get_buttons
from UI.show_main_menu import show_main_menu
from data import constants
from data.config import LINK_TO_TIMETABLE
from database.check_key import check_key
from enums.menu import Button, BaseButton
from filters.is_authorized import IsAuthorized
from filters.is_private import IsPrivate
from UI.make_keyboard import make_keyboard


router = Router()


@router.callback_query(StateFilter(None), IsAuthorized(), F.data == BaseButton.SHOW_TIMETABLE.value)
async def show_timetable(callback_query: types.CallbackQuery):
    await callback_query.message.answer(LINK_TO_TIMETABLE)
    await show_main_menu(callback_query.message, user_id=callback_query.from_user.id)


@router.message(IsPrivate(), F.text == Button.CANCEL.value)
async def command_cancel(message: types.Message, state: FSMContext):
    await message.answer(constants.CANCEL)
    await show_main_menu(message)
    await state.clear()


@router.message(IsPrivate(), Command("start"))
async def command_start(message: types.Message):
    buttons = await get_buttons(message)
    if not buttons:
        await message.answer(f"Привет {message.from_user.first_name}! {constants.ABOUT_NOT_AUTHORIZED})",
                             reply_markup=ReplyKeyboardRemove())
        return

    await message.answer(f"Привет {message.from_user.first_name}",
                         reply_markup=await make_keyboard([Button.CANCEL.value]))
    await show_main_menu(message, buttons)


@router.message(IsPrivate(), Command("help"))
async def command_help(message: types.Message):
    await message.answer(f"Нужна помощь?")


@router.message(IsPrivate(), Command("info_bot"))
async def command_info_bot(message: types.Message):
    await message.answer(f"Creator: @Mu4lka")


@router.message(StateFilter(None), IsPrivate())
async def take_key(message: types.Message):
    if not message.text:
        return
    if await IsAuthorized().__call__(message):
        return

    if await check_key(message.text, message.from_user.id, message.from_user.username):
        await command_start(message)
