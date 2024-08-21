import pandas as pd

def transform_price(price):
    """
    Transforms price values to remove the '/month' suffix if present.

    Args:
        price (str): The price value as a string.

    Returns:
        str: The transformed price value without the '/month' suffix.
    """
    if '/month' in price:
        return price.split(' /month')[0]
    return price

def transform_contributions_followers(contribution):
    """
    Transforms contribution values from a string with 'k' notation to an integer.

    Args:
        contribution (str): The contribution value as a string, potentially including 'k'.

    Returns:
        float: The transformed contribution value in integer form.
    """
    if 'k' in contribution:
        if '.' in contribution:
            return float(contribution.split('k')[0]) * 1000
        return float(contribution.split('k')[0]) * 1000
    return int(contribution)

def preprocess_data(file_path, output_path):
    """
    Reads a CSV file, transforms specific columns, and saves the preprocessed data to a new CSV file.

    Args:
        file_path (str): The path to the input CSV file.
        output_path (str): The path to the output CSV file where preprocessed data will be saved.
    """
    # Load the dataset
    df = pd.read_csv(file_path)
    
    # Apply transformations
    df['Price'] = df['Price'].apply(transform_price)
    df['Contributions'] = df['Contributions'].apply(transform_contributions_followers)
    df['Followers'] = df['Followers'].apply(transform_contributions_followers)
    
    # Save the preprocessed dataset
    df.to_csv(output_path, index=False)
    print(f"Preprocessed data has been saved to '{output_path}'.")

# Example usage
if __name__ == "__main__":
    preprocess_data("full_data.csv", "preprocessed_data.csv")
