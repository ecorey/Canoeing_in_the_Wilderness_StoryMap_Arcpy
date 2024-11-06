import arcpy

# Define the workspace and set it for arcpy
workspace = r"C:\\Users\\bengs\\OneDrive\\Documents\\ArcGIS\\Projects\\Canoeing_the_wilderness\\Canoeing_the_wilderness.gdb"
arcpy.env.workspace = workspace

# List of feature classes or layers in the map
feature_classes = ["II_Points", "III_Points", "IV_Points", "V_Points", "VI_Points", "VII_Points", "VIII_Points", "IX_Points", "X_Points"]

# Loop through each feature class
for fc in feature_classes:
    print(f"\nProcessing feature class: {fc}")

    # Check if the layer already exists in the map; if so, proceed with selection
    if arcpy.Exists(fc):
        # Apply selection where Campsite = 'Y'
        arcpy.SelectLayerByAttribute_management(fc, "NEW_SELECTION", "Campsite = 'Y'")
        
        # Check if any features were selected
        selected_count = int(arcpy.GetCount_management(fc).getOutput(0))
        if selected_count > 0:
            print(f"{selected_count} features selected in {fc} with Campsite = 'Y'")
            # Print selected features
            with arcpy.da.SearchCursor(fc, ["OBJECTID", "Campsite"]) as cursor:
                for row in cursor:
                    print(f"Feature in {fc} - OBJECTID: {row[0]}, Campsite: {row[1]}")
        else:
            print(f"No features with Campsite = 'Y' in {fc}")
    else:
        print(f"Feature class {fc} does not exist or is not in the map.")



print("Selection process completed.")
