from typing import Iterable

import pandas as pd
from sqlalchemy import Engine, Table, insert

from src.plants.constants import PlantAnnualEmissionsEnum, PlantDataEnum, TableNamesEnum
from src.plants.constants import Plant, AnnualEmissions, PlantsCustomModel
from src.plants.database import _plant_data_fk, plant_t, annual_emissions_t


def prepare(config: dict[Table, PlantsCustomModel]):

    column_names: list[str] = []
    for enum in config.values():
        column_names.extend(enum.list)

    table_to_column: dict[Table, Iterable[str]] = {}
    for table, enum in config.items():
        table_to_column.update({table: set(enum.list)})

    column_to_table: dict[str, Table] = {}
    for table, columns in table_to_column.items():
        for col in columns:
            column_to_table[col] = table

    return column_names, table_to_column, column_to_table


def data_upload(engine: Engine):

    file_path = 'data.xlsx'
    df = pd.read_excel(file_path, sheet_name="PLNT21")

    COLUMNS, TABLE_TO_COLUMN, COLUMN_TO_TABLE = prepare(
        {
            # table : table enum
            plant_t: PlantDataEnum,
            annual_emissions_t: PlantAnnualEmissionsEnum,
            # add here 
        }
    )
    
    annual_emissions_t.drop(engine)
    plant_t.drop(engine)
    plant_t.create(engine, checkfirst=True)
    annual_emissions_t.create(engine, checkfirst=True)

    with engine.connect() as connection:
        for index, row in df.iterrows():
            if index == 0: continue

            # Container that will "bucket" columns to its relating tables
            container: dict[Table, dict] = {table: {} for table in TABLE_TO_COLUMN.keys()}

            for column in COLUMNS:
                values_to_insert = container[COLUMN_TO_TABLE[column]]
                cell_value = row[column]  # Fetch value based on DataFrame column name

                if not pd.isnull(cell_value) and isinstance(cell_value, (int, float, str)):
                    values_to_insert[column] = cell_value

            # before insert to the main table
            validated_data = Plant(**container[plant_t]).data
            ins = insert(plant_t).values(**validated_data)
            connection.execute(ins)
            connection.commit()
            del container[plant_t]
            
            # other tables
            for table, insertable in container.items():
                if insertable:
                    validated_data = AnnualEmissions(**insertable).data 
                    validated_data.update({_plant_data_fk: index}) # update fk to main table
                    ins = insert(table).values(**validated_data)
                    connection.execute(ins)
                    connection.commit()
