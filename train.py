import os
from config import get_config
import torch
from dataset import Datasets
from torch.utils.data import DataLoader
import torch.nn as nn
import torch.optim as optim
from tqdm import tqdm
from torch.autograd import Variable
from PIL import Image
from torchvision import transforms
from model.conv7 import ZSSRNet

device = ('cuda' if torch.cuda.is_available() else 'cpu')


def train(model, sr_factor, learnig_rate, num_epoch, train_loader):
    model = model.to(device)

    loss_function = nn.L1Loss()
    optimizer = optim.Adam(model.parameters(), lr=learnig_rate)

    progress = tqdm(range(num_epoch))
    for epoch in progress:
        for step, image in enumerate(train_loader):
            low_resolution = Variable(image['lr'].to(device))
            high_resolution = Variable(image['hr'].to(device))
            optimizer.zero_grad()
            out = model(low_resolution)
            loss = loss_function(out, high_resolution)
            loss.backward()
            optimizer.step()

            cpu_loss = loss.data.cpu().numpy()
            progress.set_description("epoch: {epoch} Loss: {loss}, Learning Rate: {lr}".format( \
                epoch=epoch, loss=cpu_loss, lr=learnig_rate))


def tset(t_img):


if __name__ == "__main__":
    config = get_config()

    img = Image.open(config.img)
    t_img = transforms.ToTensor()(img)

    size = t_img.size()
    chanel = size[0]

    model = ZSSRNet(input_channels=chanel)

    train_dataset = Datasets(img, config.scale_factor, config.noise_std)
    # train_loader = torch.utils.data.DataLoader(dataset=train_dataset, batch_size=config.batch_size, shuffle=True)
    train(model, config.scale_factor, config.learning_rate, config.num_epoch, train_loader)
