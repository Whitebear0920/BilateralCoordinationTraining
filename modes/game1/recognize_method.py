from collections import deque
import math

class HorizontalRecognition:
    def __init__(self, amp_on=0.08, amp_off=0.04, min_interval=0.25):
        self.amp_on = amp_on
        self.amp_off = amp_off
        self.min_interval = min_interval

        self.state = "CENTER"
        self.last_switch_t = 0.0
        self.half_swings = 0
        self.count = 0

    def update(self, shoulder_xy, wrist_xy, t_sec):
        sx, _ = shoulder_xy
        wx, _ = wrist_xy
        dx = wx - sx

        # 用 hysteresis 判斷目前屬於哪個區域
        prev_state = self.state
        if self.state == "CENTER":
            if dx >= self.amp_on:
                self.state = "RIGHT"
            elif dx <= -self.amp_on:
                self.state = "LEFT"
        elif self.state == "RIGHT":
            # 回到中間帶才允許離開 RIGHT，避免抖動
            if dx <= self.amp_off:
                self.state = "CENTER"
        elif self.state == "LEFT":
            if dx >= -self.amp_off:
                self.state = "CENTER"

        # 只有在 CENTER 狀態，且跨到另一側時才算一次「半擺動」
        new_counts = 0
        if prev_state in ("RIGHT", "LEFT") and self.state == "CENTER":
            # 剛離開極值側，等待下一次進入另一側
            pass

        # 當從 CENTER 進入 RIGHT/LEFT，視為到達一側（可能形成 half-swing）
        if prev_state == "CENTER" and self.state in ("RIGHT", "LEFT"):
            # 最小時間間隔 gate（防抖）
            if (t_sec - self.last_switch_t) >= self.min_interval:
                self.last_switch_t = t_sec
                self.half_swings += 1
                # 兩次 half = 一次完整往返
                if self.half_swings >= 2:
                    self.half_swings = 0
                    self.count += 1
                    new_counts = 1

        return new_counts

class VerticalRecognition:
    def __init__(self, amp_on=0.08, amp_off=0.04, min_interval=0.25):
        self.amp_on = amp_on
        self.amp_off = amp_off
        self.min_interval = min_interval

        self.state = "CENTER"  # CENTER / DOWN / UP
        self.last_switch_t = 0.0
        self.half_swings = 0
        self.count = 0

    def update(self, shoulder_xy, wrist_xy, t_sec):
        _, sy = shoulder_xy
        _, wy = wrist_xy
        dy = wy - sy

        prev_state = self.state
        if self.state == "CENTER":
            if dy >= self.amp_on:
                self.state = "DOWN"
            elif dy <= -self.amp_on:
                self.state = "UP"
        elif self.state == "DOWN":
            if dy <= self.amp_off:
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
    def __init__(self, k_min=0.7, w_min=0.8, w_max=12.0, max_step=0.8, k_step=4, direction = "CCW"):
        self.k_min = k_min
        self.w_min = w_min
        self.w_max = w_max
        self.max_step = max_step
        self.k_step = k_step
        self.direction = direction

        self.theta_hist = deque(maxlen=30)  # 存 (t, theta)
        self.acc = 0.0
        self.total = 0

    @staticmethod
    def _unwrap_dtheta(d):
        if d > math.pi:  d -= 2*math.pi
        if d < -math.pi: d += 2*math.pi
        return d

    def update(self, shoulder_xy, elbow_xy, wrist_xy, t_sec):
        sx, sy = shoulder_xy
        ex, ey = elbow_xy
        wx, wy = wrist_xy

        # 畫圓判定基準
        L = math.hypot(ex - sx, ey - sy)#手軸到肩膀的距離
        if L < 1e-6:
            self.theta_hist.clear()
            return 0

        # 檢查手臂是否過於平放 動作不夠大
        vx, vy = (wx - ex), (wy - ey) # 計算手軸到手腕向量
        r = math.hypot(vx, vy)# 手腕繞手軸旋轉半徑
        if (r / L) < self.k_min:
            self.theta_hist.clear()
            return 0

        # 多貞同時判斷避免數降低數值抖動
        theta = math.atan2(vy, vx)
        self.theta_hist.append((t_sec, theta))
        if len(self.theta_hist) <= self.k_step:
            return 0

        # 檢查角速度
        t0, th0 = self.theta_hist[-(self.k_step+1)]
        t1, th1 = self.theta_hist[-1]
        dt = t1 - t0
        if dt <= 1e-6:
            return 0
        dtheta = self._unwrap_dtheta(th1 - th0)
        # 檢查過大旋轉角度避免誤判距離影響出現
        if abs(dtheta) > self.max_step:
            return 0
        w = abs(dtheta) / dt
        if not (self.w_min <= w <= self.w_max):
            return 0

        if self.direction == "CCW":
            if dtheta > 0:
                self.acc += dtheta
        elif  self.direction == "CW":
            if dtheta < 0:
                self.acc += abs(dtheta)
        #計算次數
        new_loops = 0
        two_pi = 1/6 * math.pi
        while abs(self.acc) >= two_pi:
            new_loops += 1
            self.total += 1
            self.acc -= math.copysign(two_pi, self.acc)

        return new_loops
