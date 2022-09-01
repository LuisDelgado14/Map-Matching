from calendar import c
from heapq import merge
import arcpy
import pandas as pd
import numpy as np
import os 



output_path=r"D:\RENCA\Renca\Results_Test"
path=r"D:\RENCA\Renca\RencaRoads\RencaWaste.gdb"

arcpy.env.workspace = path
"RencaRedVial\RedVialComunasSantiago"



#datasets=arcpy.ListDatasets()
datasets=["T433_27Proj"]


for i in range(len(datasets)):
  if(datasets[i]!=u'RencaRedVial'):
    #print(datasets[i])
    originalData=datasets[i].split("_results")
    originalData=originalData[0]
    output_path=r"D:\RENCA\Renca\Results_Test"
    dir=originalData.split("_")
    dir=dir[0]+"_"+dir[1]
    output_path=output_path+"\\"+dir
    if not os.path.exists(output_path):
      #Create a path to save as csv the shp files
      dicc_results={}
      os.mkdir(output_path)
      print("The outputs files will be saved in this path: "+output_path)
      #Search the shapefile whose name start with $originalData$ 
      for feature_results in arcpy.ListDatasets():
        if(feature_results.find(originalData)==0):
          originalLayer=path+"\\"+originalData
          print(originalLayer)
          arcpy.env.workspace=path+"\\"+feature_results
          print(arcpy.env.workspace)
          for layer_results in arcpy.ListFeatureClasses():
            arcpy.management.Delete("TEMP")
            arcpy.CopyFeatures_management(layer_results,"TEMP")
            arcpy.Near_analysis("TEMP",path+"\RencaRedVial\RedVialComunasSantiago")
            
            df_original=pd.DataFrame(arcpy.da.FeatureClassToNumPyArray(originalLayer,["OBJECTID","NEAR_FID","Hora","Speed"]),columns=["OBJECTID","NEAR_FID","Hora","Speed"])  
            df_results=pd.DataFrame(arcpy.da.FeatureClassToNumPyArray("TEMP",["OBJECTID","FID"]),columns=["OBJECTID","FID"])
            Most_nearest=pd.DataFrame(arcpy.da.FeatureClassToNumPyArray(layer_results,["OBJECTID","FID"]),columns=["OBJECTID","FID"])
            coords=arcpy.da.FeatureClassToNumPyArray(layer_results,["OBJECTID","Shape"])
            Lat=[]
            Lon=[]
            for oi,coord in coords:
              lat,lon=coord
              Lat.append(lat)
              Lon.append(lon)
            df=pd.merge(df_original,df_results,on="OBJECTID",how='inner')
            df["REAL_FID"]=df["NEAR_FID"]
            df["MMA_FID"]=df["FID"]
            df["Latitude"]=Lat
            df["Longitude"]=Lon
            df["MOST_NEAREST"]=Most_nearest["FID"]
            df=df.drop(["NEAR_FID","FID"],axis=1)
            Compare=[]
            MMA_FID=list(df["MMA_FID"])
            REAL_FID=list(df["REAL_FID"])
            for i in range(len(MMA_FID)):#This cicle compare the real FID and the algorith output FID.
              if(MMA_FID[i]==0):
                Compare.append("ZERO")
              elif(MMA_FID[i]==REAL_FID[i]):
                Compare.append("SAME")
              else:
                Compare.append("DIFFERENT")

            df["COMPARE"]=Compare


            order_of_columns=["OBJECTID","Latitude","Longitude","Hora","Speed","MOST_NEAREST","REAL_FID","MMA_FID","COMPARE"]
            df=df.reindex(columns=order_of_columns)
            df.to_csv(output_path+"\\"+layer_results+".csv",index=None)
            print("File writted in "+output_path+"\\"+layer_results+".csv")
            arcpy.management.Delete("TEMP")
          arcpy.env.workspace=path
    else:
      for feature_results in arcpy.ListDatasets():
        if(feature_results.find(originalData)==0):
          originalLayer=path+"\\"+originalData
          arcpy.env.workspace=path+"\\"+feature_results
          print(arcpy.env.workspace)
          for layer_results in arcpy.ListFeatureClasses():
            arcpy.management.Delete("TEMP")
            arcpy.CopyFeatures_management(layer_results,"TEMP")
            arcpy.Near_analysis("TEMP",path+"\RencaRedVial\RedVialComunasSantiago")
        
            df_original=pd.DataFrame(arcpy.da.FeatureClassToNumPyArray(originalLayer,["OBJECTID","NEAR_FID","Hora","Speed"]),columns=["OBJECTID","NEAR_FID","Hora","Speed"])  
            df_results=pd.DataFrame(arcpy.da.FeatureClassToNumPyArray("TEMP",["OBJECTID","FID"]),columns=["OBJECTID","FID"])
            Most_nearest=pd.DataFrame(arcpy.da.FeatureClassToNumPyArray(layer_results,["OBJECTID","FID"]),columns=["OBJECTID","FID"])
            coords=arcpy.da.FeatureClassToNumPyArray(layer_results,["OBJECTID","Shape"])
            Lat=[]
            Lon=[]
            for oi,coord in coords:
              lat,lon=coord
              Lat.append(lat)
              Lon.append(lon)
            df=pd.merge(df_original,df_results,on="OBJECTID",how='inner')
            df["REAL_FID"]=df["NEAR_FID"]
            df["MMA_FID"]=df["FID"]
            df["Latitude"]=Lat
            df["Longitude"]=Lon
            df["MOST_NEAREST"]=Most_nearest["FID"]
            df=df.drop(["NEAR_FID","FID"],axis=1)
            Compare=[]
            MMA_FID=list(df["MMA_FID"])
            REAL_FID=list(df["REAL_FID"])
            for i in range(len(MMA_FID)):#This cicle compare the real FID and the algorith output FID.
              if(MMA_FID[i]==0):
                Compare.append("ZERO")
              elif(MMA_FID[i]==REAL_FID[i]):
                Compare.append("SAME")
              else:
                Compare.append("DIFFERENT")
            df["COMPARE"]=Compare
            order_of_columns=["OBJECTID","Latitude","Longitude","Hora","Speed","MOST_NEAREST","REAL_FID","MMA_FID","COMPARE"]
            df=df.reindex(columns=order_of_columns)
            df.to_csv(output_path+"\\"+layer_results+".csv",index=None)
            print("File writted in "+output_path+"\\"+layer_results+".csv")
            arcpy.management.Delete("TEMP")
          arcpy.env.workspace=path



