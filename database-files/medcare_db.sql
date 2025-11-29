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
   status VARCHAR(20) NOT NULL,
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

