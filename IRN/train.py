import os
import torch
import random
import numpy as np
from network.image_reconstrcution_network import ImageReconstrcutionNetwork
from trainer import ImageReconstrcutionTrainer
from util.config import Config

def init_seeds(seed=0):
    #torch.manual_seed(seed)
    #torch.cuda.manual_seed(seed)
    #torch.cuda.manual_seed_all(seed)
    #torch.autograd.set_detect_anomaly(True) # enable only for debugging
    torch.backends.cudnn.deterministic = False
    torch.backends.cudnn.benchmark = True


seed=0
init_seeds(seed=seed)

cuda_device = None
if torch.cuda.is_available():
    cuda_device = 0
    os.environ['CUDA_VISIBLE_DIVICES'] = "1"
config = Config("cfg")
config.load_config()


model = ImageReconstrcutionNetwork()
trainer = ImageReconstrcutionTrainer(model, config)
trainer.train()
print("completed")

#np. set_printoptions(precision=4, suppress=True,  linewidth=250);torch.set_printoptions(sci_mode=False, precision=3, linewidth=250)
#torch.set_printoptions(sci_mode=False, precision=2, linewidth=250)
