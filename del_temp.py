import os
# path = r'C:\inetpub\wwwroot\RXBackend\temp\'
path = os.path.join("C:", os.sep,"inetpub", "wwwroot", "RXBackend", "temp")
cnt = 0

for filename in os.listdir(path):
    if filename.endswith('.html'):
        os.unlink(path + '\\' + filename)
        cnt = cnt + 1
        
print (str(cnt) + ' html file(s) removed')
        
# path = r'C:\\inetpub\\wwwroot\\RXBackend\\static\pdf\\'
path = os.path.join("C:", os.sep,"inetpub", "wwwroot", "RXBackend", "static", 'pdf')
cnt = 0

for filename in os.listdir(path):
    if filename.endswith('.pdf'):
        os.unlink(path +  '\\' + filename)
        cnt = cnt + 1

print (str(cnt) + ' pdf file(s) removed')