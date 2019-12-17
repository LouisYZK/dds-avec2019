from core.feature_exraction.example_1.video_fea import VideoFea

from concurrent.futures import ProcessPoolExecutor, wait
import threading


def gen_fea():
    vf = VideoFea()
    t1 = threading.Thread(target=vf.gen_head_fea)
    t2 = threading.Thread(target=vf.gen_face_fea)
    t1.start()
    t2.start()