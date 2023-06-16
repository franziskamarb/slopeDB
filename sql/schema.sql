CREATE TABLE SALARY
(
    Salary_group character varying NOT NULL,
    Salary bigint,
    PRIMARY KEY (Salary_group)
);

CREATE TABLE EMPLOYEE
(
    Employee_id character varying NOT NULL,
    First_Name character varying,
    Last_Name character varying,
    Job_title character varying,
    Salary_group character varying,
    Instructor_level character varying,
    Street character varying,
    House_num character varying,
    City character varying,
    Country character varying,
    Post_code character varying,
    Birthdate date,
    Age bigint,
    Sex character varying,
    Phonenumber character varying,
    PRIMARY KEY (Employee_id),
    FOREIGN KEY (Salary_group) REFERENCES SALARY(Salary_group)
);

CREATE TABLE ACCOMODATION
(
    Accomodation_id character varying NOT NULL,
    Name character varying,
    Type character varying,
    Street character varying,
    House_num character varying,
    City character varying,
    Country character varying,
    Post_code character varying,
    PRIMARY KEY (Accomodation_id)
);

CREATE TABLE SKI
(
    Ski_id character varying NOT NULL,
    Modell character varying,
    Brand character varying,
    Length character varying,
    PRIMARY KEY (Ski_id),
    UNIQUE (Ski_id)
);

CREATE TABLE HELMETS
(
    Helmet_id character varying NOT NULL,
    Brand character varying,
    Size character varying,
    PRIMARY KEY (Helmet_id),
    UNIQUE (Helmet_id)
);

CREATE TABLE POLES	
(
    Poles_id character varying NOT NULL,
    Brand character varying,
    Length character varying,
    PRIMARY KEY (Poles_id),
    UNIQUE (Poles_id)
);

CREATE TABLE STUDENT
(
    Student_id character varying NOT NULL,
    First_Name character varying,
    Last_Name character varying,
    Birthdate date,
    Adult boolean,
    Course_type character varying,
    Experience_level character varying,
    Phonenumber character varying,
    Sex character varying,
    Street character varying,
    House_num character varying,
    City character varying,
    Country character varying,
    Post_code bigint,
    Accomodation character varying,
    Ski_id character varying,
    Helmet_id character varying,
    Pole_id character varying,
    Arrival_date date,
    Departure_date date,
    PRIMARY KEY (Student_id),
    UNIQUE (Ski_id),
    UNIQUE (Helmet_id),
    UNIQUE (Pole_id),
    FOREIGN KEY (Accomodation) REFERENCES ACCOMODATION(Accomodation_id),
    FOREIGN KEY (Ski_id) REFERENCES SKI (Ski_id),
    FOREIGN KEY (Helmet_id) REFERENCES HELMETS (Helmet_id),
    FOREIGN KEY (Pole_id) REFERENCES POLES (Poles_id) 
);

CREATE INDEX idx_last_name ON STUDENT (Last_Name);


CREATE TABLE AREA
(
    Area_id character varying NOT NULL,
    Country character varying,
    City character varying,
    Name character varying,
    Difficulty_Level character varying,
    Openting_time time without time zone,
    Closing_time time without time zone,
    Magic_carpet boolean,
    PRIMARY KEY (Area_id)
);

CREATE INDEX idx_name ON AREA (Name);

CREATE TABLE SHUTTLE
(
    Shuttle_name character varying,
    Type character varying,
    Start_location character varying,
    End_location character varying,
    Capacity bigint,
    Area_id character varying,
    FOREIGN KEY (Area_id) REFERENCES AREA (Area_id)
);

CREATE INDEX idx_type ON SHUTTLE (Type);

CREATE TABLE COURSE
(
    Course_id character varying NOT NULL,
    Course_level character varying,
    Start_date date,
    End_date date,
    Area character varying,
    Employee_id character varying,
    PRIMARY KEY (Course_id),
    FOREIGN KEY (Area) REFERENCES AREA(Area_id),
    FOREIGN KEY (Employee_id) REFERENCES EMPLOYEE (Employee_id)
);

CREATE TABLE COURSE_STUDENT
(
    COURSE_Course_id character varying,
    STUDENT_Student_id character varying,
    FOREIGN KEY (COURSE_Course_id) REFERENCES COURSE (Course_id),
    FOREIGN KEY (STUDENT_Student_id) REFERENCES STUDENT (Student_id)
);
