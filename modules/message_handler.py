from .settings import dispatcher, ID_ADMIN, user_status, new_product, cursor, connection, bot
import aiogram

@dispatcher.message()
async def message_handler(message: aiogram.types.Message):
    if message.from_user.id == ID_ADMIN and ID_ADMIN in user_status and user_status[ID_ADMIN] == 'add_product_name':
        new_product['name'] = message.text
        user_status[ID_ADMIN] = 'add_product_price'
        await message.answer(text = 'Введіть ціну товару')
    elif message.from_user.id == ID_ADMIN and ID_ADMIN in user_status and user_status[ID_ADMIN] == 'add_product_price':
        new_product['price'] = int(message.text)
        user_status[ID_ADMIN] = 'add_product_description'
        await message.answer(text = 'Введіть опис товару')
    elif message.from_user.id == ID_ADMIN and ID_ADMIN in user_status and user_status[ID_ADMIN] == 'add_product_description':
        new_product['description'] = message.text
        user_status[ID_ADMIN] = ''
        cursor.execute('INSERT INTO Products (name, price, description) VALUES (?,?,?)', (new_product['name'], new_product['price'], new_product['description']))
        await message.answer(text = 'Товар успішно доданий!')
        connection.commit()
    elif message.from_user.id == ID_ADMIN and ID_ADMIN in user_status and 'edit_product_name' in user_status[ID_ADMIN]:
        index_product = int(user_status[ID_ADMIN].split('_')[-1])
        cursor.execute('UPDATE Products SET name =? WHERE id =?', (message.text, index_product))
        connection.commit()
        await message.answer(text = 'Товар успішно змінений!')
        user_status[ID_ADMIN] = ''
    elif message.from_user.id == ID_ADMIN and ID_ADMIN in user_status and 'edit_product_price' in user_status[ID_ADMIN]:
        index_product = int(user_status[ID_ADMIN].split('_')[-1])
        cursor.execute('UPDATE Products SET price =? WHERE id =?', (int(message.text), index_product))
        connection.commit()
        await message.answer(text = 'Товар успішно змінений!')
        user_status[ID_ADMIN] = ''
    elif message.from_user.id == ID_ADMIN and ID_ADMIN in user_status and 'edit_product_description' in user_status[ID_ADMIN]:
        index_product = int(user_status[ID_ADMIN].split('_')[-1])
        cursor.execute('UPDATE Products SET description =? WHERE id =?', (message.text, index_product))
        connection.commit()
        await message.answer(text = 'Товар успішно змінений!')
        user_status[ID_ADMIN] = ''
    else:
        cursor.execute('SELECT * FROM Products')
        list_product = cursor.fetchall()
        for product in list_product:
            if product[1] == message.text:
                button_buy = aiogram.types.InlineKeyboardButton(text = 'Купити', callback_data = f'button_buy_{product[0]}')
                button_bought = aiogram.types.InlineKeyboardButton(text = 'Додати до кошику', callback_data = f'button_add_{product[0]}')
                keyboard_inline = aiogram.types.InlineKeyboardMarkup(inline_keyboard = [[button_buy], [button_bought]])
                photo = aiogram.types.FSInputFile(f'image/{product[1]}.jpg')
                await bot.send_photo(chat_id = message.from_user.id, photo = photo, caption = f'Ви обрали товар - {product[1]} \nЦіна товару - {product[2]} \nОпис товару - {product[3]}', reply_markup = keyboard_inline)
        
    if message.text == 'Видалити товари' and message.from_user.id == ID_ADMIN:
        for product in list_product:
            button_delete = aiogram.types.InlineKeyboardButton(text = 'Видалити', callback_data= f'delete_product_{product[0]}')
            keyboard_inline = aiogram.types.InlineKeyboardMarkup(inline_keyboard = [[button_delete]])
            photo = aiogram.types.FSInputFile(f'image/{product[1]}.jpg')
            await bot.send_photo(chat_id = message.from_user.id, photo = photo, caption = f'Товар - {product[1]} \nЦіна товару - {product[2]} \nОпис товару - {product[3]}', reply_markup = keyboard_inline)
    elif message.text == 'Додати товари' and message.from_user.id == ID_ADMIN:
        user_status[ID_ADMIN] = 'add_product_name'
        await message.answer(text = 'Введіть назву товару')
    elif message.text == 'Змінити товари' and message.from_user.id == ID_ADMIN:
        for product in list_product:
            button_edit_name = aiogram.types.InlineKeyboardButton(text = 'Змінити назву товару', callback_data = f'edit_product_name_{product[0]}')
            button_edit_price = aiogram.types.InlineKeyboardButton(text = 'Змінити ціну товару', callback_data = f'edit_product_price_{product[0]}')
            button_edit_description = aiogram.types.InlineKeyboardButton(text = 'Змінити опис товару', callback_data = f'edit_product_description_{product[0]}')
            keyboard2 = aiogram.types.InlineKeyboardMarkup(inline_keyboard = [[button_edit_name], [button_edit_price], [button_edit_description]])
            photo = aiogram.types.FSInputFile(f'image/{product[1]}.jpg')
            await bot.send_photo(chat_id = message.from_user.id, photo = photo, caption = f'Товар - {product[1]} \nЦіна товару - {product[2]} \nОпис товару - {product[3]}', reply_markup = keyboard2)
    elif message.text == 'Оформити замовлення':
        user = message.from_user.id
        cursor.execute('SELECT * FROM Carts WHERE user_id =?', (user,))
        cart_id = cursor.fetchone()[0]
        cursor.execute('INSERT INTO Orders (user_id, product_id, cart_id) VALUES (?,?,?)', (message.from_user.id, 0, cart_id))
        connection.commit()
        await message.answer(text = 'Замовлення оформлено!')