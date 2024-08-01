from .settings import dispatcher, cursor, ID_ADMIN
import aiogram

@dispatcher.message(aiogram.filters.CommandStart())
async def welcome(message: aiogram.types.Message):
    list_button = []
    cursor.execute('SELECT * FROM Products')
    list_product = cursor.fetchall()
    for product in list_product:
        button = aiogram.types.KeyboardButton(text = product[1])
        list_button.append([button])
    keyboard = aiogram.types.ReplyKeyboardMarkup(keyboard = list_button)
    await message.answer(text = 'Вітаю користувач! \nʼЦе телеграм бот створений для покупки Техніки\n Оберіть товар', reply_markup = keyboard)
@dispatcher.message(aiogram.filters.Command('cart'))
async def show_cart(message: aiogram.types.Message):
    button_buy_product = aiogram.types.KeyboardButton(text = 'Оформити замовлення')
    keyboard_buy = aiogram.types.ReplyKeyboardMarkup(keyboard = [[button_buy_product]])
    await message.answer(text = 'Ваш кошик:', reply_markup = keyboard_buy)
    cursor.execute("SELECT * FROM Carts WHERE user_id =?", (message.from_user.id,))
    cart = cursor.fetchone()   
    count = -1
    if cart == None:
        await message.answer(text = 'Ваш кошик порожній')
    else:
        list_product1 = cart[2].split(',')
        for i in list_product1:
            count += 1
            cursor.execute("SELECT * FROM Products WHERE id =?", (int(i),))
            product = cursor.fetchone()
            button_delete_product = aiogram.types.InlineKeyboardButton(text = 'Видалити', callback_data = f'delete_cart_{count}')
            keyboard3 = aiogram.types.InlineKeyboardMarkup(inline_keyboard = [[button_delete_product]])
            await message.answer(text = f'Назва: {product[1]}\nЦіна: {product[2]}\nОпис: {product[3]}', reply_markup = keyboard3)
@dispatcher.message(aiogram.filters.Command('admin'))
async def admin(message: aiogram.types.Message):
    if message.from_user.id == ID_ADMIN:
        button_change = aiogram.types.KeyboardButton(text = 'Змінити товари')
        button_add = aiogram.types.KeyboardButton(text = 'Додати товари')
        button_remove = aiogram.types.KeyboardButton(text = 'Видалити товари')
        keyboard2 = aiogram.types.ReplyKeyboardMarkup(keyboard = [[button_change], [button_add], [button_remove]])
        await message.answer(text = 'Вітаю адмін! Що ви хочете зробити?', reply_markup = keyboard2)
    else:
        await message.answer(text = 'У вас немає доступу до адмін панелі')