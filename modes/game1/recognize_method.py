from collections import deque
import math
import cv2
import numpy as np

class HorizontalRecognition:
    def __init__(self, amp_on=0.05, amp_off=0.02, min_interval=0.25):
        # 門檻值調低，因為手指相對於手腕的移動範圍比手臂小
        self.amp_on = amp_on
        self.amp_off = amp_off
        self.min_interval = min_interval

        self.state = "CENTER"
        self.last_switch_t = 0.0
        self.half_swings = 0
        self.count = 0

    def update(self, origin_xy, target_xy, t_sec):
        ox, _ = origin_xy
        tx, _ = target_xy
        dx = tx - ox  # 指尖相對於手腕的 X 偏移

        prev_state = self.state
        if self.state == "CENTER":
            if dx >= self.amp_on:
                self.state = "RIGHT"
            elif dx <= -self.amp_on:
                self.state = "LEFT"
        elif self.state == "RIGHT":
            if dx <= self.amp_off:
                self.state = "CENTER"
        elif self.state == "LEFT":
            if dx >= -self.amp_off:
                self.state = "CENTER"

        new_counts = 0
        if prev_state == "CENTER" and self.state in ("RIGHT", "LEFT"):
            if (t_sec - self.last_switch_t) >= self.min_interval:
                self.last_switch_t = t_sec
                self.half_swings += 1
                if self.half_swings >= 2:
                    self.half_swings = 0
                    self.count += 1
                    new_counts = 1

        return new_counts

class VerticalRecognition:
    def __init__(self, amp_on=0.35, amp_off=0.15, min_interval=0.25):
        self.amp_on = amp_on
        self.amp_off = amp_off
        self.min_interval = min_interval

        self.state = "CENTER"
        self.last_switch_t = 0.0
        self.half_swings = 0
        self.count = 0

    def update(self, origin_xy, target_xy, t_sec):
        _, oy = origin_xy
        _, ty = target_xy
        dy = ty - oy  # 指尖相對於手腕的 Y 偏移
        prev_state = self.state
        if self.state == "CENTER":
            if dy >= -self.amp_on:
                self.state = "DOWN"
            elif dy <= -self.amp_on:
                self.state = "UP"
        elif self.state == "DOWN":
            if dy <= -self.amp_off:
                self.state = "CENTER"
        elif self.state == "UP":
            if dy >= -self.amp_off:
                self.state = "CENTER"

        new_counts = 0
        if prev_state == "CENTER" and self.state in ("DOWN", "UP"):
            if (t_sec - self.last_switch_t) >= self.min_interval:
                self.last_switch_t = t_sec
                self.half_swings += 1
                if self.half_swings >= 2:
                    self.half_swings = 0
                    self.count += 1
                    new_counts = 1

        return new_counts


class CircularRecognition:
    def __init__(self, k_step=5, direction="CCW", threshold=15):
        self.k_step = k_step
        self.direction = direction

        # 軌跡點歷史
        self.point_hist = deque(maxlen=20)

        # 轉彎一致性累積 (這裡我們累積「左彎」或「右彎」的次數或強度)
        self.bend_acc = 0
        self.total = 0

        # 判定門檻：累積多少次「一致的轉彎」算一圈
        self.threshold = threshold

    def update(self, origin_xy, target_xy):
        # 1. 座標轉換：依然以手腕為參考點 (ox, oy)
        ox, oy = origin_xy
        tx, ty = target_xy

        # 這裡不需要處理角度，直接記錄相對座標 (vx, vy)
        # 鏡像處理依然保留，確保左右手一致
        vx = -(tx - ox)
        vy = (ty - oy)

        self.point_hist.append((vx, vy))

        if len(self.point_hist) < 3:
            return 0

        # 2. 取得連續三個點 (間隔 k_step 幀以過濾雜訊)
        # 這裡我們用當前點、幾幀前的點、以及更早的點
        p3 = self.point_hist[-1]
        p2 = self.point_hist[-1 - self.k_step] if len(self.point_hist) > self.k_step else self.point_hist[
            len(self.point_hist) // 2]
        p1 = self.point_hist[0]

        # 3. 計算位移向量
        ax, ay = p2[0] - p1[0], p2[1] - p1[1]
        bx, by = p3[0] - p2[0], p3[1] - p2[1]

        # 4. 計算叉積 (Cross Product)
        # 在影像座標系中，Z > 0 是向右彎(CW)，Z < 0 是向左彎(CCW)
        # (這裡的正負號會隨鏡像與 Y 軸定義改變，建議實測觀察)
        cross_product = ax * by - ay * bx

        # 5. 一致性累積邏輯
        # 我們不累積角度，我們累積「轉向的正確性」
        if self.direction == "CCW":
            score = -cross_product  # 假設向左彎為負，取負變正
        else:
            score = cross_product

        # 這裡用一個簡單的「連續判定」
        if score > 0.0001:  # 有在轉彎
            self.bend_acc += 1
        elif score < -0.0001:  # 轉錯方向，立刻重置
            self.bend_acc = 0

        # 6. 結算
        new_loops = 0
        if self.bend_acc >= self.threshold:
            self.total += 1
            new_loops = 1
            self.bend_acc = 0  # 完成一圈，重置

        return new_loops