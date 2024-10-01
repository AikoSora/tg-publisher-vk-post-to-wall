from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from keyboards import kb_inline


router = Router(__name__)


@router.message(Command('start'))
async def command_start(message: Message):
    text = [
        f'Привет <b>{message.from_user.username}!</b>',
        'Я бот, который умеет делать отложенные посты из телеграм в ВК!',
        'Для того, чтобы начать, выбери нужное действие.',
    ]

    await message.answer(
        text='\n'.join(text),
        parse_mode='HTML',
        reply_markup=kb_inline.kb_builder(),
    )

    await message.delete()


@router.message(Command('help'))
async def command_help(message: Message):
    text = [
        '<b>/start - запуск бота</b>',
        '<b>/help - помощь по командам</b>'
    ]

    await message.answer(
        text='\n'.join(text),
        parse_mode='HTML',
    )

    await message.delete()
