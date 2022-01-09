"""
Split data from a directory into train and valid file
"""
import os
import numpy as np
from util.config import Config
from numpy.random import default_rng

config = Config("cfg")
config.load_config()

data_dir = config.parameters['data_dir']
files = np.array(os.listdir(data_dir))

#print(len(files))
train_size = int(len(files) * 0.8)
rng = default_rng()
train_idx = rng.choice(len(files), size=train_size, replace=False)
mask = np.ones(len(files), dtype=bool)
mask[train_idx] = 0
train_files = files[train_idx]
val_files = files[mask]

train_data_file = "metadata/train_file.txt"
val_data_file = "metadata/val_file.txt"
invalid_image_file = "./invalid_images.txt"

invalid_images = set()

with open(invalid_image_file, 'r') as f:
    for filename in f.readlines():
        invalid_images.add(filename.strip())

with open(train_data_file, 'w') as f:
    for filename in train_files:
        if filename not in invalid_images:
            f.write("%s\n"%os.path.join(data_dir, filename))

with open(val_data_file, 'w') as f:
    for filename in val_files:
        if filename not in invalid_images:
            f.write("%s\n"%os.path.join(data_dir, filename))
