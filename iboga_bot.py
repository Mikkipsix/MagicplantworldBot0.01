import os
import gspread
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from oauth2client.service_account import ServiceAccountCredentials

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Google Sheets авторизация
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("google_credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open_by_key("1HnYbGB2Mdv5Dczol8slVShPJUIJXaoj9QLu2k0wx354").sheet1

user_data = {}
questions = [
    "Как вас зовут?",
    "Из какой вы страны?",
    "Сколько Ибоги вы хотите заказать?",
    "В каком формате (кора, порошок, экстракт)?",
    "Куда доставить?",
    "Как с вами связаться (телефон или Telegram)?"
]

@dp.message_handler(commands=['start', 'order'])
async def start(message: types.Message):
    user_data[message.chat.id] = {"step": 0, "answers": []}
    await message.answer("🤲 Заказ Ибоги\n\n" + questions[0])

@dp.message_handler()
async def process_answer(message: types.Message):
    if message.chat.id not in user_data:
        await message.answer("Нажмите /order, чтобы начать оформление заказа.")
        return

    data = user_data[message.chat.id]
    step = data["step"]
    data["answers"].append(message.text)
    step += 1

    if step < len(questions):
        data["step"] = step
        await message.answer(questions[step])
    else:
        sheet.append_row(data["answers"])
        del user_data[message.chat.id]
        await message.answer("✅ Спасибо! Ваш заказ принят. Мы скоро свяжемся с вами.")
        await message.answer("""💳 Для завершения заказа, пожалуйста, переведите сумму удобным способом:

🇷🇺 Перевод на карту (Т-банк, Россия):
4377 7237 4092 3911

🌍 USDT (TRC20):
TSSamReVeLf9FWrPmoJUdrinV7Nh9y7Bjv

📤 Пожалуйста, отправьте фото или скриншот оплаты сюда.
""")

@dp.message_handler(content_types=types.ContentType.PHOTO | types.ContentType.DOCUMENT)
async def handle_payment_proof(message: types.Message):
    try:
        await bot.forward_message("@Grishatimo", from_chat_id=message.chat.id, message_id=message.message_id)
        await message.answer("✅ Чек получен. Мы подтвердим заказ в ближайшее время.")
    except Exception as e:
        await message.answer("⚠️ Не удалось переслать чек. Попробуйте позже.")
        print("Ошибка при пересылке:", e)

if __name__ == "__main__":
    executor.start_polling(dp)
