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

    def __init__(self, game):
        # variable
        self.run_flag = False # camera 控制
        self.threading_list = []
        self.frame_lock = threading.Lock()
        self.now_frame = None
        self.game = game
        # open camera
        self.camera_and_mdpp_inst = self.CameraAndMDPPControl(self)
        if self.game == "Game1":
            # open recognize pipeline
            self.movement_recognize = self.MovementRecognize(self)
        elif self.game == "Game2":
            self.hand_position_recognize = self.HandPositionRecognize(self)
        else:
            raise Exception("Unknown game type.")

    def external_api(self):
        with self.frame_lock:
            frame = None if self.now_frame is None else self.now_frame.copy()
        if self.game == "Game1":
            return {
                "now_frame" : frame,
                "left_ccw_circle":self.movement_recognize.left_ccw_circle_loop, "right_ccw_circle":self.movement_recognize.right_ccw_circle_loop,
                "left_cw_circle": self.movement_recognize.left_cw_circle_loop, "right_cw_circle": self.movement_recognize.right_cw_circle_loop,
                "left_vertical_loop":self.movement_recognize.left_vertical_loop, "right_vertical_loop":self.movement_recognize.right_vertical_loop,
                "left_horizontal_loop":self.movement_recognize.left_horizontal_loop, "right_horizontal_loop":self.movement_recognize.right_horizontal_loop,
            }
        elif self.game == "Game2":
            return {
                "now_frame" : frame,
                "wrist_coordinate" : self.hand_position_recognize.get_new_data()
            }

    def clear(self):
        self.camera_and_mdpp_inst.camera_stop()
        if self.game == "Game1":
            self.movement_recognize.clear_movement_recognize()
        elif self.game == "Game2":
            self.hand_position_recognize.clear_hand_position_recognize()
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

            #method initialize
            self.left_ccw_circle_method = RMethod.CircularRecognition(direction="CCW")
            self.right_ccw_circle_method = RMethod.CircularRecognition(direction="CCW")
            self.left_cw_circle_method = RMethod.CircularRecognition(direction="CW")
            self.right_cw_circle_method = RMethod.CircularRecognition(direction="CW")
            self.left_horizontal_method = RMethod.HorizontalRecognition()
            self.right_horizontal_method = RMethod.HorizontalRecognition()
            self.left_vertical_method = RMethod.VerticalRecognition()
            self.right_vertical_method = RMethod.VerticalRecognition()

            self.left_ccw_circle_loop = 0
            self.right_ccw_circle_loop = 0
            self.left_cw_circle_loop = 0
            self.right_cw_circle_loop = 0
            self.left_horizontal_loop = 0
            self.right_horizontal_loop = 0
            self.left_vertical_loop = 0
            self.right_vertical_loop = 0

            self.movement_recognize_main()

        def movement_recognize(self):
            while True:
                if self.clear_flag:
                    break
                if self.hmr.run_flag:
                    this_frame = self.hmr.camera_and_mdpp_inst.mdpp.get_result(self.recognize_frame_num)
                    if this_frame is not None:
                        if len(this_frame["pose_landmarks"]) > 0:
                            left_shoulder_xy = this_frame["pose_landmarks"][11][0:2]
                            right_shoulder_xy = this_frame["pose_landmarks"][12][0:2]
                            left_elbow_xy = this_frame["pose_landmarks"][13][0:2]
                            right_elbow_xy = this_frame["pose_landmarks"][14][0:2]
                            left_wrist_xy = this_frame["pose_landmarks"][15][0:2]
                            right_wrist_xy = this_frame["pose_landmarks"][16][0:2]

                            t_sec = time.time()
                            # horizontal movement
                            left_h_new_loop = self.left_horizontal_method.update(shoulder_xy=left_shoulder_xy,
                                                                                 wrist_xy=left_wrist_xy, t_sec=t_sec)
                            right_h_new_loop = self.right_horizontal_method.update(shoulder_xy=right_shoulder_xy,
                                                                                   wrist_xy=right_wrist_xy, t_sec=t_sec)
                            if left_h_new_loop > 0:
                                self.left_horizontal_loop = self.left_horizontal_method.count
                            if right_h_new_loop > 0:
                                self.right_horizontal_loop = self.right_horizontal_method.count

                            # vertical movement
                            left_v_new_loop = self.left_vertical_method.update(shoulder_xy=left_shoulder_xy,
                                                                               wrist_xy=left_wrist_xy, t_sec=t_sec)
                            right_v_new_loop = self.right_vertical_method.update(shoulder_xy=right_shoulder_xy,
                                                                                 wrist_xy=right_wrist_xy, t_sec=t_sec)
                            if left_v_new_loop > 0:
                                self.left_vertical_loop = self.left_vertical_method.count
                            if right_v_new_loop > 0:
                                self.right_vertical_loop = self.right_vertical_method.count

                            # counter clockwise circle movement
                            left_ccw_new_loop = self.left_ccw_circle_method.update(shoulder_xy=left_shoulder_xy,
                                                                                   elbow_xy=left_elbow_xy,
                                                                                   wrist_xy=left_wrist_xy, t_sec=t_sec)
                            right_ccw_new_loop = self.right_ccw_circle_method.update(shoulder_xy=right_shoulder_xy,
                                                                                     elbow_xy=right_elbow_xy,
                                                                                     wrist_xy=right_wrist_xy,
                                                                                     t_sec=t_sec)
                            if left_ccw_new_loop > 0:
                                self.left_ccw_circle_loop = self.left_ccw_circle_method.total
                            if right_ccw_new_loop > 0:
                                self.right_ccw_circle_loop = self.right_ccw_circle_method.total

                            # clockwise circle movement
                            left_cw_new_loop = self.left_cw_circle_method.update(shoulder_xy=left_shoulder_xy,
                                                                                 elbow_xy=left_elbow_xy,
                                                                                 wrist_xy=left_wrist_xy, t_sec=t_sec)
                            right_cw_new_loop = self.right_cw_circle_method.update(shoulder_xy=right_shoulder_xy,
                                                                                   elbow_xy=right_elbow_xy,
                                                                                   wrist_xy=right_wrist_xy, t_sec=t_sec)
                            if left_cw_new_loop > 0:
                                self.left_cw_circle_loop = self.left_cw_circle_method.total
                            if right_cw_new_loop > 0:
                                self.right_cw_circle_loop = self.right_cw_circle_method.total

                        self.recognize_frame_num += 1
                    else:
                        continue
                else:
                    time.sleep(0.001)

        def movement_recognize_main(self):
            t = threading.Thread(target=self.movement_recognize, daemon=True)
            t.start()
            self.hmr.threading_list.append(t)

        def clear_movement_recognize(self):
            self.clear_flag = True

    class HandPositionRecognize:
        def __init__(self, hmr):
            self.hmr = hmr
            self.clear_flag = False
            self.left_wrist_coordinate = {}
            self.right_wrist_coordinate = {}

            self.data_lock = threading.Lock()

            self.recognize_frame_num = 0
            self.taken_frame_count = 0

            self.hand_position_recognize_main()

        def clear_hand_position_recognize(self):
            self.clear_flag = True

        def get_new_data(self):
            with self.data_lock:
                idx = self.taken_frame_count
                if idx < self.recognize_frame_num:
                    l = self.left_wrist_coordinate.get(idx)
                    r = self.right_wrist_coordinate.get(idx)
                    if l is None or r is None:
                        # 該 frame 沒 landmarks 或尚未寫入完成，先不取
                        return {}
                    self.taken_frame_count += 1
                    return {"Left": l, "Right": r}
            return {}

        def hand_keep_tracking(self):
            while True:
                if self.clear_flag:
                    break
                if self.hmr.run_flag:
                    this_frame = self.hmr.camera_and_mdpp_inst.mdpp.get_result(self.recognize_frame_num)
                    if this_frame is not None:
                        if len(this_frame["pose_landmarks"]) > 0:
                            left = this_frame["pose_landmarks"][15][:2]
                            right = this_frame["pose_landmarks"][16][:2]
                        else:
                            left = None
                            right = None
                        with self.data_lock:
                            self.left_wrist_coordinate[self.recognize_frame_num] = left
                            self.right_wrist_coordinate[self.recognize_frame_num] = right
                            self.recognize_frame_num += 1
                        print(f"recognize_frame_num: {self.recognize_frame_num}")
                    else:
                        time.sleep(0.001)
                else:
                    time.sleep(0.001)

        def hand_position_recognize_main(self):
            t = threading.Thread(target=self.hand_keep_tracking, daemon=True)
            t.start()
            self.hmr.threading_list.append(t)

if __name__ == "__main__":
    hm = HandMovementRecognize("Game2")
    hm.camera_and_mdpp_inst.run_mediapipe()
    hm.camera_and_mdpp_inst.camera_start()
    try:
        while True:
            # 這裡會自動「阻塞」等待，直到 MediaPipe 出結果
            # 不再需要 time.sleep(0.001)
            data = hm.external_api()

            wrist_coords = data.get("wrist_coordinate")
            if wrist_coords:  # 檢查是否非空
                print(f"Left Wrist: {wrist_coords['Left']}")
    finally:
        hm.clear()
        cv2.destroyAllWindows()


