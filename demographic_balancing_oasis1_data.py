#!/usr/bin/env python3
"""Script to create an homogeneous sample for the OASIS dataset.

Labels encoding
"1": "Healthy Controls",
"17": "Alzheimer's Disease",
"""
from pathlib import Path
import math

import pandas as pd
from scipy.stats import chi2_contingency, ttest_ind, f_oneway

from utils import load_dataset

PROJECT_ROOT = Path.cwd()


def main():
    """Verify age and gender balance along the groups from the OASIS dataset."""
    # ----------------------------------------------------------------------------------------
    dataset_name = 'OASIS1'

    participants_path = PROJECT_ROOT / 'data' / dataset_name / 'participants.tsv'
    freesurfer_path = PROJECT_ROOT / 'data' / dataset_name / 'freesurferData.csv'

    outputs_dir = PROJECT_ROOT / 'outputs'
    ids_path = outputs_dir / (dataset_name + '_cleaned_ids.csv')

    dataset_df = load_dataset(participants_path, ids_path, freesurfer_path)
    dataset_df = dataset_df[dataset_df['Diagn'].isin([1, 17])]
    dataset_df = dataset_df.reset_index(drop=True)
    dataset_df = dataset_df.set_index('participant_id')

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
        ad_age = dataset_df[dataset_df['Diagn'] == 17].Age.values

        print('Age per diagnosis')
        print('HC = {:.1f}±{:.1f} [{:d}, {:d}]'.format(hc_age.mean(), hc_age.std(),
                                                       math.ceil(hc_age.min()), math.ceil(hc_age.max())))
        print('AD = {:.1f}±{:.1f} [{:d}, {:d}]'.format(ad_age.mean(), ad_age.std(),
                                                       math.ceil(ad_age.min()), math.ceil(ad_age.max())))
        print('')

    print_age_stats(dataset_df)

    # ----------------------------------------------------------------------------------------
    # Gender analysis
    print('------------- GENDER ANALYSIS ----------------')

    def print_gender_analysis(contingency_table):
        _, p_value, _, _ = chi2_contingency(contingency_table[[1, 17]], correction=False)
        print('Gender - HC vs AD p value {:.4f}'.format(p_value))
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
        ad_age = dataset_df[dataset_df['Diagn'] == 17].Age.values

        _, p_value = ttest_ind(hc_age, ad_age)
        print('Age - HC vs AD p value {:.4f}'.format(p_value))
        print('Age - TOTAL p value {:.4f}'.format(f_oneway(hc_age, ad_age).pvalue))
        print()
        print('')

    print_age_analysis(dataset_df)

    # HC is too young, dropping some of the youngest
    dataset_corrected_df = dataset_df

    for _ in range(49):
        conditional_mask = dataset_corrected_df['Diagn'] == 1

        hc_age = dataset_corrected_df[conditional_mask].Age

        dataset_corrected_df = dataset_corrected_df.drop(hc_age.argmin(), axis=0)
        dataset_corrected_df = dataset_corrected_df.reset_index(drop=True)

        print_age_stats(dataset_corrected_df)
        print_age_analysis(dataset_corrected_df)

    # ----------------------------------------------------------------------------------------
    # Final dataset
    print('------------- FINAL DATASET ----------------')
    print('Total of participants = {:}'.format(len(dataset_corrected_df)))
    print('')
    print('Number of participants per diagnosis')
    print(dataset_corrected_df.groupby('Diagn')['Image_ID'].count())
    print('')

    contingency_table = pd.crosstab(dataset_corrected_df.Gender, dataset_corrected_df.Diagn)
    print('Contigency table of gender x diagnosis')
    print(contingency_table)
    print('')

    print_gender_analysis(contingency_table)
    print_age_stats(dataset_corrected_df)
    print_age_analysis(dataset_corrected_df)

    dataset_corrected_df[['Image_ID']].to_csv(outputs_dir / (dataset_name + '_homogeneous_ids.csv'), index=False)


if __name__ == "__main__":
    main()
