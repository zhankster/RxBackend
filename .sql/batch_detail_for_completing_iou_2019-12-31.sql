USE [RXBackend]
GO
/****** Object:  StoredProcedure [dbo].[batch_detail_for_completing_iou]    Script Date: 12/31/2019 10:32:06 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

ALTER PROC [dbo].[batch_detail_for_completing_iou]
AS
BEGIN
	BEGIN
		SELECT 
			a.ID
			,a.DEL_BAT_ID
			,a.FIL_ID
			,a.FIL_KOP 
			,a.FIL_DATE
			,a.FAC_DCODE + ' - ' + a.FAC_DNAME as FACILITY
			,a.PAT_ID 
			,a.PAT_LNAME + ', ' + a.PAT_FNAME as NAME 
			,a.DRG_DNAME
			,a.DRG_STRENGTH 
			,a.FIL_QTY_DSP as FILL_QTY 
			,i.CREATED as IOU_DATE
			,i.CREATED_BY as PHARM_TECH
			,i.STATUS as STAT_CODE
			,ISNULL(s.DESCRIPTION, 'NA') as STAT_DESC
			,dbo.FAC_HIGHLIGHT_COLOR(a.FAC_DCODE) as COLOR
			,ISNULL(i.[STATUS], 'NA') as [STATUS]
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
			LEFT JOIN [RXBackend].[dbo].[BAT_IOU] i
				ON a.ID = i.TO_UPS_ID 
			LEFT JOIN [RXBackend].[dbo].[STATUS_CODES] s
				ON i.STATUS = s.CODE
		WHERE 
			i.ID is not null
			and i.STATUS = 'IO'
		ORDER BY
			 a.FAC_DCODE + ' - ' + a.FAC_DNAME,a.PAT_LNAME + ', ' + a.PAT_FNAME
	END
END

