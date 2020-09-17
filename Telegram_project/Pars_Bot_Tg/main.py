from telegram import Bot, Update
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackContext, Filters, MessageHandler, CallbackQueryHandler
from telegram.utils.request import Request
from logging import getLogger
from Pars_Bot_Tg.config import TG_TOKEN
from Pars_Bot_Tg.ReplyButton import option_buttons, HELP, option_buttons_pars
from Pars_Bot_Tg.New_Parcer import start
from Pars_Bot_Tg.database import get_data, get_data_ivent, set_user_id, set_data_ivent, get_data_link, set_data_links
from Pars_Bot_Tg.database import set_price, get_price

logger = getLogger(__name__)


def debug_requests(f):
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except:
            logger.exception(f'Ошибка в обработке {f.__name__}')
            raise
    return inner


def get_keyboard(keys):
    keyboard, a = [], 0
    for i in range(len(keys)):
        if a != 7:
            keyboard.append([InlineKeyboardButton(keys[i], callback_data=f'{i}')])
        else:
            break
        a += 1
    keyboard.append([
        InlineKeyboardButton('Назад', callback_data='left'),
        InlineKeyboardButton('Вперед', callback_data='right')
    ])
    return InlineKeyboardMarkup(keyboard)


def get_keyboard1(keys, links, i, price):
    keyboard = []
    keyboard.append([InlineKeyboardButton(keys + f' - {price}', url=links[i])])
    return InlineKeyboardMarkup(keyboard)


@debug_requests
def keyboard_callback_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    chat_id = update.effective_user.id
    data = query.data
    items, game = get_data_ivent(user_id=chat_id)
    link, link_image = get_data_link(user_id=chat_id)
    price = get_price(user_id=chat_id)
    games, link, link_image, price = game.split('\n'), link.split('\n'), link_image.split('\n'), price.split('\n')
    link, link_image, price = link[items:], link_image[items:], price[items:]
    gamers = games[items:]
    if data == 'right':
        if len(gamers) > 6:
            items += 7
        games = games[items:]
        query.edit_message_text(
            text='Вот что мы смогли найти:',
            reply_markup=get_keyboard(games)
        )
    elif data == 'left':
        if items >= 7:
            items -= 7
            games = games[items:]
        query.edit_message_text(
            text='Вот что мы смогли найти:',
            reply_markup=get_keyboard(games)
        )

    elif data == '0':
        context.bot.send_message(
            text=f"{gamers[0]}:<a href='{link_image[0]}'>&#8205;</a>",
            chat_id=chat_id,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=False,
            reply_markup=get_keyboard1('steampay.com', link, 0, price[0])
        )
    elif data == '1':
        context.bot.send_message(
            text=f"{gamers[1]}:<a href='{link_image[1]}'>&#8205;</a>",
            chat_id=chat_id,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=False,
            reply_markup=get_keyboard1('steampay.com', link, 1, price[1])
        )
    elif data == '2':
        context.bot.send_message(
            text=f"{gamers[2]}:<a href='{link_image[2]}'>&#8205;</a>",
            chat_id=chat_id,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=False,
            reply_markup=get_keyboard1('steampay.com', link, 2, price[2])
        )
    elif data == '3':
        context.bot.send_message(
            text=f"{gamers[3]}:<a href='{link_image[3]}'>&#8205;</a>",
            chat_id=chat_id,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=False,
            reply_markup=get_keyboard1('steampay.com', link, 3, price[3])
        )
    elif data == '4':
        context.bot.send_message(
            text=f"{gamers[4]}:<a href='{link_image[4]}'>&#8205;</a>",
            chat_id=chat_id,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=False,
            reply_markup=get_keyboard1('steampay.com', link, 4, price[4])
        )
    elif data == '5':
        context.bot.send_message(
            text=f"{gamers[5]}:<a href='{link_image[5]}'>&#8205;</a>",
            chat_id=chat_id,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=False,
            reply_markup=get_keyboard1('steampay.com', link, 5, price[5])
        )
    elif data == '6':
        context.bot.send_message(
            text=f"{gamers[6]}:<a href='{link_image[6]}'>&#8205;</a>",
            chat_id=chat_id,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=False,
            reply_markup=get_keyboard1('steampay.com', link, 6, price[6])
        )

    set_data_ivent(data_ivent=items,
                   user_id=chat_id,
                   data_text=game)


@debug_requests
def do_start(update: Update, context: CallbackContext):
    chat_id = update.effective_message.chat_id
    update.effective_message.reply_text(
        '''Добро пожаловать
Нажмите /help для большей информации''',
        reply_markup=option_buttons()
    )
    set_user_id(user_id=chat_id)


@debug_requests
def do_help(update: Update, context: CallbackContext):
    update.effective_message.reply_text(
        '''Введите название игры для поиска в интернет магазине''',
        reply_markup=option_buttons_pars()
    )


@debug_requests
def do_echo(update: Update, context: CallbackContext):
    user = update.effective_user.full_name
    text = update.effective_message.text
    chat = update.effective_user.id
    if text.lower() == 'привет' or text.lower() == 'здравствуйте':
        update.effective_message.reply_text(f'Привет {chat}')
    elif text.lower() == 'пока':
        update.effective_message.reply_text(f'Пока {user}')
    elif text == HELP:
        return do_help(update=update, context=context)
    else:
        items = start(text,
                      title=True,
                      url=True,
                      image=True,
                      price=True)
        if items == 'Ничего не найдено':
            update.effective_message.reply_text(f'{items}')
        else:
            games, link, link_image, price = items[0], items[1], items[2], items[3]
            # print(games)
            game_items = '\n'.join(games)
            link, link_image, price = '\n'.join(link), '\n'.join(link_image), '\n'.join(price)
            game = game_items.split('\n')
            update.effective_message.reply_text('Вот что мы смогли найти:',
                                                reply_markup=get_keyboard(game))
            set_data_ivent(data_ivent=0,
                           user_id=chat,
                           data_text=game_items)
            set_data_links(link=link,
                           user_id=chat,
                           link_image=link_image)
            set_price(user_id=chat,
                      price=price)


def main():
    req = Request(connect_timeout=1.0,
                  read_timeout=1.5)
    bot = Bot(token=TG_TOKEN,
              request=req)
    updater = Updater(bot=bot,
                      use_context=True)
    get_data()
    updater.dispatcher.add_handler(CommandHandler('start', do_start))
    updater.dispatcher.add_handler(CommandHandler('help', do_help))
    updater.dispatcher.add_handler(MessageHandler(Filters.all, do_echo))
    updater.dispatcher.add_handler(CallbackQueryHandler(callback=keyboard_callback_handler))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
