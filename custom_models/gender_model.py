import torch
import torch.nn as nn
from .utils import preprocessimage

class Model(nn.Module):
    def __init__(self):
        super().__init__()
        self.backbone = nn.Sequential(nn.Conv2d(3, 16, 3, padding=1),
                                        nn.BatchNorm2d(16),
                                        nn.ReLU(),
                                        nn.MaxPool2d(2, 2),
                                        nn.Conv2d(16, 32, 3, padding=1),
                                        nn.BatchNorm2d(32),
                                        nn.ReLU(),
                                        nn.MaxPool2d(2, 2),
                                        nn.Conv2d(32, 64, 3, padding=1),
                                        nn.BatchNorm2d(64),
                                        nn.ReLU(),
                                        nn.MaxPool2d(2, 2),
                                        nn.Conv2d(64, 128, 3, padding=1),
                                        nn.BatchNorm2d(128),
                                        nn.ReLU(),
                                    nn.Flatten(),)
        self.classifier = nn.Sequential(
                                        nn.Linear(128*16*6, 512),
                                        nn.ReLU(),
                                        nn.Linear(512, 1),
                                        nn.ReLU)
    def forward(self, x):
        x = self.backbone(x)
        x = x.view(x.size(0), -1)
        x = self.classifier(x)
        return x

def get_gender_model(device='cuda'):
    return torch.load('./model/gender.pt', map_location=device)

def predict_gender(model, image, thresh=0.5):
    return 'M' if model(preprocessimage(image))>thresh else 'F'