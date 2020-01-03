#!/usr/bin/env python3
"""Script to create homogeneous samples for the TOMC dataset (a.k.a FBF_Brescia dataset).

Labels encoding
"1": "Healthy Controls",
"17": "Alzheimer's Disease",
"18": "Mild Cognitive Impairment",
"""
from pathlib import Path
import math

import pandas as pd
from scipy.stats import chi2_contingency, ttest_ind, f_oneway

from utils import load_dataset

PROJECT_ROOT = Path.cwd()


def main():
    """Verify age and gender balance along the groups from the TOMC dataset."""
    # ----------------------------------------------------------------------------------------
    dataset_name = 'TOMC'

    participants_path = PROJECT_ROOT / 'data' / dataset_name / 'participants.tsv'
    freesurfer_path = PROJECT_ROOT / 'data' / dataset_name / 'freesurferData.csv'

    outputs_dir = PROJECT_ROOT / 'outputs'
    ids_path = outputs_dir / (dataset_name + '_cleaned_ids.csv')

    dataset_df = load_dataset(participants_path, ids_path, freesurfer_path)
    dataset_df = dataset_df[dataset_df['Diagn'].isin([1, 17, 18])]

    # ----------------------------------------------------------------------------------------
    print('Analysing {:}'.format(dataset_name))
    print('Total of participants = {:}'.format(len(dataset_df)))
    print('')
    print('Number of participants per diagnosis')
    print(dataset_df.groupby('Diagn')['Image_ID'].count())
    print('')

    contingency_table = pd.crosstab(dataset_df.Gender, dataset_df.Diagn)
    print('Contigency table of gender x diagnosis')
    print(contingency_table)
    print('')

    def print_age_stats(dataset_df):
        hc_age = dataset_df[dataset_df['Diagn'] == 1].Age.values
        mci_age = dataset_df[dataset_df['Diagn'] == 18].Age.values
        ad_age = dataset_df[dataset_df['Diagn'] == 17].Age.values

        print('Age per diagnosis')
        print('HC = {:.1f}±{:.1f} [{:d}, {:d}]'.format(hc_age.mean(), hc_age.std(),
                                                       math.ceil(hc_age.min()), math.ceil(hc_age.max())))
        print('MCI = {:.1f}±{:.1f} [{:d}, {:d}]'.format(mci_age.mean(), mci_age.std(),
                                                        math.ceil(mci_age.min()), math.ceil(mci_age.max())))
        print('AD = {:.1f}±{:.1f} [{:d}, {:d}]'.format(ad_age.mean(), ad_age.std(),
                                                       math.ceil(ad_age.min()), math.ceil(ad_age.max())))
        print('')

    print_age_stats(dataset_df)

    # ----------------------------------------------------------------------------------------
    # Gender analysis
    print('------------- GENDER ANALYSIS ----------------')

    def print_gender_analysis(contingency_table):
        _, p_value, _, _ = chi2_contingency(contingency_table[[1, 18]], correction=False)
        print('Gender - HC vs MCI p value {:.4f}'.format(p_value))
        _, p_value, _, _ = chi2_contingency(contingency_table[[1, 17]], correction=False)
        print('Gender - HC vs AD p value {:.4f}'.format(p_value))
        _, p_value, _, _ = chi2_contingency(contingency_table[[18, 17]], correction=False)
        print('Gender - MCI vs AD p value {:.4f}'.format(p_value))
        _, p_value, _, _ = chi2_contingency(contingency_table, correction=False)
        print('Gender - TOTAL p value {:.4f}'.format(p_value))
        print('')

    print_gender_analysis(contingency_table)

    # ----------------------------------------------------------------------------------------
    # Age analysis
    print('------------- AGE ANALYSIS ----------------')
    print_age_stats(dataset_df)

    def print_age_analysis(dataset_df):
        hc_age = dataset_df[dataset_df['Diagn'] == 1].Age.values
        mci_age = dataset_df[dataset_df['Diagn'] == 18].Age.values
        ad_age = dataset_df[dataset_df['Diagn'] == 17].Age.values

        _, p_value = ttest_ind(hc_age, mci_age)
        print('Age - HC vs MCI p value {:.4f}'.format(p_value))
        _, p_value = ttest_ind(hc_age, ad_age)
        print('Age - HC vs AD p value {:.4f}'.format(p_value))
        _, p_value = ttest_ind(ad_age, mci_age)
        print('Age - AD vs LMCI p value {:.4f}'.format(p_value))
        print('Age - TOTAL p value {:.4f}'.format(f_oneway(hc_age, mci_age, ad_age).pvalue))
        print()
        print('')

    print_age_analysis(dataset_df)

    # hc is too young, droping some of the youngest
    dataset_corrected_df = dataset_df

    for _ in range(139):
        conditional_mask = dataset_corrected_df['Diagn'] == 1

        hc_age = dataset_corrected_df[conditional_mask].Age.values
        index_to_remove = dataset_corrected_df[conditional_mask].iloc[hc_age.argmin()].name

        dataset_corrected_df = dataset_corrected_df.drop(index_to_remove, axis=0)
        dataset_corrected_df = dataset_corrected_df.reset_index(drop=True)

        print_age_stats(dataset_corrected_df)
        print_age_analysis(dataset_corrected_df)

    # ----------------------------------------------------------------------------------------
    # Final dataset
    print('------------- FINAL DATASET ----------------')
    print_gender_analysis(contingency_table)
    print_age_stats(dataset_corrected_df)
    print_age_analysis(dataset_corrected_df)

    dataset_corrected_df[['Image_ID']].to_csv(outputs_dir / (dataset_name + '_homogeneous_ids.csv'), index=False)


if __name__ == "__main__":
    main()
