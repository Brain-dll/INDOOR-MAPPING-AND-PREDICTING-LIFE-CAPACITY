from firebase import firebase
from math import *
import random



firebase = firebase.FirebaseApplication("https://firstexample-9da88.firebaseio.com/",None)

firebase.delete("/Mapping/Angle", "")


for i in range(360):
    firebase.post("/Mapping/Angle", random.randrange(100, 300))
    print("data sent   :  i = ", i)
    
    

    




