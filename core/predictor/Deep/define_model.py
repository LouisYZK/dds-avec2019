import torch
from torch import nn

import config

class UnimodalRegressorModel(nn.Module):
    def __init__(self, feature_dim):
        super().__init__()
        self.feature_dim = feature_dim
        self.rnn = torch.nn.GRU(input_size=self.feature_dim,
                                hidden_size=config.rnn_layer_dim,
                                num_layers=config.rnn_layer_num,
                                bidirectional=config.bidrectional)
        self.dropout = torch.nn.Dropout(config.dropout_rate)
        self.linear = torch.nn.Linear(config.rnn_layer_dim, 1)

    def forward(self, seq):
        rnn_out, _ = self.rnn(seq)
        x = self.dropout(rnn_out)
        x = self.linear(x)
        # dim = x.size()[1]
        # dense = torch.nn.Linear(dim, 1)
        # x = dense(x)
        return x[:, -1, :].item()