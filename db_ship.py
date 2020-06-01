import collections
import json
import pyodbc

RX_CONNECTION_STRING='DRIVER={SQL Server};SERVER=localhost;DATABASE=RXBackend;Trusted_Connection=yes'
CIPS_CONNECTION_STRING='DRIVER={SQL Server};SERVER=localhost;DATABASE=CIPS;Trusted_Connection=yes'

def get_fac_alt():
    return """ SELECT 
    a.DCODE
    , isnull(f.DNAME, '') as DNAME
    , a.IOU_EMAIL
    , a.IOU_NOTIFY
    , ISNULL(a.MNG, '') MNG
    FROM FAC_ALT a 
    LEFT JOIN CIPS.dbo.FAC f
    on a.DCODE = f.DCODE 
    ORDER by a.DCODE"""
 
def get_mng():
    return """ SELECT 
    CODE
    ,DESCRIPTION
    ,EMAIL
    ,SEND_NOTIFICATION SEND
    FROM MNG_GROUPS
    ORDER BY CODE """
    
# Returs JSON array from database
def get_json(sql):
    conn = pyodbc.connect(RX_CONNECTION_STRING)
    cur = conn.cursor()
    result = cur.execute(sql)

    items = [dict(zip([key[0] for key in cur.description], row)) for row in result]

    return items