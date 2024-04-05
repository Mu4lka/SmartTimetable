from aiogram import F, types, Router
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from UI.buttons.data_buttons import worker_buttons, admin_buttons
from UI.buttons.enums import OtherButton
from UI.buttons.enums.main_menu import BaseButton
from UI.methods import show_main_menu, get_buttons, make_keyboard
from data import constants
from data.config import LINK_TO_TIMETABLE
from database.methods import check_key
from filters import IsAuthorized, IsPrivate, IsWorker, IsAdmin

router = Router()


@router.callback_query(StateFilter(None), IsAdmin(), F.data == BaseButton.SHOW_TIMETABLE.value)
async def show_timetable_for_admin(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(LINK_TO_TIMETABLE)
    await show_main_menu(callback_query.message, admin_buttons)


@router.callback_query(StateFilter(None), IsWorker(), F.data == BaseButton.SHOW_TIMETABLE.value)
async def show_timetable(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(LINK_TO_TIMETABLE)
    await show_main_menu(callback_query.message, worker_buttons)


@router.message(IsPrivate(), IsAuthorized(), F.text == OtherButton.MAIN_MENU.value)
async def command_main_menu(message: types.Message, state: FSMContext):
    await show_main_menu(message, user_id=message.from_user.id)
    await state.clear()


@router.message(IsPrivate(), Command("start"))
async def command_start(message: types.Message, state: FSMContext):
    await state.clear()
    buttons = await get_buttons(message)
    if not buttons:
        await message.answer(
            f"Привет {message.from_user.first_name}! {constants.ABOUT_NOT_AUTHORIZED})",
            reply_markup=ReplyKeyboardRemove()
        )
        return

    await message.answer(
        f"Привет {message.from_user.first_name}",
        reply_markup=await make_keyboard([OtherButton.MAIN_MENU.value])
    )
    await show_main_menu(message, buttons)


@router.message(IsPrivate(), Command("help"))
async def command_help(message: types.Message):
    if await IsAdmin().__call__(message):
        message_text = constants.HELP_FOR_ADMIN
    elif await IsWorker().__call__(message):
        message_text = constants.HELP_FOR_WORKER
    else:
        message_text = constants.HELP_FOR_UNAUTHORIZED
    await message.answer(message_text, parse_mode="HTML")


@router.message(IsPrivate(), Command("info_bot"))
async def command_info_bot(message: types.Message):
    await message.answer(f"Creator: {constants.CREATOR_NAME}\nMade with aiogram")


@router.message(IsPrivate(), StateFilter(None))
async def take_key(message: types.Message, state: FSMContext):
    if not message.text:
        return
    if await IsAuthorized().__call__(message):
        return

    if await check_key(message.text, message.from_user.id, message.from_user.username):
        await command_start(message, state)
