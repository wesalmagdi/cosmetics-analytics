
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.decomposition import PCA
from sklearn.feature_selection import VarianceThreshold
import sys
import subprocess



def data_cleaning(df):

    original_shape = df.shape
    print("Original data shape:", original_shape)
    
    missing_before = df.isnull().sum().sum()
    print("Total missing values before cleaning:", missing_before)

    df['code'] = pd.to_numeric(df['code'], errors='coerce').fillna(0).astype('int64')

    if 'quantity' in df.columns:
        split_data = df['quantity'].astype(str).str.extract(r'(\d+\.?\d*)\s*(.*)')
        df['quantity_value'] = pd.to_numeric(split_data[0], errors='coerce')
        df['quantity_unit'] = split_data[1].str.strip()
        df = df.drop(columns=['quantity'])

    df= df.drop(columns=['countries','countries_tags','last_image_t','last_image_datetime','last_modified_datetime','last_updated_datetime'])
    df = df.rename(columns={'countries_en': 'country'})

    df=df.drop(columns=['brands_tags','brands'])
    df= df.rename(columns={'brands_en': 'brand'})

    datetime_cols = [col for col in df.columns if 'datetime' in col.lower()]
    for col in datetime_cols:
        df[col] = pd.to_datetime(df[col], errors='coerce')

    unix_time_cols = [col for col in df.columns if col.endswith('_t')]
    for col in unix_time_cols:
        df[col] = pd.to_datetime(df[col], unit='s', errors='coerce')


    url_cols = [col for col in df.columns if 'url' in col.lower()]
    if url_cols:
        df = df.drop(columns=url_cols)
        print(f"Dropped URL columns: {url_cols}")

    state_cols = [col for col in df.columns if 'states' in col.lower()]
    if state_cols:
        df = df.drop(columns=state_cols)
        print(f"Dropped states columns: {state_cols}")
    
    missing_pct = (df.isnull().sum() / len(df)) * 100
    high_missing_cols = missing_pct[missing_pct > 50].index.tolist()

    if high_missing_cols:
        print(f"Dropping columns with >50% missing values: {high_missing_cols}")
        df = df.drop(columns=high_missing_cols)
        print(f"Data shape after dropping high-missing columns: {df.shape}")
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if df[col].isnull().sum() > 0:
            median_val = df[col].median()
            df[col] = df[col].fillna(median_val)
            print(f"Filled missing in '{col}' with median: {median_val:.2f}")
    
    categorical_cols = df.select_dtypes(include=['object','string']).columns
    for col in categorical_cols:
        if df[col].isnull().sum() > 0:
            df[col] = df[col].fillna('Unknown')
            print(f"Filled missing in '{col}' with 'Unknown'")
    
    missing_after = df.isnull().sum().sum()
    
    duplicates_before = df.duplicated().sum()
    if duplicates_before > 0:
        df = df.drop_duplicates()
        print(f"Removed {duplicates_before} duplicate rows")
    else:
        print(f"No duplicate rows found")
    
    text_cols = df.select_dtypes(include=['object','string']).columns
    for col in text_cols[:]: 
        before_unique = df[col].nunique()
        df[col] = df[col].astype(str).str.strip().str.lower()
        after_unique = df[col].nunique()
        if before_unique != after_unique:
            print(f"Cleaned '{col}': {before_unique} → {after_unique} unique values")

    print(f"Data Cleaning Complete: {original_shape} → {df.shape}")
    print(f"Missing values reduced from {missing_before} to {missing_after}")

    return df


def feature_transformation(df):

    categorical_cols = df.select_dtypes(include=['object','string']).columns
    
    encoded_cols = []
    
    for col in categorical_cols:
        n_unique = df[col].nunique()
        if 2 <= n_unique <= 15:
            dummies = pd.get_dummies(df[col], prefix=col, drop_first=True)
            df = pd.concat([df, dummies], axis=1)
            encoded_cols.append(col)
            print(f" One-hot encoded '{col}' ({n_unique} categories)")
    
    df = df.drop(columns=encoded_cols)
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    if len(numeric_cols) > 0:
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(df[numeric_cols])
        df_scaled = pd.DataFrame(scaled_data, columns=numeric_cols, index=df.index)
        df = df.drop(columns=numeric_cols)
        df = pd.concat([df, df_scaled], axis=1)
    
    
    code_columns = [col for col in df.columns if 'code' in col.lower() or 'id' in col.lower()]
    for col in code_columns[:]:  
        if df[col].dtype == 'object' or df[col].dtype == 'string':
            df[f'{col}_length'] = df[col].astype(str).str.len()
            print(f"Extracted length feature from '{col}'")
    
    return df

def dimensionality_reduction(df):
    original_cols = df.shape[1]
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    if len(numeric_cols) > 0:
        variances = df[numeric_cols].var()
        constant_cols = variances[variances == 0].index.tolist()
        if constant_cols:
            df = df.drop(columns=constant_cols)
            print(f"Dropped constant columns: {constant_cols}")
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    if len(numeric_cols) > 1:
        corr_matrix = df[numeric_cols].corr().abs()
        upper_tri = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
        high_corr_cols = [column for column in upper_tri.columns if any(upper_tri[column] > 0.85)]
        if high_corr_cols:
            df = df.drop(columns=high_corr_cols)
            print(f"Dropped highly correlated columns: {high_corr_cols}")
    
    return df

def discretization(df):

    if 'brand' in df.columns:
        brand_counts = df['brand'].value_counts()
        brand_popularity = df['brand'].map(brand_counts)
        df['brand_popularity'] = pd.cut(
            brand_popularity,
            bins=[0, 10, 50, 100, float('inf')],
            labels=['Rare', 'Uncommon', 'Common', 'Very Common']
        )
        print(f"Created 'brand_popularity' category")
        print(f"Distribution:\n{df['brand_popularity'].value_counts()}")
    
    return df

def save_data(df):
    output_file = 'data_preprocessed.csv'
    df.to_csv(output_file, index=False)    
    return output_file

def main():
    file_path = sys.argv[1] 
    df = pd.read_csv(file_path, low_memory=False)
    df = data_cleaning(df)
    df = feature_transformation(df)
    df = dimensionality_reduction(df)
    df = discretization(df)
    output_file = save_data(df)
    subprocess.run(['python','analytics.py'])

if __name__ == "__main__":
    main()