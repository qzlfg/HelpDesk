from redis.asyncio import from_url

from .config import settings

valkey_client = from_url(settings.valkey_url, decode_responses=True)