
import pandas as pd

print("Loading SMS dataset...")

df = pd.read_csv(
    "SMSSpamCollection",
    sep="\t",
    header=None,
    names=["label", "text"]
)

df["label"] = df["label"].map({
    "ham": "legitimate",
    "spam": "fraud"
})

df = df.dropna()

df.to_csv(
    "data/messages.csv",
    index=False
)

print("\nDataset prepared successfully!")

print("\nDataset distribution:")
print(df["label"].value_counts())

print("\nTotal messages:", len(df))
