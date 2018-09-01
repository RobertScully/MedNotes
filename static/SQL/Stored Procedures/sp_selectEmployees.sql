CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_selectEmployees`(
)
BEGIN
    select * from tbl_employee order by employee_id;
END