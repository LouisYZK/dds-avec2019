from global_values import *

class FeatureExtration():
    def __init__(self, feature_name):
        self.feature_name = feature_name

    def gen_fea(self):
        if self.feature_name == FEATURE_EXP_2:
            from core.feature_exraction.example_2 import gen_feature
            gen_feature.gen_fea()
        elif self.feature_name == FEATURE_EXP_1:
            from core.feature_exraction.example_1 import gen_feature
            gen_feature.gen_fea()
        elif self.feature_name == 'mfcc':
            from core.feature_exraction.baseline19.LLDs import audio_llds
            audio_llds.get_audio_llds('mfcc')
        elif self.feature_name == 'egemaps':
            from core.feature_exraction.baseline19.LLDs import audio_llds
            audio_llds.get_audio_llds('egemaps')
        else:
            print(self.feature_name, 'not finished yet!')