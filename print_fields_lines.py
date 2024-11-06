import arcpy

# Define the workspace and set it for arcpy
workspace = r"C:\\Users\\bengs\\OneDrive\\Documents\\ArcGIS\\Projects\\Canoeing_the_wilderness\\Canoeing_the_wilderness.gdb"
arcpy.env.workspace = workspace

# List of line feature classes
feature_classes = ["II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]

# Loop through each line feature class
for fc in feature_classes:
    print(f"\nFeature Class: {fc}")
    
    # List and print all field names in the feature class
    fields = arcpy.ListFields(fc)
    field_names = [field.name for field in fields]
    print("Fields:", field_names)
    
    # Access and print each row of data for all fields
    with arcpy.da.SearchCursor(fc, field_names) as cursor:
        for row in cursor:
            print("Row data:", row)
