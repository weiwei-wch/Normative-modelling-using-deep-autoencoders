"""Script to combine the data from different sites from the same dataset."""
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path.cwd()


def merge_sites_data(paths, sep=','):
    """Read csv files and merge them into a single dataframe."""
    dataframe = pd.DataFrame()
    for file_path in paths:
        dataframe = dataframe.append(pd.read_csv(file_path, sep=sep))

    return dataframe


def main():
    """Combine the neuroimaging data and demographic data from different sites.

    Script will search for all neuroimaging files (i.e. freesurferData.csv) and demographic
    data (i.e. participants.tsv) inside the specified data_dir (e.g. PROJECT_ROOT / 'data' /
    'ADNI')
    """
    # ----------------------------------------------------------------------------------------
    data_dir = PROJECT_ROOT / 'data' / 'ADNI'
    output_dir = data_dir

    # ----------------------------------------------------------------------------------------
    freesurfer_paths = sorted(data_dir.glob('*/freesurferData.csv'))
    freesurfer_df = merge_sites_data(freesurfer_paths, sep=',')
    freesurfer_df.to_csv(output_dir / 'freesurferData.csv', index=False)

    # ----------------------------------------------------------------------------------------
    participants_paths = sorted(data_dir.glob('*/participants.tsv'))
    participant_df = merge_sites_data(participants_paths, sep='\t')
    participant_df.to_csv(output_dir / 'participants.tsv', sep='\t', index=False)


if __name__ == "__main__":
    main()
