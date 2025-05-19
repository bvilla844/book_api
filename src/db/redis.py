"""
import redis.asyncio as aioredis
from src.config import Config

JTI_EXPIRY = 3600  # segundos

# Cliente Redis con asyncio
token_blocklist = aioredis.from_url(Config.REDIS_URL)

async def add_jti_to_blocklist(jti: str) -> None:
    await token_blocklist.set(
        name=jti,
        value="",
        ex=JTI_EXPIRY  # 'ex' en lugar de 'exp'
    )

async def token_in_blocklist(jti: str) -> bool:
    value = await token_blocklist.get(jti)
    return value is not None

"""