CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_selectPatients`(
)
BEGIN
    select * from tbl_patient order by patient_number;
END