import arcpy
import csv

# Define the workspace and CSV path
workspace = r"C:\\Users\\bengs\\OneDrive\\Documents\\ArcGIS\\Projects\\Canoeing_the_wilderness\\Canoeing_the_wilderness.gdb"
csv_path = r"C:\\Users\\bengs\\ArcPy_Projects\\canoeing_in_the_wilderness\\line_data.csv" 

# Set the workspace for arcpy
arcpy.env.workspace = workspace

# List of feature classes to update
feature_classes = ["II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]

# Read the CSV file and store data in a dictionary by Line_ID
pace_data = {}
with open(csv_path, mode="r", encoding="cp1252") as file:
    reader = csv.DictReader(file)
    for row in reader:

        point_number = row.get("Point_Number")
        line_id = int(row.get("Line_ID"))
        pace_mph = float(row.get("Pace_MPH"))

        if point_number not in pace_data:
            pace_data[point_number] = {}
        pace_data[point_number][line_id] = pace_mph

# Loop through each feature class and update the Pace_MPH field
for fc in feature_classes:
    print(f"Processing feature class: {fc}")
    
    # Check if the feature class name (Point_Number) exists in the data
    if fc in pace_data:

        with arcpy.da.UpdateCursor(fc, ["OBJECTID", "Pace_MPH"]) as cursor:
            for row in cursor:
                line_id = row[0]  

                # Check if the Line_ID exists in the CSV data for this feature class
                if line_id in pace_data[fc]:

                    row[1] = pace_data[fc][line_id]
                    cursor.updateRow(row)
                    print(f"Updated OBJECTID {line_id} in {fc} with Pace_MPH {pace_data[fc][line_id]}")

print("Data population completed for all feature classes.")
