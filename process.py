import os
for fn in os.listdir('.'):
	if os.path.isfile(fn):
		os.rename(fn, fn.replace('filename','').replace('.png','').zfill(3)+'.png')
		print fn
