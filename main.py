# main.py (на Render)
import logging
import requests
from aiohttp import web

# === 🔑 ТОЛЬКО ТОКЕН БОТА НУЖЕН ===
BOT_TOKEN = "7503684350:AAGeKkAK1pTuAL_rjYu5ml_TJFw3A4BwPWw"
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

logging.basicConfig(level=logging.INFO)

async def yookassa_handler(request):
    try:
        data = await request.json()
        if data.get("event") == "payment.succeeded":
            metadata = data.get("object", {}).get("metadata", {})
            user_id = metadata.get("user_id")
            payment_type = metadata.get("type", "bind")

            if user_id:
                if payment_type == "bind":
                    text = "✅ Карта привязана!\nВыберите самокат:\n\nСамокат 1\nСамокат 2\nСамокат 3"
                    # В реальности — лучше отправить кнопки через бота, но для простоты — текст
                elif payment_type == "ride":
                    text = "✅ Аренда начата!"
                elif payment_type == "extension":
                    text = "✅ Аренда продлена!"
                else:
                    text = "✅ Платёж получен."

                # Отправка сообщения в Telegram
                requests.post(TELEGRAM_API, json={
                    "chat_id": user_id,
                    "text": text,
                    "parse_mode": "HTML"
                })
                logging.info(f"Отправлено сообщение пользователю {user_id}")

        return web.json_response({"status": "ok"})
    except Exception as e:
        logging.error(f"Ошибка webhook: {e}")
        return web.json_response({"error": "bad request"}, status=400)

app = web.Application()
app.router.add_post("/yookassa/webhook", yookassa_handler)

if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=8080)
