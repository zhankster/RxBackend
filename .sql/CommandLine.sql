EXEC sp_configure 'show advanced options', 1;
GO
Reconfigure;
GO
 
EXEC sp_configure 'xp_cmdshell',1
GO
Reconfigure
GO

xp_cmdshell 'ping 192.168.50.202';

xp_cmdshell 'python D:\Dev\py\pdf\p.py';

xp_cmdshell 'python C:\inetpub\wwwroot\RXBackend\del_temp.py';

