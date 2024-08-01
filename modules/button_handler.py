from .settings import dispatcher, bot, connection, cursor, ID_ADMIN, user_status
import aiogram

@dispatcher.callback_query()
async def button_handler(callback: aiogram.types.CallbackQuery):
    cursor.execute('SELECT * FROM Products')
    list_product = cursor.fetchall()
    if 'button_buy' in callback.data:
        await bot.send_message(chat_id = callback.from_user.id, text = 'Ваша покупка розглядається...')
        product_index = int(callback.data.split('_')[-1])
        button_accept = aiogram.types.InlineKeyboardButton(text = 'Прийняти✔️', callback_data = f'button_accept_{callback.from_user.id}_{product_index}')
        button_reject = aiogram.types.InlineKeyboardButton(text = 'Відхилити❌', callback_data = f'button_reject_{callback.from_user.id}')
        keyboard_inline1 = aiogram.types.InlineKeyboardMarkup(inline_keyboard= [[button_accept], [button_reject]])
        product_name = ''
        for product in list_product:
            if product[0] == product_index:
                product_name = product[1]
                break
        await bot.send_message(chat_id= ID_ADMIN, text = f'Користувач - {callback.from_user.first_name}\nПридбав товар - {product_name},Індекс - {product_index}', reply_markup= keyboard_inline1)
    elif 'button_add' in callback.data:
        await bot.send_message(chat_id = callback.from_user.id, text = 'Товар доданий до кошику!')
        cursor.execute('SELECT * FROM Carts WHERE user_id =?', (callback.from_user.id,))
        cart = cursor.fetchone()
        if cart == None:
            cursor.execute('INSERT INTO Carts (user_id, products_id) VALUES (?,?)', (callback.from_user.id, callback.data.split('_')[-1]))
        else:
            products = f'{cart[2]},{callback.data.split('_')[-1]}'
            cursor.execute('UPDATE Carts SET products_id =? WHERE user_id =?', (products, callback.from_user.id))
        connection.commit()
    elif 'button_accept' in callback.data:
        user_id = int(callback.data.split('_')[-2])
        product_id = int(callback.data.split('_')[-1])
        await bot.send_message(chat_id = user_id, text = 'Ваша покупка прийнята!')
        cursor.execute('INSERT INTO Orders (user_id, product_id, cart_id) VALUES (?,?)', (user_id, product_id, 0))
        connection.commit()
    elif 'button_reject' in callback.data:
        user_id = int(callback.data.split('_')[-1])
        await bot.send_message(chat_id = user_id, text = 'Ваша покупка відхилена!')
    elif 'delete_product' in callback.data:
        product_index = int(callback.data.split('_')[-1])
        cursor.execute('DELETE FROM Products WHERE id = ?', (list_product[product_index][0],))
        message_id = callback.message.message_id
        await bot.delete_message(chat_id = ID_ADMIN, message_id = message_id)
        await bot.send_message(chat_id= ID_ADMIN, text = 'Товар видалений!')
        connection.commit()
    elif 'edit_product_name' in callback.data:
        await bot.send_message(chat_id = ID_ADMIN, text = 'Введіть нову назву товару')
        product_id = callback.data.split('_')[-1]
        user_status[ID_ADMIN] = f'edit_product_name_{product_id}'
    elif 'edit_product_price' in callback.data:
        await bot.send_message(chat_id = ID_ADMIN, text = 'Введіть нову ціну товару')
        product_id = callback.data.split('_')[-1]
        user_status[ID_ADMIN] = f'edit_product_price_{product_id}'
    elif 'edit_product_description' in callback.data:
        await bot.send_message(chat_id = ID_ADMIN, text = 'Введіть новий опис товару')
        product_id = callback.data.split('_')[-1]
        user_status[ID_ADMIN] = f'edit_product_description_{product_id}'
    elif 'delete_cart' in callback.data:
        product_index1 = int(callback.data.split('_')[-1])
        cursor.execute("SELECT * FROM Carts WHERE user_id =?", (callback.from_user.id,))
        cart = cursor.fetchone()   
        list_product1 = cart[2].split(',')
        del list_product1[product_index1]
        message_id = callback.message.message_id
        await bot.delete_message(chat_id = callback.from_user.id, message_id = message_id)
        if len(list_product1) == 0:
            cursor.execute('DELETE FROM Carts WHERE user_id =?', (callback.from_user.id,))
        else:
            cursor.execute('UPDATE Carts SET products_id =? WHERE user_id =?', (','.join(list_product1), callback.from_user.id))
        connection.commit()