/*Find the areas where the number of courses is greater than the average number of courses across all areas.*/
--This query employs a subquery, a join, and an aggregate function to calculate the average number of courses across all areas 
--and retrieves the areas where the number of courses is higher than the average.

SELECT a.Country, a.Name as Area_Name
FROM AREA a
JOIN COURSE c ON a.Area_id = c.Area
GROUP BY a.Area_id, a.Country, a.City
HAVING COUNT(c.Course_id) > (
    SELECT AVG(Course_Count)
    FROM (
        SELECT COUNT(*) AS Course_Count
        FROM COURSE
        GROUP BY Area
    ) AS avg_courses
);

/* Retrieve the names of employees who have instructed courses in all available areas.*/
--This query utilizes a nested query, a join, and a set operator to find the names of employees who have instructed courses in all 
--available areas by comparing the distinct areas they have instructed with the distinct areas in the AREA table.
--There are no Employees that instruct a course in every area, therefore we get no results through this query

SELECT e.First_Name, e.Last_Name
FROM EMPLOYEE e
JOIN COURSE c ON e.Employee_id = c.Employee_id
GROUP BY e.Employee_id, e.First_Name, e.Last_Name
HAVING COUNT(DISTINCT c.Area) = (
    SELECT COUNT(DISTINCT Area_id)
    FROM AREA
);

/*Retrieve the top three areas with the highest number of enrolled students in courses.*/
--This query involves calculating the 10th percentile of the salaries in the EMPLOYEE table, filtering the employees with salaries 
--in the top 10%, and calculating the average salary of those employees.

SELECT a.Name AS Area_Name, COUNT(cs.STUDENT_Student_id) AS Enrolled_Students
FROM AREA a
JOIN COURSE c ON a.Area_id = c.Area
JOIN COURSE_STUDENT cs ON c.Course_id = cs.COURSE_Course_id
GROUP BY a.Name
ORDER BY Enrolled_Students DESC
LIMIT 3;

/*Retrieve the areas where the average course duration is longer than the overall average course duration across all areas.*/
--This query involves joining the AREA and COURSE tables, calculating the average course duration for each area, comparing it to the
-- overall average course duration, and selecting the areas where the average duration is longer.
SELECT a.Name AS Area_Name, AVG(c.End_date - c.Start_date) AS Average_Course_Duration
FROM AREA a
JOIN COURSE c ON a.Area_id = c.Area
GROUP BY a.Name
HAVING AVG(c.End_date - c.Start_date) > (
    SELECT AVG(End_date - Start_date)
    FROM COURSE
);

/*Find the instructors who have taught courses in consecutive years.*/
--This query requires joining the EMPLOYEE, COURSE, and COURSE_STUDENT tables, grouping by the instructor, checking for consecutive years
--in the courses, and selecting the instructors who have taught courses in consecutive years.
SELECT e.First_Name, e.Last_Name
FROM EMPLOYEE e
JOIN COURSE c1 ON e.Employee_id = c1.Employee_id
JOIN COURSE c2 ON e.Employee_id = c2.Employee_id
WHERE EXTRACT(Year FROM c2.Start_date) = Extract(YEAR FROM c1.Start_date) + 1;


/*Find the area with the most diverse range of difficulty levels in their courses.*/
--This query requires joining the AREA and COURSE tables, grouping by the area, counting the distinct difficulty levels, and selecting the 
--areas with the highest count of distinct difficulty levels.
SELECT a.Name AS Area_Name, COUNT(DISTINCT c.Course_Level) AS Difficulty_Level_Count
FROM AREA a
JOIN COURSE c ON a.Area_id = c.Area
GROUP BY a.Name
ORDER BY Difficulty_Level_Count DESC
LIMIT 1;

/*Find all information about the student who lives in Munich and all information belonging to the student*/
SELECT s.First_Name AS Student_First_Name, s.Last_Name AS Student_Last_Name,
       sk.Modell AS Ski_Modell, sk.Brand AS Ski_Brand,
       h.Brand AS Helmet_Brand, h.Size AS Helmet_Size,
       p.Brand AS Poles_Brand, p.Length AS Poles_Length,
       ar.Name AS Area_Name,
       sh.Shuttle_name,
       c.Course_level, 
       e.First_Name as Instructor_First_Name, e.Last_Name as Instructor_Last_Name,
       c.Start_date as Course_Start_Date, 
       c.End_date as Course_End_date, s.Arrival_Date, s.Departure_Date
FROM STUDENT s
JOIN ACCOMODATION a ON s.accomodation = a.accomodation_id
JOIN SKI sk ON s.Ski_id = sk.Ski_id
JOIN HELMETS h ON s.Helmet_id = h.Helmet_id
JOIN POLES p ON s.Pole_id = p.Poles_id
JOIN COURSE_STUDENT cs ON cs.student_student_id = s.student_id
JOIN COURSE c ON c.course_id = cs.course_course_id
JOIN AREA ar ON c.Area = ar.Area_id
JOIN SHUTTLE sh ON ar.Area_id = sh.Area_id
JOIN EMPLOYEE e ON e.employee_id = c.Employee_id
WHERE s.City = 'Munich'

/*Find the average Salary from every Area*/
--This query requires joining the EMPLOYEE, SALARY COURSE, and AREA tables, grouping by the Area_id, calculating the average salary, 
--and selecting the area_id and their average salary

SELECT a.Area_id, ROUND(AVG(sa.salary), 2) AS average_salary
FROM EMPLOYEE e
JOIN SALARY sa ON e.Salary_Group = sa.Salary_Group
JOIN COURSE c ON e.Employee_id = c.Employee_id
JOIN AREA a ON c.Area = a.Area_id
GROUP BY a.Area_id;

/*Retrieve the names of the students who have rented all available equipment (skis, helmets, and poles).*/
--This query involves joining the STUDENT, SKI, HELMETS, and POLES tables, checking for non-null values in the equipment foreign key columns, and 
--selecting the names of the students who have rented all available equipment.

SELECT s.First_Name, s.Last_Name
FROM STUDENT s
WHERE EXISTS (
    SELECT 1
    FROM SKI sk
    JOIN HELMETS h ON s.Helmet_id = h.Helmet_id
    JOIN POLES p ON s.Pole_id = p.Poles_id
    WHERE s.Ski_id = sk.Ski_id
)
