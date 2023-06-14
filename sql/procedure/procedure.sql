CREATE OR REPLACE FUNCTION AssignEquipmentToNewStudent()
    RETURNS TRIGGER AS
$$
DECLARE
    v_SkiID character varying;
    v_HelmetID character varying;
    v_PoleID character varying;
BEGIN
    -- Find an available ski for the new student
    SELECT ski_id
    INTO v_SkiID
    FROM ski
    WHERE ski_id NOT IN (SELECT ski_id FROM student WHERE ski_id IS NOT NULL)
    LIMIT 1;

    IF v_SkiID IS NOT NULL THEN
        NEW.ski_id := v_SkiID;
    ELSE
        -- Raise an exception if no available ski is found
        RAISE EXCEPTION 'No available ski found';
    END IF;

    -- Find an available helmet for the new student
    SELECT helmet_id
    INTO v_HelmetID
    FROM helmets
    WHERE helmet_id NOT IN (SELECT helmet_id FROM student WHERE helmet_id IS NOT NULL)
    LIMIT 1;

    IF v_HelmetID IS NOT NULL THEN
        NEW.helmet_id := v_HelmetID;
    ELSE
        -- Raise an exception if no available helmet is found
        RAISE EXCEPTION 'No available helmet found';
    END IF;

    -- Find an available pole for the new student
    SELECT poles_id
    INTO v_PoleID
    FROM poles
    WHERE poles_id NOT IN (SELECT pole_id FROM student WHERE pole_id IS NOT NULL)
    LIMIT 1;

    IF v_PoleID IS NOT NULL THEN
        NEW.pole_id := v_PoleID;
    ELSE
        -- Raise an exception if no available pole is found
        RAISE EXCEPTION 'No available pole found';
    END IF;

    RETURN NEW;
END;
$$
LANGUAGE plpgsql;




-- Erstelle den Trigger
CREATE TRIGGER trg_assign_equipment_to_new_student
    BEFORE INSERT ON student
    FOR EACH ROW
    EXECUTE FUNCTION AssignEquipmentToNewStudent();


--deutsch
-- In dieser gespeicherten Prozedur wird die Funktion AssignEquipmentToNewStudent erstellt, 
-- die als Trigger-Funktion für den Trigger trg_assign_equipment_to_new_student verwendet wird. 
-- Der Trigger wird vor dem Einfügen eines neuen Datensatzes in die STUDENT-Tabelle ausgelöst.

-- -- Die Prozedur sucht nach verfügbarer Ausrüstung, 
-- indem sie die SKI, HELMETS und POLES Tabellen über einen linken Join mit der STUDENT-Tabelle verbindet. 
-- Dabei werden nur die Ausrüstungen ausgewählt, die noch keinem Schüler zugeordnet sind. Der LIMIT 1-Befehl stellt sicher, 
-- dass nur eine verfügbare Ausrüstungseinheit ausgewählt wird.

-- Wenn verfügbare Ausrüstung gefunden wird, wird sie dem neuen Schüler zugewiesen, 
-- indem die entsprechenden Spalten im NEW-Datensatz aktualisiert werden. 
-- Wenn keine verfügbare Ausrüstung gefunden wird, wird eine Ausnahme ausgelöst.

-- Sobald der Trigger und die gespeicherte Prozedur erstellt wurden, wird die Prozedur automatisch ausgelöst, 
-- wenn ein neuer Datensatz in die STUDENT-Tabelle eingefügt wird. 
-- Die verfügbare Ausrüstung wird dem neuen Schüler zugewiesen und in der Tabelle aktualisiert.

--english
-- In this stored procedure, the AssignEquipmentToNewStudent function is created, 
-- which is used as a trigger function for the trg_assign_equipment_to_new_student trigger. 
-- The trigger is fired before inserting a new record into the STUDENT table.

-- The procedure searches for available equipment by connecting the SKI, HELMETS and POLES tables to the STUDENT table via a left join. 
-- Only the equipment that is not yet assigned to a student is selected. 
-- The LIMIT 1 command ensures that only one available equipment unit is selected.

-- If available equipment is found, it is assigned to the new student by updating the appropriate columns in the NEW record. 
-- If no available equipment is found, an exception is raised.

-- Once the trigger and stored procedure are created, 
-- the procedure will automatically fire when a new record is inserted into the STUDENT table. 
-- The available equipment will be assigned to the new student and updated in the table.