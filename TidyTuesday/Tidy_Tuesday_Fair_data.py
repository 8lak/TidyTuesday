import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv("https://raw.githubusercontent.com/rfordatascience/tidytuesday/refs/heads/main/data/2022/2022-08-09/wheels.csv")

# entries, types and names
#print(data.info())
# first couple entries
#print(data.head())

#numerical summary for each col
#print(data.describe())

# how to count nas via masking with a boolean array
is_zero_mask = data["turns"].notna()
notna_turns = data[is_zero_mask]

# masking but na is true 
is_na_mask = data["turns"].isna()
na_turns = data[is_na_mask]

#print(len(na_turns))
#print(len(notna_turns))

# value_counts returns a series objects of counts for unqiue items. mechanism like a hash map DS
#print(data['turns'].value_counts(dropna=False))

# see types of status
#print(data["status"].value_counts())
# looking at numerical symmary of turns by status grouping
status_turns = data.groupby('status')['turns'].describe()

#print(status_turns)
# check out how many closed entries exist
#print(data['closed'].value_counts())

h_Hc_Cc_subset = data.dropna(subset=['name','height','hourly_capacity','construction_cost']).copy()

# .str  
cost_numbers = h_Hc_Cc_subset['construction_cost'].str.extract(r'([\d\.]+)')[0]
numeric = pd.to_numeric(cost_numbers)

h_Hc_Cc_subset['construction_cost'] = numeric.copy()

#print(h_Hc_Cc_subset[['height','hourly_capacity','construction_cost']].describe())

highest_capacity = h_Hc_Cc_subset.sort_values(["height","hourly_capacity"],ascending=False).iloc[0:2,:]

valuesoi = highest_capacity[["name","country","height","hourly_capacity"]]



print(valuesoi)


# Create a pairplot to visualize the relationships between our key numeric variables.
# Create a scatterplot where the size of the bubbles is mapped to the construction cost.
# We also use 'hue' for cost to create a color gradient, which reinforces the size encoding.
# 'sizes' controls the min and max size of the bubbles to keep the plot readable.
# 'alpha' makes the bubbles slightly transparent to help with overlap.


bubble_plot = sns.scatterplot(
    data=h_Hc_Cc_subset,
    x='height',
    y='hourly_capacity',
    size='construction_cost',
    hue='construction_cost',
    sizes=(10, 300), # Min and max bubble size
    alpha=0.7,
    palette='viridis' # A nice color palette for continuous data
)

# Add informative labels and a clear title
plt.title('FW Height vs. Hourly Capacity (Sized by Construction Cost)', fontsize=12)
plt.xlabel('Height (meters)', fontsize=12)
plt.ylabel('Hourly Passenger Capacity', fontsize=12)

# Improve the legend
bubble_plot.legend(title='Construction Cost (USD)')

# Ensure everything fits nicely
plt.tight_layout()
plt.show()

