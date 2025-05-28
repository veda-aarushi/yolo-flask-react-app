# backend/sort.py
import numpy as np
from filterpy.kalman import KalmanFilter

def iou(bb_test, bb_gt):
    # compute IoU between two bboxes in [x1,y1,x2,y2]
    xx1 = max(bb_test[0], bb_gt[0])
    yy1 = max(bb_test[1], bb_gt[1])
    xx2 = min(bb_test[2], bb_gt[2])
    yy2 = min(bb_test[3], bb_gt[3])
    w = max(0., xx2 - xx1)
    h = max(0., yy2 - yy1)
    inter = w * h
    area1 = (bb_test[2]-bb_test[0])*(bb_test[3]-bb_test[1])
    area2 = (bb_gt[2]-bb_gt[0])*(bb_gt[3]-bb_gt[1])
    return inter / (area1 + area2 - inter)

class Track:
    def __init__(self, bbox, tid):
        # bbox = [x1,y1,x2,y2,conf]
        self.id = tid
        self.kf = KalmanFilter(dim_x=7, dim_z=4)
        # State: [x,y,w,h, vx,vy,vw,vh]
        # F matrix for dt=1 constant velocity
        self.kf.F = np.eye(7)
        for i in range(4):
            self.kf.F[i, i+3] = 1.
        self.kf.H = np.zeros((4,7)); self.kf.H[:4,:4]=np.eye(4)
        self.kf.R *= 10.
        x1,y1,x2,y2,conf = bbox
        w,h = x2-x1, y2-y1
        self.kf.x[:4] = np.array([x1,y1,w,h]).reshape((4,1))
        self.time_since_update = 0

    def predict(self):
        self.kf.predict()
        self.time_since_update += 1
        x,y,w,h = self.kf.x[:4].reshape(-1)
        return [x, y, w, h]

    def update(self, bbox):
        self.time_since_update = 0
        self.kf.update(np.array(bbox[:4]))

class Sort:
    def __init__(self, iou_threshold=0.3):
        self.tracks = []
        self.next_id = 1
        self.iou_thres = iou_threshold

    def update(self, detections):
        # detections: list of [x1,y1,x2,y2,conf]
        updated_tracks = []

        for det in detections:
            best, best_iou = None, 0
            for tr in self.tracks:
                pred = tr.predict()
                bb_pred = [pred[0], pred[1], pred[0]+pred[2], pred[1]+pred[3]]
                this_iou = iou(det, bb_pred)
                if this_iou > best_iou:
                    best_iou, best = this_iou, tr
            if best and best_iou >= self.iou_thres:
                best.update(det)
                updated_tracks.append(best)
            else:
                tr = Track(det, self.next_id)
                self.next_id += 1
                updated_tracks.append(tr)

        self.tracks = updated_tracks
        # return array [[x1,y1,x2,y2,id],...]
        out = []
        for tr in self.tracks:
            x,y,w,h = tr.predict()
            out.append([x, y, x+w, y+h, tr.id])
        return np.array(out)
