USE [RXBackend]
GO
/****** Object:  StoredProcedure [dbo].[close_iou_request]    Script Date: 1/1/2020 11:27:57 AM ******/
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
		ELSE 'NA'
	END;

IF (@STATUS = 'IF' OR @STATUS = 'IC')
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





