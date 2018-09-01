CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_GetPatientByAccess`(
IN p_user VARCHAR(45)
)
BEGIN
    select * from tbl_patient where patient_number in (select access_patient_number from tbl_patient_access where access_employee_number = p_user);
END