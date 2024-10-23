# Attempting to simplify the code to focus on essential parts and avoid errors.
import pandas as pd
from sklearn.cluster import KMeans
import ace_tools as tools

# Load dataset
file_path = '/mnt/data/synthetic_training_data_with_nama_nim.csv'
data = pd.read_csv(file_path)

# Extract relevant features for clustering (assuming non-feature columns are 'Nama' and 'NIM')
features = data.drop(columns=['Nama', 'NIM'])

# Perform KMeans clustering into 4 clusters
kmeans = KMeans(n_clusters=4, random_state=42)
data['Cluster'] = kmeans.fit_predict(features)

# Display the clustered dataset to the user
tools.display_dataframe_to_user(name="Clustered Dataset", dataframe=data)

# Prepare new data for testing (mock data)
data_new_features = {
    'Feature_1': 5, 'Feature_2': 4, 'Feature_3': 3, 'Feature_4': 2, 'Feature_5': 1,
    'Feature_6': 5, 'Feature_7': 4, 'Feature_8': 3, 'Feature_9': 2, 'Feature_10': 1,
    'Feature_11': 5, 'Feature_12': 4, 'Feature_13': 3, 'Feature_14': 2, 'Feature_15': 1,
    'Feature_16': 5, 'Feature_17': 4, 'Feature_18': 3, 'Feature_19': 2, 'Feature_20': 1,
    'Feature_21': 5, 'Feature_22': 4, 'Feature_23': 3, 'Feature_24': 2, 'Feature_25': 1,
    'Feature_26': 5, 'Feature_27': 4, 'Feature_28': 3, 'Feature_29': 2, 'Feature_30': 1,
    'Feature_31': 5, 'Feature_32': 4, 'Feature_33': 3, 'Feature_34': 2, 'Feature_35': 1,
    'Feature_36': 5, 'Feature_37': 4, 'Feature_38': 3, 'Feature_39': 2, 'Feature_40': 1
}

# Convert new data to DataFrame
data_new_df = pd.DataFrame([data_new_features])

# Predict the cluster for the new data point
new_cluster = kmeans.predict(data_new_df)

# Add predicted cluster to new data
data_new_df['Cluster'] = new_cluster

# Display the result to the user
tools.display_dataframe_to_user(name="New Data Clustering Result", dataframe=data_new_df)



# Save the clustering results to CSV files
clustered_data_file_path = "/mnt/data/clustered_dataset.csv"
new_data_cluster_file_path = "/mnt/data/new_data_clustering_result.csv"

# Save the clustered dataset
data.to_csv(clustered_data_file_path, index=False)

# Save the new data clustering result
data_new_df.to_csv(new_data_cluster_file_path, index=False)

# Provide the file paths to the user
clustered_data_file_path, new_data_cluster_file_path
