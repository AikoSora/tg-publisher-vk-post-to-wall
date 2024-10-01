from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


def kb_builder():
    """
    Function to generate inline keyboard

    :return: IKM object
    """

    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="📝 Опубликовать сейчас",
                callback_data='send_now',
            ),
            InlineKeyboardButton(
                text="🕓 Добавить в отложку",
                callback_data='add_to_deferred',
            ),
        ],
        [
            InlineKeyboardButton(
                text="⏰ Таймер выхода постов",
                callback_data='time_post',
            ),
        ],
    ])


def kb_time():
    """
    Function to generate inline keyboard

    :return: IKM object
    """

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="[❌] Каждый час",
                    callback_data='1'
                ),
                InlineKeyboardButton(
                    text="[❌] Каждые 2 часа",
                    callback_data='2'
                ),
            ],
            [
                InlineKeyboardButton(
                    text="[❌] Каждые 3 часа",
                    callback_data='3',
                ),
                InlineKeyboardButton(
                    text="[❌] Каждые 4 часа",
                    callback_data='4',
                ),
            ],
            [
                InlineKeyboardButton(
                    text="[↩️] Главное меню",
                    callback_data='-1',
                ),
            ],
        ],
    )


__all__ = (
    'kb_builder',
    'kb_time',
)
