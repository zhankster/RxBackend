USE [RXBackend]
GO

/****** Object:  StoredProcedure [dbo].[put_batch_fill_for_iou]    Script Date: 5/14/2020 2:22:29 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO


CREATE PROC [dbo].[put_batch_fill_for_iou]
(	@TO_UPS_ID INT,
	@QTY DECIMAL(10,4),
	@TECH NVARCHAR(10)
)
AS

DECLARE @NEXT_INT INT;

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


GO


