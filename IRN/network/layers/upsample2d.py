import torch
import torch.nn as nn
import torch.nn.functional as F
from network.layers.conv2d import Conv2D


class UpSample2D(nn.Module):
    def __init__(self, channels:int):
        """Constructor

        Args:
            channels (int): Number of channels
        """
        super(UpSample2D, self).__init__()
        self.conv = Conv2D(channels, channels, 1, bias=False)

    def forward(self, x:torch.Tensor) -> torch.Tensor:
        """Forward pass of the network module

        Args:
            x (torch.Tensor): Input Tensor

        Returns:
            torch.Tensor: Output Tensor
        """
        s = x.shape[2:]
        x = F.interpolate(x, size=(2*s[0], 2*s[1]), mode="bilinear", align_corners=True)
        x = self.conv(x)
        return x