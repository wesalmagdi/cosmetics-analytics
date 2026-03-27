import sys
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import subprocess

file_path = sys.argv[1]
df = pd.read_csv(file_path)

df = df[(df['brand'] != 'unknown') & (df['country'] != 'unknown')]
fig, ax = plt.subplots(1, 3, figsize=(18, 5))

top_brands = df['brand'].value_counts().nlargest(5).index
sns.countplot(x='brand', data=df[df['brand'].isin(top_brands)], ax=ax[0],
              order=top_brands)
ax[0].set_title('Top 5 Brands Count')

top_countries = df['country'].value_counts().nlargest(5)
top_countries.plot.pie(ax=ax[1], autopct='%1.1f%%')
ax[1].set_title('Top 5 Countries Proportion')

cross_tab = pd.crosstab(df['brand'], df['country'])
cross_tab = cross_tab.loc[top_brands, top_countries.index]
sns.heatmap(cross_tab, annot=True, ax=ax[2])
ax[2].set_title('Brand vs Country Heatmap')

plt.tight_layout()
plt.savefig("summary_plot.png")
plt.show()

subprocess.run(["python", "cluster.py", file_path])
