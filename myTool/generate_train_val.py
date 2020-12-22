#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'my_pic_note'
__author__ = 'deagle'
__date__ = '11/25/2020 10:51'
# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
"""

from shutil import copyfile
from shutil import rmtree

import random

import datetime
import os


'''
组织 训练集 和 验证集 
'''

percent = 0.7


# read json home to dict
def read_json_path(json_path):
    json_dict = {}
    for root, dirs, files in os.walk(json_path):
        for file in files:
            json = os.path.join(root, file)
            if 'invalid' in json:
                continue
            name = os.path.splitext(os.path.basename(json))[0]
            json_dict[name] = json
    print('total valied json file quantity: %s' % len(json_dict.keys()))
    return json_dict


# read img home to dict
def read_img_path(img_home):
    img_dict = {}
    for root, dirs, files in os.walk(img_home):
        for file in files:
            img = os.path.join(root, file)
            name = os.path.splitext(os.path.basename(img))[0]
            img_dict[name] = img
    print('total valied img quantity: %s' % len(img_dict.keys()))
    return img_dict


def main():
    label_folder = r'D:\work_source\CV_Project\datasets\label_convert\5\labels_yolo'
    img_folder = r'D:\work_source\CV_Project\datasets\label_convert\5\images'
    output = r'D:\work_source\CV_Project\datasets\train_yolo_5'
    if os.listdir(output):
        rmtree(output)
        os.mkdir(output)

    train_label = os.path.join(os.path.join(output, 'train'), 'labels')
    val_label = os.path.join(os.path.join(output, 'val'), 'labels')
    train_img = os.path.join(os.path.join(output, 'train'), 'images')
    val_img = os.path.join(os.path.join(output, 'val'), 'images')

    if not os.path.exists(train_label): os.makedirs(train_label)
    if not os.path.exists(val_label): os.makedirs(val_label)
    if not os.path.exists(train_img): os.makedirs(train_img)
    if not os.path.exists(val_img): os.makedirs(val_img)

    l_dict = read_json_path(label_folder)
    i_dict = read_img_path(img_folder)
    print('sample percent to train:', percent)
    print('train set size: ', int(len(i_dict.keys()) * percent))
    train_list = random.sample(i_dict.keys(), int(len(i_dict.keys()) * percent))
    val_list = [i for i in i_dict.keys() if i not in train_list]
    print('val set size:', len(val_list))

    for t in train_list:
        copyfile(l_dict[t], os.path.join(train_label, os.path.basename(l_dict[t])))
        copyfile(i_dict[t], os.path.join(train_img, os.path.basename(i_dict[t])))

    for v in val_list:
        copyfile(l_dict[v], os.path.join(val_label, os.path.basename(l_dict[v])))
        copyfile(i_dict[v], os.path.join(val_img, os.path.basename(i_dict[v])))


if __name__ == '__main__':
    start_time = datetime.datetime.now()
    main()
    print('time cost: %s' % str(datetime.datetime.now() - start_time).split('.')[0])
