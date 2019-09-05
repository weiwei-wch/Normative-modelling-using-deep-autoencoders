"""Script to create datasets harmonized."""
from pathlib import Path

import pandas as pd
import neuroCombat

from utils import load_dataset, COLUMNS_NAME

PROJECT_ROOT = Path.cwd()


def main():
    """"""
    # ----------------------------------------------------------------------------
    experiment_name = 'biobank_scanner1'
    model_name = 'supervised_aae_deterministic_freesurfer'

    biobank_participants_path = PROJECT_ROOT / 'data' / 'datasets' / 'BIOBANK' / 'participants.tsv'
    biobank_freesurfer_path = PROJECT_ROOT / 'data' / 'datasets' / 'BIOBANK' / 'freesurferData.csv'
    biobank_ids_path = PROJECT_ROOT / 'outputs' / experiment_name / 'cleaned_ids.csv'

    adni_participants_path = PROJECT_ROOT / 'data' / 'datasets' / 'ADNI' / 'participants.tsv'
    adni_freesurfer_path = PROJECT_ROOT / 'data' / 'datasets' / 'ADNI' / 'freesurferData.csv'

    brescia_participants_path = PROJECT_ROOT / 'data' / 'datasets' / 'FBF_Brescia' / 'participants.tsv'
    brescia_freesurfer_path = PROJECT_ROOT / 'data' / 'datasets' / 'FBF_Brescia' / 'freesurferData.csv'

    hc_label = 1
    disease_label = 17
    # ----------------------------------------------------------------------------
    # Create directories structure
    experiment_dir = PROJECT_ROOT / 'outputs' / experiment_name
    model_dir = experiment_dir / model_name
    model_dir.mkdir(exist_ok=True)

    adni_ids_path = experiment_dir / 'ADNI_homogeneous_ids.csv'
    brescia_ids_path = experiment_dir / 'FBF_Brescia_homogeneous_ids.csv'

    # ----------------------------------------------------------------------------
    # Loading data
    biobank_dataset_df = load_dataset(biobank_participants_path, biobank_ids_path, biobank_freesurfer_path)

    adni_dataset_df = load_dataset(adni_participants_path, adni_ids_path, adni_freesurfer_path)
    brescia_dataset_df = load_dataset(brescia_participants_path, brescia_ids_path, brescia_freesurfer_path)

    adni_dataset_df = adni_dataset_df.loc[(adni_dataset_df['Diagn'] == hc_label) |
                                          (adni_dataset_df['Diagn'] == disease_label)]

    brescia_dataset_df = brescia_dataset_df.loc[(brescia_dataset_df['Diagn'] == hc_label) |
                                                (brescia_dataset_df['Diagn'] == disease_label)]

    # datasets_replace_dict = {
    #     'BIOBANK-SCANNER01': 0,
    #     'SCANNER002': 1,
    #     'SCANNER003': 2,
    #     'SCANNER006': 3,
    #     'SCANNER009': 4,
    #     'SCANNER011': 5,
    #     'SCANNER012': 6,
    #     'SCANNER013': 7,
    #     'SCANNER014': 8,
    #     'SCANNER018': 9,
    #     'SCANNER019': 10,
    #     'SCANNER020': 11,
    #     'SCANNER022': 12,
    #     'SCANNER023': 13,
    #     'SCANNER024': 14,
    #     'SCANNER031': 15,
    #     'SCANNER032': 16,
    #     'SCANNER033': 17,
    #     'SCANNER035': 18,
    #     'SCANNER036': 19,
    #     'SCANNER037': 20,
    #     'SCANNER041': 21,
    #     'SCANNER053': 22,
    #     'SCANNER067': 23,
    #     'SCANNER068': 24,
    #     'SCANNER070': 25,
    #     'SCANNER072': 26,
    #     'SCANNER073': 27,
    #     'SCANNER082': 28,
    #     'SCANNER094': 29,
    #     'SCANNER099': 30,
    #     'SCANNER100': 31,
    #     'SCANNER116': 32,
    #     'SCANNER123': 33,
    #     'SCANNER128': 34,
    #     'SCANNER130': 35,
    #     'SCANNER131': 36,
    #     'SCANNER135': 37,
    #     'SCANNER136': 38,
    #     'SCANNER137': 39,
    #     'SCANNER153': 40,
    #     'SCANNER941': 41,
    #     'FBF_Brescia-SCANNER01': 42,
    #     'FBF_Brescia-SCANNER02': 43,
    #     'FBF_Brescia-SCANNER03': 44}

    datasets_replace_dict = {
        'BIOBANK-SCANNER01': 0,
        'SCANNER002': 1,
        'SCANNER003': 1,
        'SCANNER006': 1,
        'SCANNER009': 1,
        'SCANNER011': 1,
        'SCANNER012': 1,
        'SCANNER013': 1,
        'SCANNER014': 1,
        'SCANNER018': 1,
        'SCANNER019': 1,
        'SCANNER020': 1,
        'SCANNER022': 1,
        'SCANNER023': 1,
        'SCANNER024': 1,
        'SCANNER031': 1,
        'SCANNER032': 1,
        'SCANNER033': 1,
        'SCANNER035': 1,
        'SCANNER036': 1,
        'SCANNER037': 1,
        'SCANNER041': 1,
        'SCANNER053': 1,
        'SCANNER067': 1,
        'SCANNER068': 1,
        'SCANNER070': 1,
        'SCANNER072': 1,
        'SCANNER073': 1,
        'SCANNER082': 1,
        'SCANNER094': 1,
        'SCANNER099': 1,
        'SCANNER100': 1,
        'SCANNER116': 1,
        'SCANNER123': 1,
        'SCANNER128': 1,
        'SCANNER130': 1,
        'SCANNER131': 1,
        'SCANNER135': 1,
        'SCANNER136': 1,
        'SCANNER137': 1,
        'SCANNER153': 1,
        'SCANNER941': 1,
        'FBF_Brescia-SCANNER01': 2,
        'FBF_Brescia-SCANNER02': 2,
        'FBF_Brescia-SCANNER03': 2}

    biobank_dataset_df = biobank_dataset_df.replace({'Dataset': datasets_replace_dict})
    adni_dataset_df = adni_dataset_df.replace({'Dataset': datasets_replace_dict})
    brescia_dataset_df = brescia_dataset_df.replace({'Dataset': datasets_replace_dict})

    brescia_dataset_df = brescia_dataset_df.drop(['Image_ID_y'], axis=1)
    adni_dataset_df = adni_dataset_df.drop(['Image_ID_y'], axis=1)

    brescia_dataset_df = brescia_dataset_df.rename(columns={"Image_ID_x": "Image_ID"})
    adni_dataset_df = adni_dataset_df.rename(columns={"Image_ID_x": "Image_ID"})

    # discrete_cols = ['Gender']
    # continuous_cols = ['Age']
    batch_col = 'Dataset'

    result = pd.concat([biobank_dataset_df, adni_dataset_df, brescia_dataset_df])
    # result = result.loc[(result['Dataset']==0) |(result['Dataset']==3)|(result['Dataset']==4) ]
    # result = brescia_dataset_df
    dataset = result[COLUMNS_NAME]
    covars = result[['Dataset']]
    # covars = result[['Dataset', 'Age', 'Gender']]
    covars['Dataset'] = covars['Dataset'].astype(float)
    # data = dataset.values[:, :2]
    data = dataset.values

    combat_data, s_data, design, gamma_star, delta_star, s_mean, v_pool, info_dict = neuroCombat.neuroCombat(data=data,
                                                                                                             covars=covars,
                                                                                                             batch_col=batch_col)