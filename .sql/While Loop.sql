DECLARE @#IOU TABLE (ADDRESS VARCHAR(256));
INSERT INTO @#IOU 
SELECT ADDRESS ADDRESS FROM FAC_EMAIL WHERE IOU = 1 and FAC_CODE = 'AD'

DECLARE @ADDRESSES varchar(2000),
@ADDRESS varchar(256);
SET @ADDRESSES = '';

WHILE EXISTS (SELECT ADDRESS FROM @#IOU)
BEGIN
	SELECT TOP 1 @ADDRESS = ADDRESS FROM @#IOU
	SET @ADDRESSES += @ADDRESS + ';';
	PRINT @ADDRESSES;
	DELETE FROM @#IOU WHERE ADDRESS = @ADDRESS;
END

PRINT @ADDRESSES;