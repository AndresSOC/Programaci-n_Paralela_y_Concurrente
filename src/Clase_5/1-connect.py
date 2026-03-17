from sqlalchemy import create_engine,text

user="postgres"
password="1234"
host="localhost"  # or "127.0.0.1"
port="5432"
database="postgres"

def get_connection(user,password,host,port,database):
    return create_engine(
        url="postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}".format(
            user,password,host,port,database
        )
    )

with get_connection( user,password,host,port,database).connect() as connector:
    peticion = connector.execute(text("SELECT * FROM inversiones"))
    print(peticion.fetchall())