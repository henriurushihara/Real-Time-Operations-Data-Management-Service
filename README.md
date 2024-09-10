
## License

This project is licensed under the **Creative Commons Attribution-NonCommercial-NoDerivatives 4.0** license.

- You may download and view the code for personal or non-commercial purposes.
- You may not modify, distribute, or use this work for commercial purposes without explicit permission from the author, 
**Henri F. Urushihara**.

[Full License Details](https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode)


## Oracle Database Requirements

This software is designed to work with an **existing Oracle Database** that can be accessed remotely. You must have access to a remote Oracle Database instance, either hosted on your organization's infrastructure or on a cloud service like **Oracle Cloud**.

### Connecting to an Oracle Database

To use this project, you need the following details from your Oracle Database administrator:
- **Host** (the server where Oracle Database is running)
- **Port** (usually 1521 by default)
- **Service Name** (the specific Oracle Database instance you want to connect to)
- **Username** and **Password** (your credentials to access the database)

Once you have these details, update the .env (environment) file with your connection information:

ORACLE_USER=your_username
ORACLE_PASSWORD=your_password
ORACLE_HOST=your_host
ORACLE_PORT=your_port
ORACLE_SERVICE_NAME=your_service_name 


## OracleDB Installation and Setup

To run this project, you'll need to install **Oracle Instant Client** on your local machine. The Instant Client provides the tools necessary to connect to an Oracle Database. It is required for running SQL queries and for the Python `oracledb` library to connect to OracleDB.

### Why Do You Need Oracle Instant Client?

The Oracle Instant Client is essential if you're working with an Oracle Database remotely or through a local application. It provides all the necessary libraries to:
- **Run SQL queries** from your machine using tools like SQL*Plus.
- **Use Python (`oracledb` library)** to interact with OracleDB.
- **Connect to OracleDB** without needing to install the full Oracle Database software.

### Step 1: Download and Install Oracle Instant Client

1. Visit the [Oracle Instant Client download page](https://www.oracle.com/database/technologies/instant-client/downloads.html).
2. Download the appropriate version for your operating system (e.g., **Windows 64-bit**).
3. Extract the downloaded files to a directory on your computer. A common location is `C:\oracle\instantclient_19_8` for Windows users.

### Step 2: Set Up Oracle Instant Client on Your System

Once you've extracted the Instant Client, follow these steps to configure it:

#### For Windows:
1. Open the **Start Menu** and search for **Environment Variables**.
2. Click on **Edit the system environment variables**.
3. In the System Properties window, click on **Environment Variables**.
4. Under **System Variables**, click **New** and create a variable:
   - Variable name: `ORACLE_HOME`
   - Variable value: `C:\oracle\instantclient_19_8` (or wherever you extracted the Instant Client).
5. Add the same path (`C:\oracle\instantclient_19_8`) to your **`Path`** system variable.

#### For macOS/Linux:
1. Download the Instant Client from the [Oracle Instant Client download page](https://www.oracle.com/database/technologies/instant-client/downloads.html).
2. Follow the instructions provided for your operating system to set the `LD_LIBRARY_PATH` environment variable to the extracted Instant Client folder.

### Step 3: Install the Python `oracledb` Library

Once the Oracle Instant Client is set up, you can install the **`oracledb`** Python package:

```bash
pip install oracledb

Setting Up the Development Environment

1. Clone the repository.

Setting Up A Virtual Environment

To ensure the project dependencies are properly managed and isolated, follow these steps to set up a virtual environment for the project.

2. Create the Virtual Environment

In the root of your project directory, run the following command in a bash terminal to create a virtual environment:

python -m venv venv

3. Activate the Virtual Environment

For Windows:
Run the following command in your terminal

source venv/Scripts/activate

For macOS/Linux:
Run the following command in your terminal:

source venv/bin/activate

Once activated, you should see (venv) in front of your terminal prompt, indicating that the virtual environment is active.

4. Install Dependencies

After activating the virtual environment, install the required dependencies by running:

pip install -r requirements.txt

5. Deactivating the Virtual Environment
When you're done, you can deactivate the virtual environment by running:

deactivate