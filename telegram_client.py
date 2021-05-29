import asyncio
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import os
import keyboards as kb
from fastapi_websocket_rpc import RpcMethodsBase, WebSocketRpcClient
import logging
import ast

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv('TELETOKEN',
                  '1780950638:AAG0KgQ2wVgjicMG5RQjq6lZ5d4hDsfGQZk')

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

URL = "ws://localhost:9000/ws"
client = WebSocketRpcClient(URL, RpcMethodsBase())
async def start():
    await client.__aenter__()


@dp.message_handler(commands=['start'])
async def process_command_1(message: types.Message):
    await client.other.reset_or_create_machine(name=message.from_user.id)
    await message.reply("Какую вы хотите пиццу?\nБольшую или маленькую?",
                        reply_markup=kb.inline_kb1)


@dp.message_handler(commands=['hist'])
async def process_command_1(message: types.Message):
    hist = await client.other.get_hist(name=message.from_user.id)
    hist = ast.literal_eval(hist.result)
    mess = 'История заказов:\n\n'
    if not hist:
        await message.reply('Вы ещё не делали заказов!')
        return
    for i, item in enumerate(hist, 1):
        size, payment = item.split('↦')
        mess += f'{i}. {size} пиццу, оплата - {payment}\n'
    await message.reply(mess)


@dp.callback_query_handler(lambda c: c.data in ['большую', 'маленькую'])
async def process_callback_size(callback_query: types.CallbackQuery):
    id = callback_query.from_user.id
    await client.other.update_state(name=id, phrase=callback_query.data)
    await bot.send_message(id, "Как вы будете платить?",
                           reply_markup=kb.inline_kb2)
    await bot.answer_callback_query(callback_query.id)


@dp.callback_query_handler(lambda c: c.data in ['наличкой', 'картой'])
async def process_callback_payment(callback_query: types.CallbackQuery):
    id = callback_query.from_user.id
    state = await client.other.update_state(name=id,
                                            phrase=callback_query.data)
    if '↦' in state.result:
        size, payment = state.result.split('↦')
        await bot.send_message(id,
                               f"Вы хотите {size} пиццу, оплата - {payment}?",
                               reply_markup=kb.inline_kb3)
    else:
        await bot.send_message(id, f"Пожалуйста, начните с команды: /start")
    await bot.answer_callback_query(callback_query.id)


@dp.callback_query_handler(lambda c: c.data in ['accept', 'reset'])
async def process_callback_confirmation(callback_query: types.CallbackQuery):
    id = callback_query.from_user.id
    state = await client.other.get_state(name=id)
    if '↦' in state.result:
        await client.other.update_state(name=id, phrase=callback_query.data)
        if callback_query.data == 'accept':
            await bot.send_message(id, "Заказ подтвержден")
        if callback_query.data == 'reset':
            await bot.send_message(id, "Заказ отменен")
        await client.other.reset_state(name=id)
    else:
        await bot.send_message(id, f"Пожалуйста, начните с команды: /start")
    await bot.answer_callback_query(callback_query.id)


async def shutdown(dispatcher: Dispatcher):
    await client.__aexit__()
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(start())

    executor.start_polling(dp, on_shutdown=shutdown)
