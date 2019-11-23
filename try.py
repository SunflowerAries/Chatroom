import time
localtime = time.strftime("%a %b %d %H:%M:%S %Y", time.localtime())
print(localtime)
print(type(localtime), len(localtime))