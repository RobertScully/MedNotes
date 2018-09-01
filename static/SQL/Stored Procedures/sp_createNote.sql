CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_createNote`(
	IN p_note_id VARCHAR(45),
    IN p_note_title VARCHAR(45),
    IN p_note_content VARCHAR(45),
    IN p_note_date VARCHAR(45),
    IN p_patient_number VARCHAR(45)
)
BEGIN
        insert into tbl_note
        (
			note_id,
            note_title,
            note_content,
            note_date,
            patient_number
        )
        values
        (
			p_note_id,
			p_note_title ,
			p_note_content ,
			p_note_date ,
			p_patient_number 
        );
     
END