-- Вместо единиц - инпуты!!!!!!!!!!!!!!!!!!!!!
-- Умная мысль(Можно ввести переменную на функцию, которая получает значения отдельных
-- запросов, и вставляет ео в основной)

-- Запрос Учитель/Предмет/Класс
SELECT tsg_id, subject_id, teacher_id, grade_id 
FROM teachers_subjects_grades tsg 
WHERE subject_id = 1 and teacher_id = 1 and grade_id = INT('INPUT')
GROUP BY tsg_id 
ORDER BY tsg_id;

-- Запрос учителя
SELECT teacher_tg_id, teacher_name, school_name
FROM Teachers
WHERE teacher_name = 'INPUT' and school_name = 'INPUT'
GROUP BY teacher_tg_id
ORDER BY teacher_tg_id;

-- Запрос id предмета
SELECT subject_id, subject_name
FROM Subjects
WHERE subject_name = 'INPUT'
GROUP BY subject_id
ORDER BY subject_id;

-- Запрос Класса(Нет смысла, тк он равен его idшнику)
