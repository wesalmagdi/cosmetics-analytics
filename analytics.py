import sys
import pandas as pd
import subprocess

file_path = sys.argv[1]
df = pd.read_csv(file_path)
num_rows = len(df)
num_columns = df.shape[1]


insight1 = f"The preprocessed dataset contains {num_rows} rows and {num_columns} columns."

insight2 = "mean values of features:"
insight2 += df.mean(numeric_only=True).to_string()

insight3 = f"after preprocessing, the dataset contains {num_columns} transformed features"

with open("insight1.txt", "w") as f:
    f.write(insight1)

with open("insight2.txt", "w") as f:
    f.write(insight2)

with open("insight3.txt", "w") as f:
    f.write(insight3)

subprocess.run(["python", "visualize.py", file_path])
