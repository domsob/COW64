import pandas as pd
import numpy as np


# Read the main data
df = pd.read_csv('results/explanations_human_vs_generated.csv')
df = df.fillna(method='ffill')
df['Type'] = df['Type'].replace({'H': 'Human', 'G': 'Generated'})

# Read and merge LOC data
df_loc = pd.read_csv('results/loc_per_patch.csv')
df = pd.merge(df, df_loc, on=['Bug', 'Type'], how='left')

# Read and merge affected lines data
df_affected = pd.read_csv('results/affected_lines_per_patch.csv')
full_df = pd.merge(df, df_affected, on=['Bug', 'Type'], how='left')

# Save full_df to CSV
full_df.to_csv('results/CompleteEval.csv', index=False)
