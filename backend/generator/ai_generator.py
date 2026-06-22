import pandas as pd
from sdv.metadata import SingleTableMetadata
from sdv.single_table import CTGANSynthesizer

def generate_synthetic_data(csv_path, rows=100):
    print("AI GENERATOR RUNNING")
    df = pd.read_csv(csv_path)
    df_for_ctgan = df.drop(columns=["employee_id","name","email"])
    metadata = SingleTableMetadata()
    metadata.detect_from_dataframe(df_for_ctgan)
    synthesizer = CTGANSynthesizer(metadata)
    synthesizer.fit(df_for_ctgan)
    synthetic_df = synthesizer.sample(num_rows=rows)
    return synthetic_df