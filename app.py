from flask import Flask, Request
# import requests
import psycopg2

app = Flask(__name__)

# # # baw 서버 db
# passwd = '3efe88864056f4a63eeebc8a511d12675ce0c78e998192c9e0ab04438867195d'
# db = psycopg2.connect(host=host, dbname=dbname,user=user,password= passwd,port=5432)
# cur=db.cursor()

# # baw2 서버 db
host = 'ep-square-hat-ahdj2h0r.c-3.us-east-1.pg.koyeb.app'
dbname = 'koyebdb'
user = 'black_and_white_2'
passwd = 'npg_V9smkvLSd0CJ'

# db = psycopg2.connect(host=host, user=user, password=passwd, dbname=dbname, port=5432)
db = psycopg2.connect(
    host="ep-square-hat-ahdj2h0r.c-3.us-east-1.pg.koyeb.app",
    dbname="koyebdb",
    user="black_and_white_2",
    password="npg_V9smkvLSd0CJ",
    port=5432,
    sslmode="require",
    options="-c endpoint=ep-square-hat-ahdj2h0r"
)
cur=db.cursor()

@app.route('/')
def hello_world():
    return 'welcome woobs!?'


# @app.route('/api/hello', methods=['POST'])
# def hello():
#     body = Request.get_json() # 사용자가 입력한 데이터

#     responseBody = {
#         "version": "2.0",
#         "template": {
#             "outputs": [
#                 {
#                     "simpleText": {
#                         "text": "시작하셔도 됩니다."
#                     }
#                 }
#             ]
#         }
#     }

#     return responseBody



 
if __name__ == "__main__":
    app.run()