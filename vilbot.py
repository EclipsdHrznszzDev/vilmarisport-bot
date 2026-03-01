from aiogram import Bot, Dispatcher, types
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import http.server
import socketserver
import os
import threading

TOKEN = "8646189608:AAEl-cQB3IZS3dQDDH785yLV53ex_pSgSFE"
WEB_APP_URL = "https://vilmariofficial.ru/vilmarisport" # Ссылка на твой магазин

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- ФИКТИВНЫЙ ВЕБ-СЕРВЕР (ЧТОБЫ RENDER НЕ РУГАЛСЯ) ---
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'Bot is running!')

def run_web_server():
    port = int(os.environ.get('PORT', 8080))
    with socketserver.TCPServer(("", port), MyHandler) as httpd:
        print(f"🌐 Web server started on port {port}")
        httpd.serve_forever()

# --- КЛАВИАТУРЫ ---

def get_main_menu():
    btn_shop = InlineKeyboardButton(text="🛍 Магазин", web_app=WebAppInfo(url=WEB_APP_URL))
    btn_author = InlineKeyboardButton(text="👤 Об авторе", callback_data="show_author")
    
    return InlineKeyboardMarkup(inline_keyboard=[
        [btn_shop],
        [btn_author]
    ])

def get_back_keyboard():
    btn_back = InlineKeyboardButton(text="🔙 Назад", callback_data="go_main_menu")
    return InlineKeyboardMarkup(inline_keyboard=[[btn_back]])

# --- ОБРАБОТЧИКИ ---


@dp.message(lambda message: message.text == "/start")
async def start_command(message: types.Message):
    name = message.from_user.first_name
    text = f"Привет, {name}!\n\n|                  Выберите раздел:                  |"

    # Включаем статус "печатает..." на 1.5 секунды
    await asyncio.sleep(1.5) # Пауза
    
    await message.answer(
        text=text,
        reply_markup=get_main_menu()
    )

# 1. Кнопка "Автор" -> РЕДАКТИРУЕМ сообщение
@dp.callback_query(lambda c: c.data == "show_author")
async def process_callback_author(callback_query: types.CallbackQuery):
    about_text = (
        "Разработчик Иван Смирнов: @smira_92\n\n"
        "Премиум-дизайнер и разработчик.\n"
        "Работаю с брендами, помогая им выглядеть дорого и современно.\n\n"
        "Готов обсудить ваш проект!"
    )
    
    # Вместо отправки нового сообщения, мы РЕДАКТИРУЕМ текущее
    await callback_query.message.edit_text(
        text=about_text,
        reply_markup=get_back_keyboard()
    )
    await callback_query.answer()

# 2. Кнопка "Назад" -> ВОЗВРАЩАЕМ исходное сообщение
@dp.callback_query(lambda c: c.data == "go_main_menu")
async def process_callback_back(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
        text="|                  Выберите раздел:                  |",
        reply_markup=get_main_menu()
    )
    await callback_query.answer()

async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
