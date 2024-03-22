This Project is about training a AI model using transfer learning by taking a pretrained resnet50 model where binary data of pe files are fed to the model. the data is collected from various kaggle repos and fed to BPI python code which extracts pe's binary data. the data is splitted into 3 types namely train test and validate which is fed to pre trained resnet50 model. the data is trained into the model and tested along by using confusion matrix. as of now due to limited test samples the accuracy achieved is 98.19%

[update]

expanding the dataset(25672) and tested, now the model is 94.8% efficient with f_score of 0.86.

[Update]
expanded the dataset(226,572) and tested, now the model is 93.5% efficient with f_score of 0.86