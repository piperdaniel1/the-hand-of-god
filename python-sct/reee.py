lines = []
with open ("reee.txt", "r") as f:
    lines = f.readlines()
    lines = [x.strip() for x in lines]

left_col = []
right_col = []

for line in lines:
    split = line.split(" ")
    split = [x for x in split if x != ""]

    try:
        left_col.append((split[0], split[1], split[2]))
        right_col.append((split[3], split[4], split[5]))
    except IndexError:
        pass

merged_cols = []

for elem in left_col:
    merged_cols.append(float(elem[2].strip('%')))

for elem in right_col:
    merged_cols.append(float(elem[2].strip('%')))

merged_cols.append(0.01)

class Rank:
    def __init__(self, name, rank, percent):
        self.name = name
        self.rank = rank
        self.percent = percent
    
    def __str__(self):
        return f"{self.name} {self.rank}: {self.percent}"
    
    def __repr__(self):
        return f"{self.name} {self.rank}: {self.percent}"

ranks = []
names = ["Iron", "Bronze", "Silver", "Gold", "Platinum", "Diamond", "Ascendant", "Immortal", "Radiant"]
name_ind = 0
num = 1

for i in merged_cols[:-1]:
    ranks.append(Rank(names[name_ind], num, i))

    num += 1
    if num == 4:
        num = 1
        name_ind += 1

ranks.append(Rank("Radiant", 1, merged_cols[-1]))

for rank in ranks:
    print(rank)

import matplotlib.pyplot as plt


# 2x2 grid
import numpy as np

# Calculate PDF and CDF
pdf_values = np.array([rank.percent for rank in ranks])
cdf_values = np.cumsum(pdf_values)

x_labels = [f"{rank.name} {rank.rank}" for rank in ranks]

# Plot PDF (top left)
plt.subplot(2, 2, 1)
plt.plot(x_labels, pdf_values, marker='o', linestyle='-')
plt.xticks(rotation=45)
plt.title('PDF: Rank Percentages')
plt.ylabel('Percentage')
plt.grid(True)

# Plot CDF (top right)
plt.subplot(2, 2, 2)
plt.plot(x_labels, cdf_values, marker='o', linestyle='-')
plt.xticks(rotation=45)
plt.title('CDF: Cumulative Rank Percentages')
plt.ylabel('Percentage')
plt.grid(True)

# Plot horizontal bar chart for rank distribution (bottom left)
plt.subplot(2, 2, 3)
plt.barh(x_labels, pdf_values)
plt.title('Rank Distribution')
plt.xlabel('Percentage')

# Plot pie chart for top 3 rank percentages (bottom right)
plt.subplot(2, 2, 4)
top_3_ranks = sorted(ranks, key=lambda x: x.percent, reverse=True)[:3]
plt.pie([rank.percent for rank in top_3_ranks], labels=[f"{rank.name} {rank.rank}" for rank in top_3_ranks], autopct='%1.1f%%')
plt.title('Top 3 Rank Percentages')


# Adjust layout to prevent overlapping
plt.tight_layout()

# Display plots
plt.show()

# Create a table for CDF values
cdf_values = np.round(cdf_values, 2)

table_data = np.column_stack((x_labels, cdf_values))
table = plt.table(cellText=table_data, colLabels=['Rank', 'CDF Value'], loc='center')
table.auto_set_font_size(False)
table.set_fontsize(8)
table.scale(1, 1.5)
plt.axis('off')

# Adjust layout to prevent overlapping
plt.tight_layout()

# Display table in the new window
plt.show()
