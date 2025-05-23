import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mssql://Adminbd:Admin123*@serversqlazureag.database.windows.net:1433/PeliculasFlask?driver=ODBC+Driver+18+for+SQL+Server&Encrypt=yes'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
