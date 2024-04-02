CREATE TABLE IF NOT EXISTS Grades (
	grade_id SERIAL PRIMARY KEY,
	grade_num INTEGER NOT null);

CREATE TABLE IF NOT EXISTS Subjects (
	subject_id SERIAL PRIMARY KEY,
	subject_name VARCHAR(60) NOT null);

CREATE TABLE IF NOT EXISTS Teachers_subjects_grades (
    tsg_id       SERIAL PRIMARY KEY,
    subject_id INTEGER NOT NULL REFERENCES Subjects(subject_id),
    teacher_id   INTEGER NOT NULL REFERENCES Teachers(teacher_tg_id),
	grade_id   INTEGER NOT NULL REFERENCES Grades(grade_id),
    UNIQUE (subject_id, teacher_id, grade_id)
);

CREATE TABLE IF NOT EXISTS Teachers (
	teacher_tg_id SERIAL PRIMARY KEY,
	teacher_name VARCHAR(60) NOT null,
	teacher_pass VARCHAR(30) NOT NULL,
	school_name VARCHAR(60) NOT null,
	school_city VARCHAR(20) NOT null,
    UNIQUE (teacher_name, teacher_pass, school_name, school_city)
	);

CREATE TABLE IF NOT EXISTS Conspects (
	conspect_id SERIAL PRIMARY KEY,
    subject_id INTEGER NOT NULL REFERENCES Subjects(subject_id),
    teacher_id   INTEGER NOT NULL REFERENCES Teachers(teacher_tg_id),
	grade_id   INTEGER NOT NULL REFERENCES Grades(grade_id),
	conspect_theme VARCHAR,
	conspect_date VARCHAR,
	conspect_text VARCHAR NOT NULL, --Ссылка на изображение
	UNIQUE (conspect_theme, conspect_date, conspect_text)
);