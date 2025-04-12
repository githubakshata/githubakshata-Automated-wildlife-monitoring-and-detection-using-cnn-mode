import sys
import os
import time

import torch
import torchvision.transforms as transforms
from PIL import Image
import timm

classes = {'Horse': 0, 'bald_eagle': 1, 'black_bear': 2, 'bobcat': 3, 'cheetah': 4, 'cougar': 5, 'deer': 6, 'elk': 7, 
           'gray_fox': 8, 'hyena': 9, 'lion': 10, 'raccoon': 11, 'red_fox': 12, 'rhino': 13, 'tiger': 14, 'wolf': 15, 'zebra': 16}

class_index = {v:k for k,v in classes.items()}

class AnimalClassifier:
    

    def __init__(self, model_path):
        # Load Model
        self.model = timm.create_model("rexnet_150", num_classes=len(classes))
        self.model.load_state_dict(torch.load(model_path, map_location="cpu"))
        self.model.eval()

        # Define Transform (Must Match Training)
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),  # Resize to match training
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])  # ImageNet normalization
        ])

    def detect(self, image):
        # Load and Preprocess Image
        image = Image.fromarray(image)
        image = self.transform(image).unsqueeze(0)  # Add batch dimension
        
        # Predict
        with torch.no_grad():
            output = self.model(image)
            predicted_class = torch.argmax(output, dim=1).item()

        prediction = class_index[predicted_class]
        return prediction
