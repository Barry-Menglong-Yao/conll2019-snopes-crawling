import torch
import torch.nn as nn
from .conv2d import Conv2D

class EncoderBlock(nn.Module):
    def __init__(self, in_channels:int, out_channels:int, ksize:int, stride:int=1, padding:int=-1, bn:bool=True, bias:bool=True):
        """Constructor

        Args:
            in_channels (int): Number of input channels
            out_channels (int): Number of output channels
            ksize (int): kernel size to use
            stride (int, optional): stride value. Defaults to 1.
            padding (int, optional): Padding size to use Defaults to -1.
            bn (bool, optional): Flag for batch norm usage. Defaults to True.
            bias (bool, optional): Flag for bias usage. Defaults to True.
        """
        super(EncoderBlock, self).__init__()
        self.conv1 = Conv2D(in_channels, out_channels, ksize, stride=stride)
        self.conv2 = Conv2D(out_channels, 2*out_channels, ksize, stride=1)
        self.conv3 = Conv2D(2*out_channels, out_channels, ksize, stride=1)
       
    def forward(self, x:torch.Tensor) -> torch.Tensor:
        """Forward pass of the network module

        Args:
            x (torch.Tensor): Input Tensor

        Returns:
            torch.Tensor: Output Tensor
        """
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.conv3(x)
        return x