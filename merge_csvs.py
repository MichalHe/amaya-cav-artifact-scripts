import argparse
import pprint
import os

import tabulate
import pandas as pd
import numpy as np

TIMEOUT = 60

def make_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('smtlib_tools_csv', help='CSV with results of SMT tools')
    parser.add_argument('lash_csv', help='CSV with results of the LASH tool')
    return parser


def strip_lash_formula(formula_name):
    if formula_name.endswith('.lash'):
        formula_name = formula_name[:-len('.lash')]
    return strip_smt2_formula(formula_name)


def strip_smt2_formula(formula_name):
    if formula_name.endswith('.smt2'):
        formula_name = formula_name[:-len('.smt2')]
    return os.path.basename(formula_name)


def compute_table_values(src_df, reference_tool, reference_series):
    target_dict = {}
    for col in src_df.columns:
        if not col.endswith('-runtime'):
            continue
        tool = col[:-len('-runtime')]
        
        tool_values = {
            'timeouts': src_df[col].isna().sum(),
            'mean': src_df[col].mean(),
            'median': src_df[col].median(),
            'std': src_df[col].std(),
            'wins': 0,
            'wins (timeouts)': 0,
            'losses': 0,
            'losses (timeouts)': 0,
        }
        
        src_df_with_no_nan = src_df.fillna(TIMEOUT) 
        if reference_tool != tool: 
            ref_col = f'{reference_tool}-runtime' 

            ref_better = src_df_with_no_nan[src_df_with_no_nan[ref_col] < src_df_with_no_nan[col]]
            ref_better_other_timeouts = ref_better[ref_better[col] == TIMEOUT]

            other_better = src_df_with_no_nan[src_df_with_no_nan[ref_col] > src_df_with_no_nan[col]]
            other_better_ref_timeouts = other_better[other_better[ref_col] == TIMEOUT]
            tool_values.update({
                'wins': len(ref_better),
                'wins (timeouts)': len(ref_better_other_timeouts),
                'losses': len(other_better),
                'losses (timeouts)': len(other_better_ref_timeouts),
            })

        target_dict[tool] = tool_values
    return target_dict

parser = make_parser()
args = parser.parse_args()

smt_df = pd.read_csv(args.smtlib_tools_csv, sep=';', na_values=['TO'])
smt_df['name'] = smt_df['name'].apply(strip_smt2_formula)
smt_df = smt_df.sort_values(by=['name'])

lash_df_raw = pd.read_csv(args.lash_csv, sep=';')
lash_df = pd.read_csv(args.lash_csv, sep=';', na_values=['TO', 'ERR'])
lash_df['name'] = lash_df['name'].apply(strip_lash_formula)
lash_df = lash_df.sort_values(by=['name'])

# Set all runtimes to timeout where lash returned error on numerical constant too large
lash_df[lash_df['lash-result'] == 'unknown']['lash-runtime'] = TIMEOUT

# Set all LASH errors to timeouts - the errors either because the solver has been killed by OOM killer
# or because LASH crashed with segmentation fault, likeyly due to some internal overflow. There is
# nothing we can done about the segfaults.
lash_df.loc[lash_df_raw['lash-result'] == 'ERR', ['lash-runtime']] = np.nan

merged_df = pd.merge(smt_df, lash_df, on='name', how='inner')

results = compute_table_values(merged_df, 'amaya', smt_df['amaya-runtime'])
some_tool = next(iter(results))
headers = list(results[some_tool].keys())
rows = []

for tool in results:
    row = [tool]
    for field in headers:
        row.append(results[tool][field])
    rows.append(row)

print(tabulate.tabulate(rows, headers=['tool']+headers))

