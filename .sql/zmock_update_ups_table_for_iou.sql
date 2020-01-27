ALTER PROCEDURE update_ups_table_for_iou
	@UPS_ID INT
AS	
UPDATE [UPS_Shipping].[dbo].[TO_UPS] 
SET PAT_FNAME = c.PAT_FNAME
    ,PAT_LNAME = c.PAT_LNAME 
	,FIL_QTY_DSP = c.FIL_QTY_DSP
	,FIL_PRICE = c.FIL_PRICE
	,DRG_DNAME = c.DRG_DNAME
	,DRG_STRENGTH = c.DRG_STRENGTH
FROM (
	SELECT 
	FIL_ID
	,PAT_FNAME
	,PAT_LNAME
	,FIL_QTY_DSP
	,FIL_PRICE
	,DRG_DNAME
	,DRG_STRENGTH
	FROM
		[UPS_Shipping].[dbo].[_TO_UPS]
	) AS c
WHERE 
    c.FIL_ID = [UPS_Shipping].[dbo].[TO_UPS].FIL_ID
	AND [UPS_Shipping].[dbo].[TO_UPS].ID = @UPS_ID

update UPS_Shipping.dbo._TO_UPS set FIL_QTY_DSP = 256
where ID = 3864976

update UPS_Shipping.dbo._TO_UPS set FIL_QTY_DSP = 140
where ID = 3864980

update UPS_Shipping.dbo.TO_UPS set FIL_QTY_DSP = 14
where ID = 3864976


select * from UPS_Shipping.dbo._TO_UPS 
where ID = 3864976


select * from UPS_Shipping.dbo.TO_UPS 
where ID = 3864976

exec update_ups_table_for_iou 3864976