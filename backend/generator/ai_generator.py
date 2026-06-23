import pandas as pd 
from sdv.metadata import SingleTableMetadata
from sdv.single_table import CTGANSynthesizer
from faker import Faker
import random 
import numpy as np

fake = Faker()

def generate_synthetic_data(csv_path,fields,rows=100,privacy_level = "medium"):
    print("AI GENERATOR RUNNING")
    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip().str.lower()
    
    


    ctgan_columns=[]
    faker_columns=[]
    for field in fields:
        if field.generation_method =="ctgan":
            ctgan_columns.append(field.field_name.lower())
        elif field.generation_method =="faker":
            faker_columns.append(field)
    
    df_ctgan = df[ctgan_columns]

    numeric_columns = df_ctgan.select_dtypes(include=["int64","float64"]).columns
    if privacy_level == "low":
        scale =50
    elif privacy_level == "medium":
        scale =1000
    else:
        scale=2000

    for column in numeric_columns:
        if column == "salary":
            noise = np.random.laplace(loc=0,scale=scale,size=len(df_ctgan))
            df_ctgan[column]+= noise  
        elif column == "age":
            noise = 2 
            df_ctgan[column]+= noise
        else: 
            noise = 1 
            df_ctgan[column]+= noise



    metadata = SingleTableMetadata()
    metadata.detect_from_dataframe(df_ctgan)

    synthesizer =CTGANSynthesizer(metadata)
    synthesizer.fit(df_ctgan)

    synthetic_df = synthesizer.sample(num_rows = rows)
    print("faker columns")
    for field in faker_columns:
        print(field.field_name, field.field_type)  

    for field in faker_columns:
        if field.field_type == 'email':
            synthetic_df[field.field_name]= [fake.email() 
                                             for _ in range(rows)]
        elif field.field_type == "number":
            synthetic_df[field.field_name]= [random.randint(100000,999999)
                                            for _ in range(rows)]
        elif field.field_type == 'date':
            synthetic_df[field.field_name] = [fake.date()
                                              for _ in range(rows)]
        elif field.field_type == 'string':
            field_name = field.field_name.lower()
            if field_name == "name":
                synthetic_df[field.field_name]=[fake.name()
                                                for _ in range(rows)]
            elif field_name == "department":
                synthetic_df[field.field_name]=[random.choice(["HR","IT","Finance","Marketing","Operations"])
                                                for _ in range(rows)]
            else: 
                synthetic_df[field.field_name] = [fake.word()
                                                  for _ in range(rows)]
        elif field.field_type == 'boolean':
            synthetic_df[field.field_name]= [random.choice([True,False])
                                             for _ in range(rows)]
    
    print("final synthetic columns")
    print(list(synthetic_df.columns))
    print('original columns')
    print(list(df.columns))

    print("faker columns")
    for field in faker_columns:
        print(field.field_name, field.field_type)    

    for col in df.columns:
        if col not in synthetic_df.columns:
            synthetic_df[col]= None        
    synthetic_df = synthetic_df[df.columns]
    return synthetic_df
                    