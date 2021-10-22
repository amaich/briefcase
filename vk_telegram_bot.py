import aiogram
from aiogram import Bot, Dispatcher, types
# from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from config import login, password, token

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

import logging

vk_session = vk_api.VkApi(login=login, password=password, token=token)
vk = vk_session.get_api()
longpool = VkLongPoll(vk_session)

token = '2078052224:AAHnaPX8BRU5q-1JLUyVFxa3Qrtpu9t-sY4'
bot = aiogram.Bot(token=token)
dp = aiogram.Dispatcher(bot)


class Answer(StatesGroup):
    answer = State()


global callback_user
my_group_id = 207947616


@dp.message_handler(commands=['start'])
async def start_bot(message: aiogram.types.Message):
    await message.reply('ВК Чат бот', reply_markup=aiogram.types.ReplyKeyboardMarkup(resize_keyboard=True).add(
        aiogram.types.KeyboardButton('Показать чаты')))


@dp.message_handler(text=['Показать чаты'])
async def show_all_chats(message: aiogram.types.Message):
    y = vk.messages.getConversations(user_id=my_group_id)
    msg = ''
    for i in y["items"]:
        user_id = i["conversation"]["peer"]["id"]
        user = vk.users.get(user_ids=user_id)
        last_message_id = abs(i["last_message"]["from_id"])
        if last_message_id == my_group_id:
            msg = "Чат с " + user[0]["first_name"] + " " + user[0]["last_name"] + \
                  "\nПоследнее сообщение от вас:\n" + i["last_message"]["text"]
        else:
            msg = "Чат с " + user[0]["first_name"] + " " + user[0]["last_name"] + \
                  "\nПоследнее сообщение от собеседника:\n" + i["last_message"]["text"]
        await message.reply(msg, reply_markup=aiogram.types.InlineKeyboardMarkup().add(
            aiogram.types.InlineKeyboardButton(text='Ответить', callback_data=user_id)
        ))


@dp.callback_query_handler(lambda c: c.data.isdigit())
async def get_user_id(callback_query: aiogram.types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Ответить пользователю: ' + \
                           vk.users.get(user_ids=callback_query.data)[0]["first_name"] + " " + \
                           vk.users.get(user_ids=callback_query.data)[0]["last_name"])

    global callback_user
    callback_user = callback_query.data
    await Answer.answer.set()
    await bot.send_message(callback_query.from_user.id, "Введите ответ: ")


@dp.message_handler(content_types=['text'])
async def send_message(message: aiogram.types.Message, state: FSMContext):
    vk.messages.send(user_id=callback_user, message=message.text, random_id=0)

    await state.finish()


if __name__ == "__main__":
    aiogram.executor.start_polling(dp, skip_updates=False)
