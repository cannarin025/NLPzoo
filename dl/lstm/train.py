import torch
import torch.nn as nn
from helper import *
from lstm import LSTM
from evaluate import evaluate

def train(model, model_optimizer, inp, target):
    model.zero_grad()
    loss = 0

    for c in range(chunk_len):
        output = model(inp[c])
        loss += criterion(output, target[c].unsqueeze(0))

    loss.backward()
    model_optimizer.step()

    return loss.data.item() / chunk_len 


if __name__ == '__main__':
    current_file, n_characters = import_and_sanitize("../../data/shakespeare.txt")

    input_dim = output_dim = n_characters
    n_epochs = 2000
    print_every = 100
    plot_every = 10
    hidden_dim = 100
    n_layers = 1
    lr = 0.005
    chunk_len = 200

    model_lstm = LSTM(input_dim, hidden_dim, n_characters, n_characters)
    model = model_lstm # choose a model
    model_optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    criterion = nn.CrossEntropyLoss()

    start = time.time()
    all_losses = []
    loss_avg = 0

    for epoch in range(1, n_epochs + 1):
        (inp, target) = random_training_set(current_file, chunk_len)
        loss = train(model, model_optimizer, inp, target)       
        loss_avg += loss

        if epoch % print_every == 0:
            print('[%s (%d %d%%) %.4f]' % (time_since(start), epoch, epoch / n_epochs * 100, loss))
            print(evaluate(model, 'Wh', 100), '\n')

        if epoch % plot_every == 0:
            all_losses.append(loss_avg / plot_every)
            loss_avg = 0
