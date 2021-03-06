import torch
import torch.nn as nn
from torch.autograd import Variable


class VanillaRNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, n_layers=1):
        super(VanillaRNN, self).__init__()
        # define params
        self.hidden_size = hidden_size
        self.n_layers = n_layers
        # define layers
        self.encoder = nn.Embedding(input_size, hidden_size)
        self.rnn = nn.RNN(hidden_size, hidden_size, self.n_layers)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, input, hidden):
        input = self.encoder(input.view(1, -1))
        output, hidden = self.rnn(input, hidden)
        output = output.contiguous().view(-1, self.hidden_size)
        output = self.fc(output)
        return output, hidden

    def init_hidden(self):
        return Variable(torch.zeros(self.n_layers, 1, self.hidden_size))
