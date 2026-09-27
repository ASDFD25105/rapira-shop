import asyncio
import json
import pytz
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.filters import CommandStart

# === НАСТРОЙКИ: ЗАПОЛНИТЕ ТОЛЬКО ЭТИ ДВЕ СТРОКИ ===
BOT_TOKEN = "8805785582:AAFp6xt-P1L-iguQVR4djXP5EuiSpuKZkko"
ADMIN_ID = 1308796575 # Твой числовой Telegram ID из @userinfobot (БЕЗ КАВЫЧЕК)
# =======================================================

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_cmd(message: Message):
    # Твоя автоматическая ссылка с GitHub Pages
    web_app_url = "https://github.io" 
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Открыть Rapira Drop Shop ⚡", web_app=WebAppInfo(url=web_app_url))]
    ])
    await message.answer(
        f"Привет, {message.from_user.first_name}! 👋\n\n"
        "Добро пожаловать в **Rapira Drop Shop by Necro**.\n"
        "Нажми на кнопку ниже, чтобы открыть витрину пакетов голды:", 
        reply_markup=kb
    )

@dp.message(F.web_app_data)
async def web_app_data_handler(message: Message):
    data = json.loads(message.web_app_data.data)
    pack_name = data.get("pack")      
    gold_amount = data.get("gold")    
    nickname = data.get("nickname")  
    price = data.get("price")         

    # Кнопка демо-оплаты
    pay_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"💳 Оплатить {price} RUB через СБП", callback_data=f"pay:{pack_name}:{gold_amount}:{nickname}:{price}")]
    ])

    await message.answer(
        f"📦 **Счёт на оплату сформирован!**\n\n"
        f"Товар: {pack_name} ({gold_amount} голды)\n"
        f"Игровой ник: `{nickname}`\n"
        f"Сумма к оплате: **{price} рублей**\n\n"
        f"Нажмите на кнопку ниже для перехода к оплате:",
        reply_markup=pay_kb
    )

@dp.callback_query(F.data.startswith("pay:"))
async def process_test_payment(callback):
    await callback.answer("Запрос обрабатывается...")
    
    _, pack_name, gold_amount, nickname, price = callback.data.split(":")
    
    # Удаляем кнопку, чтобы избежать повторных нажатий
    await callback.message.edit_reply_markup(reply_markup=None)
    
    # Сообщение покупателю
    await callback.message.answer(
        f"🎉 **Оплата успешно завершена!**\n\n"
        f"Вы купили пакет: **{pack_name}** ({gold_amount} голды).\n"
        f"Ваш игровой ник: `{nickname}`\n\n"
        f"Necro уже зачисляет золото на твой аккаунт. Ожидай в игре 5-15 минут!"
    )
    
    # Моментальное уведомление администратору (вам в этого же бота)
    await bot.send_message(
        chat_id=ADMIN_ID,
        text=f"🚨 **НОВЫЙ ОПЛАЧЕННЫЙ ЗАКАЗ В RAPIRA SHOP!**\n\n"
             f"👤 Покупатель в TG: @{callback.from_user.username} (ID: {callback.from_user.id})\n"
             f"🎮 Игровой ник: `{nickname}`\n"
             f"📦 Купленный пак: **{pack_name}** ({gold_amount} голды)\n"
             f"💵 Получено: {price} руб. (Тестовый режим)\n\n"
             f"⚠️ Срочно зайдите в игру и отправьте голду на ник `{nickname}`."
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
  
