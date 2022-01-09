#Image Reconstruction Network

This repository is aimed to provide a template for adversarial neural network to remove special effect from images by training a simple image reconstruction network. This can be be extended to more complicated and advance neural network or a generative neural network approach.

#### Usage 

1. Run the train_valid_split.py to generate train and text data. It ignores the images defined in invalid_images.txt
```
python train_valid_split.py
```
2. Run the model training
```
python train.py
```

3. Test the model on a single image (please update the image file name in the test script to be tested). Make sure if the latest checkpoint in the checkpoints directory is the model you want to use.
```
python test.py
```