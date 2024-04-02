import psycopg2 as pg

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


#----------------------------------------------------------------
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
    VALUES (%s, %s, %s, '%s', '%s', '%s')''', (teacher_id, subject_id, grade_id, conspect_theme, conspect_date, conspect_text))
    conn.commit()


def insert_teach_sub_gr(teacher_list, subject_list=list(), grade_list=list()):
    for teacher in teacher_list:
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
#----------------------------------------------------------------
details = fetch_data()
for row in details:
    print(row)

d = select_teacher_id('Ольга Владимdировна Чернова', 'МБОУ гимназия Интелект')
print(d)
s = 0
print(select_conspect_with_date(1, 1, 11, '22-10-2019'))

def select_teacher_id_with_tg_id(teacher_name): #Запрос id учителя по имени и школе
    cursor.execute(f'''SELECT EXISTS(SELECT * FROM Teachers WHERE teacher_pass = '{teacher_name}')''')
    
    data = cursor.fetchall()
    if data[0][0]:
        cursor.execute(f'''SELECT teacher_tg_id FROM Teachers WHERE teacher_pass = '{teacher_name}' ''')
        final_id = cursor.fetchall()
        return final_id[0][0]
    else:
        return "Учитель не ведет у вас уроки, возможно вы ошиблись в написании имени учителя, или он не зарегистрирован на платформе!"
    