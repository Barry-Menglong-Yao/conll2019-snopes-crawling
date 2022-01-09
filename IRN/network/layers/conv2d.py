import torch
import torch.nn as nn
#from torch.utils.checkpoint import checkpoint

class Conv2D(nn.Module):
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
        super(Conv2D, self).__init__()
        if padding == -1:
            padding = ksize//2
        self.conv = nn.Conv2d(in_channels, out_channels, ksize, padding=padding, stride=stride, bias=bias)
        self.norm = bn
        if self.norm:
            self.bn = nn.BatchNorm2d(out_channels)
            #self.gn = nn.GroupNorm(out_channels//2, out_channels)
        self.activation = nn.LeakyReLU(0.1)
        #self.activation = nn.ELU()

    def forward(self, x:torch.Tensor) -> torch.Tensor:
        """Forward pass of the network module

        Args:
            x (torch.Tensor): Input Tensor

        Returns:
            torch.Tensor: Output Tensor
        """
        x = self.conv(x)
        if self.norm:
            x = self.bn(x)
        x = self.activation(x)
        return x