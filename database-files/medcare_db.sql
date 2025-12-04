DROP DATABASE IF EXISTS mediVerse;
CREATE DATABASE IF NOT EXISTS mediVerse;

USE mediVerse;

# ---------------------------------------------------------------------- #
# Tables                                                                 #
# ---------------------------------------------------------------------- #

CREATE TABLE IF NOT EXISTS Staff (
   staffId INT AUTO_INCREMENT PRIMARY KEY,
   name VARCHAR(255) NOT NULL,
   email VARCHAR(255) NOT NULL,
   status VARCHAR(255) NOT NULL
);
CREATE TABLE IF NOT EXISTS Patient (
   patientId INT AUTO_INCREMENT PRIMARY KEY,
   name VARCHAR(255) NOT NULL,
   gender VARCHAR(20) NOT NULL,
   DOB DATE NOT NULL,
   status VARCHAR(20) NOT NULL
);
CREATE TABLE IF NOT EXISTS Tasks (
   taskId INT AUTO_INCREMENT PRIMARY KEY,
   type VARCHAR(255) NOT NULL,
   status ENUM('pending', 'in_progress', 'completed') DEFAULT 'pending',
   dueDate DATE,
   staffId INT,
   CONSTRAINT FK_Tasks_Staff FOREIGN KEY (staffId) REFERENCES Staff (staffId)
);
CREATE TABLE IF NOT EXISTS Appointment (
   appointmentId INT AUTO_INCREMENT PRIMARY KEY,
   dateTime DATETIME NOT NULL,
   reason VARCHAR(255) NOT NULL,
   status ENUM('scheduled', 'completed') DEFAULT 'scheduled',
   staffId INT,
   patientId INT,
   CONSTRAINT FK_Appointment_Staff FOREIGN KEY (staffId) REFERENCES Staff (staffId),
   CONSTRAINT FK_Appointment_Patient FOREIGN KEY (patientId) REFERENCES Patient (patientId)
);
CREATE TABLE IF NOT EXISTS CarePlan (
   carePlanId INT AUTO_INCREMENT PRIMARY KEY,
   goals VARCHAR(255) NOT NULL,
   startTime DATETIME NOT NULL,
   endTime DATETIME,
   staffId INT,
   patientId INT,
   CONSTRAINT FK_CarePlan_Staff FOREIGN KEY (staffId) REFERENCES Staff (staffId),
   CONSTRAINT FK_CarePlan_Patient FOREIGN KEY (patientId) REFERENCES Patient (patientId)
);
CREATE TABLE IF NOT EXISTS AuditLog (
   logId INT AUTO_INCREMENT PRIMARY KEY,
   timeStamp DATETIME NOT NULL,
   action VARCHAR(255) NOT NULL,
   outcome VARCHAR(255),
   staffId INT,
   CONSTRAINT FK_AuditLog_Staff FOREIGN KEY (staffId) REFERENCES Staff (staffId)
);
CREATE TABLE IF NOT EXISTS Vitals (
   vitalsId INT NOT NULL AUTO_INCREMENT,
   type VARCHAR(255) NOT NULL,
   value INT,
   timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
   patientId INT,
   PRIMARY KEY (vitalsId, patientId),
   CONSTRAINT FK_Vitals_Patient FOREIGN KEY (patientId) REFERENCES Patient(patientId)
);
CREATE TABLE IF NOT EXISTS Conditions (
   conditionsId INT AUTO_INCREMENT PRIMARY KEY,
   conditionName VARCHAR(255) NOT NULL,
   dateDiagnosed DATETIME NOT NULL,
   notes TEXT,
   patientId INT,
   CONSTRAINT FK_Conditions_Patient FOREIGN KEY (patientId) REFERENCES Patient (patientId)
);


CREATE TABLE IF NOT EXISTS LabResult (
   labResultId INT AUTO_INCREMENT PRIMARY KEY,
   labType VARCHAR(255) NOT NULL,
   value VARCHAR(255) NOT NULL,
   date DATETIME NOT NULL,
   isModified BOOLEAN NOT NULL DEFAULT FALSE,
   isOutlier BOOLEAN NOT NULL DEFAULT FALSE,
   patientId INT NOT NULL,
   CONSTRAINT FK_LR_Patient FOREIGN KEY (patientId) REFERENCES Patient(patientId)
);


CREATE TABLE IF NOT EXISTS DataRequest (
   requestId INT AUTO_INCREMENT PRIMARY KEY,
   title VARCHAR(255) NOT NULL,
   description VARCHAR(255) NOT NULL,
   status VARCHAR(255) NOT NULL,
   dateCreated DATETIME NOT NULL,
   staffId INT,
   CONSTRAINT FK_DataRequest_Staff FOREIGN KEY (staffId) REFERENCES Staff(staffId)
);
CREATE TABLE IF NOT EXISTS Project (
   projectId INT AUTO_INCREMENT PRIMARY KEY,
   name VARCHAR(255) NOT NULL,
   startDate DATETIME NOT NULL,
   endDate DATETIME NOT NULL,
   requestId INT,
   CONSTRAINT FK_Project_DataRequest FOREIGN KEY (requestId) REFERENCES DataRequest(requestId)
);
CREATE TABLE IF NOT EXISTS Visualization (
   visualizationId INT AUTO_INCREMENT PRIMARY KEY,
   type VARCHAR(255) NOT NULL,
   dateCreated DATETIME NOT NULL,
   summary VARCHAR(255) NOT NULL,
   projectId INT,
   CONSTRAINT FK_Visualization_Project FOREIGN KEY (projectId) REFERENCES Project(projectId)
);
CREATE TABLE IF NOT EXISTS Permission (
   permissionId INT PRIMARY KEY,
   action VARCHAR(255) NOT NULL,
   resource VARCHAR(255) NOT NULL
);
CREATE TABLE IF NOT EXISTS Role (
   roleId INT PRIMARY KEY,
   name VARCHAR(255) NOT NULL,
   description VARCHAR(255) NOT NULL,
   permissionId INT,
   CONSTRAINT FK_Role_Permission FOREIGN KEY (permissionId) REFERENCES Permission(permissionId)
);
CREATE TABLE IF NOT EXISTS Department (
   departmentId INT PRIMARY KEY,
   location VARCHAR(255) NOT NULL,
   name VARCHAR(255) NOT NULL
);
CREATE TABLE IF NOT EXISTS Integration (
   integrationId INT AUTO_INCREMENT PRIMARY KEY,
   systemName VARCHAR(255) NOT NULL,
   status VARCHAR(255) NOT NULL,
   lastSyncDate DATETIME NOT NULL,
   departmentId INT,
   CONSTRAINT FK_Integration_Department FOREIGN KEY (departmentId) REFERENCES Department(departmentId)
);
CREATE TABLE IF NOT EXISTS SystemAlert (
   alertId INT AUTO_INCREMENT PRIMARY KEY,
   type VARCHAR(255) NOT NULL,
   severity VARCHAR(255) NOT NULL,
   message VARCHAR(255),
   timestamp DATETIME NOT NULL,
   departmentId INT,
   permissionId INT,
   CONSTRAINT FK_SystemAlert_Department FOREIGN KEY (departmentId) REFERENCES Department(departmentId),
   CONSTRAINT FK_SystemAlert_Permission FOREIGN KEY (permissionId) REFERENCES Permission(permissionId)
);
CREATE TABLE IF NOT EXISTS Project_Patient (
   projectId INT,
   patientId INT,
   CONSTRAINT FK_PP_Project FOREIGN KEY (projectId) REFERENCES Project(projectId),
   CONSTRAINT FK_PP_Patient FOREIGN KEY (patientId) REFERENCES Patient(patientId)
);
CREATE TABLE IF NOT EXISTS Treatment (
   treatmentId INT,
   type VARCHAR(255) NOT NULL,
   name VARCHAR(255) NOT NULL,
   dosage VARCHAR(255) NOT NULL,
   frequency VARCHAR(255) NOT NULL,
   startdate DATETIME NOT NULL,
   endDate DATETIME NOT NULL,
   patientId INT,
   PRIMARY KEY (treatmentId, patientId)
);
CREATE TABLE IF NOT EXISTS Project_Treatment (
   projectId INT,
   treatmentId INT,
   patientId INT,
   PRIMARY KEY (projectId, treatmentId, patientId),
   CONSTRAINT FK_PT_Project FOREIGN KEY (projectId) REFERENCES Project(projectId),
   CONSTRAINT FK_PT_Treatment FOREIGN KEY (treatmentId, patientId) REFERENCES Treatment(treatmentId, patientId),
      CONSTRAINT FK_PT_Patient FOREIGN KEY (patientId) REFERENCES Patient(patientId)
);
CREATE TABLE IF NOT EXISTS Staff_Role (
   staffId INT,
   roleId INT,
   PRIMARY KEY (staffId, roleId),
   CONSTRAINT FK_SR_Staff FOREIGN KEY (staffId) REFERENCES Staff(staffId),
   CONSTRAINT FK_SR_Role FOREIGN KEY (roleId) REFERENCES Role(roleId)
);
CREATE TABLE IF NOT EXISTS Project_Condition (
   projectId INT NOT NULL,
   conditionsId INT NOT NULL,
   patientId INT NOT NULL,
   PRIMARY KEY (projectId, conditionsId),
   CONSTRAINT FK_PC_Project FOREIGN KEY (projectId) REFERENCES Project(projectId),
   CONSTRAINT FK_PC_C FOREIGN KEY (conditionsId) REFERENCES Conditions(conditionsId),
   CONSTRAINT FK_PC_CP FOREIGN KEY (patientId) REFERENCES Patient(patientId)
);
CREATE TABLE IF NOT EXISTS Project_Vitals (
   projectId INT NOT NULL,
   vitalsId INT NOT NULL,
   patientId INT NOT NULL,
   PRIMARY KEY (projectId, vitalsId),
   CONSTRAINT FK_PV_Project FOREIGN KEY (projectId) REFERENCES Project(projectId),
   CONSTRAINT FK_PV_Vitals FOREIGN KEY (vitalsId, patientId) REFERENCES Vitals(vitalsId, patientId),
   CONSTRAINT FK_PV_V FOREIGN KEY (patientId) REFERENCES Patient(patientId)
);
CREATE TABLE Project_Labs (
   projectId INT NOT NULL,
   labResultId INT NOT NULL,
   patientId INT NOT NULL,
   PRIMARY KEY (projectId, labResultId),
   CONSTRAINT FK_PL_Project FOREIGN KEY (projectId) REFERENCES Project(projectId),
   CONSTRAINT FK_PL_LabResult FOREIGN KEY (labResultId)REFERENCES LabResult(labResultId),
   CONSTRAINT FK_PL_Patient FOREIGN KEY (patientId)  REFERENCES Patient(patientId)
);

# ---------------------------------------------------------------------- #
# Data                                                                   #
# ---------------------------------------------------------------------- #

INSERT INTO Staff (name, email, status) VALUES
('Orelia Streeten', 'ostreeten0@mediverse.com', 'inactive'),
('Kerk Khalid', 'kkhalid1@mediverse.com', 'active'),
('Rorie Denisevich', 'rdenisevich2@amazon.co.jp', 'inactive'),
('Fiona Runciman', 'frunciman3@mediverse.com', 'active'),
('Fancie Seeman', 'fseeman4@mediverse.com', 'inactive'),
('Donna Tassel', 'dtassel5@mediverse.com', 'inactive'),
('Norina Tather', 'ntather6@mediverse.com', 'inactive'),
('Correy Dowtry', 'cdowtry7@mediverse.com', 'active'),
('Sibylla Trewman', 'strewman8@mediverse.com', 'inactive'),
('Dareen Nardrup', 'dnardrup9@mediverse.com', 'inactive'),
('Alidia Dowle', 'adowlea@mediverse.com', 'active'),
('Betsey Brechin', 'bbrechinb@mediverse.com', 'inactive'),
('Emelina Lenglet', 'elengletc@mediverse.com', 'active'),
('Bee Whyard', 'bwhyardd@mediverse.com', 'inactive'),
('Jacques Labbet', 'jlabbete@mediverse.com', 'active'),
('Petronille Yarker', 'pyarkerf@mediverse.com', 'inactive'),
('Mallory Gaines', 'mgainesg@mediverse.com', 'inactive'),
('Cletus Northwood', 'cnorthwoodh@mediverse.com', 'inactive'),
('Nedi Geldert', 'ngelderti@mediverse.com', 'active'),
('Sigrid Brockbank', 'sbrockbankj@mediverse.com', 'active'),
('Judye Milam', 'jmilamk@mediverse.com', 'active'),
('Ursulina Poad', 'upoadl@mediverse.com', 'active'),
('Linnea Barwack', 'lbarwackm@mediverse.com', 'active'),
('Lockwood Spirit', 'lspiritn@mediverse.com', 'active'),
('Zebulon Simonson', 'zsimonsono@mediverse.com', 'active'),
('Tana Toffts', 'ttofftsp@mediverse.com', 'active'),
('Claribel Botwood', 'cbotwoodq@mediverse.com', 'inactive'),
('Pearla Albertson', 'palbertsonr@mediverse.com', 'active'),
('Oralie Adkins', 'oadkinss@mediverse.com', 'inactive'),
('Rodger Baud', 'rbaudt@mediverse.com', 'active'),
('Druci Beeken', 'dbeekenu@mediverse.com', 'active'),
('Inglebert Kordes', 'ikordesv@mediverse.com', 'active'),
('Gerrie Wyndham', 'gwyndhamw@mediverse.com', 'active'),
('Lane MacDonough', 'lmacdonoughx@mediverse.com', 'active'),
('Cybil Atte-Stone', 'cattestoney@mediverse.com', 'inactive'),
('Zachary Jeratt', 'zjerattz@mediverse.com', 'active'),
('Ambur Peeter', 'apeeter10@mediverse.com', 'inactive'),
('Maureen Hovert', 'mhovert11@mediverse.com', 'active'),
('Arlee Kembrey', 'akembrey12@mediverse.com', 'inactive'),
('Alika Lacrouts', 'alacrouts13@mediverse.com', 'active');

INSERT INTO Patient (name, gender, DOB, status) VALUES
('Udale Tather', 'male', '2017-02-08', 'active'),
('Clemmie Evitt', 'female', '1959-04-25', 'active'),
('Abigail Jarred', 'female', '1963-05-26', 'inactive'),
('Noel Gerbel', 'male', '1997-08-06', 'active'),
('Mariam Kilmister', 'female', '1941-06-30', 'inactive'),
('Jerrie De Angelo', 'female', '1961-06-01', 'active'),
('Manda Grimbleby', 'female', '2023-08-25', 'active'),
('Griffy Stot', 'male', '1951-06-11', 'inactive'),
('Clayborn Slessar', 'male', '2017-11-12', 'active'),
('Clarissa Bewsey', 'female', '2009-06-10', 'inactive'),
('Reinhard Matussov', 'male', '1950-09-11', 'active'),
('Sarena Girvin', 'female', '1954-07-21', 'active'),
('Fidelia Galvin', 'female', '1977-09-09', 'inactive'),
('Burt Backshill', 'male', '1942-05-14', 'inactive'),
('Orsola Happs', 'female', '1992-08-01', 'active'),
('Aldin Walliker', 'male', '1991-03-17', 'active'),
('Tine Hounsom', 'female', '1993-10-26', 'inactive'),
('Ave Wyburn', 'female', '2022-11-01', 'active'),
('Kin Sansum', 'male', '1960-05-13', 'inactive'),
('Egon Ricson', 'male', '1950-04-20', 'active'),
('Dot O''Hogertie', 'female', '2009-04-26', 'inactive'),
('Shellie Chominski', 'female', '1994-09-07', 'inactive'),
('Judi Kenn', 'female', '1964-05-26', 'inactive'),
('Lana Iacovides', 'female', '1943-06-26', 'inactive'),
('Dalila Simpkiss', 'female', '1971-08-12', 'active'),
('Mendel Jean', 'male', '1931-11-28', 'inactive'),
('Brigida Heliot', 'female', '2005-12-05', 'inactive'),
('Chlo Gillbey', 'female', '1995-10-17', 'active'),
('Ferris Bircher', 'male', '1957-01-17', 'inactive'),
('Dori Nowakowski', 'female', '2009-12-11', 'active'),
('Rasla Penquet', 'female', '1998-01-11', 'inactive'),
('Gualterio Averay', 'male', '1948-11-27', 'inactive'),
('Bail Jeffress', 'male', '2022-01-05', 'inactive'),
('Phillipe Hirschmann', 'male', '1960-04-29', 'inactive'),
('Ceciley Humbee', 'female', '1948-02-26', 'active'),
('Ranice Kinig', 'female', '1937-01-25', 'active'),
('Nadean Coop', 'female', '1937-11-30', 'active'),
('Linnea Stockell', 'female', '1939-07-28', 'active'),
('Deanna Valdes', 'female', '2004-10-16', 'active'),
('Jarret Rosenstock', 'male', '2022-07-12', 'active');

INSERT INTO Tasks (type, status, dueDate, staffId) VALUES
('Prepare Lab Sample', 'in_progress', '2025-12-14', 1),
('Contact Pharmacy', 'completed', '2026-03-14', 2),
('Update Patient Chart', 'completed', '2026-08-27', 3),
('Prepare Lab Sample', 'pending', '2026-03-09', 4),
('Remove Stitches', 'in_progress', '2026-06-03', 5),
('Contact Pharmacy', 'completed', '2026-12-01', 6),
('Administer IV Fluids', 'completed', '2025-12-29', 7),
('Update Patient Chart', 'pending', '2026-03-02', 8),
('Coordinate Specialist Referral', 'completed', '2026-10-29', 9),
('Update Medication List', 'in_progress', '2026-08-18', 10),
('Administer Medication', 'completed', '2026-03-30', 11),
('Prepare Lab Sample', 'pending', '2026-03-10', 12),
('Update Patient Chart', 'completed', '2026-04-12', 13),
('Administer Medication', 'in_progress', '2026-10-17', 14),
('Administer IV Fluids', 'in_progress', '2026-11-02', 15),
('Remove Stitches', 'completed', '2025-12-13', 16),
('Prepare Lab Sample', 'pending', '2026-06-04', 17),
('Check Vitals', 'pending', '2026-10-24', 18),
('Coordinate Specialist Referral', 'completed', '2026-04-15', 19),
('Update Medication List', 'pending', '2026-04-17', 20),
('Update Medication List', 'completed', '2026-05-12', 21),
('Update Medication List', 'in_progress', '2026-02-20', 22),
('Prepare Follow-Up Instructions', 'completed', '2026-06-14', 23),
('Update Medication List', 'completed', '2025-12-07', 24),
('Check Oxygen Levels', 'pending', '2026-04-06', 25),
('Update Patient Chart', 'pending', '2026-03-01', 26),
('Update Patient Chart', 'pending', '2026-04-04', 27),
('Contact Pharmacy', 'in_progress', '2026-10-19', 28),
('Administer IV Fluids', 'pending', '2026-04-30', 29),
('Conduct Pain Assessment', 'pending', '2026-04-23', 30),
('Check Oxygen Levels', 'pending', '2026-03-02', 31),
('Prepare Lab Sample', 'pending', '2026-06-26', 32),
('Check Oxygen Levels', 'completed', '2025-12-10', 33),
('Schedule Appointment', 'in_progress', '2026-01-11', 34),
('Administer Medication', 'pending', '2026-06-17', 35),
('Administer Medication', 'pending', '2026-04-15', 36),
('Prepare Lab Sample', 'completed', '2026-06-21', 37),
('Check Vitals', 'completed', '2026-08-22', 38),
('Schedule Appointment', 'in_progress', '2026-09-03', 39),
('Check Oxygen Levels', 'completed', '2026-07-28', 40);

INSERT INTO Appointment (dateTime, reason, status, staffId, patientId) VALUES
('2026-11-24 09:00:00', 'Gynecological Exam', 'completed', 1, 3),
('2026-07-20 14:30:00', 'Gynecological Exam', 'scheduled', 2, 2),
('2025-07-17 10:15:00', 'Diagnostic Testing Appointment', 'scheduled', 1, 5),
('2025-09-27 13:45:00', 'Respiratory Symptoms Evaluation', 'scheduled', 4, 4),
('2026-02-13 08:30:00', 'Imaging Results Review', 'completed', 3, 1),
('2025-10-22 11:00:00', 'Prenatal Checkup', 'scheduled', 6, 7),
('2025-05-27 15:00:00', 'Respiratory Symptoms Evaluation', 'scheduled', 2, 2),
('2025-06-18 09:45:00', 'Vaccination Appointment', 'completed', 8, 6),
('2025-08-12 14:00:00', 'Specialist Referral Consultation', 'completed', 4, 8),
('2026-11-11 10:30:00', 'Gynecological Exam', 'completed', 10, 9),
('2026-05-08 13:15:00', 'Physical Therapy Session', 'scheduled', 11, 3),
('2026-02-02 08:45:00', 'Annual Physical', 'scheduled', 12, 5),
('2025-08-06 09:30:00', 'Cardiology Follow-Up', 'scheduled', 13, 2),
('2026-06-13 11:15:00', 'Pre-Surgical Evaluation', 'completed', 14, 7),
('2025-04-11 14:30:00', 'Lab Test Review', 'completed', 3, 9),
('2026-06-05 10:00:00', 'Pediatric Wellness Visit', 'scheduled', 16, 10),
('2026-09-13 09:15:00', 'Lab Test Review', 'completed', 5, 12),
('2025-09-10 15:45:00', 'Annual Physical', 'completed', 18, 1),
('2025-02-24 11:30:00', 'Injury Assessment', 'scheduled', 7, 11),
('2026-09-12 13:00:00', 'Physical Therapy Session', 'scheduled', 20, 6),
('2025-09-16 08:00:00', 'Respiratory Symptoms Evaluation', 'completed', 2, 14),
('2026-02-04 12:15:00', 'Specialist Referral Consultation', 'completed', 22, 4),
('2025-11-09 09:45:00', 'Prenatal Checkup', 'scheduled', 6, 17),
('2025-02-22 14:00:00', 'Blood Pressure Check', 'completed', 24, 2),
('2025-11-19 10:30:00', 'Post-Surgical Follow-Up', 'completed', 25, 8),
('2026-08-01 13:15:00', 'Pediatric Wellness Visit', 'completed', 16, 10),
('2025-01-14 09:00:00', 'Prenatal Checkup', 'completed', 2, 19),
('2025-09-06 11:45:00', 'Diagnostic Testing Appointment', 'scheduled', 28, 3),
('2026-09-19 08:30:00', 'Prenatal Checkup', 'completed', 29, 6),
('2026-06-15 14:00:00', 'Diagnostic Testing Appointment', 'scheduled', 30, 5),
('2025-05-17 10:15:00', 'Injury Assessment', 'scheduled', 7, 14),
('2026-08-08 09:30:00', 'Diabetes Management Visit', 'completed', 32, 12),
('2026-06-15 15:00:00', 'Prenatal Checkup', 'scheduled', 33, 11),
('2026-06-09 11:30:00', 'Post-Surgical Follow-Up', 'scheduled', 34, 3),
('2026-04-18 13:45:00', 'Post-Surgical Follow-Up', 'completed', 35, 8),
('2026-01-28 08:45:00', 'Pre-Surgical Evaluation', 'scheduled', 36, 9),
('2025-07-04 10:00:00', 'Diabetes Management Visit', 'scheduled', 37, 2),
('2025-12-19 14:30:00', 'Vaccination Appointment', 'scheduled', 8, 7),
('2025-03-20 09:15:00', 'Cardiology Follow-Up', 'scheduled', 39, 1),
('2025-06-17 15:45:00', 'Specialist Referral Consultation', 'completed', 40, 10);

INSERT INTO CarePlan (goals, startTime, endTime, staffId, patientId) VALUES
('Strengthen Immune System', '2026-07-07 09:00:00', '2026-12-22 17:00:00', 1, 3),
('Lower Blood Pressure', '2024-12-25 08:30:00', '2026-07-04 16:30:00', 2, 5),
('Improve Sleep Quality', '2026-11-08 10:15:00', '2026-12-30 15:45:00', 3, 2),
('Improve Mobility', '2025-04-05 11:00:00', '2025-12-27 14:00:00', 4, 4),
('Promote Rehabilitation After Surgery', '2025-02-01 09:30:00', '2025-06-13 16:00:00', 5, 6),
('Strengthen Immune System', '2026-02-11 08:45:00', '2026-12-06 17:30:00', 6, 1),
('Manage Diabetes', '2025-10-11 09:00:00', '2026-06-01 16:00:00', 7, 7),
('Increase Physical Activity', '2025-09-26 10:00:00', '2026-05-02 15:00:00', 8, 2),
('Improve Sleep Quality', '2025-11-24 08:15:00', '2025-12-15 12:30:00', 9, 8),
('Monitor Blood Sugar Levels', '2026-07-03 09:00:00', '2026-07-25 14:45:00', 10, 10),
('Reduce Cholesterol Levels', '2026-10-25 08:30:00', '2026-12-26 16:00:00', 11, 3),
('Reduce Cholesterol Levels', '2025-03-08 09:15:00', '2026-03-02 15:45:00', 12, 5),
('Reduce Stress', '2025-09-11 10:00:00', '2026-04-09 16:30:00', 13, 9),
('Lower Blood Pressure', '2025-02-26 08:45:00', '2025-12-25 14:00:00', 14, 6),
('Lower Blood Pressure', '2025-05-26 09:30:00', '2026-06-18 16:00:00', 15, 11),
('Improve Hydration and Nutrition', '2025-11-29 08:00:00', '2026-03-08 15:30:00', 16, 4),
('Manage Chronic Pain', '2026-02-14 09:45:00', '2026-11-12 17:00:00', 17, 12),
('Increase Physical Activity', '2026-01-18 10:15:00', '2026-02-10 16:45:00', 18, 7),
('Reduce Stress', '2024-12-30 09:00:00', '2026-12-18 17:30:00', 19, 13),
('Improve Sleep Quality', '2026-03-13 08:30:00', '2026-03-24 15:00:00', 20, 2),
('Monitor Blood Sugar Levels', '2024-12-21 09:15:00', '2026-07-21 16:45:00', 21, 14),
('Reduce Stress', '2025-07-20 08:45:00', '2026-10-21 16:00:00', 22, 5),
('Reduce Cholesterol Levels', '2025-09-28 09:00:00', '2026-09-30 15:30:00', 23, 11),
('Monitor Blood Sugar Levels', '2026-01-16 08:30:00', '2026-11-23 17:00:00', 24, 8),
('Manage Asthma Symptoms', '2025-03-16 09:00:00', '2026-11-24 16:00:00', 25, 10),
('Lower Blood Pressure', '2026-05-03 09:45:00', '2026-12-23 15:30:00', 26, 13),
('Promote Rehabilitation After Surgery', '2025-07-15 10:00:00', '2025-12-21 16:45:00', 27, 3),
('Lower Blood Pressure', '2025-07-19 08:30:00', '2026-12-17 17:00:00', 28, 9),
('Strengthen Immune System', '2025-04-05 09:00:00', '2026-03-28 15:00:00', 29, 6),
('Reduce Cholesterol Levels', '2026-09-07 10:15:00', '2026-11-06 16:30:00', 30, 12),
('Lower Blood Pressure', '2026-08-25 08:30:00', '2026-12-12 17:00:00', 31, 8),
('Promote Rehabilitation After Surgery', '2025-12-10 09:00:00', '2025-12-20 14:30:00', 32, 7),
('Improve Mobility', '2026-02-10 08:45:00', '2026-03-16 15:00:00', 33, 4),
('Reduce Cholesterol Levels', '2026-07-26 09:00:00', '2026-08-02 16:00:00', 34, 11),
('Reduce Cholesterol Levels', '2026-09-03 10:00:00', '2026-09-19 16:30:00', 35, 2),
('Increase Physical Activity', '2025-04-15 08:30:00', '2026-11-03 17:00:00', 36, 10),
('Reduce Cholesterol Levels', '2026-12-20 09:00:00', '2026-12-31 16:30:00', 37, 5),
('Monitor Blood Sugar Levels', '2026-05-12 08:45:00', '2026-05-20 15:00:00', 38, 7),
('Manage Asthma Symptoms', '2026-04-27 09:15:00', '2026-09-23 16:00:00', 39, 9),
('Increase Physical Activity', '2026-04-21 08:30:00', '2026-06-23 17:00:00', 40, 6);

INSERT INTO AuditLog (timeStamp, action, outcome, staffId) VALUES

INSERT INTO Vitals (type, value, timeStamp, patientId) VALUES

INSERT INTO Conditions (conditionName, dateDiagnosed, notes, patientId) VALUES

INSERT INTO LabResult (labType, value, date, isModified, isOutlier, patientId) VALUES

INSERT INTO DataRequest (title, description, status, dateCreated, staffId) VALUES

INSERT INTO Project (name, startDate, endDate, requestId) VALUES

INSERT INTO Visualization (type, dateCreated, summary, projectId) VALUES

INSERT INTO Permission (action, resource) VALUES

INSERT INTO Role (name, description, permissionId) VALUES

INSERT INTO Department (location, name) VALUES

INSERT INTO Integration (systemName, status, lastSyncDate, departmentId) VALUES

INSERT INTO SystemAlert (type, severity, message, timestamp, departmentId, permissionId) VALUES

INSERT INTO Project_Patient (projectId, patientId) VALUES

INSERT INTO Treatment (type, name, dosage, frequency, startdate, endDate, patientId) VALUES

INSERT INTO Project_Treatment (projectId, treatmentId, patientId) VALUES

INSERT INTO Staff_Role (staffId, roleId) VALUES

INSERT INTO Project_Condition (projectId, conditionsId, patientId) VALUES

INSERT INTO Project_Vitals (projectId, vitalsId, patientId) VALUES

INSERT INTO Project_Labs (projectId, labResultId, patientId) VALUES
