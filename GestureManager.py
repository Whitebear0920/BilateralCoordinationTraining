from HandMovementRecognize import HandMovementRecognize
class GestureManager:
    def __init__(self):
        self.hm = None
        self.api = None

    def start(self):
        if self.hm is None:
            self.hm = HandMovementRecognize()
            self.hm.camera_and_mdpp_inst.run_mediapipe()
            self.hm.camera_and_mdpp_inst.camera_start()
            self.api = self.hm.external_api()

    def stop(self):
        if self.hm:
            self.hm.clear()
            self.hm = None
            self.api = None
