
if __name__ == '__main__':

    # Libraries
    import pandas as pd

    # Load data
    data = pd.read_csv('./db_codes.csv')

    # Format
    data = data.drop_duplicates()

    # Show
    print("\nCodes:")
    print(data)
    print("\nAre there any duplicated codes? %s" %
          data.code.duplicated().any())
