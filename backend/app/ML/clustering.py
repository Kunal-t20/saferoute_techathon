import pandas as pd
import joblib

from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

DATA_PATH = r"F:\Projects\techathon\backend\app\Data\AccidentsBig_cleaned.csv"
SAVE_PATH = r"F:\Projects\techathon\backend\app\models\clustered.csv"


def run_clustering():

    df = pd.read_csv(DATA_PATH)

    # ---- ONLY GEO FEATURES ----
    coords = df[['latitude', 'longitude']].dropna()

    scaler = StandardScaler()
    scaled_coords = scaler.fit_transform(coords)

    # ---- DBSCAN ----
    db = DBSCAN(
        eps=0.3,
        min_samples=10
    )

    clusters = db.fit_predict(scaled_coords)

    coords['cluster_id'] = clusters

    # merge back
    df = df.loc[coords.index]
    df['cluster_id'] = clusters

    df.to_csv(SAVE_PATH, index=False)

    print("Clusters created:")
    print(df['cluster_id'].value_counts())


if __name__ == "__main__":
    run_clustering()
