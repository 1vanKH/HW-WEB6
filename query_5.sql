SELECT subjects.name
FROM subjects
JOIN teachers ON subjects.teacher_id = teachers.id
WHERE teachers.name = 'Justin Hogan';