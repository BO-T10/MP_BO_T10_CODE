import torch
import torch.nn as nn
import numpy as np
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
                                                nn.MaxPool2d(2, 2),
                                                nn.Conv2d(128, 256, 3, padding=1),
                                                nn.BatchNorm2d(256),
                                                nn.ReLU(),
                                            nn.Flatten(),)
                self.classifier = nn.Sequential(
                                                nn.Linear(6144, 512),
                                                nn.ReLU(),
                                                nn.Linear(512, 5),
                                                nn.Softmax())
            def forward(self, x):
                x = self.backbone(x)
                x = x.view(x.size(0), -1)
                x = self.classifier(x)
                return x


def get_age_model(device='cuda'):
    return torch.load('./model/age.pt', map_location=device)

def predict_age(model, image, thresh=0.4):
    out = np.array(model(preprocessimage(image)))

    # Original age brackets were : '(0-15)','(16-30)','(31-45)','(46-60)','(>60)'
    age_bracks_mean = [8, 23, 36, 48, 70]
    output = []
    for o in out:
        # Calculating the age using a weighted method
        weighted_age = 0
        for i in range(5):
            weighted_age += o[i]*age_bracks_mean[i]
        weighted_age = int(np.floor(weighted_age))
        # Add conf. int. here
        output.append(weighted_age)
    return output