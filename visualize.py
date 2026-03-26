import sys
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import subprocess

file_path = sys.argv[1]
df = pd.read_csv(file_path)

fig, ax = plt.subplots(1, 3, figsize=(18, 5))

sns.countplot(x='brand', data=df, ax=ax[0])
ax[0].set_title('Brand Count')

df['country'].value_counts().plot.pie(ax=ax[1])
ax[1].set_title('Country Proportion')

cross_tab = pd.crosstab(df['brand'], df['country'])
sns.heatmap(cross_tab, annot=True, ax=ax[2])
ax[2].set_title('Brand vs Country Heatmap')

plt.tight_layout()
plt.savefig("summary_plot.png")
plt.show()

subprocess.run(["python", "cluster.py", file_path])
