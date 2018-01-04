# -*-coding:utf-8-*-
from PIL import Image
im = Image.open("test_photo.jpg")
# 获取图片的宽度和高度
img_size = im.size
print("图片宽度和高度分别是{}".format(img_size))
'''
裁剪：传入一个元组作为参数
元组里的元素分别是：（距离图片左边界距离x， 距离图片上边界距离y，
距离图片左边界距离+裁剪框宽度x+w，距离图片上边界距离+裁剪框高度y+h）
'''

x = 260
y = 260
w = 580
h = 960
region = im.crop((x, y, x+w, y+h))
region.save("testedphoto.jpg")




