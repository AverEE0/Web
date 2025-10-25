# main.py
import logging
from aiohttp import web

logging.basicConfig(level=logging.INFO)

async def yookassa_handler(request):
    try:
        data = await request.json()
        event = data.get("event")
        if event == "payment.succeeded":
            metadata = data.get("object", {}).get("metadata", {})
            user_id = metadata.get("user_id")
            logging.info(f"✅ Успешный платёж от пользователя {user_id}")
            # Здесь вы можете обновить статус аренды в БД
        return web.json_response({"status": "ok"})
    except Exception as e:
        logging.error(f"Ошибка webhook: {e}")
        return web.json_response({"error": "bad request"}, status=400)

app = web.Application()
app.router.add_post("/yookassa/webhook", yookassa_handler)

if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=8080)