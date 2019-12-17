from global_values import *

class FeatureExtration():
    def __init__(self, model):
        self.model = model

    def gen_fea(self):
        if self.model == FEATURE_EXP_2:
            from core.feature_exraction.example_2 import gen_feature
            gen_feature.gen_fea()
        elif self.model == FEATURE_EXP_1:
            from core.feature_exraction.example_1 import gen_feature
            gen_feature.gen_fea()
        else:
            print(self.model, 'not finished yet!')