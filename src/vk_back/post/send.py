from config import VK_API_KEY, VK_GROUP_ID

from vk_back.timers.converter import convert_time

import vk_api


async def send_post(photo: str) -> str:
    """
    Function to send post in vk

    :param: Photo str

    :return: str
    """

    vk_session = vk_api.VkApi(token=VK_API_KEY)

    upload = vk_api.VkUpload(
        vk_session.get_api()
    )

    photos = upload.photo_wall(photo, group_id=int(VK_GROUP_ID))

    push = vk_session.method(
        method='wall.post',
        values={
            'owner_id': f'-{VK_GROUP_ID}',
            'from_group': 1,
            'attachments': f'photo{photos[0]["owner_id"]}_{photos[0]["id"]}',
        },
    )

    return f'https://vk.com/wall-{VK_GROUP_ID}_{push["post_id"]}'


async def delay_post(photo: str, user_id: int) -> dict:
    """
    Function to send post in vk

    :param: Photo str
    :param: User id int

    :return: dict
    """

    vk_session = vk_api.VkApi(token=VK_API_KEY)

    upload = vk_api.VkUpload(
        vk_session.get_api()
    )

    photos = upload.photo_wall(photo, group_id=int(VK_GROUP_ID))

    date = convert_time(user_id)

    push = vk_session.method(
        method='wall.post',
        values={
            'owner_id': f'-{VK_GROUP_ID}',
            'from_group': 1,
            'publish_date': date,
            'attachments': f'photo{photos[0]["owner_id"]}_{photos[0]["id"]}',
        }
    )

    return {
        "post": f'https://vk.com/wall-{VK_GROUP_ID}_{push["post_id"]}',
        "date": date,
    }


__all__ = (
    'send_post',
    'delay_post',
)
