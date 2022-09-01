import arcpy
arcpy.env.overwriteOutput = True
arcpy.env.workspace = r"D:\RENCA\Renca\RencaRoads\RencaWaste.gdb"




def delete(layer):
    arcpy.management.Delete(layer)
    print (layer+" sucessfully deleted.")


def purge(layers):

    datos=arcpy.ListFeatureClasses()
    deleted=[]
    if(layers=="*"):
        for i in range(len(datos)):
            arcpy.management.Delete(datos[i])
            print str(datos[i])+" sucessfully deleted."
    else:
        for i in range(len(datos)):
            if(datos[i].startswith(layers)):
                print(datos[i])
                arcpy.management.Delete(datos[i])
                print str(datos[i])+" sucessfully deleted."


def purge_tables(tables):
    datos=arcpy.ListTables()
    deleted=[]
    if(tables=="*"):
        for i in range(len(datos)):
            arcpy.management.Delete(datos[i])
            print str(datos[i])+" sucessfully deleted."
    else:
        for i in range(len(datos)):
            if(datos[i].startswith(tables)):
                print(datos[i])
                arcpy.management.Delete(datos[i])
                print str(datos[i])+" sucessfully deleted."

purge_tables("Final")



