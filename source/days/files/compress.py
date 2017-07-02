#!/usr/bin/env python  
import Image  
import os  
import os.path  
import sys 

##set working path
path = './jan2017/01022017'

rootP = ''
cnt = 1
for root,dirs,files in os.walk(path):
    #sort by filename, avoid mistake
    files.sort()
    for f in files:
        if root != rootP:
            cnt = 1
        if 'md' in f:
            continue
        else:
            fp = os.path.join(root, f)
            img = Image.open(fp)
            w, h = img.size
            img.resize((1200, 800)).save(root+'/'+str(cnt), "JPEG")
            rootP = root
            cnt+=1
            print fp
