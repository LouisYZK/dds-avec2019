"""
Generate some statistical features of input data series
"""
import scipy.stats
import numpy as np


class StatsFea():
    def __init__(self):
        self.columns = ['mean', 'std', 'skew', 'kurtosis',
                        'peak-rms', 'iqr', 'spectral']
    def gen_fea(self, data):
        """Assume data is a one-dimentional vector
        """
        stats_fea = list()
        stats_fea.append(np.mean(data))
        stats_fea.append(np.std(data))
        stats_fea.append(scipy.stats.skew(data))
        stats_fea.append(scipy.stats.kurtosis(data))
        stats_fea.append(max(data)/np.sqrt(np.mean(np.square(data)))) # peak-rms
        stats_fea.append(scipy.stats.iqr(data)) # interquantile range)
        stats_fea.append(scipy.stats.gmean(data)/np.mean(data)) # spectral)
        return stats_fea


