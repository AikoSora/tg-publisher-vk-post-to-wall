from datetime import datetime

from aiogram import Bot, Router, F
from aiogram.types import (
    CallbackQuery,
    Message,
    InlineKeyboardMarkup,
)

from keyboards import kb_inline

from db.db_interval import get_time_interval, set_time_interval

from vk_back.post.send import send_post, delay_post

from re import compile


router = Router()

user_states = {}

html_tags_regex = compile(r'<.*?>(.*?)<\/.*?>')
a_html_tag_regex = compile(r'<a .*?>.*?</a>')
a_href_attr_regex = compile(r'<a.*?href=\"(.*?)\">.*?<.*?>')
vk_link_regex = compile(r'(http(s?)://)?vk\.com.*?')


def convert_text_style(text: str) -> str:
    """
    Function to convert telegram style text to VK style

    :param text str: Message text
    :return str: Converted message text
    """

    new_text = text

    for match in html_tags_regex.finditer(text):
        if a_html_tag_regex.match(match.group(0)):
            href = a_href_attr_regex.match(match.group(0))

            if vk_link_regex.match(href.groups()[0]):
                new_text = new_text.replace(
                    match.group(0), f'[{href.groups()[0]}|{match.groups()[0]}]'
                )
            else:
                new_text = new_text.replace(
                    match.group(0), match.groups()[0],
                )
        else:
            new_text = new_text.replace(
                match.group(0), match.groups()[0],
            )

    return new_text


async def back_menu(callback: CallbackQuery):
    """
    Function to return menu in bot

    :param callback: CallbackQuery object
    """

    user_id = callback.from_user.id
    user_states[user_id] = '-1'

    await callback.message.edit_text(
        text=f'Привет <b>{callback.from_user.username}!</b> Выбери действие',
        reply_markup=kb_inline.kb_builder(),
        parse_mode='html',
    )


@router.callback_query(F.data == 'send_now')
async def process_button(callback: CallbackQuery):

    user_id = callback.from_user.id
    user_states[user_id] = 'send_now'

    await callback.message.answer(
        text='Пришли пост, который нужно опубликовать сейчас',
    )


@router.message(F.text)
async def check_post(message: Message):

    user_id = message.from_user.id

    text = message.html_text

    if text is None:
        return await message.reply(
            text='Отправьте мне текст поста!',
        )

    if user_id not in user_states:
        return await message.reply(
            text='Ты прислал текст, а не выбрал действие!',
            reply_markup=kb_inline.kb_builder()
        )

    if user_states[user_id] == 'send_now':
        post_id = await send_post(text=convert_text_style(text))

        await message.delete()
        await message.answer(
            text=f"Пост <b>{post_id}</b> опубликован <b>{datetime.now().replace(microsecond=0)}</b>",
            reply_markup=kb_inline.kb_builder(),
            parse_mode='HTML',
        )

    elif user_states[user_id] == 'add_to_deferred':
        post_id = await delay_post(user_id=user_id, text=convert_text_style(text))

        await message.answer(
            text=f"Пост <b>{post_id['post']}</b> добавлен в отложку <b>{datetime.fromtimestamp(post_id['date'])}</b> ",
            reply_markup=kb_inline.kb_builder(),
            parse_mode='HTML',
        )
        await message.delete()

    elif user_states[user_id] == 'time_post':
        await message.reply('Выбери интервал!')

    del user_states[user_id]


@router.message(F.photo)
async def command_start(message: Message, bot: Bot):

    user_id = message.from_user.id

    text = message.text or message.caption or ''

    if user_id not in user_states:
        return await message.reply(
            text='Ты не выбрал действие!',
            reply_markup=kb_inline.kb_builder()
        )

    if user_states[user_id] == 'send_now':
        file = await bot.get_file(message.photo[-1].file_id)
        photo = await bot.download_file(file.file_path)
        post_id = await send_post(photo=photo, text=convert_text_style(text))

        await message.delete()
        await message.answer(
            text=f"Пост <b>{post_id}</b> опубликован <b>{datetime.now().replace(microsecond=0)}</b>",
            reply_markup=kb_inline.kb_builder(),
            parse_mode='HTML',
        )

    elif user_states[user_id] == 'add_to_deferred':
        file = await bot.get_file(message.photo[-1].file_id)
        photo = await bot.download_file(file.file_path)
        post_id = await delay_post(photo=photo, user_id=user_id, text=convert_text_style(text))

        await message.answer(
            text=f"Пост <b>{post_id['post']}</b> добавлен в отложку <b>{datetime.fromtimestamp(post_id['date'])}</b> ",
            reply_markup=kb_inline.kb_builder(),
            parse_mode='HTML',
        )
        await message.delete()

    del user_states[user_id]


@router.callback_query(F.data == 'time_post')
async def choice_time(callback: CallbackQuery):

    user_id = callback.from_user.id
    time_interval = get_time_interval(user_id)

    menu = kb_inline.kb_time()

    for row in menu.inline_keyboard:
        for button in row:
            if button.callback_data == "-1":
                continue
            if time_interval == button.callback_data:
                button.text = f"[✅] {button.text[4:]}"
            else:
                button.text = f"[❌] {button.text[4:]}"

    updated_menu = InlineKeyboardMarkup(
        inline_keyboard=menu.inline_keyboard
    )

    if time_interval:
        return await callback.message.edit_text(
            text='Интервал уже выбран!',
            reply_markup=updated_menu,
        )

    await callback.message.edit_text(
        text='Сейчас интервал не задан! Выбери интервал публикации постов',
        reply_markup=menu,
    )


@router.callback_query(F.data.in_(['1', '2', '3', '4', '-1']))
async def set_interval(callback: CallbackQuery):

    user_id = callback.from_user.id
    time_interval = callback.data

    if time_interval != '-1':
        set_time_interval(user_id, time_interval)
        return await choice_time(callback)

    await back_menu(callback)


@router.callback_query(F.data == 'add_to_deferred')
async def add_time_in_post(callback: CallbackQuery):

    user_id = callback.from_user.id
    user_states[user_id] = 'add_to_deferred'

    await callback.message.answer(
        text='Пришли пост, который нужно добавить в отложку',
    )
