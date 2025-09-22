import pandas as pd

REQUIRED_COLUMNS = ["product_id", "Name", "PriceUSD"]

def load_products_from_excel(file_path: str):
    # reading excel file as a data frame
    df = pd.read_excel(file_path)
    
    # checking for the existance of required columns
    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")
        
        
    # data frame clean up
    df = df.dropna(subset=REQUIRED_COLUMNS)

    # data validation
    if df["ProductID"].duplicated().any():
        raise ValueError("Duplicated ProductID found!")
    
    # converting dataframe to list of dictionaries(each row is a single dict)
    products_list = df.to_dict(orient="records")
    
    return products_list