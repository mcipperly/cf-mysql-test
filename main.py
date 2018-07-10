import json
import os
import datetime
import platform

import pymysql.cursors
from flask import Flask, request
from werkzeug.utils import secure_filename


app = Flask(__name__)


def connect_mysql():
    if os.getenv("VCAP_SERVICES"):
        csql = json.loads(os.getenv("VCAP_SERVICES"))
        print(json.dumps(csql))
        conn = pymysql.connect(host=csql["p.mysql"][0]["credentials"]["hostname"],
                               user=csql["p.mysql"][0]["credentials"]["username"],
                               password=csql["p.mysql"][0]["credentials"]["password"],
                               db=csql["p.mysql"][0]["credentials"]["name"],
                               cursorclass=pymysql.cursors.DictCursor)
    return(conn)


def dtSerializer(obj):
    if isinstance(obj, datetime.datetime):
        return(obj.isoformat())
    else:
        TypeError("Unknown serializer")


@app.before_first_request
def init_mysql():
    try:
        conn = connect_mysql()
        cursor = conn.cursor()
        sql = ("CREATE TABLE IF NOT EXISTS test_table ("
               "id INT AUTO_INCREMENT PRIMARY KEY, "
               "time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, "
               "nodename VARCHAR(255), query_string TEXT);")
        cursor.execute(sql)
    except Exception as e:
        print("Couldn't connect to MySQL: {}".format(str(e)))


@app.route('/health-check', methods=['GET'])
def health_check():
    return("OK")


@app.route('/', methods=['GET'])
def tester_app():
    try:
        conn.open
    except Exception as e:
        conn = connect_mysql()
    cursor = conn.cursor()
    sql = ("INSERT INTO test_table (nodename, query_string) VALUES "
           "('{}','{}');").format(platform.node(),
                                  json.dumps(request.args))
    cursor.execute(sql)
    conn.commit()
    sql = "SELECT * FROM test_table;"
    cursor.execute(sql)
    result = cursor.fetchall()
    return(("<html><body><pre>MySQL connection succeeded!" 
            "{}</pre></body></html>").format(json.dumps(result,
                                                        default=dtSerializer,
                                                        sort_keys=True,
                                                        indent=4)))


if __name__ == '__main__':
    app.run('0.0.0.0', port='7070')
