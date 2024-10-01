from vk_back.timers.converter import convert_time

from os import getenv

import vk_api


def get_cc_link(link: str) -> str:
    """
    Function to create short link

    :param link str: Link to convert
    :return str: short link
    """

    vk_session = vk_api.VkApi(token=getenv('VK_TOKEN', None))

    response = vk_session.method(
        method='utils.getShortLink',
        values={
            'url': link,
            'private': 1,
        },
    )

    return response.get('short_url', None)


async def send_post(photo: str = '', text: str = '') -> str:
    """
    Function to send post in vk

    :param photo str: Post attachment
    :param text str: Post message

    :return str:
    """

    if not photo and not text:
        raise Exception('Text is required if the photo parameter is not specified!')

    group = getenv('VK_GROUP', None)

    vk_session = vk_api.VkApi(token=getenv('VK_TOKEN', None))

    upload = vk_api.VkUpload(
        vk_session.get_api()
    )

    photos = None

    if photo:
        photos = upload.photo_wall(photo, group_id=int(group))

    push = vk_session.method(
        method='wall.post',
        values={
            'message': text,
            'owner_id': f'-{group}',
            'from_group': 1,
            'attachments': f'photo{photos[0]["owner_id"]}_{photos[0]["id"]}' if photos else '',
        },
    )

    return f'https://vk.com/wall-{group}_{push["post_id"]}'


async def delay_post(user_id: int, text: str = '', photo: str = '') -> dict:
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

    photos = None

    if photo:
        photos = upload.photo_wall(photo, group_id=int(group))

    date = convert_time(user_id)

    push = vk_session.method(
        method='wall.post',
        values={
            'message': text,
            'owner_id': f'-{group}',
            'from_group': 1,
            'publish_date': date,
            'attachments': f'photo{photos[0]["owner_id"]}_{photos[0]["id"]}' if photos else '',
        }
    )

    return {
        "post": f'https://vk.com/wall-{group}_{push["post_id"]}',
        "date": date,
    }


__all__ = (
    'send_post',
    'delay_post',
    'get_cc_link',
)
