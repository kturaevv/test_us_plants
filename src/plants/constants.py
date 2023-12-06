from enum import Enum
from typing import Optional, Any

from pydantic import BaseModel, Field, field_validator

from src.plants.utils import self_mapping


""" 
Following pydantic models serve as a single interface for:
    - ease of member access
    - some data validation
    - data retrieval from pandas dataframe and pipeline automation
    - table column definitions with 1 - 1 correspondance with original data
    - potential usage with a dependency injection for dynamic SQL building
    - potential usage as an endpoint Enum for ease of targeting specific columns 
"""


class PlantsCustomModel(BaseModel):

    @property
    def data(self):
        return self.model_dump(by_alias=True)
    
    @property
    def list(self):
        return list(self.model_dump().values())

class TableNames(PlantsCustomModel):
    plant_data: str = "plant_data"
    plant_annual_emmissions: str = "plant_annual_emmissions"


class Plant(PlantsCustomModel):
    data_year: Optional[Any] = Field(None, alias = "Data Year")
    plant_name: Optional[Any] = Field(None, alias = "Plant name")
    plant_file_sequence_number: Optional[Any] = Field(None, alias = "Plant file sequence number")
    plant_state_abbreviation: Optional[Any] = Field(None, alias = "Plant state abbreviation")
    plant_associated_iso_rto_territory: Optional[Any] = Field(None, alias = "Plant associated ISO/RTO Territory ")
    plant_fips_state_code: Optional[Any] = Field(None, alias = "Plant FIPS state code")
    plant_fips_county_code: Optional[Any] = Field(None, alias = "Plant FIPS county code")
    plant_county_name: Optional[Any] = Field(None, alias = "Plant county name")
    plant_latitude: Optional[Any] = Field(None, alias = "Plant latitude")
    plant_longitude: Optional[Any] = Field(None, alias = "Plant longitude")
    plant_nominal_heat_rate: Optional[Any] = Field(None, alias = "Plant nominal heat rate (Btu/kWh)")

    # This can either be within plant's main table as a summary field or be located in other
    # table in accordance with semantic separation shown in data_schema.txt.
    plant_net_generation: Optional[Any] = Field(None, alias = "Plant annual net generation (MWh)")

    @field_validator("plant_net_generation")
    @classmethod
    def some_basic_field_validation(cls, v: Any) -> float:
         
        if isinstance(v, str):
            v: str = v.strip()
            if v.startswith("(") and v.endswith(")"):
                return float(v[1:-2]) # remove parenthesis
        elif isinstance(v, (int,float)):
            return float(v)

        return v

class AnnualEmissions(PlantsCustomModel):
    Hg: Optional[Any] = Field(None, alias = "Plant annual Hg emissions (lbs)")
    NOx: Optional[Any] = Field(None, alias = "Plant annual NOx emissions (tons)")
    SO2: Optional[Any] = Field(None, alias = "Plant annual SO2 emissions (tons)")
    CO2: Optional[Any] = Field(None, alias = "Plant annual CO2 emissions (tons)")
    CH4: Optional[Any] = Field(None, alias = "Plant annual CH4 emissions (lbs)")
    N2O: Optional[Any] = Field(None, alias = "Plant annual N2O emissions (lbs)")
    NOx_biomass: Optional[Any] = Field(None, alias = "Plant annual NOx biomass emissions (tons)")
    SO2_biomass: Optional[Any] = Field(None, alias = "Plant annual SO2 biomass emissions (tons)")
    CO2_biomass: Optional[Any] = Field(None, alias = "Plant annual CO2 biomass emissions (tons)")
    CH4_biomass: Optional[Any] = Field(None, alias = "Plant annual CH4 biomass emissions (lbs)")
    N2O_biomass: Optional[Any] = Field(None, alias = "Plant annual N2O biomass emissions (lbs)")
    NOx_CHP_adjustment: Optional[Any] = Field(None, alias = "Plant annual NOx emissions CHP adjustment value (tons)")
    SO2_CHP_adjustment: Optional[Any] = Field(None, alias = "Plant annual SO2 emissions CHP adjustment value (tons)")
    CO2_CHP_adjustment: Optional[Any] = Field(None, alias = "Plant annual CO2 emissions CHP adjustment value (tons)")
    CH4_CHP_adjustment: Optional[Any] = Field(None, alias = "Plant annual CH4 emissions CHP adjustment value (lbs)")
    N2O_CHP_adjustment: Optional[Any] = Field(None, alias = "Plant annual N2O emissions CHP adjustment value (lbs)")
    CO2_equivalent: Optional[Any] = Field(None, alias = "Plant annual CO2 equivalent emissions (tons)")


# Enum definitions

TableNamesEnum = TableNames()

PlantDataEnum = Plant(**self_mapping([
        "Data Year",
        "Plant name",
        "Plant file sequence number",
        "Plant state abbreviation",
        "Plant associated ISO/RTO Territory ",
        "Plant FIPS state code",
        "Plant FIPS county code",
        "Plant county name",
        "Plant latitude",
        "Plant longitude",
        "Plant nominal heat rate (Btu/kWh)",
        "Plant annual net generation (MWh)",
    ])
)
 
PlantAnnualEmissionsEnum = AnnualEmissions(**self_mapping([
        "Plant annual Hg emissions (lbs)",
        "Plant annual NOx emissions (tons)",
        "Plant annual SO2 emissions (tons)",
        "Plant annual CO2 emissions (tons)",
        "Plant annual CH4 emissions (lbs)",
        "Plant annual N2O emissions (lbs)",
        "Plant annual NOx biomass emissions (tons)",
        "Plant annual SO2 biomass emissions (tons)",
        "Plant annual CO2 biomass emissions (tons)",
        "Plant annual CH4 biomass emissions (lbs)",
        "Plant annual N2O biomass emissions (lbs)",
        "Plant annual NOx emissions CHP adjustment value (tons)",
        "Plant annual SO2 emissions CHP adjustment value (tons)",
        "Plant annual CO2 emissions CHP adjustment value (tons)",
        "Plant annual CH4 emissions CHP adjustment value (lbs)",
        "Plant annual N2O emissions CHP adjustment value (lbs)",
        "Plant annual CO2 equivalent emissions (tons)",
    ])
)