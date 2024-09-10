
import oracledb
from contextlib import contextmanager
import logging
import os
from dotenv import load_dotenv
from datetime import datetime
import asyncio

# Load environment variables from .env file
load_dotenv()

user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
dsn = os.getenv('DB_HOST') + '/' + os.getenv('DB_SERVICE')

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class DataHelper:
    _instance = None
    _lock = asyncio.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DataHelper, cls).__new__(cls)
        return cls._instance

    async def initialize(self):
        logging.debug("Initializing DataHelper")
        async with self._lock:
            if not hasattr(self, 'pool'):
                logging.debug("Creating connection pool")
                try:
                    self.pool = oracledb.create_pool(
                        user=user,
                        password=password,
                        dsn=dsn,
                        min=2,
                        max=10,
                        increment=1
                    )
                    logging.debug("Connection pool created")
                    self.datatypes = {
                        'NUMBER': oracledb.NUMBER,
                        'CLOB': oracledb.CLOB,
                        'CURSOR': oracledb.CURSOR
                    }
                except Exception as e:
                    logging.error(f"Error while creating the connection pool: {e}")
                    raise

    @contextmanager
    def get_connection(self):
        logging.debug("Acquiring connection from pool")
        connection = self.pool.acquire()
        try:
            yield connection
        finally:
            logging.debug("Releasing connection back to pool")
            connection.close()

    async def read_clob_data(self, clob):
        logging.debug("Reading CLOB data")
        if clob is None:
            return None
        data = await asyncio.to_thread(clob.read)
        logging.debug("CLOB data read successfully")
        return data

    async def read_clob(self, proc_name, params=[]):
        logging.debug(f"Preparing to call procedure: {proc_name} with params: {params}")
        result = None
        with self.get_connection() as conn:
            cursor = conn.cursor()
            out_param = cursor.var(oracledb.CLOB)
            logging.debug(f"Executing procedure: {proc_name} with params: {params}")
            try:
                await asyncio.to_thread(cursor.callproc, proc_name, params + [out_param])
                clob_value = out_param.getvalue()
                result = await self.read_clob_data(clob_value)
            except Exception as e:
                logging.error(f"Error executing procedure: {proc_name}, Error: {e}")
                raise
            finally:
                cursor.close()
            logging.debug(f"Procedure {proc_name} completed with result: {result}")
        return result

    async def read_cursor(self, proc_name, params=[]):
        logging.debug(f"Preparing to call procedure: {proc_name} with params: {params}")
        result = []
        with self.get_connection() as conn:
            cursor = conn.cursor()
            out_param = cursor.var(oracledb.CURSOR)
            logging.debug(f"Executing procedure: {proc_name} with params: {params}")
            try:
                await asyncio.to_thread(cursor.callproc, proc_name, [out_param] + params)
                cursor_result = out_param.getvalue()
                if cursor_result is None:
                    logging.error("Cursor result is None")
                    raise ValueError("Cursor result is None")
                columns = [desc[0] for desc in cursor_result.description]
                while True:
                    rows = await asyncio.to_thread(cursor_result.fetchmany, 100)  # Fetch in batches of 100
                    if not rows:
                        break
                    data = [dict(zip(columns, row)) for row in rows]
                    result.extend(self.format_dates(data))
                    logging.debug(f"Fetched {len(rows)} rows, total fetched so far: {len(result)}")
                logging.debug("Cursor data read successfully")
            except Exception as e:
                logging.error(f"Error executing procedure: {proc_name}, Error: {e}")
                raise
            finally:
                cursor.close()
            logging.debug(f"Procedure {proc_name} completed with result: {result}")
        return result

    async def call_procedure(self, proc_name, params=[], return_type='CURSOR', fetch_size=100):
        logging.debug(f"Preparing to call procedure: {proc_name} with params: {params}")
        result = []
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if return_type == 'CURSOR':
                out_param = cursor.var(oracledb.CURSOR)
                cursor.callproc(proc_name, [out_param] + params)
                        
                columns = [desc[0] for desc in out_param.getvalue().description]
                rows = out_param.getvalue().fetchall()
                data = [dict(zip(columns, row)) for row in rows]
                        
                result = self.format_dates(data)
            elif return_type == 'NUMBER':
                out_param = cursor.var(oracledb.NUMBER)
                logging.debug(f"Executing procedure: {proc_name} with params: {params}")
                try:
                    await asyncio.to_thread(cursor.callproc, proc_name, params + [out_param])
                    await asyncio.to_thread(conn.commit)
                    result = out_param.getvalue()
                    logging.debug(f"Procedure executed, result: {result}")
                except Exception as e:
                    logging.error(f"Error executing procedure: {proc_name}, Error: {e}")
                    raise
            elif return_type == 'CLOB':
                out_param = cursor.var(oracledb.CLOB)
                logging.debug(f"Executing procedure: {proc_name} with params: {params}")
                try:
                    await asyncio.to_thread(cursor.callproc, proc_name, params + [out_param])
                    clob_value = out_param.getvalue()
                    result = await self.read_clob_data(clob_value)
                    logging.debug(f"CLOB result: {result}")
                except Exception as e:
                    logging.error(f"Error executing procedure: {proc_name}, Error: {e}")
                    raise
            else:
                logging.debug(f"Executing procedure: {proc_name} with params: {params}")
                try:
                    await asyncio.to_thread(cursor.callproc, proc_name, params)
                    await asyncio.to_thread(conn.commit)
                    logging.debug("Procedure executed and committed")
                except Exception as e:
                    logging.error(f"Error executing procedure: {proc_name}, Error: {e}")
                    raise
            cursor.close()

        logging.debug(f"Procedure {proc_name} completed with result: {result}")
        return result

    def fetch_all(self, cursor):
        logging.debug("Fetching all rows from cursor")
        return [dict(zip([column[0] for column in cursor.description], row)) for row in cursor]

    def fetch_single_result(self, cursor):
        logging.debug("Fetching single row from cursor")
        row = cursor.fetchone()
        if not row:
            return None
        columns = [col[0].lower() for col in cursor.description]
        return dict(zip(columns, row))

    def format_dates(self, data):
        logging.debug("Formatting dates in result data")
        for item in data:
            for key, value in item.items():
                if isinstance(value, datetime):
                    item[key] = value.strftime('%Y-%m-%d %H:%M:%S')
        return data

# Dependency to get a DataHelper instance
def get_db():
    return DataHelper._instance

# Ensure the pool is created at startup
async def startup_event():
    await DataHelper().initialize()
