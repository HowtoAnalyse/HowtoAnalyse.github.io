---
layout: post
title: Project Summary on Text Classification
author: sara
categories: [Machine Learning]
image: assets/images/dogs/pexels-photo-144640.png
featured: False
---
# Code structure
--------------

```
├── base
│   └── base_model.py        - the abstract class of the model.
│ 
├── model                    - neural nets
│   │── fastText_model.py    - fastText model
│   └── cnn_model.py         - CNN
│
├── trainer 
│   └── textClf_trainer.py   - trainer for text classification models
│
├── configs
│   │── fastText_ops.json    - configurations of fastText model
│   │── cnn_ops.json         - configurations of CNN
│   └── config.yml           - configurations when using pre-trained glove or word2vec
│   
├──  mains
│    └── textClf_main.py     - run the pipeline
│  
├──  data_loader  
│    └── textClf_data.py     - load and process data with word and char n-grams options.
│ 
└── utils
     ├── config.py           - load configuration files and locate checkpoint folder
     └── logger.py           - logentries api

```

# Project architecture 
--------------

<div align="center">

<img align="center" hight="600" width="600" src="https://github.com/Mrgemy95/Tensorflow-Project-Templete/blob/master/figures/diagram.png?raw=true">

</div>

## Main Components

### Models
--------------
- #### **Base model**
    
    Base model is an abstract class that contains most shared stuff among different neural networks:
    - ***Save*** -This function to save a checkpoint to the folder. 
    - ***Load*** -This function to load a checkpoint from the folder.
    - ***Cur_epoch, Global_step counters*** -These variables to keep track of the current epoch and global step.
    It is inherited by models created for this project

- #### **FastText**

    [Bag of Tricks for Efficient Text Classification](https://arxiv.org/abs/1607.01759)

- #### **CNN**

    [Convolutional Neural Networks for Sentence Classification](http://www.aclweb.org/anthology/D14-1181)

### Trainer
--------------
    
- #### textClf_trainer
    
    All models in this project share one trainer. It implement the training process of each step and each epoch.

### Data Loader

This class is responsible for raw data handling with feature engineering options including word or char n-grams, and provide an easy interface that can be used by the trainer.

### Logger

A common module for log management and analytics using Logentries API.

### Configuration

Cnofigurations for created or pre-trained model

### Main

The main part containing pipeline instructions of the entire project.
1. Parse the config file.
2. Create a tensorflow session.
3. Create an instance of "Model", "Data_Generator" and "Logger" and parse the config to all of them.
4. Create an instance of "Trainer" and pass all previous objects to it.

# Reference

1. [Bag of Tricks for Efficient Text Classification](https://arxiv.org/abs/1607.01759)
2. [Convolutional Neural Networks for Sentence Classification](http://www.aclweb.org/anthology/D14-1181)
3. [text_classification](https://github.com/brightmart/text_classification)
4. [Tensorflow Project Template](https://github.com/MrGemy95/Tensorflow-Project-Template/blob/master/README.md)