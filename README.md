# MC-collision-CNN
In the Belle II electromagnetic calorimeter (ECL), two particle showers close together, the energy may be overlap. It is difficult to separate the energy. Under Monte Carlo simulation, the shower is grouped into 5×5 CsI crystals without 4 corners. By the image map of the energies, convolutional neural network (CNN) is used to split the photon shower. Choose the energy distribution of the showers under 2 GeV, the dataset is concerned as the training model. The energy of 4 GeV as the dataset that test the model. Mainly test the influence of CNN models of different structures on energy resolution. In addition, test Fully-connected network as a simple model, and test LeNet and AlexNet as a famous kind of CNN. The purpose is to improve the energy resolution.

## system
- MacBook M1

# test
1. Use verify.cc to count root data into Map data and variable
2. dist_classification.py to classify the distance between the extrema of the region
3. create_gamma_map to generate npz files with image area 21x21
4.CNN-2D_21x21.py to run the model
- 21x21 puts the center point between particles at the center of the picture, if you want to throw 27x50 directly into the model, you don’t need pre-processing