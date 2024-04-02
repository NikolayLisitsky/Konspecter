import telebot
from telebot import types
import psycopg2 as pg

#---------------------------------------------------------- Ключ от ТГ бота и переменные
k = 0
bot = telebot.TeleBot('7092776879:AAHO082ySqRKgz_w8Dup904kUZXjsV9ifZU')

# Для Получения конспекта и для добавления конспектоу учителем
tech = 0 #Учитель
grd = 0 #Класс
subj = 0 #Предмет
shkola = '' #Школа
dat = '' #Дата
tema = '' #Тема
photki = [] #Фотки
final_photo = 0
col_vo_photo = 0
last_message = 0

# Для регистрации учителя
uchitel_name = ''
uchitel_city = ''
uchitel_school = ''
uchitel_grades = []
uchitel_subjects = []


#---------------------------------------------------------- Проверка подключения к БД
try:
    conn = pg.connect(
        host='localhost',
        database='postgres',
        port=5432,
        user='postgres',
        password='C0ck1ya'
    )
 
    cursor = conn.cursor()
    print("Connection established.")
 
except Exception as err:
    print("Something went wrong.")
    print(err)

#---------------------------------------------------------------- Работа с БД
def fetch_data(): #Запрос инфы к БД (базовый запросик)
    cursor.execute('''SELECT teacher_tg_id, teacher_name, school_name
FROM Teachers''')
    data = cursor.fetchall()
    return data


def select_teacher_id(teacher_name, school_name): #Запрос id учителя по имени и школе
    cursor.execute(f'''SELECT EXISTS(SELECT * FROM Teachers WHERE teacher_name = '{teacher_name}' and school_name = '{school_name}')''')
    
    data = cursor.fetchall()
    if data[0][0]:
        cursor.execute(f'''SELECT teacher_tg_id FROM Teachers WHERE teacher_name = '{teacher_name}' and school_name = '{school_name}' ''')
        final_id = cursor.fetchall()
        return final_id[0][0]
    else:
        return "Учитель не ведет у вас уроки, возможно вы ошиблись в написании имени учителя, или он не зарегистрирован на платформе!"

def select_teacher_id_with_tg_id(teacher_name): #Запрос id учителя по tg_id
    cursor.execute(f'''SELECT EXISTS(SELECT * FROM Teachers WHERE teacher_pass = '{teacher_name}')''')
    
    data = cursor.fetchall()
    if data[0][0]:
        cursor.execute(f'''SELECT teacher_tg_id FROM Teachers WHERE teacher_pass = '{teacher_name}' ''')
        final_id = cursor.fetchall()
        return final_id[0][0]
    else:
        return "Учитель не ведет у вас уроки, возможно вы ошиблись в написании имени учителя, или он не зарегистрирован на платформе!"


def select_subject_id(input_subject): #Запрос id предмета
    cursor.execute(f'''SELECT EXISTS(SELECT * FROM Subjects WHERE subject_name = '{input_subject}')''')
    data = cursor.fetchall()
    if data[0][0]:
        cursor.execute(f'''SELECT subject_id
FROM Subjects
WHERE subject_name = '{input_subject}' ''')
        final_id = cursor.fetchall()
        return final_id[0][0]
    else:
        return "Предмет не найден, возможно вы ошиблись в написании предмета!"


def select_conspect_with_theme(teacher_id, subject_id, grade_id, conspect_theme): #Запрос конспекта по теме
    cursor.execute(f'''SELECT conspect_id, teacher_id, subject_id, grade_id, conspect_theme, conspect_date, conspect_text
FROM Conspects
WHERE teacher_id = {teacher_id} and subject_id = {subject_id} and grade_id = {grade_id} and conspect_theme = '{conspect_theme}'
GROUP BY conspect_id
ORDER BY conspect_id;''')
    data = cursor.fetchall()
    return data


def select_conspect_with_date(teacher_id, subject_id, grade_id, conspect_date): #Запрос конспекта по дате
    cursor.execute(f'''SELECT conspect_id, teacher_id, subject_id, grade_id, conspect_theme, conspect_date, conspect_text
FROM Conspects
WHERE teacher_id = {teacher_id} and subject_id = {subject_id} and grade_id = {grade_id} and conspect_date = '{conspect_date}'
GROUP BY conspect_id
ORDER BY conspect_id;''')
    data = cursor.fetchall()
    return data


def F(teacher, subject, grade):
    cursor.execute(f'''SELECT EXISTS(SELECT * FROM Teachers_subjects_grades WHERE teacher_id = '{teacher}' and subject_id = '{subject}' and grade_id = '{grade}')''')
    thruth_result = cursor.fetchall()[0][0]
    return thruth_result

#----------------------------------------------------------------

def create_entry(): #Добавление данных в БД
    cursor.execute('''INSERT INTO Teachers (teacher_name, teacher_pass, school_name, school_city)
                    VALUES (%s, %s, %s, %s)''', ('Имя учителя', 'tg_id', 'Школа', 'Город'))
    conn.commit()


def insert_teachers(teacher_name, teacher_pass, school_name, school_city): #Добавление данных в БД
    cursor.execute('''INSERT INTO Teachers (teacher_name, teacher_pass, school_name, school_city)
                    VALUES (%s, %s, %s, %s)''', (teacher_name, teacher_pass, school_name, school_city))
    conn.commit()


def insert_subject(input_sub):
    cursor.execute(f'''INSERT INTO Subjects(subject_name)
    VALUES ({input_sub})''')
    conn.commit()


def insert_conspects(teacher_id, subject_id, grade_id, conspect_theme, conspect_date, conspect_text):
    cursor.execute('''INSERT INTO Conspects(teacher_id, subject_id, grade_id, conspect_theme, conspect_date, conspect_text)
    VALUES (%s, %s, %s, %s, %s, %s)''', (teacher_id, subject_id, grade_id, conspect_theme, conspect_date, conspect_text))
    conn.commit()


def insert_teach_sub_gr(teacher, subject_list=list(), grade_list=list()):
    for subject in subject_list:
        for grade in grade_list:
            cursor.execute(f'''SELECT EXISTS(SELECT * FROM Teachers_subjects_grades WHERE teacher_id = '{teacher}' and subject_id = '{subject}' and grade_id = '{grade}')''')
            thruth = cursor.fetchall()[0][0]
            if thruth == False: 
                cursor.execute('''INSERT INTO Teachers_subjects_grades (teacher_id, subject_id, grade_id)
                VALUES (%s, %s, %s)''', (teacher, subject, grade))
                conn.commit()
            else:
                continue
    return 'DB updated'
#---------------------------------------------------------- 


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    bot.send_message(message.chat.id, f'{user_id}')

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Посмотреть конспект")
    btn2 = types.KeyboardButton("Добавить конспект")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, text="Привет, {0.first_name}! Я Конспектер, твой помощник!".format(message.from_user), reply_markup=markup)



@bot.message_handler(content_types=['photo'])

def photo(message):
    global final_photo
    print('message.photo =', message.photo)
    fileID = message.photo[-1].file_id
    print('fileID =', fileID)
    file_info = bot.get_file(fileID)
    print('file.file_path =', file_info.file_path)
    downloaded_file = bot.download_file(file_info.file_path)
    final_photo += 1
    if col_vo_photo != final_photo:
        with open(f"Фото\{fileID}.jpg", 'wb') as new_file:
            photki.append(f"Фото\{fileID}.jpg")
            new_file.write(downloaded_file)
    else:
        with open(f"Фото\{fileID}.jpg", 'wb') as new_file:
            photki.append(f"Фото\{fileID}.jpg")
            new_file.write(downloaded_file)
        final_photo = 0
        bot.register_next_step_handler(message, add_conspect_to_db)

@bot.message_handler(content_types=['text'])
def func(message):
    if message.text == 'Посмотреть конспект':
        bot.send_message(message.chat.id, text="Введите свою школу:")
        bot.register_next_step_handler(message, get_info_first)
    elif message.text == 'Добавить конспект':
        if check_registration(message):
            bot.send_message(message.chat.id, text="Введите предмет:") #Переменная будет в след функции
            bot.register_next_step_handler(message, add_conspect_first)



#------------------------------------------------------------------- Регистрация
def check_registration(message):
    cursor.execute(f'''SELECT EXISTS(SELECT * FROM Teachers WHERE teacher_pass = '{message.chat.id}')''')
    data = cursor.fetchall()
    if data[0][0]:
        return True
    else:
        bot.send_message(message.chat.id, text="Вы не зарегистрированы! Введите полное ФИО:")
        bot.register_next_step_handler(message, registration_1)
        pass

def registration_1(message):
    global uchitel_name
    uchitel_name = message.text

    bot.send_message(message.chat.id, text="Введите вашу школу:")
    bot.register_next_step_handler(message, registration_2)

def registration_2(message):
    global uchitel_school
    uchitel_school = message.text
    
    bot.send_message(message.chat.id, text="Введите ваш город:")
    bot.register_next_step_handler(message, registration_3)

def registration_3(message):
    global uchitel_city
    uchitel_city = message.text

    bot.send_message(message.chat.id, text="Введите предметы, которые будете преподавать (Через запятую, с большой буквы каждый предмет):")
    bot.register_next_step_handler(message, registration_4)

def registration_4(message):
    global uchitel_subjects
    for i in message.text.split(', '): 
        uchitel_subjects.append(int(select_subject_id(i)))
    
    bot.send_message(message.chat.id, text="Введите классы, в которых будете преподавать, через пробел.(1 2 11):")
    bot.register_next_step_handler(message, registration_5)

def registration_5(message):
    global uchitel_name
    global uchitel_city
    global uchitel_school
    global uchitel_grades
    global uchitel_subjects
    print(message.text.split(' '))
    for i in message.text.split(' '):
        uchitel_grades.append(int(i))
    print(uchitel_name, uchitel_school, uchitel_city, uchitel_subjects, uchitel_grades, sep=' | ')
    action_1 = insert_teachers(uchitel_name, str(message.chat.id), uchitel_school, uchitel_city)
    tch_id = select_teacher_id(uchitel_name, uchitel_school)
    
    action_2 = insert_teach_sub_gr(tch_id, uchitel_grades, uchitel_subjects)
    print(action_1, action_2)

    uchitel_name = ''
    uchitel_city = ''
    uchitel_school = ''
    uchitel_grades = []
    uchitel_subjects = []

    bot.send_message(message.chat.id, text="Вы успешно зарегистрированы!")
    



    
#-------------------------------------------------------------- Запрос конспекта
def get_info_first(message):

    global shkola
    shkola = message.text
    print(shkola)

    bot.send_message(message.chat.id, text="Введите свой класс:")
    bot.register_next_step_handler(message, get_info_second)
    
def get_info_second(message):

    global grd
    grd = message.text
    print(grd)

    bot.send_message(message.chat.id, text="Введите предмет:")
    bot.register_next_step_handler(message, get_info_third)

def get_info_third(message):

    global subj
    subj = message.text
    print(subj)

    bot.send_message(message.chat.id, text="Введите имя учителя:")
    bot.register_next_step_handler(message, get_info_forth)

def get_info_forth(message):

    global tech
    tech = message.text
    print(tech)

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Дате', callback_data='data'))
    markup.add(types.InlineKeyboardButton('Теме', callback_data='theme'))
    bot.reply_to(message, "Искать по:", reply_markup = markup)

def data_info(message):
    global subj
    global grd
    global dat
    global tema
    global tech
    global shkola

    dat = message.text
    value_1 = select_teacher_id(tech, shkola)
    value_2 = select_subject_id(subj)
    if value_1 != 'Учитель не ведет у вас уроки, возможно вы ошиблись в написании имени учителя, или он не зарегистрирован на платформе!' and value_2 != "Предмет не найден, возможно вы ошиблись в написании предмета!":
        ans = select_conspect_with_date(value_1, value_2, grd, dat)
        if len(ans)!= 0:
            new_lst = ans[-1][-1].split(', ')
            for i in new_lst:
                sti = open(i, 'rb')
                print(sti)
                bot.send_photo(message.chat.id, sti)
        else:
            bot.send_message(message.chat.id, f'Конспект по данной теме не найден!')
        tech = 0
        grd = 0
        subj = 0
        shkola = ''
        dat = ''
        tema = ''
        pass
    else:
        if value_1 == 'Учитель не ведет у вас уроки, возможно вы ошиблись в написании имени учителя, или он не зарегистрирован на платформе!':
            bot.send_message(message.chat.id, 'Вы ошиблись в написании имени учителя или он не ведет у вашего класса уроки!')
            bot.register_next_step_handler(message, start)
        elif value_2 != "Предмет не найден, возможно вы ошиблись в написании предмета!":
            bot.send_message(message.chat.id, 'Конспект не найден, возможно вы ошиблись в написании предмета!')
            bot.register_next_step_handler(message, start)

def theme_info(message):
    global subj
    global grd
    global dat
    global tema
    global tech
    global shkola

    tema = message.text
    value_1 = select_teacher_id(tech, shkola)
    value_2 = select_subject_id(subj)
    if value_1 != 'Учитель не ведет у вас уроки, возможно вы ошиблись в написании имени учителя, или он не зарегистрирован на платформе!' and value_2 != "Предмет не найден, возможно вы ошиблись в написании предмета!":
        ans = select_conspect_with_theme(value_1, value_2, grd, tema)
        if len(ans)!= 0:
            new_lst = ans[-1][-1].split(', ')
            for i in new_lst:
                sti = open(i, 'rb')
                print(sti)
                bot.send_photo(message.chat.id, sti)
        else:
            bot.send_message(message.chat.id, f'Конспект по данной теме не найден!')
        tech = 0
        grd = 0
        subj = 0
        shkola = ''
        dat = ''
        tema = ''
        pass
    else:
        if value_1 == 'Учитель не ведет у вас уроки, возможно вы ошиблись в написании имени учителя, или он не зарегистрирован на платформе!':
            bot.send_message(message.chat.id, 'Вы ошиблись в написании имени учителя, или он не ведет у вашего класса уроки!')
            bot.register_next_step_handler(message, start)
        elif value_2 != "Предмет не найден, возможно вы ошиблись в написании предмета!":
            bot.send_message(message.chat.id, 'Конспект не найден, возможно вы ошиблись в написании предмета!')
            bot.register_next_step_handler(message, start)

def review(message): # Пример сохранения текста в переменную
    ms_to_save = message.text
    print(ms_to_save)


#------------------------------------------------------------------- Добавление конспекта
def add_conspect_first(message):
    bot.send_message(message.chat.id, text="Введите класс(только цифру):")

    global subj
    subj = select_subject_id(message.text)
    print(subj)

    bot.register_next_step_handler(message, add_conspect_second)

def add_conspect_second(message):
    bot.send_message(message.chat.id, text="Введите тему конспекта:")

    global grd
    grd = int(message.text)
    print(grd)
    
    bot.register_next_step_handler(message, add_conspect_third)

def add_conspect_third(message):
    bot.send_message(message.chat.id, text="Введите сегодняшнюю дату в формате DD.MM.YYYY:")

    global tema
    tema = message.text
    print(tema)
    
    bot.register_next_step_handler(message, add_conspect_forth)

def add_conspect_forth(message):
    bot.send_message(message.chat.id, text="Сколько фото вы будете добавлять? Введите цифру:")

    global dat
    dat = message.text
    print(dat)
    # last_message = message.id Надо будет подумать над этим вариантом
    bot.register_next_step_handler(message, add_conspect_5)

def add_conspect_5(message):
    bot.send_message(message.chat.id, text="Пришлите фото(ки) конспекта и когда закончите, напишите любое сообщение(Я доработаю, но пока так):")

    global col_vo_photo
    col_vo_photo = int(message.text)
    print(col_vo_photo)
    # last_message = message.id Надо будет подумать над этим вариантом
    # bot.register_next_step_handler(message, add_conspect_to_db)

def add_conspect_to_db(message):
    global subj
    global grd
    global dat
    global tema
    global tech
    global shkola
    global photki

    tch_id = select_teacher_id_with_tg_id(str(message.chat.id))
    print(tch_id, subj, grd, tema, dat, ', '.join(photki))
    action_1 = insert_conspects(tch_id, subj, grd, tema, dat, ', '.join(photki))
    print(action_1)

    bot.send_message(message.chat.id, 'Конспект добавлен!')
    tech = 0 
    grd = 0 
    subj = 0 
    shkola = ''
    dat = '' 
    tema = ''
    photki = []



@bot.callback_query_handler(func=lambda callback: True)

def ans(callback):
    cid = callback.message.chat.id
    keyboard = types.InlineKeyboardMarkup()
    if callback.data == "data":
        bot.send_message(cid, "Введите дату конспекта", reply_markup=keyboard)
        cid_2 = callback.message
        bot.register_next_step_handler(cid_2, data_info)
    elif callback.data == "theme":
        bot.send_message(cid, "Введите тему конспекта", reply_markup=keyboard)
        cid_2 = callback.message
        bot.register_next_step_handler(cid_2, theme_info)


bot.infinity_polling()