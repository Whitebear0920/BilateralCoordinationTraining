from collections import deque
import math

class HorizontalRecognition:
    pass

class VerticalRecognition:
    pass

class CircularRecognition:
    def __init__(self, k_min=0.7, w_min=0.8, w_max=12.0, max_step=0.8, k_step=4):
        self.k_min = k_min
        self.w_min = w_min
        self.w_max = w_max
        self.max_step = max_step
        self.k_step = k_step

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

        L = math.hypot(ex - sx, ey - sy)
        if L < 1e-6:
            self.theta_hist.clear()
            return 0

        vx, vy = (wx - ex), (wy - ey)
        r = math.hypot(vx, vy)
        if (r / L) < self.k_min:
            self.theta_hist.clear()
            return 0

        theta = math.atan2(vy, vx)
        self.theta_hist.append((t_sec, theta))

        # 不夠長就不算
        if len(self.theta_hist) <= self.k_step:
            return 0

        t0, th0 = self.theta_hist[-(self.k_step+1)]
        t1, th1 = self.theta_hist[-1]
        dt = t1 - t0
        if dt <= 1e-6:
            return 0

        dtheta = self._unwrap_dtheta(th1 - th0)

        # (1) 單步角度變化上限（丟掉追蹤跳點）
        if abs(dtheta) > self.max_step:
            return 0

        w = abs(dtheta) / dt

        # (2) 角速度上下限 gate
        if not (self.w_min <= w <= self.w_max):
            return 0

        # 通過 gate 才累積
        self.acc += dtheta

        new_loops = 0
        two_pi = 2 * math.pi
        while abs(self.acc) >= two_pi:
            new_loops += 1
            self.total += 1
            self.acc -= math.copysign(two_pi, self.acc)

        return new_loops
