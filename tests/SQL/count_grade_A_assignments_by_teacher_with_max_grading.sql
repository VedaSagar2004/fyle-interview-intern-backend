WITH teacher_with_most_graded_assignments AS (
    SELECT teacher_id, count(*) as graded_assignments 
    FROM assignments
    WHERE grade IS NOT NULL
    GROUP BY teacher_id
    ORDER BY count(*) DESC
    LIMIT 1
)
SELECT COUNT(*) as a_grades
FROM assignments a
JOIN teacher_with_most_graded_assignments t ON a.teacher_id = t.teacher_id
WHERE a.grade = 'A'