CREATE VIEW v_STUDENT AS
SELECT 
s.Student_id,
s.First_Name,
s.Last_Name,
s.Birthdate,
(CASE WHEN (CURRENT_DATE - s.Birthdate) > 6575 THEN 'Yes' ELSE 'No' END) AS Adult,
(EXTRACT(YEAR FROM CURRENT_DATE) - EXTRACT(YEAR FROM s.Birthdate)) AS Age,
s.Course_type,
s.Experience_level,
s.Phonenumber,
s.Sex,
s.Street,
s.House_num,
s.Post_code,
s.City,
s.Country,
s.Arrival_date,
s.Departure_date,
a.Name,
sk.Brand AS Ski_Brand,
sk.Modell AS Ski_Modell,
sk.Length AS Ski_Length,
h.Brand AS Helmet_brand,
h.Size AS Helmet_size_in_cm,
p.Brand AS Poles_Brand,
p.Length AS Poles_Length_in_cm
FROM STUDENT s
LEFT OUTER JOIN SKI sk ON s.Ski_id = sk.Ski_id
LEFT OUTER JOIN HELMETS h ON s.Helmet_id = h.Helmet_id
LEFT OUTER JOIN POLES p ON s.Pole_id = p.Poles_id
LEFT OUTER JOIN ACCOMODATION a ON s.Accomodation = a.Accomodation_id


CREATE VIEW v_STUDENT_MATERIAL
AS
SELECT
s.student_id
,s.First_Name
,s.Last_Name
,s.Birthdate
,sk.Brand as Ski_Brand
,sk.Modell as Ski_Modell
,sk.Length as Ski_Length
,h.Brand as Helment_brand
,h.Size as Helment_size_in_cm
,p.Brand as Poles_Brand
,p.Length as Poles_Length_in_cm
FROM STUDENT s
LEFT OUTER JOIN SKI sk
    ON s.Ski_id = sk.Ski_id
LEFT OUTER JOIN HELMETS h
    ON s.Helmet_id = h.Helmet_id
LEFT OUTER JOIN POLES p
    ON s.Pole_id = p.Poles_id


CREATE VIEW v_STUDENT_COURSE_EMPLOYEE
AS 
SELECT 
 s.First_Name
,s.Last_Name
,c.Course_id
,c.Course_level
,e.First_Name as Instructor_FirstName
,e.Last_Name as Instructor_LastName
,e.Instructor_level
,e.Job_Title
FROM STUDENT s
LEFT OUTER JOIN COURSE_STUDENT cs
    ON s.Student_id = cs.STUDENT_Student_id
LEFT OUTER JOIN COURSE c
    ON cs.COURSE_Course_id = c.Course_id
LEFT OUTER JOIN EMPLOYEE e
    ON c.Employee_id = e.Employee_id
    

CREATE VIEW v_EMPLOYEE 
AS 
SELECT
 e.Employee_id 
,e.First_Name
,e.Last_Name
,e.Job_title
,e.Salary_group
,s.Salary
,e.Instructor_level
,e.Street
,e.House_num
,e.City
,e.Country
,e.Post_code
,e.Birthdate
,[Age] = YEAR(GETDATE()) - YEAR(s.Birthdate)
,e.Sex
,e.Phonenumber  
FROM EMPLOYEE e
LEFT OUTER JOIN SALARY s
    ON e.Salary_group = s.Salary_group


CREATE MATERIALIZED VIEW v_COURSE_AREA_SHUTTLE
AS
SELECT
 c.Course_id
,c.Course_level
,c.Start_date
,c.End_date
,a.Area_Name
,s.Shuttle_name
,s.Start_location
,s.End_location
,e.First_Name as Skiinstructor_FirstName
,e.Last_Name as Skiinstructor_LastName
FROM COURSE c
LEFT OUTER JOIN AREA a 
    ON c.Area = a.Area_id
LEFT OUTER JOIN SHUTTLE s 
    ON a.Area_id = s.Area_id
LEFT OUTER JOIN EMPLOYEE e 
    ON c.Employee_id = e.Employee_id
