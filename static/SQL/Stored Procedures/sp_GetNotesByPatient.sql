CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_GetNotesByPatient`(
IN p_patient VARCHAR(45)
)
BEGIN
    select * from tbl_note join tbl_patient where tbl_patient.patient_number = p_patient;
END