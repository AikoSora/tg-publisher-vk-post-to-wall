from vk_back.timers.converter import convert_time

from os import getenv

import vk_api


async def send_post(photo: str, text: str = '') -> str:
    """
    Function to send post in vk

    :param photo str: Post attachment
    :param text str: Post message

    :return str:
    """

    group = getenv('VK_GROUP', None)

    vk_session = vk_api.VkApi(token=getenv('VK_TOKEN', None))

    upload = vk_api.VkUpload(
        vk_session.get_api()
    )

    photos = upload.photo_wall(photo, group_id=int(group))

    push = vk_session.method(
        method='wall.post',
        values={
            'message': text,
            'owner_id': f'-{group}',
            'from_group': 1,
            'attachments': f'photo{photos[0]["owner_id"]}_{photos[0]["id"]}',
        },
    )

    return f'https://vk.com/wall-{group}_{push["post_id"]}'


async def delay_post(photo: str, user_id: int, text: str = '') -> dict:
    """
    Function to send post in vk

    :param photo str: Post attachment
    :param user_id int: User id in database
    :param text str: Post message

    :return dict:
    """

    group = getenv('VK_GROUP', None)

    vk_session = vk_api.VkApi(token=getenv('VK_TOKEN', None))

    upload = vk_api.VkUpload(
        vk_session.get_api()
    )

    photos = upload.photo_wall(photo, group_id=int(group))

    date = convert_time(user_id)

    push = vk_session.method(
        method='wall.post',
        values={
            'message': text,
            'owner_id': f'-{group}',
            'from_group': 1,
            'publish_date': date,
            'attachments': f'photo{photos[0]["owner_id"]}_{photos[0]["id"]}',
        }
    )

    return {
        "post": f'https://vk.com/wall-{group}_{push["post_id"]}',
        "date": date,
    }


__all__ = (
    'send_post',
    'delay_post',
)
