USE [RXBackend]
GO

/****** Object:  StoredProcedure [dbo].[batch_detail_for_processing_iou]    Script Date: 12/10/2019 11:10:17 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

ALTER PROC [dbo].[batch_detail_for_processing_iou]
	@BATCH_ID INT
AS
BEGIN

DECLARE @EXCEPTION INT;

SELECT @EXCEPTION=EXCEPTION_FLAG FROM BAT_COMPLETE WHERE DEL_BAT_ID=@BATCH_ID;

IF @EXCEPTION = 1
	BEGIN		
		SELECT
			 ex.DEL_BAT_ID
			,ex.EXCEPTION_CODE
			,ex.TO_UPS_ID
			,a.FAC_DCODE + ' - ' + a.FAC_DNAME as FACILITY
			,a.FAC_DCODE
			,a.ID
			,a.PAT_ID 
			,a.FIL_ID 
			,a.FIL_KOP 
			,a.PAT_LNAME + ', ' + a.PAT_FNAME as NAME 
			,a.DRG_DNAME
			,a.DRG_STRENGTH 
			,a.FIL_QTY_DSP as QTY 
			,a.FAC_NOT_DTEXT as SHIP
			,c.TCH_INITIALS as TECH 
			,dbo.FAC_HIGHLIGHT_COLOR(a.FAC_DCODE) as COLOR
			, 'Y' as EXCEPTION
			,ISNULL(i.STATUS, 'NA') as STATUS
			,ISNULL(QTY, 0) IOU_QTY
		FROM 
			BAT_EXCEPTIONS  ex
			LEFT JOIN [UPS_Shipping].[dbo].[TO_UPS] a
				ON a.ID=ex.TO_UPS_ID
			LEFT JOIN [CIPS].[dbo].[DEL_BAT] b 
				ON a.DEL_BAT_ID = b.ID
			LEFT JOIN [CIPS].[dbo].[USR] c 
				ON b.PRINT_USR_ID = c.ID
			LEFT JOIN [RXBackend].[dbo].[BAT_PRE_PROCESSED] e
				ON a.DEL_BAT_ID=e.DEL_BAT_ID
			LEFT JOIN [RXBackend].[dbo].[BAT_IOU] i
				ON a.DEL_BAT_ID = i.DEL_BAT_ID AND a.FIL_ID = i.FIL_ID
		WHERE
			ex.DEL_BAT_ID=@BATCH_ID
			-- ADDED FOR CIPS 08/2018 UPGRADE
			AND a.FIL_QTY_DSP > 0 
			AND ex.EXCEPTION_CODE >=200 AND ex.EXCEPTION_CODE < 400
		ORDER BY
			 a.FIL_KOP
			,NAME;
	END
-- No Exception.  Pull the entire batch.
ELSE
	BEGIN
		SELECT 
			 a.DEL_BAT_ID
			,a.FAC_DCODE + ' - ' + a.FAC_DNAME as FACILITY
			,a.FAC_DCODE
			,a.ID
			,a.PAT_ID 
			,a.FIL_ID 
			,a.FIL_KOP 
			,a.PAT_LNAME + ', ' + a.PAT_FNAME as NAME 
			,a.DRG_DNAME
			,a.DRG_STRENGTH 
			,a.FIL_QTY_DSP as QTY 
			,a.FAC_NOT_DTEXT as SHIP 
			,c.TCH_INITIALS as TECH 
			,dbo.FAC_HIGHLIGHT_COLOR(a.FAC_DCODE) as COLOR
			,'N' as EXCEPTION
			,ISNULL(i.STATUS, 'NA') as STATUS
			,ISNULL(QTY, 0) IOU_QTY
		FROM 
			[UPS_Shipping].[dbo].[TO_UPS] a
			LEFT JOIN [CIPS].[dbo].[DEL_BAT] b 
				ON a.DEL_BAT_ID = b.ID
			LEFT JOIN [CIPS].[dbo].[USR] c 
				ON b.PRINT_USR_ID = c.ID
			LEFT JOIN [RXBackend].[dbo].[BAT_COMPLETE] d
				ON d.DEL_BAT_ID=a.DEL_BAT_ID 
			LEFT JOIN [RXBackend].[dbo].[BAT_PRE_PROCESSED] e
				ON a.DEL_BAT_ID=e.DEL_BAT_ID
			LEFT JOIN [BAT_EXCEPTIONS] ex
				ON a.DEL_BAT_ID=ex.DEL_BAT_ID
			LEFT JOIN [RXBackend].[dbo].[BAT_IOU] i
				ON a.DEL_BAT_ID = i.DEL_BAT_ID AND a.FIL_ID = i.FIL_ID
		WHERE 
			 a.DEL_BAT_ID = @BATCH_ID
			-- ADDED FOR CIPS 08/2018 UPGRADE
	 		AND a.FIL_QTY_DSP > 0
		ORDER BY
			 a.FIL_KOP
			,NAME;
	END
END

GO


