# Real-Time Operations Data Management Service

**Here, I have created a high-performance service** for managing oil and gas well and division data, leveraging Oracle database-backed FastAPI with JSON and CLOB chunking for handling huge data sets. This service is designed to power up real-time operations in the energy sector or any industry where large datasets and complex queries demand maximum efficiency and scalability.

## Key Design Considerations
### JSON, CLOBs, and 4000-Character Chunking

Handling massive data sets from the Oracle database can be tricky. Oracle imposes a 4000-character limit when working with strings and JSON objects in PL/SQL. But, thanks to **CLOB (Character Large Objects)**, we can handle much larger data sets. This project uses a **chunking technique** to split large JSON results into 4000-character pieces, ensuring data can be retrieved without causing any API timeouts or hangs.

This approach ensures even the largest data sets can be transferred smoothly from OracleDB to the FastAPI service—allowing this project to **scale to handle massive production data in real-time**!

## Features & Highlights
- **High-Performance JSON Handling**: All database queries return results in JSON format, thanks to the clever use of Oracle's JSON functions.
- **CLOB Support**: For handling massive amounts of data (think thousands of rows), this service converts the SQL results into CLOB (Character Large Objects) and efficiently processes them using 4000-character chunking. This prevents **API timeouts** or **hangs** when fetching huge data sets.
- **4000-Chunking**: By breaking large JSON outputs into 4000-character pieces, this project bypasses Oracle's limitations and ensures smooth delivery of data across all API endpoints.

### Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Database Procedures](#database-procedures)
- [OracleDB Installation and Setup](#oracledb-installation-and-setup)
- [Setting Up the Development Environment](#setting-up-the-development-environment)
- [License](#license)

---

## Installation

To get started, you’ll need Python 3.9+, Oracle Instant Client, and some basic Oracle DB credentials (or an accessible Oracle Cloud instance). Here's the quick setup guide.

### Prerequisites:
- Python 3.9+
- Docker (optional for running OracleDB in a container)
- Oracle Instant Client

### Setup Steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/yourproject.git
   cd yourproject

2. Set up the Python environment:

python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

3. Install the dependencies:

pip install -r requirements.txt

4. Create an environment configuration file: Create a .env file in the project root with your Oracle connection information:

ORACLE_USER=your_username
ORACLE_PASSWORD=your_password
ORACLE_HOST=your_host
ORACLE_PORT=1521
ORACLE_SERVICE_NAME=your_service_name

5. Run the FastAPI server:

uvicorn service:app --reload

The API will be available at http://localhost:8000.

## Usage
This project offers API endpoints that interact with your Oracle database, providing division and well summaries, daily summaries, and more. The API processes large data sets using optimized chunking techniques to ensure smooth performance without hanging.

Swagger UI
To view and test the endpoints interactively, visit http://localhost:8000/docs.

### Example cURL for Well Summary:

curl -X GET "http://localhost:8000/well-summary?well_id=1851797476&division_id=63"

cURL for Daily Well Summary:

curl -X GET "http://localhost:8000/well-summary-by-day?well_id=1851797476&division_id=63"

## Project Structure

yourproject/
├── DATABASE/
│   ├── Get_ODM_Data_Pkg_Body.sql    # SQL script for the package body
│   ├── Get_ODM_Data_Pkg_Spec.sql    # SQL script for the package specification
├── venv/                            # Virtual environment directory
├── .env                             # Environment variables for DB credentials
├── data_helper.py                   # DataHelper class for managing database connections and procedure calls
├── models.py                        # Pydantic models for request/response validation
├── service.py                       # Main FastAPI application
├── requirements.txt                 # Python dependencies
├── README.md                        # Documentation (you're reading it!)
└── LICENSE                          # License information

## API Endpoints
GET /division-list
Fetches the list of divisions in JSON format.

Response: JSON array of divisions.
GET /division-summary
Fetches a summary of well data for each division, including total oil produced and financial data.

GET /well-summary?well_id={well_id}&division_id={division_id}
Fetches summary data for a given well and division.

GET /well-summary-by-day?well_id={well_id}&division_id={division_id}
Returns daily well data for a given well and division, using 4000-character chunking for efficient data transfer.

## Database Procedures
The Oracle procedures for data retrieval are located in the DATABASE/ folder.

1. Get_ODM_Data_Pkg.Get_Division_List
Fetches a JSON list of all divisions.
2. Get_ODM_Data_Pkg.Get_Division_Summary_Data
Fetches a JSON summary of each division’s well data, oil production, and financials.
3. Get_ODM_Data_Pkg.Get_Well_Summary_Data
Fetches a JSON summary of a well’s data, given a well_id and division_id.
4. Get_ODM_Data_Pkg.Get_Well_Summary_By_Day
Returns a JSON array of well summary data, chunked in 4000-character segments, for daily oil production and sales.

## OracleDB Installation and Setup
To run this project, you'll need to install Oracle Instant Client on your local machine. The Instant Client provides the tools necessary to connect to an Oracle Database. It is required for running SQL queries and for the Python oracledb library to connect to OracleDB.

### Why Do You Need Oracle Instant Client?
The Oracle Instant Client is essential if you're working with an Oracle Database remotely or through a local application. It provides all the necessary libraries to:

Run SQL queries from your machine using tools like SQL*Plus.
Use Python (oracledb library) to interact with OracleDB.
Connect to OracleDB without needing to install the full Oracle Database software.

#### Step 1: Download and Install Oracle Instant Client
Visit the Oracle Instant Client download page.
Download the appropriate version for your operating system (e.g., Windows 64-bit).
Extract the downloaded files to a directory on your computer. A common location is C:\oracle\instantclient_19_8 for Windows users.

#### Step 2: Set Up Oracle Instant Client on Your System
Once you've extracted the Instant Client, follow these steps to configure it:

##### For Windows:
Open the Start Menu and search for Environment Variables.
Click on Edit the system environment variables.
In the System Properties window, click on Environment Variables.
Under System Variables, click New and create a variable:
Variable name: ORACLE_HOME
Variable value: C:\oracle\instantclient_19_8 (or wherever you extracted the Instant Client).
Add the same path (C:\oracle\instantclient_19_8) to your Path system variable.

##### For macOS/Linux:
Download the Instant Client from the Oracle Instant Client download page.
Follow the instructions provided for your operating system to set the LD_LIBRARY_PATH environment variable to the extracted Instant Client folder.

#### Step 3: Install the Python oracledb Library
Once the Oracle Instant Client is set up, you can install the oracledb Python package:

pip install oracledb

## Setting Up the Development Environment
Clone the repository.

### Setting Up A Virtual Environment
To ensure the project dependencies are properly managed and isolated, follow these steps to set up a virtual environment for the project.

### Create the Virtual Environment
In the root of your project directory, run the following command in a bash terminal to create a virtual environment:

python -m venv venv

### Activate the Virtual Environment

#### For Windows: Run the following command in your terminal:

source venv/Scripts/activate

#### For macOS/Linux: Run the following command in your terminal:

source venv/bin/activate

Once activated, you should see (venv) in front of your terminal prompt, indicating that the virtual environment is active.

### Install Dependencies
After activating the virtual environment, install the required dependencies by running:

pip install -r requirements.txt

### Deactivating the Virtual Environment
When you're done, you can deactivate the virtual environment by running:

deactivate

## License

This project is licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 license.

You may download and view the code for personal or non-commercial purposes.
You may not modify, distribute, or use this work for commercial purposes without explicit permission from the author, Henri F. Urushihara.

Full License Details