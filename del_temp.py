import os
path = r'D:\\Dev\\FLW\\IHS\\RXBackend_mod\\temp\\'

for filename in os.listdir(path):
    if filename.endswith('.html'):
        # print(path + filename)
        os.unlink(path + filename)