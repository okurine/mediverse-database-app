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
   status ENUM('pending', 'in_progress', 'completed') DEFAULT 'pending',
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
   severity ENUM('warning', 'critical') DEFAULT 'warning' NOT NULL,
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

-- Sample Staff
INSERT INTO Staff (name, email, status) VALUES
('Dr. Alice Smith', 'alice.smith@mediverse.com', 'active'),
('Dr. Bob Johnson', 'bob.johnson@mediverse.com', 'active'),
('Nurse Carol White', 'carol.white@mediverse.com', 'inactive');

-- Sample Patients
INSERT INTO Patient (name, gender, DOB, status) VALUES
('John Doe', 'Male', '1985-03-15', 'active'),
('Jane Roe', 'Female', '1990-07-22', 'active'),
('Sam Green', 'Male', '1975-11-02', 'inactive');

-- Sample Tasks
INSERT INTO Tasks (type, status, dueDate, staffId) VALUES
('Check Vitals', 'pending', '2025-11-25', 1),
('Administer Medication', 'in_progress', '2025-11-26', 3),
('Schedule Appointment', 'completed', '2025-11-24', 2);

-- Sample Appointments
INSERT INTO Appointment (dateTime, reason, status, staffId, patientId) VALUES
('2025-11-25 09:00:00', 'Routine Checkup', 'scheduled', 1, 1),
('2025-11-26 14:00:00', 'Follow-up', 'completed', 2, 2);

-- Sample Care Plans
INSERT INTO CarePlan (goals, startTime, endTime, staffId, patientId) VALUES
('Lower blood pressure', '2025-11-20 08:00:00', '2026-05-20 08:00:00', 1, 1),
('Manage diabetes', '2025-11-22 09:00:00', '2026-11-22 09:00:00', 2, 2);

-- Sample Vitals
INSERT INTO Vitals (type, value, timestamp, patientId) VALUES
('Blood Pressure', 120, '2025-11-24 08:00:00', 1),
('Heart Rate', 72, '2025-11-24 08:05:00', 2);

-- Sample Conditions
INSERT INTO Conditions (conditionName, dateDiagnosed, notes, patientId) VALUES
('Hypertension', '2023-05-10', 'Requires daily monitoring', 1),
('Diabetes', '2020-02-15', 'Type 2', 2);

-- Sample Lab Results
INSERT INTO LabResult (labType, value, date, patientId) VALUES
('Blood Glucose', '110 mg/dL', '2025-11-23 07:30:00', 2),
('Cholesterol', '190 mg/dL', '2025-11-22 08:00:00', 1);

-- Sample Data Requests
INSERT INTO DataRequest (title, description, status, dateCreated, staffId) VALUES
('Patient Vitals Report', 'Request for weekly vitals summary', 'pending', '2025-11-23 10:00:00', 1);

-- Sample Projects
INSERT INTO Project (name, startDate, endDate, requestId) VALUES
('Hypertension Study', '2025-11-24 00:00:00', '2026-11-24 00:00:00', 1);

-- Sample Project_Patient mapping
INSERT INTO Project_Patient (projectId, patientId) VALUES
(1, 1),
(1, 2);

-- Sample Treatments
INSERT INTO Treatment (treatmentId, type, name, dosage, frequency, startdate, endDate, patientId) VALUES
(1, 'Medication', 'Lisinopril', '10mg', 'Once Daily', '2025-11-24 08:00:00', '2026-11-24 08:00:00', 1),
(2, 'Medication', 'Metformin', '500mg', 'Twice Daily', '2025-11-24 08:00:00', '2026-11-24 08:00:00', 2);

-- Sample Project_Treatment mapping
INSERT INTO Project_Treatment (projectId, treatmentId, patientId) VALUES
(1, 1, 1),
(1, 2, 2);

-- Sample Staff Roles
INSERT INTO Permission (permissionId, action, resource) VALUES
(1, 'read', 'Patient Data'),
(2, 'write', 'Treatment Plan');

INSERT INTO Role (roleId, name, description, permissionId) VALUES
(1, 'Doctor', 'Can view and update patient records', 2),
(2, 'Nurse', 'Can view patient records', 1);

INSERT INTO Staff_Role (staffId, roleId) VALUES
(1, 1),
(3, 2);

