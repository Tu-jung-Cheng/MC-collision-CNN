import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split


Gamma_Map = np.load('Gamma_Map.npz')

M=Gamma_Map['M0_21']
gamma0MCE=Gamma_Map['gamma0MCE']
gamma1MCE=Gamma_Map['gamma1MCE']
gamma0E=Gamma_Map['gamma0E']
gamma1E=Gamma_Map['gamma1E']
y_train=np.zeros((len(gamma0MCE),2))
#print(M.shape,y_train.shape)
for i in range(len(gamma0MCE)):
    y_train[i][0]=gamma0MCE[i]
    y_train[i][1]=gamma1MCE[i]

x, y = np.array(M), np.array(y_train)
x_train, x_test, y_train, y_test=train_test_split(x, y, test_size=0.20)

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import *
from tensorflow.keras.optimizers import Adam,Adadelta, Adagrad, Adamax, Nadam
import tensorflow as tf
from tensorflow.keras.regularizers import l2 
model = Sequential()
model.add(Reshape((21,21,1), input_shape=(21,21)))
model.add(Conv2D(64, kernel_size=(5,5), activation='relu'))
#model.add(Dropout(0.001))

model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Conv2D(128, kernel_size=(3,3), activation='relu'))
#model.add(Dropout(0.1))

model.add(Flatten())
#model.add(Dropout(0.1))
model.add(Dense(1000, activation="relu"))
#model.add(BatchNormalization())

#model.add(Dropout(0.1))
#model.add(Dense(2))
model.add(Dense(2, kernel_regularizer=l2(0.08)))


model.compile(loss='mse',optimizer=Adam(),metrics=['accuracy'])
#model.compile(loss='mse',optimizer = tf.keras.optimizers.SGD(learning_rate =0.5),metrics=['accuracy'])


model.fit(x_train, y_train, epochs=20, batch_size=70,validation_data=(x_test, y_test))
'''
model.save('my_model_2GeV.h5')
print('Performance (training)')
print('Loss: %.5f, Acc: %.5f' % tuple(model.evaluate(x_train, y_train)))
print('Performance (testing)')
print('Loss: %.5f, Acc: %.5f' % tuple(model.evaluate(x_test, y_test)))
'''


ypred = model.predict(x_train)
gammaE,gammaE_1=[],[]
for i in range(len(ypred)):
    gammaE.append(ypred[i,0]-y_train[i,0])
    gammaE_1.append(ypred[i,1]-y_train[i,1])
print('training')

print("particle 0  avg={:.4f}, std={:.4f}".format(np.average(gammaE),np.std(gammaE)))
print("particle 1  avg={:.4f}, std={:.4f}".format(np.average(gammaE_1),np.std(gammaE_1)))
fig = plt.figure(figsize=(12,6), dpi=80)
plt.subplot(1,2,1)

bins = np.linspace(-0.5, 0.5, 50)

plt.hist(gammaE, bins, alpha = 0.6)
plt.hist(gammaE_1, bins, alpha = 0.6)
#plt.legend(['gamma0-gamma0MCE', 'gamma1-gamma1MCE'])
plt.legend([r"$E_{\gamma_0}-E_{\gamma_{0,MC}}$", r"$E_{\gamma_1}-E_{\gamma_{1,MC}}$"])

plt.title("training")

ypred_1 = model.predict(x_test)
gammaE_t,gammaE_1_t=[],[]
for i in range(len(ypred_1)):
    #gammaE.append(ypred[i,0]-y_train[i,0])
    #gammaE_1.append(ypred[i,1]-y_train[i,1])
    gammaE_t.append(ypred_1[i,0]-y_test[i,0])
    gammaE_1_t.append(ypred_1[i,1]-y_test[i,1])

print('testing')

print("particle 0  avg={:.4f}, std={:.4f}".format(np.average(gammaE_t),np.std(gammaE_t)))
print("particle 1  avg={:.4f}, std={:.4f}".format(np.average(gammaE_1_t),np.std(gammaE_1_t)))
plt.subplot(1,2,2)

bins = np.linspace(-0.5, 0.5, 50)

plt.hist(gammaE_t, bins, alpha = 0.6)
plt.hist(gammaE_1_t, bins, alpha = 0.6)

#plt.legend(['gamma0-gamma0MCE', 'gamma1-gamma1MCE'])
plt.legend([r"$E_{\gamma_0}-E_{\gamma_{0,MC}}$", r"$E_{\gamma_1}-E_{\gamma_{1,MC}}$"])

plt.title("testing")
"""

fig = plt.figure(figsize=(6,6), dpi=80)
bins = np.linspace(-0.5, 0.5, 50)

plt.hist(gammaE, bins, alpha = 0.6, label='Train_Map-gammaMCE')
plt.hist(gammaE_1, bins, alpha = 0.6, label='E-gammaMCE')
"""

import time
t = time.localtime()
result = time.strftime("%m%d_%H%M%S", t)
plt.savefig('21x21_{}.png'.format(result))
#plt.show()


