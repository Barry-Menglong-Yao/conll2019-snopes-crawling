import os
import time
import torch
import glob
import random
from numba import jit, njit
import numpy as np
from typing import List
from nltk.corpus import wordnet
from imgaug import augmenters as iaa
import imgaug as ia
from PIL import Image, ImageDraw, ImageFont


class AddWaterMark(object):
    """This class is responsible for adding watermark text to the image

    """
    def __init__(self):
        """Constructor

        Args:
            size (List[int]): desired size of the image after crop
        """
        path = '/usr/share/fonts'
        fonts_paths = glob.glob(os.path.join(path, '*/*/*'))
        assert len(fonts_paths) > 0, "No fonts found, please check you path [%s]"%path
        
        self.fonts = []
        # create different fonts from font size of 28 to 36 
        # for font_path in fonts_paths:
        #     for font_size in range(28, 36):
        #         self.fonts.append(ImageFont.truetype(font_path, font_size))
        
        for font_size in range(28, 36):
            self.fonts.append(ImageFont.truetype('/home/aditya/misinformation/IRN-master/NotoMono-Regular.ttf', font_size))
            

        self.texts = [w for w in wordnet.words() if w.isalpha()]
        aug = iaa.BlendAlpha((0.1, 0.3),foreground=iaa.Add(100),background=iaa.Multiply(0.2))
        self.opacity_aug = iaa.Sequential([aug])

    def __call__(self, data:dict) ->  dict:
        """class call method 

        Args:
            data (dict): dictionary image and annotation

        Returns:
            dict: dictionary image and annotation
        """

        data['target'] = data['image'].copy()

        if random.random()>0.3:
            image = Image.fromarray(data['image'])
            font_ids = random.randint(0, len(self.fonts)-1)
            font = self.fonts[font_ids]
            draw = ImageDraw.Draw(image)
            stroke_width = random.randint(2, 5)
            text_color = (random.randint(204, 220), random.randint(176, 188), random.randint(39, 72))

            text = self.texts[random.randint(0, len(self.texts)-1)]
            text_size = font.getsize(text)
            img_size = image.size[0:2]

            loc = (random.randint (0, max(1, img_size[0]-text_size[0]-1)), random.randint (0, max(1, img_size[1]-text_size[1]-1)))
            
            draw.text(loc, text,text_color,font=font, stroke_width=stroke_width)
            data['image'] = np.asarray(image)
        return data

class RandomCropAndPad(object):
    """This class is responsible for cropping the image.

    """
    def __init__(self, size:List[int]):
        """Constructor

        Args:
            size (List[int]): desired size of the image after crop
        """
        self.crop_size = np.array(size).astype(np.int32)

    def __call__(self, data:dict) ->  dict:
        """class call method 

        Args:
            data (dict): dictionary image and annotation

        Returns:
            dict: dictionary image and annotation
        """
        image = data['image']
        target = data['target']
        h, w = image.shape[0:2]
        # If width and height is greater then the crop window
        hpad = self.crop_size[0] - h
        wpad = self.crop_size[1] - w
        hpad1 = hpad2 = wpad1 = wpad2 = 0

        if hpad > 0:
            hpad1 = np.random.randint(0, hpad)
            hpad2 = hpad - hpad1
        if wpad > 0:
            wpad1 = np.random.randint(0, wpad)
            wpad2 = wpad - wpad1
        
        image = np.pad(image, ((hpad1, hpad2), (wpad1, wpad2), (0, 0)), 'constant')
        target = np.pad(target, ((hpad1, hpad2), (wpad1, wpad2), (0, 0)), 'constant')

        image, target = RandomCropAndPad.crop(image, target, self.crop_size)

        data['image'] = image
        data['target'] = target

        return data

    @staticmethod
    def crop(image: np.ndarray, target: np.ndarray,  crop_size:np.ndarray) -> List[np.ndarray]:
        """ Crop the image for desired size and remove the annotation which does not fit in the size

        Args:
            image (np.ndarray): Full size Image
            target (np.ndarray): Full size Image target
            crop_size (np.ndarray): h and w

        Returns:
            List[np.ndarray]: cropped image and valid annotation
        """
        h, w = image.shape[0:2]
        h_diff  = h - crop_size[0]
        w_diff  = w - crop_size[1]
        x1 = y1= 0
        if h_diff>0:
            y1 = np.random.randint(0, h - crop_size[0])
        if w_diff>0:
            x1 = np.random.randint(0, w - crop_size[1])
        
        y2 = y1 + crop_size[0]
        x2 = x1 + crop_size[1]
        image = image[y1:y2, x1:x2]
        target = target[y1:y2, x1:x2]
        return image, target

class SizeTransformation(object):
    """This class is responsible for cropping or resizing the image based on probability
    """
    def __init__(self, config_params:dict, resize_flag:bool=False):
        """constructor

        Args:
            config_params (dict): Configuration Parameters
            resize_flag (bool, optional): A flag to constrint to do only resize. Defaults to False.
        """
        self.size = config_params['image_size']
        self.resize_flag = resize_flag
        self.crop = RandomCropAndPad(self.size)
        self.resize= iaa.Resize({"height": self.size [0], 'width': self.size [1]}, interpolation="linear")
        

    def __call__(self, data:dict) -> dict:
        """class call method 

        Args:
            data (dict): dictionary image and annotation

        Returns:
            dict: dictionary image and annotation
        """ 
        image = data['image']
        target = data['target']

        if self.resize_flag or np.random.rand() < 0.5:  # resize the images
            resized_image = self.resize(image=image)
            data ['image'] = resized_image
            resized_image = self.resize(image=target)
            data ['target'] = resized_image
            
        else: #crop
            data = self.crop(data)

        return data

class Rotate(object):
    """Rotates the image and annotation
    """
    def __init__(self, config_params:dict):
        """constructor

        Args:
            config_params (dict): Configuration Parameters
        """
        self.max_rot = config_params['max_rotation']

    def __call__(self, data:dict) -> dict:
        """class call method 

        Args:
            data (dict): dictionary image and annotation

        Returns:
            dict: dictionary image and annotation
        """
        
        if np.random.rand() < 0.3: 
            rot_aug = iaa.Affine(rotate=np.random.randint(-self.max_rot, self.max_rot, 1))
            image = data['image']
            image = rot_aug(image=image)
    
        return data


class HorizontalFlip(object):
    """It flips the images across y axis and adjust the annotations
    """

    def __call__(self, data:dict) -> dict:
        """class call method 

        Args:
            data (dict): dictionary image and annotation

        Returns:
            dict: dictionary image and annotation
        """
        if np.random.rand() < 0.5: 
            image = data['image']
            
            h, w = image.shape[0:2]
            image = np.fliplr(image)
            data['image'] = image
        return data

class Scaling(object):
    """Scale the images
    """
    def __call__(self, data:dict) -> dict:
        """class call method 

        Args:
            data (dict): dictionary image and annotation

        Returns:
            dict: dictionary images and annotations
        """
        
        data['image'] = data['image'] / 255
        data['normalized_image'] = np.array(data['image'], copy=True)
        return data

class Normalize(object):
    """Normalize the image 
    """
    def __init__(self, mean:np.ndarray=None, std:np.ndarray=None):
        """Constructor

        Args:
            mean (np.ndarray, optional): mean of the training dataset. Defaults to None.
            std (np.ndarray, optional): std of the training dataset. Defaults to None.
        """
        if mean is not None:
            self.mean = mean.reshape(1, 1, -1)
            self.std = std.reshape(1, 1, -1)
        else:
            self.mean = None
            self.std = None

    def __call__(self, data:dict) -> dict:
        """class call method 

        Args:
            data (dict): dictionary image and annotation

        Returns:
            dict: dictionary images and annotations
        """
        data['image'] = data['image'] / 255
        data['target'] = data['target'] / 255
        if self.mean is not None and self.std is not None:
            data['normalized_image'] = (data['image'] - self.mean)/self.std
        else:
            data['normalized_image'] = data['image'].copy()

        return data


class PropertyAugmentation(object):
    def __init__(self, config:dict=None):
        """Constructor

        Args:
            config (dict, optional): Configuration parameter instance. Defaults to None.
        """
        random_aug = lambda aug: iaa.Sometimes(0.3, aug)
        self.aug_seq = iaa.Sequential([
                        random_aug(iaa.MultiplyAndAddToBrightness(mul=(0.5, 1.5), add=(-30, 30))),
                        random_aug(iaa.AddToHueAndSaturation((-50, 50), per_channel=False)),
                        random_aug(iaa.ChangeColorTemperature((2000, 6000))),
                        random_aug(iaa.GammaContrast((0.5, 1.0))),
                        random_aug(iaa.GaussianBlur(sigma=(0.0, 1.1))),
                        iaa.BlendAlpha((0.1, 0.3),foreground=iaa.Add(100),background=iaa.Multiply(0.2)),
                       ])
        
    def __call__(self, data:dict) -> dict:
        """class call method 

        Args:
            data (dict): dictionary image and annotation

        Returns:
            dict: dictionary image and annotation
        """
        data['image'] = self.aug_seq(image = data['image'])
        return data


class ToTensor(object):
    """Converts the image and annotation to Tensors
    """
    def __call__(self, data):
        """class call method 

        Args:
            data (dict): dictionary image and annotation

        Returns:
            dict: dictionary image and annotation
        """
        data['image'] = torch.from_numpy(np.transpose(data['image'], [2, 0, 1])).float()
        data['normalized_image'] = torch.from_numpy(np.transpose(data['normalized_image'], [2, 0, 1])).float()
        data['target'] = torch.from_numpy(np.transpose(data['target'], [2, 0, 1])).float()
        return data