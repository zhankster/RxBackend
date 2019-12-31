

CREATE TABLE [dbo].[BAT_IOU_TRANS](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[IOU_ID] [int] NOT NULL,
	[ADD_QTY] [decimal](10, 4) NULL,
	[USER] [nchar](10) NOT NULL,
	[TRANS_TYPE] [nchar](20) NULL,
	[TRANS_DATE] [datetime] NOT NULL
);



