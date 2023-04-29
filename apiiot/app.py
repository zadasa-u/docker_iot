import asyncio
from fastapi import FastAPI
from sqlalchemy import create_engine, MetaData, select, URL
from sqlalchemy.orm import sessionmaker
import os

app = FastAPI(root_path="/api")
url_object = URL.create(
    "mysql+pymysql",
    username=os.environ["MARIADB_USER"],
    password=os.environ["MARIADB_USER_PASS"],
    host=os.environ["MARIADB_SERVER"],
    database=os.environ["MARIADB_DB"],
)
engine = create_engine(url_object)
Session = sessionmaker(engine)
meta = MetaData()
meta.reflect(bind=engine)
mediciones=meta.tables[os.environ["MARIADB_TABLE"]]

@app.get("/ultimos")
def ultima():
    with Session() as session:
        ultimos = session.execute(select(mediciones).order_by(mediciones.c.id.desc())).first()
        columnas=[c.name for c in mediciones.columns]
        ultimos_zip=zip(columnas,ultimos)
        return ultimos_zip
