CREATE PROC [dbo].[put_fac_alt_notify]
(	@DCODE VARCHAR(8),
	@IOU_EMAIL VARCHAR(4000),
	@MNG VARCHAR(12),
	@IOU_NOTIFY BIT
)
AS
BEGIN

INSERT INTO [dbo].[FAC_ALT]
           ([DCODE]
           ,[NOTIFY_TYPE]
           ,[EMAIL]
           ,[FAX1]
           ,[PHONE1]
           ,[USER1]
           ,[IOU_EMAIL]
           ,[MNG]
           ,[IOU_NOTIFY])
     VALUES
           (@DCODE
           ,''
           ,''
           ,''
           ,''
           ,''
           ,@IOU_EMAIL
           ,@MNG
           ,@IOU_NOTIFY)

END