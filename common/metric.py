"""
define some metric tools using commonly
"""
import numpy as np

def ccc_score(x, y):
    """calcute the CCC coieffcient base on paper [1]
        [1] https://www.ncss.com/wp-content/themes/ncss/pdf/Procedures/PASS/Lins_Concordance_Correlation_Coefficient.pdf
    """
    # assume x and y are ndarray by default

    rho = np.corrcoef(x, y)[0, 1]
    m_x, m_y, std_x, std_y = np.mean(x), np.mean(y), np.std(x), np.std(y)
    ccc = (2 * rho * std_x * std_y) / ((m_x - m_y) ** 2 + std_y ** 2 + std_x ** 2)

    return ccc

if __name__  == '__main__':
    x = np.random.randint(0, 10, 10)
    y = np.ones(10)
    print(ccc_sore(x, y))