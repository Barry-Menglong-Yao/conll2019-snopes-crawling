import os
import cv2
import glob
import torch 
import numpy as np
from util.config import Config

from network.image_reconstrcution_network import ImageReconstrcutionNetwork

model = ImageReconstrcutionNetwork()

# load the model 
checkpoints = glob.glob("checkpoints/[0-9]*.pth")
ckpt = max(checkpoints, key=os.path.getmtime)
checkpoint_state_dict = torch.load(ckpt, map_location="cpu")
model.load_state_dict(checkpoint_state_dict)

config = Config("cfg")
config.load_config()

device = torch.device("cpu")
if config.parameters['cuda_flag']:
    device = torch.device("cuda:1")

model = model.to(device)
image_filename = "/home/jeet/workspace/dataset/cv/mode3_latest/images/22-110-0-4-eyes-sudan-miscaptioned.jpg"

image = cv2.cvtColor(cv2.imread(image_filename), cv2.COLOR_BGR2RGB)
image = cv2.resize(image, (512, 384), interpolation=cv2.INTER_AREA)
image = torch.from_numpy(image).float().cuda().permute(2, 0, 1).unsqueeze(0)
image /= 255

image = image.to(device)
with torch.no_grad():
    reconstructed_image = model(image).cpu().permute(0, 2, 3, 1)

reconstructed_image = np.uint8(reconstructed_image[0]*255)
cv2.imwrite("results.png", cv2.cvtColor(reconstructed_image, cv2.COLOR_RGB2BGR))

