CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_selectNotes`(
)
BEGIN
    select * from tbl_note order by note_id DESC;
END