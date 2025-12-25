from MDP_Mul_Process import MDP_MUL_PROCE
import threading
import time
import cv2

class HandMovementRecognize:
    # 開相機
    # 使用模型
    # 結果判斷
    # 提供結果

    def __init__(self):
        # variable
        self.camera_frame_width = 640
        self.camera_frame_height = 480
        self.mdpp = None
        self.threading_list = []
        self.frame_lock = threading.Lock()
        self.now_frame = None

        # open camera
        self.camera_inst = self.CameraControl(self)

    class CameraControl:
        def __init__(self, hmr):
            self.hmr = hmr
            self.run_flag = False
            self.cap = None

        def camera_presetting_and_test(self):
            ret, frame = self.cap.read()
            if not ret:
                raise Exception("Can't receive frame (stream end?). Exiting ...")
            else:
                print(f"Camera open success.")

        def camera_catch_frame_loop(self):
            while self.run_flag:
                if self.hmr.mdpp is None:
                    deadline = time.time() + 1.0
                    print(f"MDPP not initialized.")
                    while self.run_flag and self.hmr.mdpp is None and time.time() < deadline:
                        time.sleep(0.05)
                    if self.hmr.mdpp is None:
                        print(f"camera time out.")
                        break

                ret, frame = self.cap.read()

                if not ret:
                    time.sleep(0.005)
                    continue
                with self.hmr.frame_lock:
                    self.hmr.now_frame = frame

        def camera_start(self):
            self.run_flag = True
            self.cap = cv2.VideoCapture(0)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.hmr.camera_frame_width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.hmr.camera_frame_height)
            if not self.cap.isOpened():
                raise Exception("Camera open failed.")
            self.camera_presetting_and_test()

            t = threading.Thread(target=self.camera_catch_frame_loop, daemon=True)
            t.start()
            self.hmr.threading_list.append(t)
            print(f"Start sending frame into mediapipe.")

        def camera_stop(self):
            self.run_flag = False
            if self.cap is not None:
                self.cap.release()
            for t in self.hmr.threading_list:
                if t is not None and t.is_alive():
                    t.join(timeout=2)
            try:
                self.hmr.threading_list.clear()
            finally:
                print(f"Stop sending frame into mediapipe.")

    def run_mediapipe(self):
        self.mdpp = MDP_MUL_PROCE()
        self.mdpp.pose_init()
        self.mdpp.start_worker()

    def movement_recognize(self):
        pass

    def external_api(self):
        pass

    def clear(self):
        self.camera_inst.camera_stop()
        if self.mdpp is not None:
            self.mdpp.clear()

if __name__ == "__main__":
    hm = HandMovementRecognize()
    hm.run_mediapipe()
    hm.camera_inst.camera_start()
    try:
        while True:
            if hm.now_frame is not None:
                with hm.frame_lock:
                    frame = None if hm.now_frame is None else hm.now_frame.copy()
                cv2.imshow("test",frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                time.sleep(0.001)
    finally:
        hm.clear()
        cv2.destroyAllWindows()


