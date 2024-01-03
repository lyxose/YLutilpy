
# %% 
import cv2
import os
import random

def frame2video(path='_temp_VideoData',vidname='output'):
    '''
    path: the folder of frames (file names: 0.jpg, 1.jpg, 2.jpg...)
    ***
    All the frames should be with the same size
    '''
    img = cv2.imread(f'{path}/0.jpg')  #读取第一张图片
    fps = 25
    imgInfo = img.shape
    size = (imgInfo[1],imgInfo[0])  #获取图片宽高度信息
    print(size)
    fourcc = cv2.VideoWriter_fourcc(*"DVIX")
    videoWrite = cv2.VideoWriter(f'{vidname}.mp4',fourcc,fps,size)# 根据图片的大小，创建写入对象 （文件名，支持的编码器，5帧，视频大小（图片大小））

    files = os.listdir(f'{path}/')
    out_num = len(files)
    for i in range(0,out_num):
        fileName = f'{path}/'+str(i)+'.jpg'    #循环读取所有的图片,假设以数字顺序命名
        img = cv2.imread(fileName)
        videoWrite.write(img)# 将图片写入所创建的视频对象
    videoWrite.release()
# %%
