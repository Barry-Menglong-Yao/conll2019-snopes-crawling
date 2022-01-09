import torch
import math
import torch.nn as nn
from typing import List
from torch.nn import BatchNorm2d
from network.layers.conv2d import Conv2D
from network.layers.upsample2d import UpSample2D

class Decoder(nn.Module):
    def __init__(self):
        """Constructor

        Args:
            nc (int, optional): number of classes. Defaults to 90.
            n_anchors (int, optional): number of anchors. Defaults to 3.
        """
        super(Decoder, self).__init__()
        self.uconv5 = UpSample2D(512)
        self.conv5 = Conv2D(2*512, 256, 3, 1)
        self.uconv4 = UpSample2D(256)
        self.conv4 = Conv2D(2*256, 128, 3, 1)
        self.uconv3 = UpSample2D(128)
        self.conv3 = Conv2D(128, 64, 3, 1)
        self.uconv2 = UpSample2D(64)
        self.conv2 = Conv2D(64, 32, 3, 1)
        self.uconv1 = UpSample2D(32)
        self.conv1 = Conv2D(32, 3, 7, 1)

    def forward(self, ec3:torch.Tensor, ec4:torch.Tensor,  ec5:torch.Tensor) -> List[torch.Tensor]:
        """Forward pass of the network module

        Args:
            x (torch.Tensor): Input Tensor

        Returns:
            torch.Tensor: Output Tensor
        """
        dc5 = self.uconv5(ec5)
        dc5 = self.conv5(torch.cat((ec4, dc5), dim=1))
        dc4 = self.uconv4(dc5)
        dc4 = self.conv4(torch.cat((ec3, dc4), dim=1))
        dc3 = self.uconv3(dc4)
        dc3 = self.conv3(dc3)
        dc2 = self.uconv2(dc3)
        dc2 = self.conv2(dc2)
        dc1 = self.uconv1(dc2)
        dc1 = self.conv1(dc1)

        return dc1