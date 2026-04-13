import math


class AngleRecognizer:
    def __init__(self):
        pass

    def update(self, wrist, index, t_sec):
        """
        計算食指尖相對於手腕的角度
        wrist: [x, y] 手腕座標
        index: [x, y] 食指尖座標
        """
        # dx: 食指在手腕的左右偏移量
        dx = index[0] - wrist[0]

        # dy: 重要！MediaPipe 的 Y 軸向下為正
        # 當食指在手腕「之上」時，index[1] 會小於 wrist[1]
        # 因此 wrist[1] - index[1] 會得到正值，代表向上向量
        dy = wrist[1] - index[1]

        # math.atan2(dy, dx) 會回傳弧度 (-pi 到 pi)
        # 轉換為角度後：
        # 90度 代表正上方 (食指垂直朝上)
        # 0度 代表水平向右
        # 180度 代表水平向左
        angle = math.degrees(math.atan2(dy, dx))

        # 將角度轉換為 0 ~ 360 度格式
        # 這樣正上方依然是 90，正下方會變成 270
        if angle < 0:
            angle += 360

        # --- 移除原本的限制邏輯 ---
        # 如果你希望食指主要在上方活動 (0 ~ 180度)
        # 且要防止手指「垂下去」低於水平面，可以加一個簡單的限制：
        # 如果手指向下指，強制鎖定在水平位置
        if 0 <= angle <= 180:
            angle += 180
        else:
            if angle > 180:
                angle = 360
            elif angle < 0:
                angle = 180
        print(angle)
        return angle