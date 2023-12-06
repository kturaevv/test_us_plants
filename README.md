# FastAPI Example Project

This project delivers:
  - 2 API endpoints that cover:
    - `/plants/net_generation` for ->
      - We want to show map of only annual net generation field
      - We want to limit by top - n 
      - We want to filter by state
      - We want single plant's details
    - `/plants/state_aggregate` for ->
      - We want to show aggregate of actual and percentage values of states generation
- Endpoints are secured behind custom auth module
- Potential future database schema `data_schema.txt` based on semantic separation of columns 
- Streamlined setup for ease of extending the dataset into database:
  - Tailored pydantic models as a data interface for data retrieval, validation, usage and more
  - Automated pipeline for uploading arbitrary number of columns from the dataset
- The project utilizes Docker for containerization and compose for orchestration

## Justfile
The project uses [Just](https://github.com/casey/just) for command automation and ease of access. A better alternative to Makefile. 

All shortucts are located in `justfile` in root directory. To view the commands you can also do:
```shell
just -l
```
Info about installation can be found [here](https://github.com/casey/just#packages).


## Local Development

Make sure to have `just` installed on you system and run for complete setup:
```
cat .env.example > .env
just setup
```
