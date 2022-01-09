import os
import glob
import time
import torch
import torch.nn as  nn
import numpy as np
import torchvision
import torch.autograd.profiler as profiler
from torch.utils.tensorboard import SummaryWriter
from viz.visualization import Visualization
from dataloader.custom_dataloader import CustomDataLoader
import torch.optim.lr_scheduler as lr_scheduler


class ImageReconstrcutionTrainer:
    def __init__(self, model, config):
        self.config = config
        self.cuda_flag = self.config.parameters['cuda_flag']
        self.model = model

        if self.cuda_flag:
            self.model = self.model.cuda()
        data_loader = CustomDataLoader(config, self.config.parameters['workers'])
        self.batch_size = self.config.parameters['batch_size']
        self.train_loader, self.val_loader = data_loader.get_loader()
        self.writer = SummaryWriter()
        self.viz = Visualization(self.writer, self.config)
        self.loss_function = nn.MSELoss()

        #self.optimizer = torch.optim.SGD(self.model.parameters(), lr=self.config.parameters['lr'], momentum=0.9)
        self.optimizer = torch.optim.AdamW(self.model.parameters(), lr=self.config.parameters['lr'], weight_decay=1e-4)
        self.load()

        image_size = self.config.parameters['image_size']
        dummy_input = torch.autograd.Variable(torch.randn((2, 3, image_size[0], image_size[1]), device="cuda"))
        self.writer.add_graph(self.model, dummy_input)
    

    def train(self):
        optimizer = self.optimizer
        if self.config.parameters['apex_amp']:
            self.model, optimizer = amp.initialize(self.model, optimizer, opt_level=self.config.parameters['opt_level'],
                                                   loss_scale=self.config.parameters['loss_scale'])
        iteration = 0
        # save time by avoiding accessing dot wise element
        apex_amp_flag = self.config.parameters['apex_amp']
        grad_accumulation_step = self.config.parameters['grad_accumulation_step']
        dataset_length = len(self.train_loader.dataset)

        viz_image_count = self.config.parameters['viz_image_count']

        for epoch in range(self.config.parameters['epochs']):
            train_loss = 0.0
            accumulated_loss = 0
            for i, data in enumerate(self.train_loader):
                images = data['image']
                target = data['target']
                normalized_images = data['normalized_image']
                
                if self.cuda_flag:
                    images = images.cuda(non_blocking=True)
                    target = target.cuda(non_blocking=True)
                    normalized_images = normalized_images.cuda(non_blocking=True)
                # scale the image 
                iteration += 1
                prediction = self.model(normalized_images)
                loss = self.loss_function(prediction, target)
                if apex_amp_flag:
                    with amp.scale_loss(loss, optimizer) as scaled_loss:
                        scaled_loss.backward()
                else:
                    loss.backward() # without amp

                accumulated_loss += loss
                if (i+1) % grad_accumulation_step == 0 or i==dataset_length-1:
                    optimizer.step()
                    optimizer.zero_grad()
                    self.writer.add_scalar("Batch/1.Loss", accumulated_loss, iteration)
                    accumulated_loss = 0

                image_count = len(images)
                loss = loss.item()
                train_loss += loss*image_count  

                # run it 1000 times per epoch
                if iteration % 200  == 0:
                    self.save(epoch=epoch+1) #save the model
                    with torch.no_grad():
                        if images.shape[0] >= viz_image_count:
                            self.viz.plot(images, prediction, target, iteration)

            
                # t5 = time.time()
                # print("Batch took %.4f Model took %.4f Backprop took %.4f" % (t5-t1, t3-t2, t4-t3))
                # t1 = time.time()
            
            te1 = time.time()
            train_loss /= dataset_length
            
            self.writer.add_scalar("Training/1.Loss", train_loss, epoch)
            self.writer.add_scalar("Training/7.Learning_Rate", self.config.parameters['lr'], epoch)
            te2 = time.time()
            
            self.save(epoch=epoch+1) #save the model

            if (epoch+1) % 30 == 0:
                self.validaton_performance(epoch)
                self.config.parameters['lr'] *= 0.8
                for param_group in optimizer.param_groups:
                     param_group['lr'] = self.config.parameters['lr']

    def validaton_performance(self, epoch):
        val_loss = 0
        iteration = 0
        self.model.eval()
        dataset_length = len(self.val_loader.dataset)

        for i, data in enumerate(self.train_loader):
            images = data['image']
            target = data['target']
            normalized_images = data['normalized_image']
            if self.cuda_flag:
                images = images.cuda(non_blocking=True)
                target = target.cuda(non_blocking=True)
                normalized_images = normalized_images.cuda(non_blocking=True)
            with torch.no_grad():
                prediction = self.model(normalized_images)
                loss = self.loss_function(prediction, target)
                val_loss += loss.item() * len(images)

        val_loss /= dataset_length
        self.writer.add_scalar("Validation/1.Loss", val_loss, epoch)
        self.model.train()

    def save(self, epoch, file="model.pth"):
        
        if not os.path.exists("checkpoints"):
            os.mkdir("checkpoints")
        torch.save(self.model.state_dict(), "checkpoints/{:02d}.pth".format(epoch))
        torch.save(self.optimizer.state_dict(), "checkpoints/optimizer_{:02d}.pth".format(epoch))
        
    def load(self, file=" model.pth"):
        checkpoints = glob.glob("checkpoints/[0-9]*.pth")
        if len(checkpoints)>0:
            ckpt = max(checkpoints, key=os.path.getmtime)
            checkpoint_state_dict = torch.load(ckpt)
            model_state_dict = self.model.state_dict()
            for key in model_state_dict:
                if key in checkpoint_state_dict and  model_state_dict[key].shape!=checkpoint_state_dict[key].shape:
                    checkpoint_state_dict[key] = model_state_dict[key]

            self.model.load_state_dict(checkpoint_state_dict)
        else:
            print("No checkpoint found to load weights")






