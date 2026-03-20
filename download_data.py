import pandas as pd
import os

# Create data directory if it doesn't exist
os.makedirs('data', exist_ok=True)

# URL for the dataset
url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"

# Column names for the dataset
column_names = [
    'Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness',
    'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age', 'Outcome'
]

print("📥 Downloading diabetes dataset...")

# Download and save the dataset
df = pd.read_csv(url, names=column_names)
df.to_csv('data/diabetes.csv', index=False)

print(f"✅ Dataset downloaded successfully!")
print(f"   Location: {os.path.abspath('data/diabetes.csv')}")
print(f"   Shape: {df.shape}")
print(f"   Samples: {len(df)}")
print(f"   Features: {len(df.columns)-1}")
print(f"\n📊 First 5 rows:")
print(df.head())

print(f"\n📈 Dataset statistics:")
print(f"   Patients with diabetes: {df['Outcome'].sum()} ({df['Outcome'].mean()*100:.1f}%)")
print(f"   Patients without diabetes: {len(df) - df['Outcome'].sum()} ({(1-df['Outcome'].mean())*100:.1f}%)")