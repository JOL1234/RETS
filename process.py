# -*- coding: cp1252 -*-
import arcpy, time

# Local variables:
Lisiting_csv = "......Lisiting.csv"
Lisiting_Layer = 'Lisiting_Layer'
GC_Boundary = r'...GC_Boundary'
RealEstateNew = r'...MLS'
MLS_Real_Estate_Listings = "MLS Real Estate Listings"


arcpy.env.overwriteOutput = True
arcpy.Delete_management(GISweb_SDE_MLS_RealEstateNew)
print("Layer Deleted")
# Process: Make XY Event Layer
arcpy.MakeXYEventLayer_management(Lisiting_csv, "longitude", "latitude", Lisiting_Layer, "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119522E-09;0.001;0.001;IsHighPrecision", "")
print ("Event Layer Created")
# Process: Clip
arcpy.Clip_analysis(Lisiting_Layer, GC_Boundary, RealEstate, "")
print ("Clip complete")

# Process: Changing decoded board values in to their respective numbers.
arcpy.CalculateField_management(RealEstate, "Board", "myCalc(!Board!)", "PYTHON_9.3", "def myCalc(Board):\n  if (Board[:4] == 'Sout'):\n    return '24'\n  elif (Board[:4] == 'REAL'):\n    return '43'\n  else:\n    return 'test'")
# Process: Add Field
arcpy.AddField_management(RealEstate, "srcLink", "TEXT", "", "", "250", "", "NULLABLE", "NON_REQUIRED", "")
print ("Image URL field Add complete")
# Process: Calculate Field for image
arcpy.CalculateField_management(RealEstate, "srcLink", "url( !MLS_Number!, !Board!)", "PYTHON_9.3", "def url(MLS_Number, Board):\n	if MLS_Number[:2]=='GB':\n		 return 'https://cdn.realtor.ca/listing/reb43/highres/'+ MLS_Number[-1:]+'/gb'+MLS_Number[2:]+'_1.jpg'\n	elif MLS_Number[:2]=='SG':\n		return 'https://cdn.realtor.ca/listing/reb24/highres/'+ MLS_Number[-1:]+'/sg'+MLS_Number[2:]+'_1.jpg'\n	elif (MLS_Number[:2]<>'GB'or MLS_Number[:2]<>'GB') and (Board == '43'):\n		return 'https://cdn.realtor.ca/listing/reb43/highres/'+MLS_Number[-1:]+'/'+MLS_Number+'_1.jpg'\n	elif (MLS_Number[:2]<>'GB'or MLS_Number[:2]<>'GB') and (Board == '24'):\n		return 'https://cdn.realtor.ca/listing/reb24/highres/'+ MLS_Number[-1:]+'/'+MLS_Number+'_1.jpg'\n	else:\n		return 'N/A'")
print ("Image URL Calculate complete")

# Process: Add Field
arcpy.AddField_management(RealEstate, "RealtorURL", "TEXT", "", "", "250", "", "NULLABLE", "NON_REQUIRED", "")
print ("RealtorURL field Add complete")
# Process: Calculate Field
arcpy.CalculateField_management(RealEstate, "RealtorURL", "'http://www.realtor.ca/propertydetails.aspx?ref='+ !MLS_Number! +'&boardid='+ !Board!", "PYTHON_9.3", "")
print ("RealtorURL Calculate complete")
		
