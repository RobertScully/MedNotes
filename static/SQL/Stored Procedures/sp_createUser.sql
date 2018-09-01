CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_createUser`(
	IN p_staffid VARCHAR(45),
    IN p_firstname VARCHAR(45),
    IN p_surname VARCHAR(45),
    IN p_email VARCHAR(45),
    IN p_job VARCHAR(45),
    IN p_password VARCHAR(200)
)
BEGIN
    if ( select exists (select 1 from tbl_employee where employee_staffid = p_staffid) ) THEN
     
        select 'Account already exists with this email address.';
     
    ELSE
     
        insert into tbl_employee
        (
			employee_staffid,
            employee_firstname,
            employee_surname,
            employee_email,
            employee_job,
            employee_password
        )
        values
        (
			p_staffid,
            p_firstname,
            p_surname,
            p_email,
            p_job,
            p_password
        );
     
    END IF;

END