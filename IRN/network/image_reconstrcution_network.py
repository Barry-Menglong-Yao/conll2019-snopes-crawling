import torch
import math
import torch.nn as nn
from typing import List
from torch.nn import BatchNorm2d
from network.encoder import Encoder
from network.decoder import Decoder


class ImageReconstrcutionNetwork(nn.Module):
    def __init__(self):
        """Constructor

        Args:
            nc (int, optional): number of classes. Defaults to 90.
            n_anchors (int, optional): number of anchors. Defaults to 3.
        """
        super(ImageReconstrcutionNetwork, self).__init__()
        self.encoder = Encoder()
        self.decoder = Decoder()
        self.sigmoid = nn.Sigmoid()
        self.init_weights()
        self.get_parameters_count()

    def forward(self, x:torch.Tensor) -> List[torch.Tensor]:
        """Forward pass of the network module

        Args:
            x (torch.Tensor): Input Tensor

        Returns:
            torch.Tensor: Output Tensor
        """
        ec3, ec4, ec5 = self.encoder(x)
        x = self.decoder(ec3, ec4, ec5)
        x = self.sigmoid(x)

        return x
        
    def get_parameters_count(self):
        count = 0
        for parameter in self.parameters():
            count += parameter.numel()

        print("Total Parameters: %d" % count)

    def init_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                torch.nn.init.kaiming_normal_(m.weight, mode="fan_out", nonlinearity="leaky_relu")
                if m.bias is not None:
                    torch.nn.init.constant_(m.bias, 0)

            elif isinstance(m, BatchNorm2d):
                torch.nn.init.constant_(m.weight, 1)
                torch.nn.init.constant_(m.bias, 0)


