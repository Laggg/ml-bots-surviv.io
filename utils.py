import os
import cv2
import torch
import numpy as np
import torch
import torch.nn as nn
import torchvision.models as models
import matplotlib.pyplot as plt


def get_driver_path(driver_path):
    folder_path = driver_path.split('/')[0]
    driver = [
        x for x in os.listdir(driver_path.split('/')[0]) if 'driver' in x
    ][0]
    return folder_path + "/" + driver


def check_device(device):
    ''' check if cuda is available for inference '''
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    return device


class NeuralNet(nn.Module):
    def __init__(self, num_ftrs=512, num_inv=16):
        super().__init__()
        self.backbone = models.resnet18(pretrained=True)
        self.backbone.fc = nn.Flatten()
        self.head = nn.Sequential(
            nn.Linear(
                in_features=num_ftrs + num_inv,
                out_features=8
            )
        )

    def forward(self, x):
        p2v = self.backbone(x[0])
        z = torch.cat([p2v, x[1]], dim=1)
        z = self.head(z)
        return z


class BRAIN():
    def __init__(self, agent, model, device='CPU', plot_state=True):
        self.dir_aug = np.array(
            [[0, 1, 2, 3, 4, 5, 6, 7, 8],  # real image
             [0, 3, 4, 5, 6, 7, 8, 1, 2],  # rotate 90 o'clock
             [0, 5, 6, 7, 8, 1, 2, 3, 4],  # rotate 180
             [0, 7, 8, 1, 2, 3, 4, 5, 6],  # rotate 270
             [0, 1, 8, 7, 6, 5, 4, 3, 2],  # real image + gor flip
             [0, 7, 6, 5, 4, 3, 2, 1, 8],  # rotate 90 o'clock + gor flip
             [0, 5, 4, 3, 2, 1, 8, 7, 6],  # rotate 180 + gor flip
             [0, 3, 2, 1, 8, 7, 6, 5, 4]])  # rotate 270 + gor flip

        self.agent = agent
        self.model = model
        self.device = device
        if self.device != 'CPU':
            self.model = self.model.to(self.device)
        self.plot_state = plot_state

    def choose_action(self, scr):
        p0 = cv2.resize(
            scr, (84, 84), interpolation=cv2.INTER_AREA)[:, :, ::-1]
        if self.plot_state:
            self.see_plot(p0)
        p_main = np.zeros((8, 84, 84, 3))
        p_main[0, :, :, :] = p0.copy()
        for aug in range(1, 8):
            if aug == 1:
                p = cv2.rotate(p0, cv2.ROTATE_90_CLOCKWISE)
            elif aug == 2:
                p = cv2.rotate(p0, cv2.ROTATE_180)
            elif aug == 3:
                p = cv2.rotate(p0, cv2.ROTATE_90_COUNTERCLOCKWISE)
            elif aug == 4:
                p = cv2.flip(p0, 1)
            elif aug == 5:
                p = cv2.rotate(p0, cv2.ROTATE_90_CLOCKWISE)
                p = cv2.flip(p, 1)
            elif aug == 6:
                p = cv2.rotate(p0, cv2.ROTATE_180)
                p = cv2.flip(p, 1)
            elif aug == 7:
                p = cv2.rotate(p0, cv2.ROTATE_90_COUNTERCLOCKWISE)
                p = cv2.flip(p, 1)
            p_main[aug, :, :, :] = p
        p_main = torch.tensor(
            p_main.astype(np.float32) / 127.5 - 1
        ).permute(0, 3, 1, 2)  # 8x84x84x3-->8x3x84x84

        inv = torch.tensor(
            np.array([
                self.agent.hp / 100,  # hp
                self.agent.sp / 100,  # sp
                self.agent.left_bullets > 0,  # weapon_mag
                self.agent.band / 30,  # bandage
                self.agent.medk / 4,  # medicine
                self.agent.cola / 15,  # cola
                self.agent.pill / 4,  # pills
                self.agent.helmet / 3,  # helmet
                self.agent.vest / 3,  # vest
                self.agent.backpack / 3,  # backpack
                self.agent.zoom / 15,  # zoom
                self.agent.use_band,  # use_band
                self.agent.use_medk,  # use_medk
                self.agent.use_cola,  # use_cola
                self.agent.use_pill,  # use_pill
                self.agent.reloading
            ]).astype(np.float32))  # reloading
        inv = torch.cat([inv.view(1, -1)] * 8, dim=0)

        if self.device != 'CPU':
            p_main = p_main.to(self.device)
            inv = inv.to(self.device)

        with torch.no_grad():
            predictions = self.model((p_main, inv))
            for i in range(8):
                temp = predictions[i, :]
                predictions[i, :] = temp[self.dir_aug[i][1:] - 1]
            predictions = predictions.sum(dim=0).view(1, 8)
        _, action = torch.max(predictions, 1)
        return action.item()

    def see_plot(self, pict, size=(5, 5)):
        plt.figure(figsize=size)
        plt.imshow(pict)
        plt.grid()
        plt.show()
