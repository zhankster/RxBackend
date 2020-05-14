CREATE PROC [dbo].[put_mng_groups]
(	@CODE VARCHAR(12),
	@DESCRIPTION VARCHAR(200),
	@EMAIL VARCHAR(4000),
	@SEND_NOTIFICATION BIT
)
AS
BEGIN

INSERT INTO [dbo].[MNG_GROUPS]
           ([CODE]
           ,[DESCRIPTION]
           ,[EMAIL]
           ,[SEND_NOTIFICATION])
     VALUES
           (@CODE
           ,@DESCRIPTION
           ,@EMAIL
           ,@SEND_NOTIFICATION)

END