USE [RXBackend]
GO

/****** Object:  StoredProcedure [dbo].[put_batch_fill_for_iou]    Script Date: 5/14/2020 1:43:52 PM ******/
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
FROM UPS_Shipping.dbo.TO_UPS 
WHERE ID = @TO_UPS_ID;

SELECT @FOUND = 1 FROM FAC_ALT WHERE DCODE = @FAC;

IF (@FOUND = 0)
	RETURN;

SELECT 
 @FCODE = ISNULL(f.DCODE, 'NONE')
, @FEMAIL = ISNULL(f.IOU_EMAIL, 'NONE')
, @FNOTIFY = ISNULL(f.IOU_NOTIFY, 0)
, @MCODE = ISNULL(m.CODE, 'NONE')
, @MEMAIL = ISNULL(m.EMAIL, 'NONE')
, @MNOTIFY = ISNULL(m.SEND_NOTIFICATION, 0)
FROM  FAC_ALT f 
	LEFT JOIN MNG_GROUPS m ON f.MNG = m.CODE
WHERE f.DCODE =  @FAC;

IF (@FNOTIFY = 0 AND @MNOTIFY = 0)
	RETURN;

SET @SUBJECT = 'Item ordered but not shipped – IHS Pharmacy';

SET @tableHTML =
N'<span>' + @SUBJECT + '</span><br />' + CHAR(10) +  
N'<p>Facility: ' + @FAC + ' - ' + @NAME + '<br />' + CHAR(10) +
N'Patient Involved: ' + ISNULL(@PAT_FNAME, ' ') + ' ' + ISNULL(@PAT_LNAME, ' ') + '<br />' + CHAR(10) +
N'Medication: ' + ISNULL(@DRG_DNAME, '') + ' - ' +ISNULL(@DRG_STRENGTH, '') + '<br />' + CHAR(10) +
N'Fill Date: ' + CONVERT(VARCHAR(10), CAST(@FIL_DATE AS DATE), 101)  + '<br />' + CHAR(10) +
N'Quantity Ordered: ' + CAST(@FIL_QTY_DSP AS VARCHAR)  + '<br />' + CHAR(10) +
N'Shipped Quantity: ' + CAST( (@FIL_QTY_DSP - @QTY) AS VARCHAR)  + '<br />' + CHAR(10) +
N'Date Reported: ' + CONVERT(VARCHAR(10), CAST(GETDATE() AS DATE), 101)  + '<br />' + CHAR(10) +
N'Tech: ' + @TECH +  '<br />' + CHAR(10) +
N'</p><p>
CONFIDENTIALITY NOTICE: This email message, including any attachments, is for the sole use of the intended recipient(s) and may contain confidential and privileged 
information or otherwise be protected by law. Any unauthorized review, use, disclosure or distribution is prohibited. if you are not the intended recipient, please contact the 
sender by reply email and destroy all copies of the original message.
</p>';

IF (@FNOTIFY = 1)
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



GO


SELECT FAC_DCODE
, FAC_DNAME
, DRG_DNAME
, DRG_STRENGTH
, PAT_FNAME
, PAT_LNAME
, FIL_QTY_DSP
, FIL_DATE
FROM UPS_Shipping.dbo.TO_UPS 
WHERE ID = 3864987

SELECT 
 ISNULL(f.DCODE, 'NONE') as FCODE
, ISNULL(f.IOU_EMAIL, 'NONE') as FEMAIL
, ISNULL(f.IOU_NOTIFY, 0) FNOTIFY
, ISNULL(m.CODE, 'NONE') as MCODE
, ISNULL(m.EMAIL, 'NONE') as MEMAIL
, ISNULL(m.SEND_NOTIFICATION, 0) MNOTIFY
FROM  FAC_ALT f 
	LEFT JOIN MNG_GROUPS m ON f.MNG = m.CODE
WHERE f.DCODE =  'AD'

584381

<tr class="iou_row" id="3864987_iourow">
								<td>
									BROWN, SHEM
									<input type="hidden" value="BROWN, SHEM" id="3864987_name" name="3864987_name">
									<input type="hidden" value="" id="3864987_kop" name="3864987_kop">
									<input type="hidden" value="2020-05-14" id="3864987_filldate" name="3864987_filldate">
								</td>
								<td>
									LISINOPRIL - 10MG
									<input type="hidden" value="LISINOPRIL" id="3864987_drgname" name="3864987_drgname">
									<input type="hidden" value="10MG" id="3864987_drgstrength" name="3864987_drgstrength">
								</td>
								<td>
									28.00 
									<input type="hidden" value="28.00" id="3864987_qty" name="3864987_qty">
								</td>
								<td class="na ">
									NA
									<input type="hidden" value="NA " id="3864987_status" name="3864987_status">
								</td>
								<td>
									<input class="P_check" type="checkbox" value="3864987" name="cbfil" id="3864987_present">
								</td>
								<td>
									<input class="" type="text" id="3864987_iouqty" name="3864987_iouqty" value="28.00" size="6"> 
									<!-- <input type="hidden" value="" id="3864987_iouqty" name="3864987_iouqty"/> -->
								</td>
							</tr>
