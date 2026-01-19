from flask import Flask, Request
# import requests
import psycopg2

app = Flask(__name__)

# # # baw 서버 db
# passwd = '3efe88864056f4a63eeebc8a511d12675ce0c78e998192c9e0ab04438867195d'
# db = psycopg2.connect(host=host, dbname=dbname,user=user,password= passwd,port=5432)
# cur=db.cursor()

# # baw2 서버 db
host = 'ep-square-art-a1z9cevu.ap-southeast-1.pg.koyeb.app'
dbname = 'koyebdb'
user = 'blackwhite2'
passwd = 'npg_0yM9hKGPBlkX'

db = psycopg2.connect(host=host, user=user, password=passwd, dbname=dbname, port=5432)

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