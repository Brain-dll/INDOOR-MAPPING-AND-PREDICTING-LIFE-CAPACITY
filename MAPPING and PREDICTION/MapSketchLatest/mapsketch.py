import turtle
import random
import time
import os
from firebase import firebase
from math import *
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

scale = 1                       # SCALE FOR THE RECTANGLE AREA TO DRAW AFTERWARDS
radius = 5                      # RADIUS OF THE CIRCLE IMAGES
scanWidthDegree = int(40)       # SCAN ANGLE

firebase = firebase.FirebaseApplication("YOUR FIREBASE REALTIME DATABASE REPO ADRESS (URL)",None)

while True:
    result = firebase.get('/MAPPRIME','')       ## measurements are obtained from server (MAPPRIME our database folder you have to create and choose own folder) 
    if result != None:
        result = result["Angle"].values()
        if len(result) == 360:
            result = list(enumerate(result))         
            result1 = [list(item) for item in result]
            
            air_quality = firebase.get("/DATAPRIME/Air-quality", "")  ## like MAPPRIME
            humidity = firebase.get("/DATAPRIME/Humidity", "")
            temperature = firebase.get("/DATAPRIME/Temperature", "")
            print("DATA Obtained")
            break
        else:
            print("More Data Required")
    else:
        print("No Data")
        time.sleep(1)




##########              TO TRIM THE RANDOM PEAKS                  
##########              TO TRIM THE RANDOM PEAKS


a = 0       # previous value index
b = 0       # next value index

for x in range(len(result1)):       ## to check x-1 and x+1 when there is peak
    if x == 0:
        a = len(result1)-1
        b = x+1
    elif x == len(result1)-1:
        a = x-1
        b = 0
    else:
        a = x-1
        b = x+1
    if abs(result1[x][1]-result1[a][1])>100 and abs(result1[b][1]-result1[a][1])<50:
        result1[x][1] = (result1[b][1]+result1[a][1])/2
        



for x in range(len(result1)):       ## to check x-2 and x+2 when there is peak
    if x == 0 or x == 1:
        a = x-2+len(result1)
        b = x+2
    elif x == len(result1)-1 or len(result1)-2:
        a = x-2
        b = x+2-len(result1)
    else:
        a = x-2
        b = x+2
    if abs(result1[x][1]-result1[a][1])>100 and abs(result1[b][1]-result1[a][1])<50:
        result1[x][1] = (result1[b][1]+result1[a][1])/2
        
        
        
        
for x in range(len(result1)):       ## to check x-3 and x+3 when there is peak
    if x == 0 or x == 1  or x == 2:
        a = x-3+len(result1)
        b = x+3
    elif x == len(result1)-1 or len(result1)-2:
        a = x-3
        b = x+3-len(result1)
    else:
        a = x-3
        b = x+3
    if abs(result1[x][1]-result1[a][1])>100 and abs(result1[b][1]-result1[a][1])<50:
        result1[x][1] = (result1[b][1]+result1[a][1])/2
    
############                END
############                END

  

#############               TO SETUP SCANNING FOR SMALL (MORE ACCURATE) 
#############               PARTS AROUND 0 90 180 AND 270 TO HAVE BETTER SKETCH

rightAverage = 0
upAverage = 0
leftAverage = 0
downAverage = 0

cosIndex = -scanWidthDegree/2
halfScanAngle = int(scanWidthDegree/2)

for x in range(scanWidthDegree+1):
    if x < halfScanAngle:
        rightAverage += result1[360-halfScanAngle+x][1]*cos(radians(cosIndex))
    else:
        rightAverage += result1[x-halfScanAngle][1]*cos(radians(cosIndex))
    
    upAverage += result1[90-halfScanAngle+x][1]*cos(radians(cosIndex))
    leftAverage += result1[180-halfScanAngle+x][1]*cos(radians(cosIndex))
    downAverage += result1[270-halfScanAngle+x][1]*cos(radians(cosIndex))
    cosIndex+=1

rightAverage = rightAverage/(scanWidthDegree+1)
upAverage = upAverage/(scanWidthDegree+1)
leftAverage = leftAverage/(scanWidthDegree+1)
downAverage = downAverage/(scanWidthDegree+1)

rightAverage = int(rightAverage)        # average distances from each direction
upAverage = int(upAverage)
leftAverage = int(leftAverage)
downAverage = int(downAverage)


###############                         END
###############                         END



#################              TURTLE SETUP AND RED DOT ON MIDDLE READY
#################              TURTLE SETUP AND RED DOT ON MIDDLE READY

screen = turtle.Screen()
screen.bgcolor('gray')
rootwindow = screen.getcanvas().winfo_toplevel()
rootwindow.call('wm', 'attributes', '.', '-topmost', '1')
rootwindow.call('wm', 'attributes', '.', '-topmost', '0')

myPen = turtle.Turtle()
myPen.color('red')
myPen.width(5)
myPen.speed(0)
myPen.hideturtle()


myPen.penup()
myPen.setpos(0,-radius)
myPen.pendown()
myPen.begin_fill()
myPen.circle(radius)
myPen.end_fill()
myPen.penup()
    
myPen.color("white")            ## writing some parameters on screen
myPen.setpos(-335, 260)
stringAirquality = "Air-quality     : %s" %air_quality
myPen.write(stringAirquality, False, align="left", font=("Arial", 15, "normal"))

myPen.setpos(-335, 230)
stringHumidity = "Humidity       : %s" %humidity
myPen.write(stringHumidity, False, align="left", font=("Arial", 15, "normal"))

myPen.setpos(-335, 200)
stringTemperature = "Temperature : %s" %temperature
myPen.write(stringTemperature, False, align="left", font=("Arial", 15, "normal"))


#################               END
#################               END


##################              DRAWING BLUE DOTS
##################              DRAWING BLUE DOTS

myPen.width(5)
myPen.color('Blue')
for x in range(len(result1)):
    if x <= halfScanAngle or x>=(360-halfScanAngle):
        myPen.color('green')
    elif x >= (90-halfScanAngle) and x<=(90+halfScanAngle):
        myPen.color('green')
    elif x >= (180-halfScanAngle) and x<=(180+halfScanAngle):
        myPen.color('green')
    elif x >= (270-halfScanAngle) and x<=(270+halfScanAngle):
        myPen.color('green')
    else:
        myPen.color('blue')
        
    degree = result1[x][0]
    length = result1[x][1]
    
    os.system('cls')
    print('Degree: ', degree)
    print('Length', length)
    
    myPen.setpos((scale*length*cos(radians(degree)), scale*length*sin(radians(degree))))
    myPen.setheading(degree)
    myPen.right(90)
    myPen.forward(radius)
    myPen.setheading(degree)
    
    myPen.pendown()
    myPen.begin_fill()
    myPen.circle(radius)
    myPen.end_fill()
    myPen.penup()

##################                  END
##################                  END



##################                  CALCULATE THE AREA
##################                  IN CM2 AND PRINT

area = (rightAverage+leftAverage)*(upAverage+downAverage)
os.system('cls')
print('AVERAGE AREA (CM2): ', area)
    
##################                  END
#################                   END



######################              TO SKETCH THE ESTIMATED AVERAGE AREA
######################

rightAverage *= scale
upAverage *= scale
leftAverage *= scale
downAverage *= scale

myPen.color('orange')
myPen.width(5)
myPen.speed(3)

myPen.setpos((0,0))         #### moving the cursor to the top right corner
myPen.setheading(90)
myPen.forward(upAverage)
myPen.right(90)
myPen.forward(rightAverage)
myPen.right(180)

myPen.pendown()
for i in range(2):
    myPen.forward(rightAverage+leftAverage)
    myPen.left(90)
    myPen.forward(upAverage+downAverage)
    myPen.left(90)
    
myPen.penup()
myPen.setpos((0,0))         #### moving the cursor back to origin
myPen.setheading(0)

myPen.color("orange")           ### typing area as text on the screen
myPen.setpos(-100, 250)
myPen.write("Area Measured", False, align="left", font=("Arial", 25, "normal"))
myPen.setpos(-100, 215)
myPen.write(str(area) + " cm2", False, align="left", font=("Arial", 25, "normal"))



###############         MACHINE LEARNING TO CALCULATE # OF PEOPLE CAN LIVE HERE
###############         DRAWING DATA

data = pd.read_csv("veri.csv") # TRAIN DATA  veriyi csv den çektim

result2 = firebase.get('/DATAPRIME','')
result2 = list(result2.values())
firebase.put("/DATAPRIME", "Area", area)
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
human_number = floor(Y_pred)  # insan sayısı, virgüllü olamaz tabana yuvarladım

# UPLOAD DATA TO MY CLOUD SERVER
firebase.put("","NOFPRIME", human_number) # Upload new data

myPen.color("black")
myPen.setpos(140, 256)
stringHumanNumber = "LIFE CAPACITY : %s" %human_number
myPen.write(stringHumanNumber, False, align="left", font=("Arial", 15, "normal"))
myPen.color("orange")

###############         END
###############         END


#################                   adding some spice
#################

myPen.speed(0)
fraction = (leftAverage+rightAverage) / 8
topX = -leftAverage                         ### topX, topY
topY = upAverage                            ### botX, botY
botX = -leftAverage
botY = upAverage
upRemaining = leftAverage+rightAverage         
leftRemaining = upAverage+downAverage
downRemaining = leftAverage+rightAverage
rightRemaining = upAverage+downAverage

fillingCompleted = False
topIsDone = False
leftIsDone = False

while fillingCompleted == False:
    if topIsDone == False:
        topX += fraction
        upRemaining -= fraction
        if upRemaining < fraction:
            topIsDone = True
    else:
        if upRemaining > 0:
            topX += upRemaining
            topY -= upRemaining
            upRemaining = 0
        if rightRemaining > fraction:
            topY -= fraction
            rightRemaining -= fraction
            
    if leftIsDone == False:
        botY -= fraction
        leftRemaining -= fraction
        if leftRemaining < fraction:
            leftIsDone = True
    else:
        if leftRemaining > 0:
            botX -= leftRemaining
            botY -= leftRemaining
            downRemaining += leftRemaining
            leftRemaining = 0
        if downRemaining > fraction:
            botX += fraction
            downRemaining -= fraction
    
    if rightRemaining < fraction and downRemaining < fraction:
        fillingCompleted = True
        
    myPen.setpos((topX, topY))
    myPen.pendown()
    myPen.setpos((botX, botY))
    myPen.penup()
                
##################              END
##################              END

turtle.mainloop()




