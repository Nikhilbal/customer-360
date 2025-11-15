import pandas as pd
import os
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt

FEATURES_PATH = "data/feature_store/customer360_features.csv"
OUTPUT_PATH = "data/feature_store/customer_segments.csv"

def main():
    print("\n🚀 Starting K-Means Segmentation...")

    # Load engineered features
    print(f"📥 Loading features from {FEATURES_PATH}...")
    df = pd.read_csv(FEATURES_PATH)

    # Only clustering numeric features
    features = df[["Recency", "Frequency", "Monetary", "CLV", "Avg_Order_Value"]]

    print("📊 Scaling features...")
    scaler = StandardScaler()
    scaled = scaler.fit_transform(features)

    # Find best number of clusters using silhouette score
    scores = {}
    print("\n🔍 Finding optimal cluster count...")
    for k in range(2, 10):
        model = KMeans(n_clusters=k, random_state=42)
        model.fit(scaled)
        score = silhouette_score(scaled, model.labels_)
        scores[k] = score
        print(f"➡ k={k} → silhouette score={score:.4f}")

    best_k = max(scores, key=scores.get)
    print(f"\n🏆 Best number of clusters: {best_k}")

    # Train final model
    print("\n🧠 Training final KMeans model...")
    final_model = KMeans(n_clusters=best_k, random_state=42)
    df["Segment"] = final_model.fit_predict(scaled)

    # Label segments based on value tiers
    print("🎯 Assigning human-readable segment names...")
    df["Segment_Label"] = df["Segment"].map({
        0: "Bronze",
        1: "Silver",
        2: "Gold",
        3: "Platinum",
        4: "Diamond"
    }).fillna("Other")

    # Save result
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    print(f"\n✅ Segmentation complete!")
    print(f"📁 Results saved to: {OUTPUT_PATH}")

    # Optional: Visualize clusters
    print("\n📊 Generating visualization...")
    plt.scatter(df["Recency"], df["Monetary"], c=df["Segment"])
    plt.xlabel("Recency")
    plt.ylabel("Monetary Value")
    plt.title("Customer Segments")
    plt.show()


if __name__ == "__main__":
    main()
