import aiohttp
from fastapi import APIRouter

ai_router = APIRouter()

@ai_router.post("/suggest")
async def get_suggestions(text: str):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://api.languagetool.org/v2/check",
            data={"text": text, "language": "en-US"}
        ) as response:
            result = await response.json()
            return result.get("matches", [])