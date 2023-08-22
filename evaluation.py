import pandas as pd
import numpy as np


# Read data 
df = pd.read_csv('results/CompleteEval.csv')
df = df.replace({'Yes': 1, 'No': 0})

# Get statistics about human and generated affected lines
# -------------------------------------------------------

affected_lines_human = df[df['Type'] == 'Human']['Affected_lines'].tolist()
affected_lines_generated = df[df['Type'] == 'Generated']['Affected_lines'].tolist()

print("Affected lines human (mean): ", np.mean(affected_lines_human))
print("Affected lines generated (mean): ", np.mean(affected_lines_generated))
print("Affected lines human (std): ", np.std(affected_lines_human))
print("Affected lines generated (std): ", np.std(affected_lines_generated))

# -------------------------------------------------------


# Say yes (1) if all three runs say yes, otherwise no (0)
# -------------------------------------------------------
grouped = df.groupby(["Bug", "Type"]).sum().reset_index()
for col in df.loc[:, 'Correctness Condition':'Consistency Change']:
    grouped[col] = grouped[col].apply(lambda x: 1 if x == 3 else 0)

grouped = grouped.groupby(["Type"]).sum().reset_index()
grouped.insert(0, 'EvalType', 'Three of three')

three_of_three = grouped

# -------------------------------------------------------


# Say yes (1) if at least one out of three runs say yes, otherwise no (0)
# -------------------------------------------------------
grouped = df.groupby(["Bug", "Type"]).max().reset_index()
for col in df.loc[:, 'Correctness Condition':'Consistency Change']:
    grouped[col] = grouped[col].apply(lambda x: 1 if x == 1 else 0)

grouped = grouped.groupby(["Type"]).sum().reset_index()
grouped.insert(0, 'EvalType', 'One of three')

one_of_three = grouped

# -------------------------------------------------------

columns_list = ['Run', 'LOC', 'Consistency Condition', 'Consistency Consequence', 'Consistency Position', 'Consistency Cause', 'Consistency Change', 'Affected_lines']

three_of_three = three_of_three.drop(columns=columns_list)
one_of_three = one_of_three.drop(columns=columns_list)
three_of_three = three_of_three.transpose()
one_of_three = one_of_three.transpose()

merged_df = pd.concat([one_of_three, three_of_three], axis=1)


print(merged_df.to_latex(index=True)) 