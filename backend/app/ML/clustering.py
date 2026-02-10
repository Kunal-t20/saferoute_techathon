import pandas as pd
from sklearn.cluster import DBSCAN   # DBSCAN = Density Based Spatial Clustering
from ML.preprocessing import preprocess
from sklearn.preprocessing import StandardScaler
import pickle

# 1. Load and preprocess dataset
file_path = r"F:\Projects\techathon\backend\app\Data\india_metro_accidents_2000.csv"
df = preprocess(file_path)

# 2. Select geographic coordinates
coordinates = df[['Latitude', 'Longitude']]

# 3. Scale coordinates (important for distance-based algorithms)
scaler = StandardScaler()
scaled_coordinates = scaler.fit_transform(coordinates)

# 4. Apply DBSCAN clustering
# eps = radius distance
# min_samples = minimum points to form a cluster
density_cluster_model = DBSCAN(eps=0.3, min_samples=10)
cluster_labels = density_cluster_model.fit_predict(scaled_coordinates)

# 5. Assign cluster labels to dataframe
df['cluster_id'] = cluster_labels

# 6. Check cluster distribution
print(df['cluster_id'].value_counts())

cluster_model=r"F:\Projects\techathon\backend\app\models\cluster_model.pkl"
# 7. Save clustering model (Density-Based model, NOT Database)
with open(cluster_model, 'wb') as f:
    pickle.dump(density_cluster_model, f)

scaler_path=r"F:\Projects\techathon\backend\app\models\scaler.pkl"
# 8. Save scaler for future coordinate transforms
with open(scaler_path, 'wb') as f:
    pickle.dump(scaler, f)

clutered_csv_path=r"F:\Projects\techathon\backend\app\models\clustered.csv"
# 9. Save clustered dataset for heatmap usage
df.to_csv(clutered_csv_path, index=False)
