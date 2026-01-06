import os
import cv2
import multiprocessing as mp
mp.set_start_method("spawn", force=True)
import threading
import queue
import mediapipe as mp_task
import numpy as np

def _mdp_worker(model_kind, model_path, input_q, output_q):
    BaseOptions = mp_task.tasks.BaseOptions
    VisionRunningMode = mp_task.tasks.vision.RunningMode

    if model_kind == "pose":
        Landmarker = mp_task.tasks.vision.PoseLandmarker
        Options = mp_task.tasks.vision.PoseLandmarkerOptions
        options = Options(
            base_options=BaseOptions(model_asset_path=model_path),
            running_mode=VisionRunningMode.IMAGE
        )
    elif model_kind == "face":
        Landmarker = mp_task.tasks.vision.FaceLandmarker
        Options = mp_task.tasks.vision.FaceLandmarkerOptions
        options = Options(
            base_options=BaseOptions(model_asset_path=model_path),
            running_mode=VisionRunningMode.IMAGE
        )
    elif model_kind == "hands":
        Landmarker = mp_task.tasks.vision.HandLandmarker
        Options = mp_task.tasks.vision.HandLandmarkerOptions
        options = Options(
            base_options=BaseOptions(model_asset_path=model_path),
            running_mode=VisionRunningMode.IMAGE,
            num_hands=2
        )
    else:
        # 不應該發生，保護一下
        raise ValueError(f"Unknown model_kind: {model_kind}")

    landmarker = Landmarker.create_from_options(options)

    while True:
        job = input_q.get()
        if job is None:
            # 收到結束訊號
            break

        idx, frame = job

        # 轉成 Mediapipe Image
        mp_image = mp_task.Image(
            image_format=mp_task.ImageFormat.SRGB,
            data=frame
        )

        result = landmarker.detect(mp_image)

        # 序列化 result（只回傳 numpy / list，不能回傳 Mediapipe 原生物件）
        serialized = _serialize_result(model_kind, result)

        output_q.put((idx, serialized))


def _serialize_result(model_kind, result):
    if model_kind == "pose":
        lm_list = []
        if result.pose_landmarks:
            # 取第一個人
            for lm in result.pose_landmarks[0]:
                lm_list.append([lm.x, lm.y, lm.z, lm.visibility])
        return {"pose_landmarks": lm_list}

    elif model_kind == "face":
        faces = []
        if result.face_landmarks:
            # 取第一張臉
            face0 = []
            for lm in result.face_landmarks[0]:
                face0.append([lm.x, lm.y, lm.z])
            faces.append(face0)
        return {"face_landmarks": faces}

    elif model_kind == "hands":
        hands = []
        if result.hand_landmarks:
            hands_detected_list = []
            for i, hand in enumerate(result.hand_landmarks):
                # 讀取 Left / Right
                handed = None
                if result.handedness:
                    handed = result.handedness[i][0].category_name  # "Left" 或 "Right"
                    score = result.handedness[i][0].score  # 信心度（可選）
                else:
                    handed = "Unknown"
                    score = 0.0
                hands_detected_list.append(handed)
                # Landmark 座標
                lm_list = []
                for lm in hand:
                    lm_list.append([lm.x, lm.y, lm.z])
                hands.append({
                    "type": handed,
                    "score": score,
                    "landmarks": lm_list
                })
            hands_detected_list.sort()
            if hands_detected_list != ["Left", "Right"]:
                hands = []
        return {"hand_landmarks": hands}
    else:
        return {}

class MDP_MUL_PROCE:
    def __init__(self, MODEL_ROOT_PATH=r".\model", process_nums=4):
        mp.set_start_method("spawn", force=True)

        if not os.path.exists(MODEL_ROOT_PATH):
            raise ValueError(f"The {MODEL_ROOT_PATH} does not exist. Please check model file.")

        self.MODEL_ROOT_PATH = MODEL_ROOT_PATH
        self.process_nums = process_nums

        # Mediapipe 相關設定
        self.model_kind = None        # "pose" / "face" / "hands"
        self.model_path = None        # 對應 task model 路徑

        # multiprocessing Queue
        self.input_q = mp.Queue()
        self.output_q = mp.Queue()

        # workers
        self.workers = []

        # 管理狀態
        self.image_counter = 0
        self.results = {}             # idx -> serialized_result
        self.run_worker = False
        self.clear_flag = False

        # 用一個 thread 收 output_q 的資料
        self._collector_thread = None
        self._collector_lock = threading.Lock()

    # ========== Model 初始化 ==========
    def pose_init(self):
        model_path = os.path.join(self.MODEL_ROOT_PATH, "pose_landmarker_full.task")
        if not os.path.exists(model_path):
            raise ValueError(f"The {model_path} does not exist. Please check 'Pose' model.")
        self.model_kind = "pose"
        self.model_path = model_path

    def face_init(self):
        model_path = os.path.join(self.MODEL_ROOT_PATH, "face_landmarker.task")
        if not os.path.exists(model_path):
            raise ValueError(f"The {model_path} does not exist. Please check 'Face' model.")
        self.model_kind = "face"
        self.model_path = model_path

    def hands_init(self):
        model_path = os.path.join(self.MODEL_ROOT_PATH, "hand_landmarker.task")
        if not os.path.exists(model_path):
            raise ValueError(f"The {model_path} does not exist. Please check 'Hand' model.")
        self.model_kind = "hands"
        self.model_path = model_path

    # ========== Worker 管理 ==========
    def _start_workers_if_needed(self):
        if self.model_kind is None or self.model_path is None:
            raise RuntimeError("Please call pose_init / face_init / hands_init before start_worker().")

        if self.workers:
            # 已經啟動過就不重啟
            return

        self.clear_flag = False

        for _ in range(self.process_nums):
            p = mp.Process(
                target=_mdp_worker,
                args=(self.model_kind, self.model_path, self.input_q, self.output_q)
            )
            p.start()
            self.workers.append(p)

    def _start_collector_if_needed(self):
        if self._collector_thread is not None and self._collector_thread.is_alive():
            return

        self._collector_thread = threading.Thread(target=self._collector_loop, daemon=True)
        self._collector_thread.start()

    def _collector_loop(self):
        while not self.clear_flag:
            try:
                idx, out_data = self.output_q.get(timeout=0.1)
            except queue.Empty:
                continue

            with self._collector_lock:
                self.results[idx] = out_data

    def start_worker(self):
        self._start_workers_if_needed()
        self._start_collector_if_needed()
        self.run_worker = True

    def stop_worker(self):
        self.run_worker = False

    # ========== 對外介面：送進 image、取得結果 ==========
    def image_input(self, frame: np.ndarray):
        if not self.run_worker:
            # 若尚未 start_worker，這裡直接丟掉（也可以選擇 buffer，看你之後要不要）
            return None

        # 簡單保證是 RGB
        if frame.ndim == 2:
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
        elif frame.shape[2] == 4:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2RGB)
        else:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        idx = self.image_counter
        self.image_counter += 1

        self.input_q.put((idx, frame))
        return idx

    def get_result(self, idx):
        with self._collector_lock:
            return self.results.get(idx, None)

    def clear_memory(self):
        self.results = {}
        self.image_counter = 0

    def get_processed_frame_nums(self):
        if not self.results:
            return 0
        return max(self.results.keys()) + 1

    def get_all_results_in_order(self):
        with self._collector_lock:
            return [self.results[k] for k in sorted(self.results.keys())]

    # ========== 清理 ==========
    def clear(self):
        self.run_worker = False
        self.clear_flag = True

        # 關閉 worker
        for _ in self.workers:
            self.input_q.put(None)

        for p in self.workers:
            p.join()
        self.workers.clear()

        # 等 collector thread 結束
        if self._collector_thread is not None:
            self._collector_thread.join(timeout=1.0)
            self._collector_thread = None

        # 可視需要清空結果
        with self._collector_lock:
            self.results.clear()
        self.image_counter = 0

        print("MDP_MUL_PROCE cleared.")


# ================================
# 測試用 main（參考用）
# ================================
"""
if __name__ == "__main__":
    mp.set_start_method("spawn", force=True)
    mdpp = MDP_MUL_PROCE()
    mdpp.hands_init()
    mdpp.start_worker()

    cap = cv2.VideoCapture(0)

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            idx = mdpp.image_input(frame)

            # 示範：馬上問有沒有結果（通常會有 latency）
            if idx is not None:
                # res = mdpp.get_result(idx)
                length = mdpp.get_processed_frame_nums()
                if length > 0:
                    mdpp.get_result(length-1)
                    # print(mdpp.get_result(length-1))
                # 這裡你可以加一些 debug print 看結果格式
                # print(idx, length)

            # ESC 離開
            if cv2.waitKey(1) & 0xFF == 27:
                break
    finally:
        cap.release()
        mdpp.clear()
"""