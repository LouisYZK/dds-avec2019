"""
Extract the audio features from origin data 
according to the paper of exmaple model01

They are:

Modulation of amplitude || 
It is used to find the amplitude of two signals that are multiplied by the superimposed signals. 1
Envelope || 
It represents the varying level of an audio signal over time. 1
Autocorrelation || 
It shows the repeating patterns between observations as a function of the time lag between them. 1
Onset detector || 
It is used to detect a sudden change in the energy or any changes in the statistical properties of a signal. 1
Entropy of energy || 
It is a measure of abrupt changes in the energy level of an audio signal. 1
Tonal power ratio ||
It is obtained by taking the ratio of the tonal power of the spectrum components to the overall power. 1
RMS power Root mean square (RMS) || 
approximates the volume of an audio frame. 1
ZCR ||
Zero Crossing Rate (ZCR) is the number of times the signal changes sign in a given period of time. 1


PLP ||
It is a technique to minimize the differences between speakers. 9
MFCC ||
It is a representation of the short-term power spectrum of an audio signal. 12
Spectral decrease ||
It computes the steepness of the decrease of the spectral envelope. 1
Spectral rolloff ||
It can be treated as a spectral shape descriptor of an audio signal. 1
Spectral flux ||
It is a measure of spectral change between two successive frames. 1
Spectral centroid ||
It is a measure to characterize the center mass of the spectrum. 1
Spectral slope ||
It is the gradient of the linear regression of a spectrum. 1
Spectral autocorrelation ||
It is a function that measures the regular harmonic spacing in the spectrum of the speech signal. 1
"""


