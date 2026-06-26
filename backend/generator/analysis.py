import pandas as pd
from .models import SyntheticDataset



def calculate_quality(original_file,synthetic_file):
    original_df = pd.read_csv(original_file)
    synthetic_df = pd.read_csv(synthetic_file)
    quality_report ={    }
    categorical_report={}
    total_difference =0
    count =0 
    numeric_columns = original_df.select_dtypes(include = ["int64","float64"]).columns
    categorial_columns = original_df.select_dtypes(include=["object","bool"]).columns

    for column in numeric_columns:
        if column == "employee_id":
            continue
        original_mean = original_df[column].mean()
        synthetic_mean = synthetic_df[column].mean()
        if original_mean !=0:
            difference_percent = abs((original_mean - synthetic_mean)/original_mean ) * 100
        else : difference_percent =0
            
        if column != 'employee_id':
            total_difference += difference_percent
            count += 1
        quality_report[column]= {
            "original_mean": round(original_mean,2),
            "synthetic_mean": round(synthetic_mean,2),
            "difference_percentage": round(difference_percent,2),
            "original_Min": original_df[column].min(),
            "synthetic_min": synthetic_df[column].min(),
            "original_max": original_df[column].max(),
            "synthetic_max": synthetic_df[column].max(),
            "original_std": round(original_df[column].std(),2),
            "synthetic_std": round(synthetic_df[column].std(),2)
            }

    for column in categorial_columns:
        if column in ["name","email"]:
           continue
        original_distribution = ( original_df[column].value_counts(normalize=True).mul(100).round(2).to_dict())
        synthetic_distribution = (synthetic_df[column].value_counts(normalize=True).mul(100).round(2).to_dict())
        categorical_report[column]= {
            "original": original_distribution,
            "synthetic": synthetic_distribution
            }
    if count > 0:
        average_difference = total_difference/count
    else: average_difference = 0 
    quality_score =max(0,round(100- average_difference,2))
    if quality_score >= 90:
        quality_rating ="Excellent"
    elif quality_score >= 75:
        quality_rating = "Good"
    elif quality_score >=60:
        quality_rating ="Fair"
    else:
        quality_rating="Poor"

    return{
        "quality_score": quality_score,
        "quality_rating":quality_rating,
        "quality_metrics": quality_report,
        "categorical_metrics": categorical_report,
        "original_rows":len(original_df),
        "synthetic_rows":len(synthetic_df),
        "original_columns":len(original_df.columns),
        "synthetic_columns":len(synthetic_df.columns),
    }

def calculate_privacy(original_file,synthetic_file):
    original_df =pd.read_csv(original_file)
    synthetic_df = pd.read_csv(synthetic_file)
    original_df.columns =(original_df.columns.str.strip().str.lower())

    synthetic_df.columns =(synthetic_df.columns.str.strip().str.lower())

    duplicate_count =0 

    for _,row in synthetic_df.iterrows():
        if original_df.eq(row).all(axis=1).any():
            duplicate_count+=1

    total_rows =len(synthetic_df)

    duplicate_percentage =round((duplicate_count/total_rows)*100,2)

    privacy_score =max(0,round(100 - duplicate_percentage,2))
    
    if privacy_score>=90:
        privacy_rating ='Excellent'
    elif privacy_score>=75:
        privacy_rating= "Good"
    elif privacy_score>= 60:
        privacy_rating ="Fair"
    else: privacy_rating = 'Poor'

    return {
            "total_synthetic_rows": total_rows,
            "duplicate_rows": duplicate_count,
            "duplicate_percentage": duplicate_percentage,

            "privacy_score": privacy_score,
            "privacy_rating": privacy_rating,
            
        }