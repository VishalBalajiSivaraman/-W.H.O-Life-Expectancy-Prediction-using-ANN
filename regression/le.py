# -*- coding: utf-8 -*-
"""LE.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1MMziSYCgvUDUK-YpNgJ_zlXrAU7Tby4A
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import zipfile

zip = zipfile.ZipFile('archive.zip')
zip.extractall()

df=pd.read_csv("Life Expectancy Data.csv")
df['LE']=df['Life expectancy ']
df['GDP']=round(df['GDP'])
df['Alcohol']=round(df['Alcohol'])
df[' BMI ']=round(df[' BMI '])
df[' HIV/AIDS']=round(df[' HIV/AIDS'])
df['Schooling']=round(df['Schooling'])
df[' thinness  1-19 years']=round(df[' thinness  1-19 years'])
df[' thinness 5-9 years']=round(df[' thinness 5-9 years'])
df=df.drop(columns=['Year','Life expectancy ','Income composition of resources'])
df=df.dropna(how='any')

df

df['Country'].unique()

from sklearn.preprocessing import LabelEncoder
le=LabelEncoder()
le1=LabelEncoder()
df['Status']=le.fit_transform(df['Status'])
df['Country']=le1.fit_transform(df['Country'])
df

X=df.iloc[:,:-1].values
y=df.iloc[:,-1].values

X[:,15:16]

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2 ,random_state = 1)

from sklearn.preprocessing import StandardScaler
norm = StandardScaler()
X_train[:,15:16] = norm.fit_transform(X_train[:, 15:16])
X_test[:, 15:16] = norm.fit_transform(X_test[:, 15:16])

X_train[:,15:16]

import tensorflow as tf
ann = tf.keras.models.Sequential()
ann.add(tf.keras.layers.Dense(units=100, activation='relu'))
ann.add(tf.keras.layers.Dense(units=100, activation='relu'))
ann.add(tf.keras.layers.Dense(units=100, activation='relu'))
ann.add(tf.keras.layers.Dense(units=1))

ann.compile(optimizer = 'adam', loss = 'mean_squared_error')
history=ann.fit(X_train, y_train, batch_size=32, epochs=2500)
ann.save("LE.h5")

plt.figure(0)
plt.plot(history.history['loss'], label='training loss')
plt.title('Loss')
plt.xlabel('epochs')
plt.ylabel('loss')
plt.legend()
plt.savefig('Loss.png')
print("Saved Model & Graph to disk")

model = tf.keras.models.load_model('LE.h5')
print("Loaded model from disk")

y_pred = model.predict(X_test)
y_pred=np.round(y_pred)
np.set_printoptions(precision=2)
print(np.concatenate((y_pred.reshape(len(y_pred),1), y_test.reshape(len(y_test),1)),1))

from sklearn.metrics import r2_score
print("Accuracy Score for the algorithm=>{}%".format(round(r2_score(y_test,y_pred)*100),2))
