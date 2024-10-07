import pandas as pd

# Define file paths
input_file = "/home/dibbo-roy/Wild-Fire-Mapping/DataImages/outputFiltered2.xyz"  # Path to your .xyz file
output_file = "/home/dibbo-roy/Wild-Fire-Mapping/DataImages/output.csv"  # Path to save the .csv file

# Read the .xyz file into a DataFrame
# Assuming the file is space-separated or tab-separated and has 3 columns: X, Y, Z
df = pd.read_csv(input_file, sep=' ', header=None)

# Assigning default column names (if not provided in .xyz file)
df.columns = ["Longitude", "Latitude", "Altitude"]

# Save DataFrame to .csv file
df.to_csv(output_file, index=False)