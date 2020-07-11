# veri.csv ile kod aynı dizinde olmalı

from firebase import firebase
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import math

# DRAWIMG DATA
data = pd.read_csv("veri.csv") # TRAIN DATA  veriyi csv den çektim

firebase = firebase.FirebaseApplication("https://fir-arduino-269f4.firebaseio.com/",None)

result2 = firebase.get('/DATA','')
result2 = list(result2.values())
result2[1] = result2[1]/10000.0 # Convert cm unit area to m unit area
result2 = np.array(result2)
result2 = result2.reshape(1,-1)  # Air-quality, Area, Humudity, Temperature veriyi tek satıra çevirmek için şekillendirdim

# DATA SPLİT
x_train = data.iloc[:,:-1].values  # veri kümem öğrenme verisini ve sonucu beraber tutuyordu onları ayırdım
y_train = data.iloc[:,-1:].values

# DATA NEW DESIGN ayırdığım verilerin parametre isimlerini verdim tekrardan 
X_train = pd.DataFrame(data = x_train, index = range(34), columns = ["Air-q","Area","Humidity","Temperature"])
Y_train = pd.DataFrame(data = y_train, index = range(34), columns= ["NoL"])
X_test = pd.DataFrame(data = result2, index = range(1), columns = ["Air-q","Area","Humidity","Temperature"])

# REGRESSION
regression = LinearRegression()  # modelin nesnesini oluşturdum

regression.fit(X_train,Y_train)  # öğrenme verisini ve sonucu verdim . böylece algoritma parametreler arası ilişki kurdu
Y_pred = regression.predict(X_test) # tahmin için internetten .ektiğim veriyi girdim

# FLOOR NUMBER
human_number = math.floor(Y_pred)  # insan sayısı, virgüllü olamaz tabana yuvarladım



# UPLOAD DATA TO MY CLOUD SERVIS
firebase.delete("/NUMBEROFLIFE", "")  # Delete old data
upload = firebase.post("/NUMBEROFLIFE/", human_number) # Upload new data

