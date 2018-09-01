CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_validateLogin`(
IN p_staffid VARCHAR(20)
)
BEGIN
    select * from tbl_employee where employee_staffid = p_staffid;
END