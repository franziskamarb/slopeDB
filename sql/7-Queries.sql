SQL Query-1:

SELECT e.First_Name, e.Last_Name, s.Salary
FROM EMPLOYEE e
JOIN SALARY s ON e.Salary_group = s.Salary_group
WHERE e.Job_title = 'Manager';

Description: This query retrieves the first name, last name, and salary of all employees who have the job title "Manager". 
It combines information from the EMPLOYEE and SALARY tables using a join operation.

SQL Query-2:

SELECT s.Name, COUNT(*) AS Total_Students
FROM STUDENT s
JOIN COURSE_STUDENT cs ON s.Student_id = cs.STUDENT_Student_id
GROUP BY s.Name;

Description: This query counts the number of students in each course and displays the course name along with the total number of students. 
It joins the STUDENT and COURSE_STUDENT tables and groups the results by course name.

SQL Query 3:

SELECT e.First_Name, e.Last_Name, c.Course_level
FROM EMPLOYEE e
JOIN COURSE c ON e.Employee_id = c.Employee_id
WHERE e.Job_title = 'Instructor';

Description: This query retrieves the first name, last name, and course level of all employees who have the job title "Instructor". 
It combines information from the EMPLOYEE and COURSE tables using a join operation.

SQL Query 4:

SELECT a.Name, COUNT(*) AS Total_Courses
FROM AREA a
JOIN COURSE c ON a.Area_id = c.Area
GROUP BY a.Name;
Description: This query counts the number of courses in each area and displays the area name along with the total number of courses. 
It joins the AREA and COURSE tables and groups the results by area name.

SQL Query 5:

SELECT s.First_Name, s.Last_Name, COUNT(cs.COURSE_Course_id) AS Total_Courses
FROM STUDENT s
LEFT JOIN COURSE_STUDENT cs ON s.Student_id = cs.STUDENT_Student_id
GROUP BY s.First_Name, s.Last_Name
HAVING COUNT(cs.COURSE_Course_id) >= 3;

Description: This query retrieves the first name, last name, and total number of courses for each student who is enrolled in at least 3 courses. 
It combines information from the STUDENT and COURSE_STUDENT tables using a left join operation and groups the results by first name and last name. 
The HAVING clause filters the results to display only students with at least 3 courses.

SQL Query 6:

SELECT e.First_Name, e.Last_Name, AVG(s.Salary) AS Average_Salary
FROM EMPLOYEE e
JOIN SALARY s ON e.Salary_group = s.Salary_group
GROUP BY e.First_Name, e.Last_Name;
Description: This query calculates the average salary for each employee and displays the first name, last name, and average salary. 
It combines information from the EMPLOYEE and SALARY tables using a join operation and groups the results by first name and last name.

SQL Query 7:

SELECT a.Name, COUNT(*) AS Total_Employees
FROM AREA a
JOIN COURSE c ON a.Area_id = c.Area
JOIN EMPLOYEE e ON c.Employee_id = e.Employee_id
WHERE e.Job_title = 'Instructor'
GROUP BY a.Name;
Description: This query counts the number of employees who are instructors in each area and displays the area name along with the total number of employees. 
It joins the AREA, COURSE, and EMPLOYEE tables, filtering for employees with the job title "Instructor". The results are grouped by area name.
