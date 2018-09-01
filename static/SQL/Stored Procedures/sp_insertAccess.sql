CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_insertAccess`(
	IN p_patient_number VARCHAR(45),
    IN p_employee_number VARCHAR(45)
)
BEGIN
        insert into tbl_patient_access
        (
			access_patient_number,
            access_employee_number
        )
        values
        (
			p_patient_number,
            p_employee_number
        );
     
END