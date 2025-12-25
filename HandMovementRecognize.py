from MDP_Mul_Process import MDP_MUL_PROCE
import RecognizeMethod as RMethod
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
        self.run_flag = False
        self.threading_list = []
        self.frame_lock = threading.Lock()
        self.now_frame = None
        # open camera
        self.camera_and_mdpp_inst = self.CameraAndMDPPControl(self)
        # open recognize pipeline
        self.movement_recognize = self.MovementRecognize(self)

    def external_api(self):
        pass

    def clear(self):
        self.camera_and_mdpp_inst.camera_stop()
        self.movement_recognize.clear_movement_recognize()
        if self.camera_and_mdpp_inst is not None:
            self.camera_and_mdpp_inst.mdpp.clear()

    class CameraAndMDPPControl:
        def __init__(self, hmr):
            self.camera_frame_width =  640
            self.camera_frame_height = 480
            self.hmr = hmr
            self.cap = None
            self.mdpp = None
            self.count_catch_images = 0

        def camera_presetting_and_test(self):
            ret, frame = self.cap.read()
            if not ret:
                raise Exception("Can't receive frame (stream end?). Exiting ...")
            else:
                print(f"Camera open success.")

        def run_mediapipe(self):
            self.mdpp = MDP_MUL_PROCE()
            self.mdpp.pose_init()
            self.mdpp.start_worker()

        def camera_catch_frame_and_input_mdpp_loop(self):
            while self.hmr.run_flag:
                if self.mdpp is None:
                    deadline = time.time() + 1.0
                    print(f"MDPP not initialized.")
                    while self.hmr.run_flag and self.mdpp is None and time.time() < deadline:
                        time.sleep(0.005)
                    if self.mdpp is None:
                        print(f"camera time out.")
                        break

                ret, frame = self.cap.read()
                if not ret:
                    time.sleep(0.005)
                    continue
                with self.hmr.frame_lock:
                    self.count_catch_images += 1
                    self.hmr.now_frame = frame

                self.mdpp.image_input(self.hmr.now_frame.copy())

        def camera_start(self):
            self.hmr.run_flag = True
            self.cap = cv2.VideoCapture(0)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.camera_frame_width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.camera_frame_height)
            if not self.cap.isOpened():
                raise Exception("Camera open failed.")
            self.camera_presetting_and_test()

            t = threading.Thread(target=self.camera_catch_frame_and_input_mdpp_loop, daemon=True)
            t.start()
            self.hmr.threading_list.append(t)
            print(f"Start sending frame into mediapipe.")

        def camera_stop(self):
            self.hmr.run_flag = False
            if self.cap is not None:
                self.cap.release()
            for t in self.hmr.threading_list:
                if t is not None and t.is_alive():
                    t.join(timeout=2)
            try:
                self.hmr.threading_list.clear()
            finally:
                print(f"Stop sending frame into mediapipe.")

    class MovementRecognize:
        def __init__(self, hmr):
            # variable
            self.recognize_frame_num = 0
            self.hmr = hmr
            self.clear_flag = False

            self.movement_recognize_main()
        


        def movement_recognize(self):
            #method initialize
            circle_method = RMethod.CircularRecognition()

            # body landmark  extraction
            while True:
                if self.clear_flag:
                    break
                if self.hmr.run_flag:
                    this_frame = self.hmr.camera_and_mdpp_inst.mdpp.get_result(self.recognize_frame_num)
                    if this_frame is not None:
                        self.recognize_frame_num += 1
                    else:
                        continue
                    if len(this_frame["pose_landmarks"]) > 0:
                        left_shoulder_xy = this_frame["pose_landmarks"][11][0:2]
                        right_shoulder_xy = this_frame["pose_landmarks"][12][0:2]
                        left_elbow_xy = this_frame["pose_landmarks"][13][0:2]
                        right_elbow_xy = this_frame["pose_landmarks"][14][0:2]
                        left_wrist_xy = this_frame["pose_landmarks"][15][0:2]
                        right_wrist_xy = this_frame["pose_landmarks"][16][0:2]

                        t_sec = time.time()
                        # horizontal movement

                        # vertical movement

                        # circle movement
                        new_loop = circle_method.update(shoulder_xy=left_shoulder_xy, elbow_xy=left_elbow_xy, wrist_xy=left_wrist_xy, t_sec=t_sec)
                        if new_loop >= 0:
                            print(f"new loop detected. total : {circle_method.total}")
                else:
                    time.sleep(0.001)

        def movement_recognize_main(self):
            t = threading.Thread(target=self.movement_recognize, daemon=True)
            t.start()
            self.hmr.threading_list.append(t)

        def clear_movement_recognize(self):
            self.clear_flag = True

if __name__ == "__main__":
    hm = HandMovementRecognize()
    hm.camera_and_mdpp_inst.run_mediapipe()
    hm.camera_and_mdpp_inst.camera_start()
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


