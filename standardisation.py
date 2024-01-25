import os.path
import sys
import pandas as pd
from data_gathering import fetch_table_data_from_db, credential_dict
from datetime import datetime
sys.dont_write_bytecode = True


house_df = fetch_table_data_from_db(credential_dict)
new_processed_df_path = './pre_processed_house_df.xlsx'
date_formats_mapping_dict = {
    "%Y%m%dT%H%M%S": "%d-%m-%Y",
    "%d/%m/%Y": "%d-%m-%Y",
    "%Y-%m-%d": "%d-%m-%Y"
}


def null_standardisation(house_price_df):
    func_name = "null_standardisation"
    try:
        null_df = house_price_df[house_price_df.isnull().any(axis=1)]
        if not null_df.empty:
            house_price_df = house_price_df.dropna()
        return True, func_name, house_price_df
    except Exception as null_value_finder:
        print(str(null_value_finder))
        return False, func_name, house_price_df


def date_standardisation(house_price_df, date_mapping_dict):
    func_name = "date_standardisation"
    try:
        house_price_df['date'] = house_price_df['date'].apply(lambda x: datetime.strptime(str(x), '%Y%m%dT%H%M%S').strftime(date_mapping_dict['%Y%m%dT%H%M%S']))
        return True, func_name, house_price_df
    except Exception as date_conversion:
        print(str(date_conversion))
        return False, func_name, house_price_df


def price_standardisation(house_price_df):
    func_name = "price_standardisation"
    try:
        # house_price_df['price(in 1000)'] = house_price_df['price(in 1000)'].apply(lambda x: round(int(x)))
        house_price_df['price(in 1000)'] = house_price_df['price(in 1000)'].apply(lambda x: x*100 if len(str(float(x)).split('.')[0]) == 6 else x*10 if len(str(float(x)).split('.')[0]) > 6 else x*1000)
        return True, func_name, house_price_df
    except Exception as round_number_conversion:
        print(str(round_number_conversion))
        return False, func_name, house_price_df


# def view_standardisation(house_price_df):
#     func_name = "bathroom_standardisation"
#     try:
#         house_price_df['bathrooms'] = house_price_df['bathrooms'].apply(lambda x: round(int(x)))
#         return True, func_name, house_price_df
#     except Exception as round_number_conversion:
#         print(str(round_number_conversion))
#         return False, func_name, house_price_df
#
#
# def condition_standardisation(house_price_df):
#     func_name = "floors_standardisation"
#     try:
#         house_price_df['floors'] = house_price_df['floors'].apply(lambda x: round(int(x)))
#         return True, func_name, house_price_df
#     except Exception as round_number_conversion:
#         print(str(round_number_conversion))
#         return False, func_name, house_price_df


def save_the_dataframe(new_house_price_df, house_price_df):
    func_name = "save_the_dataframe"
    try:
        house_price_df.to_excel(new_house_price_df, index=False, engine='openpyxl')
        print("File Saved!")
        return True, func_name
    except Exception as save_error:
        print(str(save_error))
        return False, func_name


def main():
    if not os.path.exists(new_processed_df_path):
        if not house_df.empty:
            null_processing_status, function_name, null_processed_house_price_df = null_standardisation(house_df)
            if null_processing_status:
                date_processing_status, function_name, date_processed_house_price_df = date_standardisation(null_processed_house_price_df, date_formats_mapping_dict)
                if date_processing_status:
                    price_processing_status, function_name, price_processed_house_price_df = price_standardisation(date_processed_house_price_df)
                    # if price_processing_status:
                    #     save_status, function_name = save_the_dataframe(new_processed_df_path, price_processed_house_price_df)
                    # else:
                    #     print(f"Something's Wrong, pls start backtracking with: {function_name}")
                else:
                    print(f"Something's Wrong, pls start backtracking with: {function_name}")
            else:
                print(f"Something's Wrong, pls start backtracking with: {function_name}")
        else:
            print("Something's Wrong, pls check if the initial dataframe was properly passed or not!")

    new_house_price_df = pd.read_excel(new_processed_df_path)
    if not new_house_price_df.empty:
        return new_house_price_df
    else:
        return house_df


if __name__ == "__main__":
    main()