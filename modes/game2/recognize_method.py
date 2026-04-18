import math


class AngleRecognizer:
    def __init__(self):
        pass

    def _calculate_segment_angle(self, base, tip):
        """
        內部分析函數：計算單一手指段的角度
        base: [x, y] 手指根部 (MCP)
        tip: [x, y] 指尖
        """
        dx = tip[0] - base[0]
        # MediaPipe Y 軸向下為正，所以用 base - tip 讓向上向量變為正值
        dy = base[1] - tip[1]

        # 使用 atan2 取得弧度並轉角度
        angle = math.degrees(math.atan2(dy, dx))

        # 標準化為 0 ~ 360 度
        if angle < 0:
            angle += 360

        return angle

    def update(self, mid_base, mid_tip, pinky_base, pinky_tip, t_sec):
        """
        mid_base/tip: 中指根部(9)與指尖(12)
        pinky_base/tip: 小指根部(17)與指尖(20)
        """
        # 分別計算中指與小指的角度
        angle_mid = self._calculate_segment_angle(mid_base, mid_tip)
        angle_pinky = self._calculate_segment_angle(pinky_base, pinky_tip)

        # 取平均值
        avg_angle = (angle_mid + angle_pinky) / 2.0

        # 這裡可以根據你的遊戲需求保留或修改原有的限制邏輯
        # 例如：只偵測上半圓
        # if avg_angle > 180:
        #     avg_angle = 180 # 舉例：強制限制在上方

        # print(f"Mid: {angle_mid:.1f}, Pinky: {angle_pinky:.1f}, Avg: {avg_angle:.1f}")
        return avg_angle