USE [RXBackend]
GO

/****** Object:  StoredProcedure [dbo].[put_batch_fill_for_iou]    Script Date: 12/16/2019 4:32:05 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO


CREATE PROC [dbo].[put_batch_fill_for_iou]
(	@TO_UPS_ID INT,
	@QTY INT,
	@TECH NVARCHAR(10)
)
AS

DECLARE @EXISTS BIT;
SET @EXISTS = 0;

SELECT 
	@EXISTS = 1 
FROM 
	BAT_IOU
WHERE 
	[TO_UPS_ID] = @TO_UPS_ID
	AND [CLOSE_DATE] IS NOT NULL

IF (@EXISTS = 0)
	BEGIN 
		INSERT INTO [dbo].[BAT_IOU]
			   ([TO_UPS_ID]
			   ,[QTY]
			   ,[PHARM_TECH]
			   ,[SHIP_TECH]
			   ,[STATUS]
			   ,[CREATED]
			   ,[LAST_USER]
			   ,[LAST_UPDATE]
			   ,[CLOSE_DATE])
		 VALUES
			   (@TO_UPS_ID
			   ,@QTY
			   ,@TECH
			   ,''
			   ,'IO'
			   ,GETDATE()
			   ,''
			   ,NULL
			   ,NULL);
	END
ELSE
	BEGIN
		UPDATE 
			BAT_IOU
		SET
			[QTY] = @QTY
			,[LAST_USER] = @TECH
			,[LAST_UPDATE] = GETDATE()
		WHERE
			[TO_UPS_ID] = @TO_UPS_ID		
	END


GO

