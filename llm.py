import aiohttp
from config import Config

user_contexts = {}

async def query_llm(user_id: int, message: str) -> str:
    if user_id not in user_contexts:
        user_contexts[user_id] = [{"role": "system", "content": Config.SYSTEM_PROMPT}]

    user_contexts[user_id].append({"role": "user", "content": message})

    headers = {
        "Authorization": f"Bearer {Config.OPENROUTER_API_KEY}",
        "HTTP-Referer": Config.HTTP_REFERER,
        "Content-Type": "application/json"
    }

    payload = {
        "model": Config.MODEL,
        "messages": user_contexts[user_id][-Config.CONTEXT_LENGTH:],
        "temperature": Config.TEMPERATURE
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(Config.OPENROUTER_API_URL, headers=headers, json=payload) as resp:
                data = await resp.json()
                if resp.status == 200:
                    reply = data["choices"][0]["message"]["content"]
                    user_contexts[user_id].append({"role": "assistant", "content": reply})
                    return reply
                else:
                    return f"⚠️ API Error: {data.get('error', {}).get('message', 'Unknown error')}"
    except Exception as e:
        return f"🔴 Ошибка соединения: {e}"

def reset_context(user_id: int):
    user_contexts.pop(user_id, None)
