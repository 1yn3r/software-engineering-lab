DROP DATABASE IF EXISTS e_learning;
CREATE DATABASE IF NOT EXISTS e_learning;
USE e_learning;

-- Bảng tài khoản sinh viên
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    fullname VARCHAR(100)
);

CREATE TABLE lectures (
    lecture_id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(20) UNIQUE NOT NULL,
    title VARCHAR(255) NOT NULL
);

-- Bảng lecture mà sinh viên đã có
CREATE TABLE student_lectures (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    lecture_id INT,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (lecture_id) REFERENCES lectures(lecture_id) ON DELETE CASCADE
);

CREATE TABLE questions (
    question_id INT AUTO_INCREMENT PRIMARY KEY,
    lecture_id INT NOT NULL,
    content TEXT NOT NULL,
    answer_a VARCHAR(255),
    answer_b VARCHAR(255),
    answer_c VARCHAR(255),
    answer_d VARCHAR(255),
    correct_answer CHAR(1),
    FOREIGN KEY (lecture_id) REFERENCES lectures(lecture_id) ON DELETE CASCADE
);

INSERT INTO users (username, password, fullname)
VALUES ('sv001', '123456', 'Nguyen Van A');

INSERT INTO lectures (code, title)
VALUES ('LEC101', 'Basic Math and Geography');

INSERT INTO questions (lecture_id, content, answer_a, answer_b, answer_c, answer_d, correct_answer)
VALUES
(1, 'What is 2 + 2?', '3', '4', '5', '6', 'B'),
(1, 'What is the capital of France?', 'Berlin', 'Paris', 'Rome', 'Madrid', 'B');

INSERT INTO lectures (code, title)
VALUES ('LEC200', 'English for Beginners');
INSERT INTO questions (lecture_id, content, answer_a, answer_b, answer_c, answer_d, correct_answer)
VALUES 
(2, 'What is the synonym of "big"?', 'Small', 'Large', 'Tiny', 'Short', 'B'),
(2, 'What is the antonym of "happy"?', 'Joyful', 'Glad', 'Sad', 'Cheerful', 'C');

INSERT INTO lectures (code, title)
VALUES ('LEC300', 'Introduction to Programming');
INSERT INTO questions (lecture_id, content, answer_a, answer_b, answer_c, answer_d, correct_answer)
VALUES 
(3, 'Which language is primarily used for web development?', 'Python', 'Java', 'HTML', 'C++', 'C'),
(3, 'What does "CSS" stand for?', 'Cascading Style Sheets', 'Computer Style Sheets', 'Creative Style System', 'Colorful Style Sheets', 'A');

INSERT INTO student_lectures (user_id, lecture_id)
VALUES (1, 1);