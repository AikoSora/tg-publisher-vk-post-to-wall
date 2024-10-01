import os

# Telegram Bot API
TOKEN = os.environ.get("TG_TOKEN")

# VK API
VK_API_KEY = os.environ.get("VK_TOKEN")
VK_GROUP_ID = os.environ.get("VK_GROUP")


__all__ = (
    'TOKEN',
    'VK_API_KEY',
    'VK_GROUP_ID',
)
