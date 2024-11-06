import arcpy
import csv

# Define the workspace and CSV path
workspace = r"C:\\Users\\bengs\\OneDrive\\Documents\\ArcGIS\\Projects\\Canoeing_the_wilderness\\Canoeing_the_wilderness.gdb"  
csv_path = r"C:\\Users\\bengs\\ArcPy_Projects\\canoeing_in_the_wilderness\\canoeing_the_river.csv"  

# Set the workspace for arcpy
arcpy.env.workspace = workspace

# List of feature classes to update and corresponding Point_Numbers
feature_classes = {
    "II_Points": "II",
    "III_Points": "III",
    "IV_Points": "IV",
    "V_Points": "V",
    "VI_Points": "VI",
    "VII_Points": "VII",
    "VIII_Points": "VIII",
    "IX_Points": "IX",
    "X_Points": "X"
}

# Read the CSV file and store data in a dictionary by Point_ID, grouped by Point_Number
canoeing_data = {}
with open(csv_path, mode="r", encoding="cp1252") as file:
    reader = csv.DictReader(file)
    for row in reader:
        point_number = row["Point_Number"]
        point_id = int(row["Point_ID"])
        
        # Initialize a dictionary for each Point_Number if not already present
        if point_number not in canoeing_data:
            canoeing_data[point_number] = {}
        
        # Store the row data in the dictionary under the appropriate Point_Number and Point_ID
        canoeing_data[point_number][point_id] = {
            "Date": row["Date"],
            "Day": row["Day"],
            "Time": row["Time"],
            "Event": row["Event"],
            "Campsite": row["Campsite"]
        }

# Loop through each feature class and update fields
for fc, point_number in feature_classes.items():
    print(f"Processing feature class: {fc}")

    # Check if the point_number has data in the dictionary
    if point_number not in canoeing_data:
        print(f"No data found in CSV for feature class {fc}. Skipping.")
        continue

    # Open an update cursor on the feature class, using OBJECTID as the matching field
    with arcpy.da.UpdateCursor(fc, ["OBJECTID", "Date", "Day", "Time", "Event", "Campsite"]) as cursor:
        for row in cursor:
            point_id = row[0]  

            if point_id in canoeing_data[point_number]:
                data = canoeing_data[point_number][point_id]

                # Update the fields from the CSV data
                row[1] = data["Date"]
                row[2] = data["Day"]
                row[3] = data["Time"]
                row[4] = data["Event"]
                row[5] = data["Campsite"]
                
                # Update the row
                cursor.updateRow(row)
                print(f"Updated OBJECTID {point_id} in {fc}")

print("Data population completed for all feature classes.")
