import os
import torch
import numpy as np
from sklearn.metrics import mean_squared_error

import config
from core.predictor.Deep import create_dataset
from core.predictor.Deep.define_model import UnimodalRegressorModel
from common.log_handler import get_logger
logger = get_logger()

def ccc_score(x, y):
	# Computes the metrics CCC
	#  CCC:  Concordance correlation coeffient
	# Input:  x,y: numpy arrays (one-dimensional)
	# Output: CCC

	x_mean = np.nanmean(x)
	y_mean = np.nanmean(y)

	covariance = np.nanmean((x - x_mean) * (y - y_mean))

	x_var = np.nanmean((x - x_mean) ** 2)
	y_var = np.nanmean((y - y_mean) ** 2)

	CCC = (2 * covariance) / (x_var + y_var + (x_mean - y_mean) ** 2)

	return CCC

def custom_loss(output, target):

	out_mean = torch.mean(output)
	target_mean = torch.mean(target)

	covariance = torch.mean( (output - out_mean) * (target - target_mean) )
	target_var = torch.mean( (target - target_mean)**2)
	out_var = torch.mean( (output - out_mean)**2 )

	ccc = 2.0 * covariance/(target_var + out_var + (target_mean-out_mean)**2 + 1e-10)
	loss_ccc = 1.0 - ccc

	return loss_ccc

def train_unimodal_seq(train_loader, model, optimizer):
    running_loss = 0.
    predictors_corr = list()
    labels_corr = list()

    for i, train_data in enumerate(train_loader):
        features, labels = train_data
        optimizer.zero_grad()
        
        features = features.cuda()
        labels = labels.cuda()
        
        predictions = model.forward(features)
        labels = labels.view(predictions.size()[0], -1)
        
        loss = custom_loss(predictions, labels)
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item()
		


def start(feature):
    train_ds = create_dataset.get_loader(feature, dataset_type='train')
    model = UnimodalRegressorModel(feature).cuda()
    best_ccc = -1
    optimizer = torch.optim.Adam(model.parameters(), lr=config.learning_rate)
    
    for epoch in range(config.epochs_num):
        train_loss, train_ccc = train_unimodal_seq(train_ds, model, optimizer)
        
        logger.info(f'[Train in Deep Modle] epoch {epoch}, train loss {train_loss}, train_ccc {train_ccc}')
