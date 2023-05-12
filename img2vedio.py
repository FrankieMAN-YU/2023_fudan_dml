"""
Created on Tue May 12 20:16:06 2023
@author: Manyu Li
@credit: zqq
"""
import os
from PIL import Image
import cv2
import json
import time
from tqdm import tqdm
from glob import glob


def image_to_video(image_path, media_path):
    '''
    图片合成视频函数
    :param image_path: 图片路径
    :param media_path: 合成视频保存路径
    :return:
    '''
    # 获取图片路径下面的所有图片名称
    # image_names = os.listdir(image_path)
    image_names = glob(f"{image_path}*.jpg")
    for i in range(len(image_names)):
        image_names[i] = image_names[i].split("/")[-1]
    # 对提取到的图片名称进行排序
    image_names.sort(key=lambda n: int(n[:-4]))
    # 设置写入格式
    fourcc = cv2.VideoWriter_fourcc('M', 'P', '4', 'V')
    # 设置每秒帧数
    fps = 30  # 由于图片数目较少，这里设置的帧数比较低
    # 读取第一个图片获取大小尺寸，因为需要转换成视频的图片大小尺寸是一样的
    image = Image.open(image_path + image_names[0])
    # 初始化媒体写入对象
    media_writer = cv2.VideoWriter(media_path, fourcc, fps, image.size)
    # 遍历图片，将每张图片加入视频当中
    for image_name in image_names:
        im = cv2.imread(os.path.join(image_path, image_name))
        media_writer.write(im)
    # 释放媒体写入对象
    media_writer.release()
    print(f'视频{vedio_name}写入完成！')

for image_path in tqdm(glob("./test/*/")):
    # 图片路径
    vedio_name = image_path.split("/")[-2]
#     image_path =  "./test/wg2022_ir_020_split_08/"
    # 视频保存路径+名称
    media_path = f"videos/{vedio_name}.mp4"
    # 调用函数，生成视频
    image_to_video(image_path, media_path)

