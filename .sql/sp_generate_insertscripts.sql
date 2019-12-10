----------Final Procedure To generate Script------

CREATE PROCEDURE sp_generate_insertscripts
(
    @TABLE_NAME VARCHAR(MAX),
    @FILTER_CONDITION VARCHAR(MAX)=''
)
AS
BEGIN

SET NOCOUNT ON

DECLARE @CSV_COLUMN VARCHAR(MAX),
        @QUOTED_DATA VARCHAR(MAX),
        @TEXT VARCHAR(MAX)

SELECT @CSV_COLUMN=STUFF
(
    (
     SELECT ',['+ NAME +']' FROM sys.all_columns 
     WHERE OBJECT_ID=OBJECT_ID(@TABLE_NAME) AND 
     is_identity!=1 FOR XML PATH('')
    ),1,1,''
)

SELECT @QUOTED_DATA=STUFF
(
    (
     SELECT ' ISNULL(QUOTENAME('+NAME+','+QUOTENAME('''','''''')+'),'+'''NULL'''+')+'','''+'+' FROM sys.all_columns 
     WHERE OBJECT_ID=OBJECT_ID(@TABLE_NAME) AND 
     is_identity!=1 FOR XML PATH('')
    ),1,1,''
)

SELECT @TEXT='SELECT ''INSERT INTO '+@TABLE_NAME+'('+@CSV_COLUMN+')VALUES('''+'+'+SUBSTRING(@QUOTED_DATA,1,LEN(@QUOTED_DATA)-5)+'+'+''')'''+' Insert_Scripts FROM '+@TABLE_NAME + @FILTER_CONDITION

--SELECT @CSV_COLUMN AS CSV_COLUMN,@QUOTED_DATA AS QUOTED_DATA,@TEXT TEXT

EXECUTE (@TEXT)

SET NOCOUNT OFF

END

EXEC sp_generate_insertscripts 'USER_ROLE'

select * from OVERRIDE
