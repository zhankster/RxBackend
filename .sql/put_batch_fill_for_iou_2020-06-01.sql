USE [RXBackend]
GO
/****** Object:  StoredProcedure [dbo].[put_batch_fill_for_iou]    Script Date: 6/1/2020 1:12:43 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
ALTER PROC [dbo].[put_batch_fill_for_iou]
(	@TO_UPS_ID INT,
	@QTY DECIMAL(10,4),
	@TECH NVARCHAR(10)
)
AS

DECLARE @NEXT_INT INT
, @FAC VARCHAR(8)
, @NAME VARCHAR(50)
, @DRG_DNAME VARCHAR(50)
, @DRG_STRENGTH VARCHAR(50)
, @FIL_QTY_DSP DECIMAL(10,4)
, @FIL_ID INT
, @TECH_USR_ID VARCHAR(50)
, @TECH_NAME VARCHAR(50)
, @TECH_EMAIL VARCHAR(80)
, @PAT_FNAME VARCHAR(50)
, @PAT_LNAME VARCHAR(50)
, @FIL_DATE DATETIME
, @FOUND bit
, @FCODE VARCHAR(8)
, @FEMAIL VARCHAR(4000)
, @FNOTIFY BIT
, @MCODE VARCHAR(12)
, @MEMAIL VARCHAR(4000)
, @MNOTIFY BIT
, @tableHTML NVARCHAR(MAX)
, @SUBJECT VARCHAR(256)
;

SET @NEXT_INT = NEXT VALUE FOR dbo.iou_count; 

BEGIN 
	INSERT INTO [dbo].[BAT_IOU]
			([ID]
			,[TO_UPS_ID]
			,[QTY]
			,[CREATED_BY]
			,[CLOSED_BY]
			,[STATUS]
			,[CREATED]
			,[LAST_USER]
			,[LAST_UPDATE]
			,[CLOSE_DATE])
		VALUES
			(@NEXT_INT
			,@TO_UPS_ID
			,@QTY
			,@TECH
			,''
			,'IO'
			,GETDATE()
			,''
			,NULL
			,NULL);
END

BEGIN
	INSERT INTO [dbo].[BAT_IOU_TRANS]
			   ([IOU_ID]
			   ,[ADD_QTY]
			   ,[USER_NAME]
			   ,[TRANS_TYPE]
			   ,[TRANS_DATE])
     VALUES
           (@NEXT_INT
           ,0
           ,@TECH
           ,'Created'
           ,GETDATE())
END
BEGIN 

SET @FOUND = 0;

SELECT @FAC = FAC_DCODE
, @NAME = FAC_DNAME
, @DRG_DNAME = DRG_DNAME
, @DRG_STRENGTH = DRG_STRENGTH
, @PAT_FNAME = PAT_FNAME
, @PAT_LNAME = PAT_LNAME
, @FIL_QTY_DSP = FIL_QTY_DSP
, @FIL_DATE = FIL_DATE
, @FIL_ID = FIL_ID
FROM UPS_Shipping.dbo.TO_UPS 
WHERE ID = @TO_UPS_ID;

SET @TECH_NAME = '';
SET @TECH_EMAIL = '';

SELECT @TECH_NAME = FNAME + ' ' + LNAME 
, @TECH_EMAIL = EMAIL
FROM CIPS.dbo.FIL f
INNER JOIN CIPS.dbo.USR u on f.TECH_USR_ID = u.ID
WHERE f.ID = @FIL_ID

SELECT @FOUND = 1 FROM FAC_ALT WHERE DCODE = @FAC;

IF (@FOUND = 0)
	RETURN;

--, @FEMAIL = ISNULL(f.IOU_EMAIL, 'NONE')
SELECT 
 @FCODE = ISNULL(f.DCODE, 'NONE')
, @FNOTIFY = ISNULL(f.IOU_NOTIFY, 0)
, @MCODE = ISNULL(m.CODE, 'NONE')
, @MEMAIL = ISNULL(m.EMAIL, 'NONE')
, @MNOTIFY = ISNULL(m.SEND_NOTIFICATION, 0)
FROM  FAC_ALT f 
	LEFT JOIN MNG_GROUPS m ON f.MNG = m.CODE
WHERE f.DCODE =  @FAC;

DECLARE @#IOU TABLE (ADDRESS VARCHAR(256));
INSERT INTO @#IOU 
SELECT ADDRESS ADDRESS FROM FAC_EMAIL WHERE IOU = 1 and FAC_CODE = @FCODE;

DECLARE @ADDRESS varchar(256);
SET @FEMAIL = '';

WHILE EXISTS (SELECT ADDRESS FROM @#IOU)
BEGIN
	SELECT TOP 1 @ADDRESS = ADDRESS FROM @#IOU
	SET @FEMAIL += @ADDRESS + ';';
	DELETE FROM @#IOU WHERE ADDRESS = @ADDRESS;
END

IF (@FEMAIL = '' AND @MNOTIFY = 0)
	RETURN;

IF (@FIL_QTY_DSP - @QTY > 0)
	RETURN;

SET @SUBJECT = 'Item ordered but not shipped – IHS Pharmacy';

SET @tableHTML =
N'<span>Your facility has ordered an item that IHS does not have in stock. Unless we contact you and tell you otherwise, we will ship as soon as possible. 
If this is an emergency item that you cannot wait to receive, you may want to get it from your backup pharmacy. Please let us know if we can assist 
you in any way.</span><br />' +
@TECH_NAME + ' ' + @TECH_EMAIL + CHAR(10) +  CHAR(10) + 
N'<p>Facility: ' + @FAC + ' - ' + @NAME + '<br />' + CHAR(10) +
N'Patient Involved: ' + ISNULL(@PAT_FNAME, ' ') + ' ' + ISNULL(@PAT_LNAME, ' ') + '<br />' + CHAR(10) +
N'Medication: ' + ISNULL(@DRG_DNAME, '') + ' - ' +ISNULL(@DRG_STRENGTH, '') + '<br />' + CHAR(10) +
N'Fill Date: ' + CONVERT(VARCHAR(10), CAST(@FIL_DATE AS DATE), 101)  + '<br />' + CHAR(10) +
N'Quantity Ordered: ' + CAST(@FIL_QTY_DSP AS VARCHAR)  + '<br />' + CHAR(10) +
N'Shipped Quantity: ' + CAST( (@FIL_QTY_DSP - @QTY) AS VARCHAR)  + '<br />' + CHAR(10) +
N'Tech: ' + @TECH_NAME +  '<br />' + CHAR(10) +
N'</p><p>
CONFIDENTIALITY NOTICE: This email message, including any attachments, is for the sole use of the intended recipient(s) and may contain confidential and privileged 
information or otherwise be protected by law. Any unauthorized review, use, disclosure or distribution is prohibited. if you are not the intended recipient, please contact the 
sender by reply email and destroy all copies of the original message.
</p>';

IF (@FEMAIL <> '')
BEGIN
		--EXEC msdb.dbo.sp_send_dbmail
		--@profile_name = 'IHS Email',
		--@recipients =   @FEMAIL
		--@subject = @SUBJECT,
		--@body = @tableHTML,
		--@body_format = 'HTML' ;

	execute msdb.dbo.sp_send_dbmail 
    @profile_name =   'BH Mail' 
  ,   	@recipients =   @FEMAIL     
  ,   	@from_address =   'hank.d.allen@gmail.com'   
  ,   	@reply_to =   'hank.d.allen@gmail.com'    
  ,   	@subject =   @SUBJECT
  ,   	@body =   @tableHTML
  ,   	@body_format =   'HTML'

		print @tableHTML;
END

IF (@MNOTIFY = 1)
BEGIN
		--EXEC msdb.dbo.sp_send_dbmail
		--@profile_name = 'IHS Email',
		--@recipients =   @MEMAIL
		--@subject = @SUBJECT,
		--@body = @tableHTML,
		--@body_format = 'HTML' ;

	execute msdb.dbo.sp_send_dbmail 
    @profile_name =   'BH Mail' 
  ,   	@recipients =   @MEMAIL     
  ,   	@from_address =   'hank.d.allen@gmail.com'   
  ,   	@reply_to =   'hank.d.allen@gmail.com'    
  ,   	@subject =   @SUBJECT
  ,   	@body =   @tableHTML
  ,   	@body_format =   'HTML'

		print @tableHTML;
END



END