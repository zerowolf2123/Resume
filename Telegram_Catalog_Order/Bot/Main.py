from telegram import Bot, Update, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler, Filters, CallbackContext
from telegram.ext import CallbackQueryHandler
from telegram.utils.request import Request
from Settings.Config import TG_TOKEN, ADMIN_ID, EDIT_TEXT, NEXT_EDIT, FINISH, TEXT
from logging import getLogger
from Database.Database_users_contents import create_users_database, create_contents_database, set_users_values
from Database.Database_users_contents import set_contents_value, get_users_values, get_contents_value, delete_cat_posts
from Database.Database_users_contents import get_post_teg_value, delete_users, delete_database, get_id_post, get_url
from Database.Database_users_contents import update_update_post, delete_id_post, get_tegs, set_ivent_catalogs
from Button.Inline_Buttons import get_keyboard_url, get_keyboard_callback_data, get_keyboard_cat
from Button.Reply_Buttons import option_buttons, CATALOG, BOT

logger = getLogger(__name__)


def f(l):
    n = []
    for i in l:
        if i not in n:
            n.append(i)
    return n


"""
1. Начать делать сам каталог + 
2. Сделать возможным исправление постов +
3. Удаление конкретных постов +
4. Запретить делать подкаталоги в каталогах, где есть посты без подкаталогов
5. Вывести пост по id + 
6. Прикрепить parsmode +
7. Сделать документацию к нему +
8. Сделать пролистывание + 
9. Сделать кнопки с ссылками + 
"""


def debug_requests(f):
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except:
            logger.exception(f'Ошибка в обработке {f.__name__}')
            raise
    return inner


@debug_requests
def do_start(update: Update, context: CallbackContext):
    chat_id = update.effective_message.chat_id
    name = update.effective_user.full_name
    set_users_values(user_id=chat_id,
                     tg_name=name)
    # Admin ответ
    if chat_id in ADMIN_ID:
        context.bot.send_message(chat_id=chat_id,
                                 text=f'''Добро пожаловать адинистратор {name}

Чтобы открыть меню команд нажмите /admin_help''',
                                 reply_markup=option_buttons())
    else:
        update.effective_message.reply_text('''Добро пожаловать.

Здесь размещен каталог таваров. Они помещенны в различные категории, приятного пользования.
Чтобы открыть каталог товаров нажмите /catalog''')


@debug_requests
def do_catalog(update: Update, context: CallbackContext):
    chat_id = update.effective_message.chat_id
    contents = get_tegs()
    posts, tegs = [], []
    for i in contents:
        if '@' in i:
            a = i.find('@')
            posts.append(i.split('@')[0].replace('&', ''))
            tegs.append(i[:a+1])
        else:
            posts.append(i.replace('&', ''))
            tegs.append(i)
    posts = f(posts)
    tegs = ' '.join(f(tegs))
    set_ivent_catalogs(ivent='catalog', chat_id=chat_id, a_start=0, a_end=0)
    context.bot.send_message(chat_id=chat_id,
                             text='''Каталог открыт: ''',
                             reply_markup=get_keyboard_cat(name_post=posts,
                                                           teg=tegs,
                                                           cat='catalog',
                                                           chat_id=chat_id,
                                                           a_start=0,
                                                           a_end=0))


# Admin команда
@debug_requests
def do_admin_help(update: Update, context: CallbackContext):
    chat_id = update.effective_message.chat_id
    create_contents_database()
    if chat_id in ADMIN_ID:
        context.bot.send_message(chat_id=chat_id,
                                 text='''Команды для работы с ботом:

1. <b>&велосипеды</b> - так вы создаете раздел в каталоге, если его нет
2. <b>&велосипеды@детские</b> - так вы создаете подраздел в каталоге (ЗАПРЕЩЕННО добавлять подразделы в католаги
где есть посты)
3. <b>Name:</b> - так вы объявляете название поста (Все команды исполнять с новой строчки)
4. <b>Url:</b> - ссылка на товар
5. <b>%&</b> - вывод всех разделов в каталоге
6. <b>%&велосипеды@детские</b> - выводит все посты конкретного подраздела
7. <b>delete 9654</b> - удаляет пост с указанным id
8. <b>delete all &велосипеды@детские или &велосипеды</b> - удаляет все посты подкаталога и сам каталог
9. <b>print 9654</b> - выводит пост под конкретным id 
10. /edit - изменяет выбранный вами пост (/cancel для досрочного выхода)
11. /users - выводит id и ник всех участников бота
12. /delete_users - удаляет вышедших пользователей из базы данных
13. /delete_posts - удаляет все посты из базы данных
14. /doc_text - документация по редактированию текста''',
                                 parse_mode=ParseMode.HTML)


# Admin команда
@debug_requests
def do_doc_text(update: Update, context: CallbackContext):
    chat_id = update.effective_message.chat_id
    if chat_id in ADMIN_ID:
        context.bot.send_message(text='''Доступные виды редактиврования текста:
1.`~<b>...</b>` - Текст внутри будет жирным
2. `<i>...</i>` - Под наклоном
3. `<a href="ссылка">текс который будет ссылкой</a>` - так вы делаете текст ссылкой
4. `<code>...</code>` - меняете цвет строки (1 строки это важно)
5. `<pre>...</pre>` так вы меняете текст нескольких строк
6. `Текст <a href="Ссылка на фото">&#8205;</a>` - Так вы прикрепляете фото к посту, 
обязательно перед ссылкой указывать какой то текст''',
                                 chat_id=chat_id,
                                 parse_mode=ParseMode.MARKDOWN)


# Admin команда
@debug_requests
def do_edit(update: Update, context: CallbackContext):
    chat_id = update.effective_message.chat_id
    if chat_id in ADMIN_ID:
        context.bot.send_message(text='Выберите, что будете редактировать',
                                 chat_id=chat_id,
                                 reply_markup=get_keyboard_url())
        print(1)
        return NEXT_EDIT


# Admin ответ
@debug_requests
def do_next_edit(update: Update, context: CallbackContext):
    chat_id = update.effective_message.chat_id
    text = update.effective_message.text
    content = []
    try:
        a = int(text)
        if chat_id in ADMIN_ID:
            if context.user_data[TEXT] == 'TEXT':
                content = get_id_post(id_post=a)
            elif context.user_data[TEXT] == 'URL':
                content = get_url(id_post=a)
            if content == 'Ничего не найдено':
                context.bot.send_message(text='Ничего не найдено. Введите id правильно или закончите операцию',
                                         chat_id=chat_id)
                return NEXT_EDIT
            content_text = f'Название поста - {content[0]}\n\n{content[1]}'
            context.bot.send_message(text=content_text,
                                     chat_id=chat_id)
            context.bot.send_message(text='Введите исправленный текст',
                                     chat_id=chat_id)
            context.user_data[EDIT_TEXT] = a
            return FINISH
    except:
        context.bot.send_message(text='Введите id правильно',
                                 chat_id=chat_id)
        return NEXT_EDIT


# Admin команда
@debug_requests
def do_finish(update: Update, context: CallbackContext):
    chat_id = update.effective_message.chat_id
    text = update.effective_message.text
    if chat_id in ADMIN_ID:
        context.bot.send_message(text='Пост успешно изменен',
                                 chat_id=chat_id)
        if context.user_data[TEXT] == 'TEXT':
            update_update_post(id_post=context.user_data[EDIT_TEXT],
                               post=text)
        elif context.user_data[TEXT] == 'URL':
            update_update_post(id_post=context.user_data[EDIT_TEXT],
                               url=text)
        return ConversationHandler.END


# Admin команда
@debug_requests
def do_cancel(update: Update, context: CallbackContext):
    chat_id = update.effective_message.chat_id
    if chat_id in ADMIN_ID:
        context.bot.send_message(text='Вы досрочно завершили операцию',
                                 chat_id=chat_id)
        return ConversationHandler.END


# Admin команда
@debug_requests
def do_delete(update: Update, context: CallbackContext):
    chat_id = update.effective_message.chat_id
    if chat_id in ADMIN_ID:
        delete_users()
        context.bot.send_message(chat_id=chat_id,
                                 text='Все неактивные пользователи удалены из бота')


# Admin команда
@debug_requests
def do_delete_database(update: Update, context: CallbackContext):
    chat_id = update.effective_message.chat_id
    if chat_id in ADMIN_ID:
        delete_database()
        context.bot.send_message(text='''Вы удалили все посты''',
                                 chat_id=chat_id)
        create_contents_database()


# Admin команда
@debug_requests
def do_get_users(update: Update, context: CallbackContext):
    chat_id = update.effective_message.chat_id
    if chat_id in ADMIN_ID:
        users = get_users_values()
        user = []
        if len(users) > 0:
            for key, value in users:
                user.append(f'ID: {key}; Name: {value}')
            user = '\n'.join(user)
        else:
            user = 'Ничего не найдено'
        context.bot.send_message(chat_id=chat_id,
                                 text=user)


@debug_requests
def do_echo(update: Update, context: CallbackContext):
    chat_id = update.effective_message.chat_id
    text = update.effective_message.text
    # Admin ответ
    if chat_id in ADMIN_ID:
        if text == CATALOG:
            do_catalog(update=update, context=context)
        elif text == BOT:
            text = '''В данном боте вы можете найти интересные для себя товары,
которые можете сразу же и купить'''
            context.bot.send_message(chat_id=chat_id,
                                     text=text)
        else:
            command = text.split()
            if text == '%&':
                contents = get_contents_value()
                content = []
                for key, value, post_id, url in contents:
                    content.append(f'{key}: {value}, {post_id}')
                content = '\n'.join(content)
                text = f'{content}'
            elif text[0] == '%' and text[1] == '&' and text.count('@') == 1 and len(text) > 2:
                contents = get_post_teg_value(teg=text[1:])
                content = []
                for key, value, post_id, url in contents:
                    content.append(f'{key}: {value}, {post_id}\nURL: {url}')
                content = '\n'.join(content)
                text = f'{content}'
            elif command[0] == 'delete' and command[1] != 'all':
                try:
                    text = int(command[1])
                    delete_id_post(id_post=text)
                    text = f'Пост с id {text} успешно удален'
                except:
                    text = 'Вводите id правильно'
            elif command[0] == 'print':
                try:
                    text = int(command[1])
                    post = get_id_post(id_post=text)
                    text = f'Название поста: {post[0]}\n\n{post[1]}'
                except:
                    text = 'Вводите id правильно'
            elif command[0] == 'delete' and command[1] == 'all':
                delete_cat_posts(teg=command[2])
                text = f'Посты и каталог {command[2]} удалены'
            else:
                text = text.split('\n')
                count_teg = text[0].count('&')
                count_a = text[0].count('@')
                if count_teg == 1 and text[0][0] == '&' and count_a == 0 and text[1][0:5] == 'Name:' and text[2][:4] == 'Url:':
                    contents, content, error = get_tegs(), [], 0
                    teg = text[0]
                    for i in contents:
                        if '@' in i:
                            if teg in i:
                                error = 1
                    if error == 1:
                        text=f'''В каталоге {teg} есть подкаталоги, чтобы внести пост в 
каталог вам следует удалить все подкаталоги'''
                    else:
                        name_post = text[1][6:]
                        url = text[2][5:]
                        text = '\n'.join(text[3:])
                        set_contents_value(teg=teg.replace(' ', ''), content=text, name_post=name_post, url=url)
                        text = 'Пост был добавлен'
                elif count_teg == 1 and text[0][0] == '&' and count_a == 1 and text[0][1] != '@' and text[1][0:5] == 'Name:' and text[2][:4] == 'Url:':
                    teg = text[0]
                    name_post = text[1][6:]
                    url = text[2][5:]
                    text = '\n'.join(text[3:])
                    set_contents_value(teg=teg.replace(' ', ''), content=text, name_post=name_post, url=url)
                    text = 'Пост был добавлен'
            if text != CATALOG and text != BOT:
                context.bot.send_message(chat_id=chat_id,
                                         text=text)


def main():
    req = Request(connect_timeout=1.0,
                  read_timeout=1.5)
    bot = Bot(token=TG_TOKEN,
              request=req)
    updater = Updater(bot=bot,
                      use_context=True,)
    info = bot.get_me()
    logger.info(f'loading {info}')
    create_users_database()
    updater.dispatcher.add_handler(CommandHandler('start', do_start))
    # Admin команда
    updater.dispatcher.add_handler(CommandHandler('admin_help', do_admin_help))
    # Admin команда
    updater.dispatcher.add_handler(CommandHandler('delete_users', do_delete))
    # Admin команда
    updater.dispatcher.add_handler(CommandHandler('users', do_get_users))
    # Admin команда
    updater.dispatcher.add_handler(CommandHandler('delete_posts', do_delete_database))
    edit_post = ConversationHandler(
        entry_points={
            CommandHandler('edit', do_edit)
        },
        states={
            NEXT_EDIT: {
                MessageHandler(Filters.all, do_next_edit, pass_user_data=True)
            },
            FINISH: {
                MessageHandler(Filters.all, do_finish, pass_user_data=True)
            }
        },
        fallbacks={
            CommandHandler('cancel', do_cancel)
        }
    )
    updater.dispatcher.add_handler(CommandHandler('catalog', do_catalog))
    updater.dispatcher.add_handler(CommandHandler('doc_text', do_doc_text))
    updater.dispatcher.add_handler(edit_post)
    updater.dispatcher.add_handler(MessageHandler(Filters.text, do_echo))
    updater.dispatcher.add_handler(CallbackQueryHandler(callback=get_keyboard_callback_data))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
