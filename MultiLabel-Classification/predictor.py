import os
from pprint import pprint

import imageio
import numpy as np
import torch

from misc import imutils
from net.resnet50_cam import Net
import torch.nn.functional as F

from voc12.dataloader import TorchvisionNormalize

# CAT_LIST = ['aeroplane', 'bicycle', 'bird', 'boat',
#             'bottle', 'bus', 'car', 'cat', 'chair',
#             'cow', 'diningtable', 'dog', 'horse',
#             'motorbike', 'person', 'pottedplant',
#             'sheep', 'sofa', 'train',
#             'tvmonitor']
CAT_LIST = ['bicycle', 'building', 'bus', 'car',
            'fence', 'motorcycle', 'pedestrian', 'pole',
            'rider', 'road', 'sidewalk', 'sky', 'terrain',
            'traffic light', 'traffic sign', 'train',
            'truck', 'vegetation', 'wall']

pth_file_path = os.path.abspath(os.path.join(os.getcwd(), "../MultiLabel-Classification"
                                                          "/sess/res50_cam.pth.pth"))

# state_dict = torch.load("./sess/res50_cam.pth.pth")
state_dict = torch.load(pth_file_path)
model = Net().cuda(0)
model.load_state_dict(state_dict)
model.eval()


def predict(img_path: str) -> dict:
    image = np.asarray(imageio.imread(img_path))
    img_normal = TorchvisionNormalize()
    image = img_normal(image)
    image = imutils.HWC_to_CHW(image)
    image = torch.from_numpy(image)
    image = image.float()
    image = image.cuda(0)
    image = torch.unsqueeze(image, 0)
    # label = np.array([0, 0, 0, 0, 0,
    #                   0, 0, 0, 0, 0,
    #                   0, 0, 1, 0, 1,
    #                   0, 0, 0, 0, 0])

    with torch.no_grad():
        out = model(image)
        # loss = F.multilabel_soft_margin_loss(out, torch.from_numpy(label).cuda(0))
        out = torch.sigmoid(out)
    out = out.cpu().numpy().tolist()[-1]
    results = []
    for idx in range(len(out)):
        if out[idx] >= 0.01:
            results.append({
                "keyword": CAT_LIST[idx],
                "score": int(out[idx] * 1000) / 1000
            })
    results = sorted(results, key=lambda item: -item["score"])
    res_json = {
        "result": results,
        "result_num": len(results)
    }

    return res_json


if __name__ == '__main__':
    res = predict("VOCdevkit/VOC2012_test/JPEGImages/2012_004316.jpg")
    pprint(res)
