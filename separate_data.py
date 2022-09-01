import arcpy
from datetime import datetime
from datetime import timedelta
import pandas as pd

arcpy.env.overwriteOutput = True
arcpy.env.workspace = r"D:\RENCA\Renca\RencaRoads\RencaWaste.gdb"

originalData="T436_24Proj"
FID_mma=[]
lat_ori=[]
lon_ori=[]
speed=[]
Fecha=[]
Hora=[]
NEAR_FID=[]
NEAR_X=[]
NEAR_Y=[]



sr = arcpy.Describe(originalData).spatialReference



#["Velocidad","NEAR_FID","SHAPE@XY","Hora","NEAR_FID","NEAR_X","NEAR_Y"]
np_array=arcpy.da.FeatureClassToNumPyArray(originalData,["Fecha","Latitud","Longitud","Velocidad","NEAR_FID","Hora"],spatial_reference=sr)
#print(np_array)
Cords=arcpy.da.FeatureClassToNumPyArray(originalData,["Shape"],spatial_reference=sr)

Lat=[]
Lon=[]

for i in range(len(Cords)):
    lat,lon=Cords[i][0]
    Lat.append(lat)
    Lon.append(lon)

  


df=pd.DataFrame(np_array,columns=["Fecha","Hora","Latitud","Longitud","Velocidad","NEAR_FID"])
df["Latitud(UTM)"]=Lat
df["Longitud(UTM)"]=Lon

#print(df.head())




FMT = '%H:%M:%S'
inicio=0
tol=35
tramos=[]
td=timedelta(seconds=30)
for i in range(0,len(df)-1):
    #actual=str(df.iloc[i].Hora)
    actual=datetime.strptime(str(df.iloc[i].Hora),FMT)
    stop=datetime.strptime(str(df.iloc[i+1].Hora),FMT)
    diff=stop-actual
    if((diff)>td):
        tramos.append(df.iloc[inicio:i])
        inicio=i+1



for tramo in tramos:
    if(len(tramo)>10):
        print(tramo)
'''

print(tramos)

    for finalRow in finalCursor:
        FID_mma.append(finalRow[1])
        speed.append(finalRow[0])
        #lat_ori.append(round(float(finalRow[2][0])/10000,4))
        #lon_ori.append(round(float(finalRow[2][1])/100000,4))
        lat_ori.append(finalRow[2][0])
        lon_ori.append(finalRow[2][1])
        var=(finalRow[3])
        NEAR_FID.append(finalRow[4])
        NEAR_X.append(finalRow[5])
        NEAR_Y.append(finalRow[6])
        var=str(var)
        var=datetime.strptime(var, "%H:%M:%S")
        Hora.append(var)





spatial_reference = arcpy.Describe(originalData).spatialReference

dicc={}
tramos=[]
cont=1
dicc[cont]=tramos

recordar=[]

desde=1
sets=[]

for i in range(len(FID_mma)):
    var=str(Hora[i])
    var=var.split(" ")
    var=var[1]
    Hora[i]=var



sets=[]
conjunto=[]
desde=1
hasta=1000
for i in range(1,len(FID_mma)):
    FMT = '%H:%M:%S'
    var= datetime.strptime(Hora[i],FMT)-datetime.strptime(Hora[i-1],FMT)
    var=str(var)
    #print(var)
    hour=var[0:1]
    minutes=var[2:4]
    seconds=var[5:]
    time_delta=(int(hour)*3600)+(int(minutes)*60)+int(seconds)
    if(time_delta <=120):
        conjunto.append((i,Hora[i]))
    else:

        conjunto.append((i,Hora[i]))
        #print(conjunto)
        sets.append(conjunto)
        conjunto=[]



           
tramos=[]
OBJ_ID=1
for s in sets:
    if(len(s)>=20):
        inicio,t1=s[0]
        fin,t2=s[-1]
        
        limites=originalData+"_"+str(inicio)+"_"+str(fin+1)
        arcpy.CreateFeatureclass_management(arcpy.env.workspace, limites, "POINT", "", "DISABLED", "DISABLED",spatial_reference)
        arcpy.AddField_management(limites,"FID","LONG")
        arcpy.AddField_management(limites,"Latitude","LONG")
        arcpy.AddField_management(limites,"Longitude","LONG")
        arcpy.AddField_management(limites,"Speed","String")
        arcpy.AddField_management(limites,"Hora","String")
        arcpy.AddField_management(limites,"NEAR_FID","LONG")
        arcpy.AddField_management(limites,"NEAR_X","LONG")
        arcpy.AddField_management(limites,"NEAR_Y","LONG")
        cursor=arcpy.da.InsertCursor(limites,"*")
        OBJ_ID=inicio
        for i in range(inicio-1,fin):
            row=[OBJ_ID,(lat_ori[i],lon_ori[i]),FID_mma[i],lat_ori[i],lon_ori[i],speed[i],Hora[i],NEAR_FID[i],NEAR_X[i],NEAR_Y[i]]
            OBJ_ID+=1
            cursor.insertRow(row)
        del cursor
        print(limites+" created")
        

'''