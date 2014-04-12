import MySQLdb as mysql
import pandas as pd
import pandas.io.sql as psql
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from constants import db

def create_connect_by_mysqldb(config):
    return mysql.connect(**db['dev'])


def import_to_db(conn, df):
    try:
        psql.write_frame(df, 'locallists', conn,
                flavor="mysql", if_exists='append', index=None)
        conn.commit()
    finally:
        conn.close()
    print 'mysql done'


if __name__ == '__main__':
    import sys
    input_file = sys.argv[1]
    date = sys.argv[2]

    df = pd.read_csv(input_file)
    df['date'] = date
    df = df.where(pd.notnull(df), None)
    conn = create_connect_by_mysqldb(db['dev'])
    import_to_db(conn, df)
