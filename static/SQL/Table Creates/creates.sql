CREATE database MedNotes;

CREATE TABLE `tbl_employee` (
  `employee_id` BIGINT NOT NULL AUTO_INCREMENT,
  `employee_staffid` varchar(45) NOT NULL,
  `employee_password` VARCHAR(200) NULL,
  `employee_firstname` varchar(45) NOT NULL,
  `employee_surname` varchar(45) NOT NULL,
  `employee_email` varchar(45) NOT NULL,
  `employee_job` varchar(40) DEFAULT NULL,
  PRIMARY KEY (`employee_id`));

CREATE TABLE `tbl_note` (
  `note_id` int(11) NOT NULL AUTO_INCREMENT primary key,
  `note_title` varchar(45) DEFAULT NULL,
  `note_content` varchar(10000) DEFAULT NULL,
  `note_date` datetime DEFAULT NULL,
  `patient_number` VARCHAR(45) NOT NULL,
  CONSTRAINT FOREIGN KEY fk_patient_number(patient_number) 
  REFERENCES tbl_patient(patient_number)
);

CREATE TABLE `tbl_patient` (
  `patient_number` VARCHAR(45) NOT NULL,
  `patient_firstname` VARCHAR(45) NULL,
  `patient_surname` VARCHAR(45) NULL,
  PRIMARY KEY (`patient_number`));

  
CREATE TABLE `tbl_patient_access` (
  `access_id` BIGINT NOT NULL AUTO_INCREMENT,
  `access_patient_number` VARCHAR(45) NOT NULL,
  `access_employee_number` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`access_id`));

select * FROM tbl_employee;
select * FROM tbl_note;
select * from tbl_patient;
select * from tbl_patient_access;