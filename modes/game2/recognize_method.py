import math

class AngleRecognizer:
    def __init__(self):
        pass

    def update(self, wrist, elbow, t_sec):
        dx = elbow[0] - wrist[0]
        dy = wrist[1] - elbow[1]  # Y 軸向上為負，所以用 wrist - elbow

        # 取得 -180 ~ 180 的角度
        angle = math.degrees(math.atan2(dy, dx))

        # 轉換為 0 ~ 360 格式
        if angle < 0:
            angle += 360

        # 【關鍵】強制約束在 180~360 之間 (半圓限制)
        # 如果手低於水平線 (落在 0~180 區間)，強制歸位到最近的邊界
        if 0 <= angle < 180:
            if angle < 90:
                angle = 360  # 靠右邊界
            else:
                angle = 180  # 靠左邊界

        return angle


