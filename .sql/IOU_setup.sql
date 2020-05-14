select * from users where username like 'h%' or username like 'b%'
31 - hanka 4 - bryant 6 - dakotar
select * from user_role where USER_ID in (31,4,6, 35)
select u.* from users u inner join USER_ROLE r on u.id = r.ID where r.ROLE_ID = 1
select * from role
exec [dbo].[get_user_by_id] 35
EXEC get_user_by_username 'hallen'
EXEC get_user_by_username 'bryant'

select * from UPS_Shipping.dbo.TO_UPS where DEL_BAT_ID = 584263
select * from UPS_Shipping.dbo.TO_UPS where FIL_ID = 9198314
select * from UPS_Shipping.dbo.TO_UPS where FIL_ID = 9198042
--INSERT INTO dbo.[role] VALUES('PharmTech')

--update USER_ROLE set ROLE_ID = 1 where id = 31
exec [dbo].[get_user_by_username] 'hanka'
EXEC dbo.batch_detail_for_pre_processing 583938
EXEC dbo.batch_detail_for_processing_facility 583938
EXEC dbo.todays_all_rx_by_facility 'AH'
EXEC [dbo].get_batch_total_cost 583938
EXEC [dbo].[batch_detail_for_pre_processing] 584236
EXEC [dbo].[batch_detail_for_processing_iou] 584236
EXEC [dbo].[batch_detail_for_completing_iou]
select * from UPS_Shipping.dbo.TO_UPS where DEL_BAT_ID = 584236
update UPS_Shipping.dbo.TO_UPS set FIL_QTY_DSP = 10.558 where FIL_ID = 9198042

select  DISTINCT DEL_BAT_ID, FAC_DCODE from UPS_Shipping.dbo.TO_UPS where DEL_BAT_ID in (583938, 583972,584370)
select  * from UPS_Shipping.dbo.TO_UPS where DEL_BAT_ID in (583938, 583972,584370)
EXEC [dbo].[batch_detail_for_processing_iou] 584263

update UPS_Shipping.dbo.TO_UPS set FIL_DATE = CAST(GETDATE() as DATE) --'2019-12-11 00:00:00.000'

delete from BAT_PRE_PROCESSED
delete from BAT_COMPLETE
delete from BAT_RECONCILED
select * from BAT_PRE_PROCESSED
select * from BAT_COMPLETE
select * from BAT_RECONCILED
select * from [dbo].[BAT_EXCEPTIONS]
--truncate table [dbo].[BAT_IOU]
--truncate table [dbo].[BAT_IOU_TRANS]
select * from [dbo].[BAT_IOU] order by CREATED desc
select * from [dbo].[BAT_IOU_TRANS] order by TRANS_DATE desc
select * from [dbo].[STATUS_CODES]

--Mock records for RX Processing
INSERT INTO BAT_PRE_PROCESSED VALUES (584381, GETDATE(), 'NA')
INSERT INTO BAT_PRE_PROCESSED VALUES (584263, GETDATE(), 'NA')
INSERT INTO BAT_PRE_PROCESSED VALUES (584370, GETDATE(), 'NA')
SELECT * FROM BAT_PRE_PROCESSED

--Mock records for Complete
INSERT INTO BAT_COMPLETE VALUES (584381,'OE','NA','NA', 1,'NA', GETDATE(),0)
INSERT INTO BAT_COMPLETE VALUES (584263, 'WY','NA','NA', 1,'NA', GETDATE(),0)
INSERT INTO BAT_COMPLETE VALUES (584370, 'AH', 'NA','NA', 1,'NA', GETDATE(),0)
SELECT * FROM BAT_COMPLETE

--Mock records for Reconciled
INSERT INTO BAT_RECONCILED VALUES (584381,'NA', GETDATE())
INSERT INTO BAT_RECONCILED VALUES (584263, 'NA', GETDATE())
INSERT INTO BAT_RECONCILED VALUES (584370, 'NA', GETDATE())
SELECT * FROM BAT_RECONCILED

SELECT DISTINCT DEL_BAT_ID from UPS_Shipping.dbo.TO_UPS
exec [dbo].[batch_detail_for_processing_iou] 584263
EXEC dbo.batch_detail_for_completing_iou 
exec [dbo].[close_iou_request] 3863331, 'RH', 'IC'
select * from STATUS_CODES
select * from [dbo].[BAT_IOU]

SELECT
	a.id
	,a.username
	,a.password
	,a.salt
	,a.enabled
	,c.description as role
	,a.INTIALS as initials
FROM
	[RXBackend].[dbo].[users] a
	LEFT JOIN [RXBackend].[dbo].[user_role] b
		on a.ID=b.id
	LEFT JOIN [RXBackend].[dbo].[role] c
		on b.role_id=c.id
WHERE
	a.username='hanka'
	AND a.enabled = 1

SELECT
	a.id
	,a.username
	,a.password
	,a.salt
	,a.enabled
	,c.description as role
	,a.INTIALS as initials
FROM
	[RXBackend].[dbo].[users] a
	LEFT JOIN [RXBackend].[dbo].[user_role] b
		on a.ID=b.user_id
	LEFT JOIN [RXBackend].[dbo].[role] c
		on b.role_id=c.id
WHERE
	a.username='hanka'
	AND a.enabled = 1


ALTER TABLE table_name
ADD column_name data_type column_constraint;

ID	DESC
1	COMPLETE
2	COMPLETE WITH EXCEPTION
3	COMPLETE WITH UNFILLABLE

INSERT 	COMPLETE
2	COMPLETE WITH EXCEPTION
3	COMPLETE WITH UNFILLABLE

INSERT INTO STATUS_CODES VALUES('IO', 'IOU', 'Open')
INSERT INTO STATUS_CODES VALUES('IF', 'IOU', 'Filled')
INSERT INTO STATUS_CODES VALUES('IC', 'IOU', 'User Closed')
INSERT INTO STATUS_CODES VALUES('IS', 'IOU', 'System Closed')
INSERT INTO STATUS_CODES VALUES('IP', 'IOU', 'Partial')
INSERT INTO STATUS_CODES VALUES('IIV', 'IOU', 'Invalidated')
--TRUNCATE TABLE STATUS_CODES
SELECT *  FROM STATUS_CODES

select * from users where username like 'h%' or username like 'b%'
31 - hanka 4 - bryant 6 - dakotar
select * from user_role where USER_ID in (31,4,6, 35, 33)
select u.* from users u inner join USER_ROLE r on u.id = r.ID where r.ROLE_ID = 1
select * from role
exec [dbo].[get_user_by_id] 35
EXEC get_user_by_username 'dadams'
EXEC get_user_by_username 'bryant'

SELECT
	a.id
	,a.username
	,a.password
	,a.salt
	,a.enabled
	,c.description as role
	,a.INTIALS as initials
	,b.ROLE_ID
	,b.USER_ID ROLE_
FROM
	[RXBackend].[dbo].[users] a
	LEFT JOIN [RXBackend].[dbo].[user_role] b
		on a.ID=b.ID
	LEFT JOIN [RXBackend].[dbo].[role] c
		on b.role_id=c.id
WHERE
	a.username='hallen'
	AND a.enabled = 1
SELECT * INTO [UPS_Shipping].[dbo]._TO_UPS FROM [UPS_Shipping].[dbo].[TO_UPS]
--EXEC update_ups_table_for_iou

ALTER PROC	[dbo].[get_iou_total_cost]
@IOU_ID INT, @QTY DECIMAL(10,4)
AS
BEGIN
SELECT 
20 * @QTY AS EXT_COST

END

[dbo].[get_iou_total_cost] 10, 84
78 28 IF 0 28 28 hanka
