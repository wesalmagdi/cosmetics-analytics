import sys
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

file_path = sys.argv[1]
df = pd.read_csv(file_path)

num_cols = df.select_dtypes('number').columns

fig, ax = plt.subplots(1, 3, figsize=(18, 5))

sns.boxplot(y=df[num_cols[0]], ax=ax[0])
ax[0].set_title('Boxplot')

sns.histplot(df[num_cols[0]], bins=20, ax=ax[1])
ax[1].set_title('Histogram')

sns.heatmap(df[num_cols].corr(), annot=True, cmap='coolwarm', ax=ax[2])
ax[2].set_title('Correlation Heatmap')

plt.tight_layout()
plt.savefig("summary_plot.png")
plt.show()
