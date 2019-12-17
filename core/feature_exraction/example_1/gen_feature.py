from core.feature_exraction.example_1.video_fea import VideoFea



def gen_fea():
    vf = VideoFea()
    vf.gen_head_fea()
    vf.gen_face_fea()