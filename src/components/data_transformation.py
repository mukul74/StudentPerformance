import sys
from dataclasses import dataclass

from log_symbols import LogSymbols
import os
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_ob_file_path=os.path.join('artifact','preprocessor.pkl')


class DataTransformation:
    def __init__(self):
        self.data_transformer_config = DataTransformationConfig()

    def get_DataTransformer_Object(self):
        """Responsible for Transformation

        Raises:
            CustomException: _description_

        Returns:
            _type_: _description_
        """
        try: 
            numerical_columns = ["writing score", "reading score"]
            categorical_columns = [
                "gender",
                "race/ethnicity",
                "parental level of education",
                "lunch",
                "test preparation course"
            ]

            numerical_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler())
                ]
            )
            categorical_pipeline = Pipeline(
                steps=[
                        ("imputer", SimpleImputer(strategy="most_frequent")),
                        ("one hot encoder",OneHotEncoder())
                        # ("scalar", StandardScaler())
                ]
            )
            
            logging.info("Numerical Columns Encoding Completed")
            logging.info("Categorical Columns Encoding Completed")

            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline", numerical_pipeline, numerical_columns),
                    ("cat_pipeline", categorical_pipeline, categorical_columns)
                ]
            )

            return preprocessor
        except Exception as e:
            raise CustomException(e,sys)
    
    def initiate_data_transformation(self,train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Reading of Train and Test data complete")

            logging.info("Obtaining preprocessing object")
            
            preprocessing_obj = self.get_DataTransformer_Object()

            target_column_name = "math score"
            numerical_columns = ["writing score", "reading score"]

            input_feature_train_df = train_df.drop(columns = [target_column_name], axis=1)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns = [target_column_name], axis=1)
            target_feature_test_df = test_df[target_column_name]

            logging.info(f"Applying preprocessing object pipeline to Train and Test Dataframe")

            input_feature_train_array = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_array = preprocessing_obj.fit_transform(input_feature_test_df)

            train_arr = np.c_[input_feature_train_array, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_array, np.array(target_feature_test_df)]

            logging.info(f"Saved preprocessing object")

            save_object(
                self.data_transformer_config.preprocessor_ob_file_path,
                obj=preprocessing_obj
            )

            return (
                train_arr,
                test_arr,
                self.data_transformer_config.preprocessor_ob_file_path,

            )

        except Exception as e:
                raise CustomException(e,sys)
                pass
