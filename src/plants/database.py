from sqlalchemy import (
    Column,
    ForeignKey,
    Float,
    Integer,
    String,
    Table,
    MetaData,
)
from sqlalchemy.orm import registry, relationship

from src.database import metadata
from src.plants.constants import PlantAnnualEmissionsEnum, PlantDataEnum, TableNamesEnum


_plant_data_fk = "plant_fk"

plant_t = Table(
    TableNamesEnum.plant_data,
    metadata,
    Column("id", Integer, primary_key=True),
    Column(PlantDataEnum.plant_file_sequence_number, Integer, unique=True),
    Column(PlantDataEnum.data_year, Integer, nullable=True),
    Column(PlantDataEnum.plant_name, String, nullable=True),
    Column(PlantDataEnum.plant_state_abbreviation, String, nullable=True),
    Column(PlantDataEnum.plant_associated_iso_rto_territory, String, nullable=True),
    Column(PlantDataEnum.plant_fips_state_code, Integer, nullable=True),
    Column(PlantDataEnum.plant_fips_county_code, Integer, nullable=True),
    Column(PlantDataEnum.plant_county_name, String, nullable=True),
    Column(PlantDataEnum.plant_latitude, Float, nullable=True),
    Column(PlantDataEnum.plant_longitude, Float, nullable=True),
    Column(PlantDataEnum.plant_nominal_heat_rate, Float, nullable=True),
    Column(PlantDataEnum.plant_net_generation, Float, nullable=True)
)

# Additional plant's details
annual_emissions_t = Table(
    TableNamesEnum.plant_annual_emmissions,
    metadata,
    Column("id", Integer, primary_key=True),
    Column(_plant_data_fk, Integer, ForeignKey(TableNamesEnum.plant_data + ".id"), nullable=True),
    Column(PlantAnnualEmissionsEnum.Hg, Float, nullable=True),
    Column(PlantAnnualEmissionsEnum.NOx, Float, nullable=True),
    Column(PlantAnnualEmissionsEnum.SO2, Float, nullable=True),
    Column(PlantAnnualEmissionsEnum.CO2, Float, nullable=True),
    Column(PlantAnnualEmissionsEnum.CH4, Float, nullable=True),
    Column(PlantAnnualEmissionsEnum.N2O, Float, nullable=True),
    Column(PlantAnnualEmissionsEnum.NOx_biomass, Float, nullable=True),
    Column(PlantAnnualEmissionsEnum.SO2_biomass, Float, nullable=True),
    Column(PlantAnnualEmissionsEnum.CO2_biomass, Float, nullable=True),
    Column(PlantAnnualEmissionsEnum.CH4_biomass, Float, nullable=True),
    Column(PlantAnnualEmissionsEnum.N2O_biomass, Float, nullable=True),
    Column(PlantAnnualEmissionsEnum.NOx_CHP_adjustment, Float, nullable=True),
    Column(PlantAnnualEmissionsEnum.SO2_CHP_adjustment, Float, nullable=True),
    Column(PlantAnnualEmissionsEnum.CO2_CHP_adjustment, Float, nullable=True),
    Column(PlantAnnualEmissionsEnum.CH4_CHP_adjustment, Float, nullable=True),
    Column(PlantAnnualEmissionsEnum.N2O_CHP_adjustment, Float, nullable=True),
    Column(PlantAnnualEmissionsEnum.CO2_equivalent, Float, nullable=True)
)

class PlantTable(object):
    pass


class AnnualEmissionsTable(object):
    pass


mapper_registry = registry(metadata=metadata)

mapper_registry.map_imperatively(PlantTable, plant_t)
mapper_registry.map_imperatively(
    AnnualEmissionsTable,
    annual_emissions_t, 
    properties={
        "plants": relationship(PlantTable, backref=TableNamesEnum.plant_data)
    },)

