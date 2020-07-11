



################            FIRST MODULATION ON THE DATA            
################            2 FORS
"""

for x in range(1, len(result1)-1):
    if abs(result1[x+1][1]-result1[x][1])>3 and abs(result1[x+1][1] - result1[x-1][1]) <= 5:
        result1[x][1] = (result1[x+1][1]+result1[x-1][1])/2
    

liste = []
for i in range(len(result1)-1):
    if abs(result1[i+1][1] - result1[i][1]) <= 5:
        liste.append(result1[i+1][1])
        
    elif abs(result1[i+1][1] - result1[i][1]) > 5 and len(liste)>=2:
        min = liste[0]
        max = result1[i+1][1]
        back = len(liste) + 1
        
        liste = list()

        n = abs(max - min)

        unit = n / back
        if max - min > 0:
            for k in range(i-back,i+1):
                result1[k][1] = ceil(result1[k][1] + (unit * (k - (i - back))))
        if max - min < 0:
            for k in range(i-back,i+1):
                result1[k][1] = ceil(result1[i][1] - (unit * (k - (i - back))))
        min = max

"""
###############                         END
###############                         END



#################           SECOND MODULATION ON THE DATA              
#################           2 FORS
"""

for i in range(1,len(result1)-1):
    if result1[i][1] > 400 or result1[i][1] < 2:
        result1[i][1] = (result1[i-2][1] + result1[i+2][1]) / 2 
    if abs(result1[i+1][1] - result1[i-1][1]) < 3 and abs(result1[i+1][1] - result1[i][1]) > 5 :
        result1[i][1] = (result1[i+1][1] + result1[i-1][1]) / 2

liste = []
for i in range(len(result1)-1):
    if abs(result1[i+1][1] - result1[i][1]) <= 5:
        
        liste.append(result1[i+1][1])
        
    elif abs(result1[i+1][1] - result1[i][1]) > 5 and len(liste) >= 2:
        min = liste[0]
        max = result1[i+1][1]
        back = len(liste)
        
        liste = list()

        n = abs(max - min)
        unit = n / back
        if max - min > 0:
            for k in range(i-back+1,i+1):
                result1[k][1] = ceil(result1[i-back][1] + (unit * ((k + 1) - (i - back+1))))
        if max - min < 0:
            for k in range(i-back,i+1):
                result1[k][1] = ceil(result1[i-back][1] - (unit * ((k + 1) - (i - back+1))))
        min = max
        
"""     
###################                     END
###################                     END


####################        THIRD MODULATION ON THE DATA               
####################        2 FORS
"""

for i in range(1,len(result)-1):
    if result1[i][1] > 400 or result1[i][1] < 2:
        result1[i][1] = (result1[i-2][1] + result1[i+2][1]) / 2 
    if abs(result1[i+1][1] - result1[i-1][1]) < 3 and abs(result1[i+1][1]- result1[i][1]) > 5 :
        result1[i][1] = (result1[i+1][1] + result1[i-1][1]) / 2
        
      
for k in [0,90,180,270]:
    corner = (result1[k+89][1]**2 + result1[k][1]**2) ** 0.5
    angle = degrees(atan(result1[k+89][1] / result1[k][1]))
    dif_b = corner - result1[k][1]
    dif_a = corner - result1[k+89][1]
    angle = int(angle)
    for x in range(k,angle+k):
        result1[x][1] = result1[k][1] + ((x - k) * (dif_b / angle))
    
    for x in range(angle+k, k+89):
        result1[x][1] = corner - ((x - (angle+k)) * (dif_a / (89 - angle)))
    if k > 0:
        result1[k][1] = (result1[k-1][1] + result1[k+1][1]) / 2

"""
###################                     END
###################                     END





