import cv2
import math
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# 1. 配置模型設定
BaseOptions = python.BaseOptions
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = PoseLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=r"C:\Users\fangt\Documents\Github\BilateralCoordinationTraining\assets\model\pose_landmarker_full.task"),
    running_mode=VisionRunningMode.IMAGE
)

# 2. 建立偵測器
# 注意：這裡使用 context manager (with...) 可以確保資源正確釋放
with PoseLandmarker.create_from_options(options) as landmarker:
    cap = cv2.VideoCapture(r"C:\Users\fangt\Downloads\295.jpg")

    while cap.isOpened():
        success, frame = cap.read()
        if not success: break

        # 3. 轉換圖片格式
        # OpenCV 預設是 BGR，需轉為 RGB，再轉為 MediaPipe 專用的 Image 物件
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

        # 4. 執行偵測
        detection_result = landmarker.detect(mp_image)
        print(detection_result.pose_landmarks[0][15])
        print(detection_result.pose_landmarks[0][16])

        cv2.imshow('MediaPipe Tasks API', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()