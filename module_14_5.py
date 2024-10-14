from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from PIL import Image, ImageDraw, ImageFont
from crud_functions import *

for i in range(1, count_str + 1):
    product = f'Product{i}'
    image = Image.new("RGB", (385, 138), color='black')
    image.save(f"Product{i}.png")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("arial.ttf", size=48)
    draw.text((50, 40), product, color='white', font=font)
    image.save(f"Product{i}.png")
    # image.show()

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button_info = KeyboardButton(text='Информация')
button_calculate = KeyboardButton(text='Рассчитать')
button_buy = KeyboardButton(text='Купить')
button_reg = KeyboardButton(text='Регистрация')

kb.add(button_info, button_calculate, button_buy, button_reg)

kb_line = InlineKeyboardMarkup(resize_keyboard=True)

button_line1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button_line2 = InlineKeyboardButton(text='Формула расчета', callback_data='formulas')
kb_line.add(button_line1, button_line2)

kb_line_Product = InlineKeyboardMarkup(resize_keyboard=True)
button_Product1 = InlineKeyboardButton(text='Product1', callback_data='product_buying')
button_Product2 = InlineKeyboardButton(text='Product2', callback_data='product_buying')
button_Product3 = InlineKeyboardButton(text='Product3', callback_data='product_buying')
button_Product4 = InlineKeyboardButton(text='Product4', callback_data='product_buying')
kb_line_Product.add(button_Product1, button_Product2, button_Product3, button_Product4)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State()




@dp.message_handler(text='Регистрация')
async def sing_up(message):
    await message.answer('Введите имя пользователя (только латинский алфавит):')
    await RegistrationState.username.set()



























@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    if is_included(message.text) is True:
        await message.answer('Пользователь существует, введите другое имя')
        await RegistrationState.username.set()

    else:
        await state.update_data(username=message.text)
        await message.answer('Введите свой email:')
        await RegistrationState.email.set()





























@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    await message.answer('Введите свой возраст:"')
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age=message.text)
    new_user = await state.get_data()
    add_user(new_user['username'], new_user['email'], new_user['age'])
    await message.answer('Вы успешно зарегистрировались')
    await state.finish()












@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer(f"Привет, {message.from_user.username}! Чем могу помочь?", reply_markup=kb)


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer("Выбери опцию", reply_markup=kb_line)


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    formula = ('Формула для мужчин:\n10 * Вес + 6,25 * Рост – 5 * Возраст + 5'
               '\nФормула для женщин:\n10 * Вес + 6,25 * Рост – 5 * Возраст – 161')
    await call.message.answer(formula)
    await call.answer()


@dp.message_handler(text='Информация')
async def inform(message):
    await message.answer('Этот бот поможет расчитать норму калорий в день')


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()
    await call.answer()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    await message.answer(10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5)
    await state.finish()


"""старая функция"""
# @dp.message_handler(text='Купить')
# async def get_buying_list(message):
#     for i in range(1, 5):
#         with open(f'Product{i}.png', 'rb') as img:
#             await message.answer_photo(img, f'Название: Product{i} | Описание: описание {i} | Цена: {i * 100}')
#     await message.answer("Что желаете приобрести:", reply_markup=kb_line_Product)


@dp.message_handler(text='Купить')
async def get_buying_list(message):
    sqlite3.connect('database.db')
    all_products = get_all_products()
    index = 0
    while count_str > index:
        with open(f'Product{index + 1}.png', 'rb') as img:
            await message.answer_photo(img,
                                       f'Название: {all_products[index][1]} | Описание: {all_products[index][2]} | Цена: {all_products[index][3]}')
            index += 1
    await message.answer("Что желаете приобрести:", reply_markup=kb_line_Product)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    initiate_db()
    connection.commit()
    connection.close()
