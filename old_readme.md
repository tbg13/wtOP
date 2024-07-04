# Data Engineering Project - One Piece Universe

## High-Level Milestones

NT = Non-Tech readers // T = Tech readers

### Infrastructure & Extraction

**Set Up Containerized Environment**
- **NT**: Set up a consistent and portable environment to run all project components.
- **T**: Use Docker for Linux containerized development. Create a custom image that includes all necessary components.

**Develop Data Retrieval Service**
- **NT**: Create a service to fetch data from a wiki.
- **T**: Implement a scraping service using Python to extract data from a wiki and store it in a raw format within the Docker container.

**Develop API for Scraped Data**
- **NT**: Create an API to serve the scraped data after initial cleaning.
- **T**: Use FastAPI to create endpoints that expose the cleaned (Silver) data. This will simulate a real API and provide endpoints for further use by Airbyte.

**Deploy Data Integration Tool**
- **NT**: Deploy a tool to handle data extraction and loading processes.
- **T**: Use Airbyte to connect to the FastAPI service and manage data extraction. Configure Airbyte to extract cleaned (Silver) data from the FastAPI endpoints and store it in MinIO.

### Storage & Transformation

**Set Up Object Storage**
- **NT**: Configure a system to store raw data safely.
- **T**: Use MinIO as S3-compatible object storage to store Silver data extracted by Airbyte.

**Configure Data Integration via CLI**
- **NT**: Set up and manage data connections and transfers using command-line tools.
- **T**: Use Airbyte CLI for configuring data sources (FastAPI) and destinations (MinIO).

**Set Up Analytical Database**
- **NT**: Install and configure a database optimized for analytical queries.
- **T**: Use DuckDB for storing and querying processed (Gold) data.

**Develop Transformation Models**
- **NT**: Build models to clean and prepare data for analysis.
- **T**: Use dbt to develop and manage transformation models that process Silver data into Gold data and store it in DuckDB.

### Orchestration & Automation

**Deploy Workflow Orchestration Tool**
- **NT**: Set up a tool to manage and schedule data workflows.
- **T**: Use Dagster for orchestrating data pipelines, including the ingestion from FastAPI via Airbyte, transformations using dbt, and loading into DuckDB.

**Version Control and CI/CD**
- **NT**: Implement version control and continuous integration/delivery processes to automate testing and deployment.
- **T**: Use Git for version control.
- **T**: Use GitHub Actions to set up CI/CD pipelines.

### Analysis & Visualization

**Perform Data Analysis**
- **NT**: Analyze the processed data and visualize the results.
- **T**: Connect to DuckDB using DBeaver for querying and visualization.

**Build Interactive Visualization**
- **NT**: Create an interactive visualization to present the analysis results.
- **T**: Use Streamlit to build the visualization interface.

### Further Improvements
- Dockerize the whole application by separating each component into its own docker apps and volumes
- Expose API for other ppl use

## Tech considerations
- Why MinIO and DuckDB for storage ?
  
DuckDB's primary strength lies in its ability to handle in-process, high-perf analytics and querying. Storage is optimized for said purposes (columnar format), rather than raw data ingestion. This is where MinIO comes in: MinIO is designed for storing large amount of unstructured or semi-structured data (object storage)

MinIO handles long-term storage of large (silver) datasets : it is responsible for scability and durability. 
DuckDB handles data transformation and analytics-ready dataset : it is responsible for performance and analytics.

Added benefit is separating storage layer and processing layer.

- How do MinIO and DuckDB work together then ?

1) Storage (Minio): Contains raw and cleaned (Silver) data.
2) Extraction (Airbyte): Moves and parses data from Minio to DuckDB.
3) Processing (DuckDB):  
3.a) Transformation (dbt): Performs data transformations within DuckDB.  
3.b) Storage (DuckDB): Stores transformed (Gold) data within DuckDB.

