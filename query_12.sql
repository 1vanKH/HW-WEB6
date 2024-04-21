SELECT students.name, grades.grade
FROM grades
JOIN subjects ON grades.subject_id = subjects.id
JOIN students ON grades.student_id = students.id
JOIN groups ON students.group_id = groups.id
WHERE subjects.name = 'four' AND groups.name = 'but'
ORDER BY grades.date_received DESC
LIMIT 1;