from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import CallbackContext
from Database.Database_users_contents import set_last_ivent, get_last_ivent, get_name_post, get_tegs, get_url
from Database.Database_users_contents import get_name_teg, set_ivent_catalogs, get_last_ivent_catalogs
from Settings.Config import TEXT


def get_keyboard_cat(chat_id, name_post=None, teg=None, cat=None, url=None, a_start=None, full_teg=None,
                     a_end=None):
    keyboard, a, b, c = [], a_start, 0, a_end
    if name_post != None:
        if a_end == 0 and a_start == 0:
            set_ivent_catalogs(chat_id=chat_id,
                               ivent=cat,
                               a_start=c,
                               a_end=a)
        content = get_last_ivent_catalogs(ivent=cat, chat_id=chat_id)
        '''if content != None:
            if content[0] > 7:
                a = content[1]
                if a_end != None:
                    c = content[1]'''
        for i in range(len(name_post)):
            if a % 7 == 0 and a != 0 and b != 0 and cat != 'incatalog':
                break
            elif cat == 'incatalog' and a % 6 == 0 and a != 0 and b != 0:
                break
            else:
                b += 1
                if '_' in name_post[i]:
                    name_post[i] = name_post[i].replace('_', ' ')
                keyboard.append([InlineKeyboardButton(name_post[i], callback_data=f'{i}')])
            a += 1
        if cat != 'post':
            set_last_ivent(last_ivent=f'{cat} {teg}',
                           chat_id=chat_id)
        elif cat == 'post':
            if full_teg != None:
                text = f'{cat} {"&".join(name_post)} ${full_teg}'
            else:
                text = f'{cat} {"&".join(name_post)}'
            set_last_ivent(last_ivent=text,
                           chat_id=chat_id)
    if c != None and a != None:
        if a == 7 and len(name_post) >= 7 and cat != 'incatalog':
            keyboard.append([InlineKeyboardButton('Закрыть', callback_data='close'),
                             InlineKeyboardButton('Вперед', callback_data='next')])
        elif a == 6 and len(name_post) > 6 and cat == 'incatalog':
            keyboard.append([InlineKeyboardButton('Закрыть', callback_data='close'),
                             InlineKeyboardButton('Вперед', callback_data='next')])
        elif a > 6 and len(name_post) > 6 and cat == 'incatalog':
            keyboard.append([InlineKeyboardButton('Вперед', callback_data='next'),
                             InlineKeyboardButton('Назад', callback_data='back')])
            keyboard.append([InlineKeyboardButton('Закрыть', callback_data='close')])
        elif a % 7 != 0 and a > 7:
            keyboard.append([InlineKeyboardButton('Закрыть', callback_data='close'),
                             InlineKeyboardButton('Назад', callback_data='back')])
        elif a % 7 == 0 and len(name_post) == 7:
            keyboard.append([InlineKeyboardButton('Закрыть', callback_data='close'),
                             InlineKeyboardButton('Назад', callback_data='back')])
        elif a > 7:
            keyboard.append([InlineKeyboardButton('Вперед', callback_data='next'),
                             InlineKeyboardButton('Назад', callback_data='back')])
            keyboard.append([InlineKeyboardButton('Закрыть', callback_data='close')])
        elif cat == 'catalog':
            keyboard.append([InlineKeyboardButton('Закрыть', callback_data='close')])
        if cat == 'incatalog':
            keyboard.append([InlineKeyboardButton('Вернуться в каталог', callback_data='back_catalog')])
    if url != None:
        keyboard.append([InlineKeyboardButton('Ссылка на товар', url=url)])
        keyboard.append([InlineKeyboardButton('Вернуться в подкаталог', callback_data='back_incatalog')])
    elif cat == 'post':
        keyboard.append([InlineKeyboardButton('Вернуться в подкаталог', callback_data='back_incatalog')])
    if c != None and a != None:
        set_ivent_catalogs(chat_id=chat_id,
                           ivent=cat,
                           a_start=c,
                           a_end=a)
    return InlineKeyboardMarkup(keyboard)


def get_keyboard_url():
    keyboard = [
        [
            InlineKeyboardButton('Текст', callback_data='text'),
            InlineKeyboardButton('URL', callback_data='url')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def f(l):
    n = []
    for i in l:
        if i not in n:
            n.append(i)
    return n


def get_keyboard_callback_data(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data
    chat_id = update.effective_message.chat_id
    tegs, teg, cat, post, posts, teg_name, a, b, full_teg = [], [], [], [], '', '', 0, 0, ''
    last_ivent, ivent, catalogs = [], '', ''
    if data != 'text' and data != 'url':
        last_ivent = get_last_ivent(chat_id=chat_id)[0].split()
        ivent = str(last_ivent[0])
        if '$' in last_ivent[-1]:
            catalogs = last_ivent[1:-1]
            full_teg = last_ivent[-1].replace('$', '')
        else:
            catalogs = last_ivent[1:]
        if data == 'back_incatalog':
            tegs = get_tegs(ivent=full_teg.split('@')[0])
        else:
            tegs = get_tegs()
        for i in range(len(tegs)):
            tegs[i] = tegs[i].replace(' ', '')
        tegs = f(tegs)
        if ivent == 'post':
            teg_name = ' '.join(catalogs)
            if '&' in teg_name:
                teg_name = teg_name.split('&')
                a = 'list'
    if data == 'next' or data == 'back' or data == 'back_incatalog' or data == 'back_catalog':
        if ivent == 'catalog' or ivent == 'incatalog' or data == 'back_incatalog' or data == 'back_catalog':
            for i in tegs:
                if '@' not in i:
                    teg.append(i.replace(' ', ''))
                    cat.append(i.replace(' ', '').replace('&', ''))
                elif '@' in i and data == 'back_incatalog':
                    teg.append(i.replace(' ', ''))
                    cat.append(i.split('@')[1].replace(' ', ''))
                else:
                    c = i.find('@')
                    teg.append(i[:c + 1].replace(' ', ''))
                    cat.append(i.split('@')[0].replace(' ', '').replace('&', ''))
            teg = f(teg)
            cat = f(cat)
        b = get_last_ivent_catalogs(chat_id=chat_id, ivent=ivent)
    if data == '0':
        if ivent == 'post':
            if a == 'list':
                teg_name = teg_name[0]
        else:
            if ivent == 'incatalog':
                posts = get_name_teg(teg=catalogs[0])
            teg_name = catalogs[0]
            if ivent == 'catalog' and '@' not in teg_name:
                posts = get_name_teg(teg=catalogs[0])
    elif data == '1':
        if ivent == 'post':
            if a == 'list':
                teg_name = teg_name[1]
        else:
            if ivent == 'incatalog':
                posts = get_name_teg(teg=catalogs[1])
            teg_name = catalogs[1]
            if ivent == 'catalog' and '@' not in teg_name:
                posts = get_name_teg(teg=catalogs[1])
    elif data == '2':
        if ivent == 'post':
            if a == 'list':
                teg_name = teg_name[2]
        else:
            if ivent == 'incatalog':
                posts = get_name_teg(teg=catalogs[2])
            teg_name = catalogs[2]
            if ivent == 'catalog' and '@' not in teg_name:
                posts = get_name_teg(teg=catalogs[2])
    elif data == '3':
        if ivent == 'post':
            if a == 'list':
                teg_name = teg_name[3]
        else:
            if ivent == 'incatalog':
                posts = get_name_teg(teg=catalogs[3])
            teg_name = catalogs[3]
            if ivent == 'catalog' and '@' not in teg_name:
                posts = get_name_teg(teg=catalogs[3])
    elif data == '4':
        if ivent == 'post':
            if a == 'list':
                teg_name = teg_name[4]
        else:
            if ivent == 'incatalog':
                posts = get_name_teg(teg=catalogs[4])
            teg_name = catalogs[4]
            if ivent == 'catalog' and '@' not in teg_name:
                posts = get_name_teg(teg=catalogs[4])
    elif data == '5':
        if ivent == 'post':
            if a == 'list':
                teg_name = teg_name[5]
        else:
            if ivent == 'incatalog':
                posts = get_name_teg(teg=catalogs[5])
            teg_name = catalogs[5]
            if ivent == 'catalog' and '@' not in teg_name:
                posts = get_name_teg(teg=catalogs[5])
    elif data == '6':
        if ivent == 'post':
            if a == 'list':
                teg_name = teg_name[6]
        else:
            if ivent == 'incatalog':
                posts = get_name_teg(teg=catalogs[6])
            teg_name = catalogs[6]
            if ivent == 'catalog' and '@' not in teg_name:
                posts = get_name_teg(teg=catalogs[6])
    elif data == 'next':
        teg = ' '.join(teg[b[1]:])
        cat = []
        if ivent == 'post':
            if ivent == 'post':
                a = get_name_teg(teg=full_teg)
                for i in a:
                    cat.append(i[0])
            cat = cat[b[1]:]
        elif ivent == 'incatalog':
            for i in catalogs[6:]:
                cat.append(i.split('@')[1])
            teg = ' '.join(catalogs[6:])
        elif ivent == 'catalog':
            catalogs = get_tegs()
            for i in range(len(catalogs)):
                r = catalogs[i].find('@')
                catalogs[i] = catalogs[i][:r+1]
            catalogs = f(catalogs)
            for i in catalogs[b[1]:]:
                cat.append(i.replace('&', '').replace('@', ''))
        query.edit_message_text(text='Следующие по списку',
                                reply_markup=get_keyboard_cat(name_post=cat, chat_id=chat_id, teg=teg,
                                                              cat=ivent, a_start=b[1], a_end=b[1], full_teg=full_teg))
    elif data == 'back':
        teg, d = ' '.join(teg[b[1]-8:b[1]-1]), 0
        if ivent == 'post':
            a = get_name_teg(teg=full_teg)
            for i in a:
                cat.append(i[0])
            d = b[1] - 8
            if b[1] > 14:
                cat = cat[b[1] - 8:b[1]]
                b = d
            else:
                cat = cat[:b[1]-1]
                b, d = 0, 0
        elif ivent == 'incatalog':
            a = catalogs[0].split('@')[0]
            c = get_tegs(ivent=a)
            cat = []
            for i in c:
                cat.append(i.split('@')[1])
            teg = ' '.join(c)
            if b[1] >= 12:
                d = b[0] - 6
                b = d
                cat = cat[b:]
            else:
                b, d = 0, 0
        elif ivent == 'catalog':
            d = b[0]-7
            if b[1] >= 14:
                print(cat)
                b = d
                cat = cat[b:]
            else:
                b, d = 0, 0
        query.edit_message_text(text='Предыдущие по списку',
                                reply_markup=get_keyboard_cat(name_post=cat, chat_id=chat_id, teg=teg,
                                                              cat=ivent, a_end=d, a_start=b, full_teg=full_teg))
    elif data == 'back_incatalog':
        query.edit_message_text(text='Вы вернулись в подразделы',
                                reply_markup=get_keyboard_cat(name_post=cat, chat_id=chat_id, teg=' '.join(teg),
                                                              cat='incatalog', a_end=0, a_start=0))
    elif data == 'back_catalog':
        query.edit_message_text(text='Вы вернулись в подразделы',
                                reply_markup=get_keyboard_cat(name_post=cat, chat_id=chat_id, teg=' '.join(teg),
                                                              cat='catalog', a_end=0, a_start=0))
    elif data == 'close':
        query.edit_message_text(text='Каталог закрыт')
    elif data == 'text':
        context.user_data[TEXT] = 'TEXT'
        context.bot.send_message(text='Введите id поста, текст которого вы будете редактировать',
                                 chat_id=chat_id)
    elif data == 'url':
        context.user_data[TEXT] = 'URL'
        context.bot.send_message(text='Введите id поста, url которого вы будете редактировать',
                                 chat_id=chat_id)
    if data in '0123456':
        for i in tegs:
            if teg_name in i:
                if '@' in teg_name and (ivent == 'catalog' or ivent == 'incatalog'):
                    teg.append(i.replace(' ', ''))
                    cat.append(i.split('@')[1].replace(' ', ''))
        teg = ' '.join(teg)
        if '@' in teg_name and ivent == 'catalog':
            query.edit_message_text(text='Подкаталог открыт',
                                    reply_markup=get_keyboard_cat(name_post=cat, chat_id=chat_id, teg=teg,
                                                                  cat='incatalog', a_start=0, a_end=0))
        elif '@' in teg_name and ivent == 'incatalog':
            for i in posts:
                post.append(i[0])
            query.edit_message_text(text='Доступные посты:',
                                    reply_markup=get_keyboard_cat(name_post=post, chat_id=chat_id, teg='&'.join(post),
                                                                  cat='post', a_start=0, a_end=0, full_teg=teg))
        elif '@' not in teg_name and ivent == 'catalog':
            for i in posts:
                post.append(i[0])
            query.edit_message_text(text='Доступные посты',
                                    reply_markup=get_keyboard_cat(name_post=post, chat_id=chat_id, teg='&'.join(post),
                                                                  cat='post', a_start=0, a_end=0))
        elif ivent == 'post':
            url = get_url(name_post=teg_name)[0].replace(' ', '')
            name = get_name_post(name_post=teg_name)
            query.edit_message_text(text=f'{teg_name}\n\n{name[0]}',
                                    parse_mode=ParseMode.HTML,
                                    reply_markup=get_keyboard_cat(cat='post', url=url, chat_id=chat_id))

