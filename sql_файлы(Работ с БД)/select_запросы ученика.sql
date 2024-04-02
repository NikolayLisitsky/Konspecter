-- Вместо единиц - инпуты!!!!!!!!!!!!!!!!!!!!!
-- Умная мысль(Можно ввести переменную на функцию, которая получает значения отдельных
-- запросов, и вставляет ео в основной)

-- Запрос конспекта по ученику по теме
SELECT conspect_id, teacher_id, subject_id, grade_id, conspect_theme, conspect_date, conspect_text
FROM Conspects
WHERE teacher_id = 1 and subject_id = 1 and grade_id = 1 and conspect_theme = '1'
GROUP BY conspect_id
ORDER BY conspect_id;

-- Запрос конспекта по ученику по дате
SELECT conspect_id, teacher_id, subject_id, grade_id, conspect_theme, conspect_date, conspect_text
FROM Conspects
WHERE teacher_id = 1 and subject_id = 1 and grade_id = 1 and conspect_date = '1'
GROUP BY conspect_id
ORDER BY conspect_id;

-- Запрос для проверки работают ли добавления
SELECT tsg_id, teacher_id, subject_id, grade_id
FROM Teachers_subjects_grades 
WHERE subject_id = 1 and teacher_id = 1 and grade_id = 1
GROUP BY tsg_id
ORDER BY tsg_id;

-- Запрос id по имени учителя(Убрать teacher_name)
SELECT teacher_tg_id, teacher_name
FROM Teachers
WHERE teacher_name = 'Ольга Владимировна Фигель'

-- Запрос id по названию предмета(Убрать subject_name)
SELECT subject_id, subject_name
FROM Subjects
WHERE subject_name = 'Русский язык'
-- Запрос Класса(Нет смысла, тк он равен его idшнику)