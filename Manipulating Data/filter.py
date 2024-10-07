import pandas as pd

# Define file paths
input_file = "/home/dibbo-roy/Wild-Fire-Mapping/DataImages/output.xyz"
output_file = "/home/dibbo-roy/Wild-Fire-Mapping/DataImages/outputFiltered2.xyz"

# Define chunk size (number of rows to process at a time)
chunk_size = 1000000  # Adjust based on your memory capacity

# Create an empty list to store filtered chunks
filtered_chunks = []

# Read the file in chunks and process each chunk
for chunk in pd.read_csv(input_file, sep=' ', header=None, chunksize=chunk_size):
    # Step 1: Remove points with altitude -32768
    # Assuming the third column (index 2) is the altitude
    filtered_chunk = chunk[chunk[2] != -32768]

    # Append the processed chunk to the list
    filtered_chunks.append(filtered_chunk)

# Concatenate all chunks and save to a new file
filtered_data = pd.concat(filtered_chunks)
filtered_data.to_csv(output_file, sep=' ', index=False, header=False)