from ai_generator import generate_synthetic_data

syntethic_df = generate_synthetic_data("employee_training.csv",rows=20)
print(syntethic_df.head())