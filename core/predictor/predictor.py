from abc import abstractmethod, ABCMeta

class Predictor(object):
    """
    Abstract base class: predictor
    train: using any model, unimodal or multi-modal
    predict: generate result on giving data set
    metric: generate metric results on giving development set
    """
    __metaclass__ = ABCMeta
    
    def __init__(self):
        pass

    @abstractmethod
    def train(self):
        """
        return a model
        """
        pass

    @abstractmethod
    def predict(self):
        pass

    @abstractmethod
    def metric(self):
        pass    