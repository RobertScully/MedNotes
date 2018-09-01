CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_addNote`(
    IN p_title varchar(45),
    IN p_description varchar(1000),
    IN p_user_id bigint
)
BEGIN
    insert into tbl_note(
        note_title,
        note_content,
        note_user_id,
        note_date
    )
    values
    (
        p_title,
        p_description,
        p_user_id,
        NOW()
    );
END