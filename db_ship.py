import collections
import json
import pyodbc

def get_fac_alt():
    return """ SELECT 
    a.DCODE
    , isnull(f.DNAME, '') as DNAME
    , a.IOU_EMAIL
    , a.IOU_NOTIFY
    , ISNULL(a.MNG, '') MNG
    FROM FAC_ALT a 
    LEFT JOIN CIPS.dbo.FAC f
    on a.DCODE = f.DCODE """
 
def get_mng():
    return """ SELECT 
    CODE
    ,DESCRIPTION
    ,EMAIL
    ,SEND_NOTIFICATION SEND
    FROM MNG_GROUPS """