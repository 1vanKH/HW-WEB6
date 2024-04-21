SELECT students.name, grades.grade
FROM students
JOIN groups ON students.group_id = groups.id
JOIN grades ON students.id = grades.student_id
JOIN subjects ON grades.subject_id = subjects.id
WHERE groups.name = 'but' AND subjects.name = 'four';