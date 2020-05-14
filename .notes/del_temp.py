import os
path = r'temp\\'
cnt = 0

for filename in os.listdir(path):
    if filename.endswith('.html'):
        os.unlink(path + filename)
        cnt = cnt + 1
        
print (cnt + ' html file(s) removed')
        
path = r'static\\pdf\\'
cnt = 0

for filename in os.listdir(path):
    if filename.endswith('.pdf'):
        os.unlink(path + filename)
        cnt = cnt + 1

print (cnt + ' pdf file(s) removed')

path = r'D:\\Dev\\FLW\\IHS\\RXBackend_mod\\temp\\'

for filename in os.listdir(path):
    if filename.endswith('.html'):
        # print(path + filename)
        os.unlink(path + filename)