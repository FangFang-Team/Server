import argparse
import json

import voc12.dataloader
import numpy as np
from tqdm import tqdm

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--train_list", default=r'F:\Coco_City\data\train_anno.json', type=str)
    parser.add_argument("--val_list", default=r'F:\Coco_City\data\val_anno.json', type=str)
    # parser.add_argument("--out", default="cls_labels.npy", type=str)
    parser.add_argument("--out", default="cls2_labels.npy", type=str)

    # parser.add_argument("--voc12_root", default=r"F:\Code_WorkSpace\PyWorkSpace\Interactive_Graphic_Annotation_System"
    #                                             r"\Multi-label_Natural_Image_Classification_Tag_System\VOCdevkit"
    #                                             r"\VOC2012", type=str)
    args = parser.parse_args()

    with open(args.train_list, "r") as f:
        train_list = json.load(f)

    with open(args.val_list, "r") as f:
        val_list = json.load(f)

    train_val_list = np.concatenate([train_list, val_list], axis=0)

    d = dict()

    for item in tqdm(train_val_list):
        file_name = item["file_name"]
        label = np.zeros(19, dtype=np.float32)
        label_index = item["labels"]
        for idx in label_index:
            label[idx] = 1

        d[file_name] = label

    np.save(args.out, d)

    # train_name_list = voc12.dataloader.load_img_name_list(args.train_list)
    # val_name_list = voc12.dataloader.load_img_name_list(args.val_list)
    #
    # train_val_name_list = np.concatenate([train_name_list, val_name_list], axis=0)
    # label_list = voc12.dataloader.load_image_label_list_from_xml(train_val_name_list, args.voc12_root)
    #
    # total_label = np.zeros(20)
    #
    # d = dict()
    # for img_name, label in zip(train_val_name_list, label_list):
    #     d[img_name] = label
    #     total_label += label
    #
    # print(total_label)
    # np.save(args.out, d)
    pass