USE [RXBackend]
GO

/****** Object:  StoredProcedure [dbo].[close_iou_request]    Script Date: 2/2/2020 8:29:59 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

ALTER PROC [dbo].[close_iou_request]
(	@IOU_ID INT,
	@ADD_QTY DECIMAL(10,4),
	@TECH NVARCHAR(10),
	@STATUS NVARCHAR(3)
)
AS
DECLARE
	@TRANS_TYPE NCHAR(20);

SET @TRANS_TYPE = CASE @STATUS
		WHEN 'IC' THEN 'User Complete'
		WHEN 'IF' THEN 'Filled'
		WHEN 'IP' THEN 'Partial'
		WHEN 'IS' THEN 'System Closed'
		WHEN 'IIV' THEN 'Invalidated'
		ELSE 'NA'
	END;

IF (@STATUS = 'IF' OR @STATUS = 'IC'  OR @STATUS = 'IIV')
BEGIN
	UPDATE [dbo].[BAT_IOU]
	   SET [CLOSED_BY] = @TECH 
	   	  ,[CLOSE_DATE] = GETDATE()
		  ,[STATUS] = @STATUS
		  ,[COMP_QTY] = [COMP_QTY] + @ADD_QTY
		  ,[LAST_USER] = @TECH
		  ,[LAST_UPDATE] = GETDATE()
	 WHERE [ID] = @IOU_ID;
 END

IF (@STATUS = 'IP')
BEGIN
	UPDATE [dbo].[BAT_IOU]
	   SET [STATUS] = @STATUS
		  ,[COMP_QTY] = [COMP_QTY] + @ADD_QTY
		  ,[LAST_USER] = @TECH
		  ,[LAST_UPDATE] = GETDATE()
	 WHERE [ID] = @IOU_ID;
END

IF (@STATUS = 'IS')
BEGIN
	UPDATE [dbo].[BAT_IOU]
	   SET [STATUS] = @STATUS
		  ,[COMP_QTY] = [COMP_QTY] + @ADD_QTY
		  ,CLOSE_DATE = GETDATE()
		  ,CLOSED_BY = @TECH
		  ,[LAST_USER] = @TECH
		  ,[LAST_UPDATE] = GETDATE()
	 WHERE [ID] = @IOU_ID;
END


INSERT INTO [dbo].[BAT_IOU_TRANS]
           ([IOU_ID]
           ,[ADD_QTY]
           ,[USER_NAME]
           ,[TRANS_TYPE]
           ,[TRANS_DATE])
     VALUES
           (@IOU_ID
           ,@ADD_QTY
           ,@TECH
           ,@TRANS_TYPE
           ,GETDATE())

--INSERT INTO STATUS_CODES VALUES('IO', 'IOU', 'Open')
--INSERT INTO STATUS_CODES VALUES('IF', 'IOU', 'Filled')
--INSERT INTO STATUS_CODES VALUES('IC', 'IOU', 'User Closed')
--INSERT INTO STATUS_CODES VALUES('IS', 'IOU', 'System Closed')
--INSERT INTO STATUS_CODES VALUES('IP', 'IOU', 'Partial')
--INSERT INTO STATUS_CODES VALUES('IIV', 'IOU', 'Invalidated')





GO


