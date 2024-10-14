import pyodbc as odb
from fastapi import FastAPI
from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List
from fastapi.middleware.cors import CORSMiddleware



# إعدادات الاتصال
class DatabaseConfig:
    database = 'Bank_Company'
    username = 'mohamed'
    password = '125630'
    server = '127.0.0.1\\sqlexpress'

# نموذج البيانات
class Record(BaseModel):
    ID: int
    Amount: float
    Date: Optional[datetime]
    No_recipt: int
    Note: Optional[str]
    Name: str
    Due_Date: Optional[datetime]
    No_check: Optional[datetime]
    Company: Optional[str]
    Bank_name: str
    Period_date: Optional[datetime]
    Enable: Optional[bool]
    Receipt_it_Date: Optional[datetime]
    Receipt_it_No: Optional[int]
    Deferred_to: Optional[datetime]
    Check_out: Optional[datetime]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # يمكنك تحديد المواقع المسموح بها
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)
# دالة للاتصال بقاعدة البيانات
def get_connection():
    conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={DatabaseConfig.server};DATABASE={DatabaseConfig.database};UID={DatabaseConfig.username};PWD={DatabaseConfig.password}'
    return odb.connect(conn_str)

app.get('/hi')
def sayhi():
    return ("hi")

# دالة لاسترجاع السجلات
@app.get('/record', response_model=List[Record])
async def read_records():
    try:
        with get_connection() as cnxn:
            cursor = cnxn.cursor()
            query = "SELECT * FROM Tab_BankTransactions"
            rows = cursor.execute(query).fetchall()
        
        # تحويل الصفوف إلى نموذج Record
        records = [
            Record(
                ID=row[0],
                Amount=row[1],
                Date=row[2],
                No_recipt=row[3],
                Note=row[4],
                Name=row[5],
                Due_Date=row[6],
                No_check=row[7],
                Company=row[8],
                Bank_name=row[9],
                Period_date=row[10],
                Enable=row[11],
                Receipt_it_Date=row[12],
                Receipt_it_No=row[13],
                Deferred_to=row[14],
                Check_out=row[15]
            ) for row in rows
        ]
        
        return records

    except odb.Error as e:
        return {"error": str(e)}

