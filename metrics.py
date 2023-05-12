"""
Created on Tue May 12 19:22:11 2023
@author: Manyu Li
"""
import json
from tqdm import tqdm

def calc_iou(bbox1, bbox2):
    '''
    input bbox1 -> (xmin, ymin, width, height)
    input bbox2 -> (xmin, ymin, width, height)
    return iou between bbox1 and bbox2
    '''
    bbox1_area = bbox1[2] * bbox1[3]
    bbox2_area = bbox2[2] * bbox2[3]
    total_area = bbox1_area + bbox2_area
    
    xmin, ymin, xmax, ymax = max(bbox1[0], bbox1[0]), max(bbox1[1], bbox2[1]), \
                             min(bbox1[0] + bbox1[2], bbox1[0] + bbox2[2]), min(bbox1[1] + bbox1[3], bbox1[1] + bbox2[3])
    if xmin >= xmax or ymin >= ymax: return 0
    else:
        inter = (xmax - xmin) * (ymax - ymin)
        return inter / (total_area - inter)
    
def custom_acc(pre_json_path, gt_json_path):
    with open(pre_json_path, 'r') as f:
        pred = json.load(f)
    with open(gt_json_path, 'r') as f:
        gt = json.load(f)
    T = len(pred['res'])
    Tstar = acc1 = acc2 = 0
    alpha = 0.2
    p = 0.3
    for i in tqdm(range(T)):
        if gt['exist'][i] == 1:
            delta = 1
            Tstar += 1
            if len(pred['res'][i]) == 0: pt = 1
            else: pt = 0
        else:
            delta = 0

        if pt == 0 and delta == 1:
            # detected
            acc1 += calc_iou(pred['res'][i], gt['gt_rect'][i])
        if pt == 0 and delta == 0:
            # target on empty bg
            pass
        if pt == 1 and delta == 1:
            # leak object
            acc2 += 1
        if pt == 1 and delta == 0:
            # bg
            acc1 += 1
    return acc1 / T - alpha * pow(acc2/Tstar, p)


if __name__ == "__main__":
    pre_json_path = "20190925_111757_1_2.json"
    gt_json_path = "IR_label.json"
    custom_acc(pre_json_path, gt_json_path)