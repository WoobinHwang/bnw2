from flask import Flask, request
# import requests
import psycopg2

app = Flask(__name__)

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

@app.route('/api/hello', methods=['POST'])
def hello():
    body = request.get_json() # 사용자가 입력한 데이터

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": "시작하셔도 됩니다."
                    }
                }
            ]
        }
    }

    return responseBody

# 유저가 입력 한 값 반환
@app.route('/api/test', methods=['POST'])
def test():
    body = request.get_json() # 사용자가 입력한 데이터

    # 입력값 줄바꿈 제거
    body2 = str(body['userRequest']['utterance']).strip() 
    userID = str(body['userRequest']['user']['id'])

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": body2 + "입력완료! \n" + userID
                    }
                }
            ]
        }
    }

    return responseBody




# # 채널 접속
@app.route('/api/enterchannel', methods=['POST'])
def enterchannel():
    db = psycopg2.connect(host=host, dbname=dbname,user=user,password= passwd,port=5432)
    cur=db.cursor()

    try:
        body = request.get_json() # 사용자가 입력한 데이터

        
        id_data = '%s' %str(body['userRequest']['user']['id'])
        idid_data = "'%s'" %str(body['userRequest']['user']['id'])
        try :
            text = body['userRequest']['utterance'].split(" ")[0]
        except :
            text = "korea"
            
        channel_data = '%s' %text
        channelchannel_data = "'%s'" %text
        cur=db.cursor()

        cur.execute("SELECT * FROM blackwhite2 WHERE channel=%s;" % (channelchannel_data))
        rows = cur.fetchall()

        cur.execute("SELECT * FROM blackwhite2 WHERE channel=%s AND userid=%s;" % (channelchannel_data, idid_data))
        rows2 = cur.fetchall()

        cur.execute("SELECT * FROM blackwhite2 WHERE userid=%s;" % (idid_data))
        rows3 = cur.fetchall()

        if len(rows2) != 0:
            result = "해당 채널에 이미 접속중이십니다"
        elif len(rows3) != 0:
            result = "이미 다른 채널에 접속중이십니다"
        elif len(rows) < 2:
            cur.execute("INSERT INTO blackwhite2 (userid, channel, score, turn, numbers, usenum) VALUES (%s, %s, %s, %s, %s, %s);"
                , (id_data, channel_data, 0, 0, 200, 0) )
            db.commit()
            result = "채널에 참가하였습니다"
        else :
            result = "해당 채널에 이미 사람이 다 찼습니다."
    except:
        result = "에러 발생 관리자 문의"

    cur.close() # # cur 객체 연결 해제
    db.close() # # db 인스턴스 연결 해제

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": result
                    }
                }
            ]
        }
    }

    return responseBody


# # 숫자 제출하기
@app.route('/api/submitnumber', methods=['POST'])
def submitnumber():
    db = psycopg2.connect(host=host, dbname=dbname,user=user,password= passwd,port=5432)
    cur=db.cursor()

    try:
    
        body = request.get_json() # 사용자가 입력한 데이터

        id_data = '%s' %str(body['userRequest']['user']['id'])
        idid_data = "'%s'" %str(body['userRequest']['user']['id'])
        round_winner = '%s' %("first")
        round_loser = '%s' %("second")
        where_round_winner = "'%s'" %("first")
        where_round_loser = "'%s'" %("second")


        target_data = body['userRequest']['utterance']

        if (target_data == '발화 내용'):
            text = '0'
        else:
            text = target_data.split(" ")[0]
        
        

        cur.execute("SELECT * FROM blackwhite2 WHERE userid=%s AND turn='0';" % (idid_data))
        find_channel = cur.fetchall()

        userchannel = find_channel[0][1]
        channel_data = '%s' %(userchannel)
        channelchannel_data = "'%s'" %(userchannel)

        cur.execute("SELECT * FROM blackwhite2 WHERE userid=%s AND channel=%s;" % (idid_data, channelchannel_data))
        user_rows = cur.fetchall()

        cur.execute("SELECT * FROM blackwhite2 WHERE userid!=%s AND channel=%s;" % (idid_data, channelchannel_data))
        enemy_rows = cur.fetchall()

        where_user_turn = "'%s'" %(len(user_rows)-1)
        where_enemy_turn = "'%s'" %(len(enemy_rows)-1)

        cur.execute("SELECT * FROM blackwhite2 WHERE userid=%s AND channel=%s AND turn=%s;" % (idid_data, channelchannel_data, where_user_turn))
        user_last_rows = cur.fetchone()

        cur.execute("SELECT * FROM blackwhite2 WHERE userid!=%s AND channel=%s AND turn=%s;" % (idid_data, channelchannel_data, where_enemy_turn))
        enemy_last_rows = cur.fetchone()
        
        # # 이미 10점이면 바로 종료
        if (user_last_rows[2] >= 10) or (enemy_last_rows[2]>=10):
            result = "이미 게임이 끝나있습니다\n'나' %s : %s '상대'"%(user_last_rows[2], enemy_last_rows[2])
        else:
            # # 상대가 없을 때
            if (len(enemy_rows) == 0):
                    result = "상대방이 들어오지 않았습니다."
            # # 보유 포인트보다 더 많이 제출하려고 할 때
            elif (user_last_rows[4]-int(text) < 0) or (int(text) < 0) :
                result = "현재 남은 포인트는 %d개입니다.\n다시 제출하세요." %(user_last_rows[4])

            else:
                # # 숫자 정상적으로 제출
                # # 길이가 같을 때 입력한 사람이 제출
                if(len(user_rows) == len(enemy_rows)) :
                    if (user_last_rows[6] == 'second'):
                        result = "상대방의 차례입니다. 기다려주세요."
                    else:
                        cur.execute("INSERT INTO blackwhite2 (userid, channel, score, turn, numbers, usenum) VALUES (%s, %s, %s, %s, %s, %s);"
                            , (id_data, channel_data, user_last_rows[2], user_last_rows[3] + 1, user_last_rows[4] - int(text), int(text)) )
                        db.commit()
                        result = "%s라운드 제출 완료!" %(user_last_rows[3] + 1)
                elif(len(user_rows) > len(enemy_rows)):
                    result = "상대방이 제출 할 차례입니다."
                elif(len(user_rows) < len(enemy_rows)):
                    
                    
                    # # 양쪽 다 제출했으니 숫자를 비교 할 예정
                    enemy_num = enemy_last_rows[5]
                    user_num = int(text)

                    # # 제출 한 사람이 승리 할 경우
                    if (user_num > enemy_num):
                        # # 유저 승리로 입력
                        cur.execute("INSERT INTO blackwhite2 (userid, channel, score, turn, numbers, usenum, result) VALUES (%s, %s, %s, %s, %s, %s, %s);"
                            , (id_data, channel_data, user_last_rows[2] + 1, user_last_rows[3] + 1, user_last_rows[4] - int(text), int(text), round_winner ))
                        # # 상대 패배로 입력
                        cur.execute("UPDATE blackwhite2 SET result=%s WHERE userid!=%s AND channel=%s AND turn=%s;" % (where_round_loser, idid_data, channelchannel_data, where_enemy_turn))
                        db.commit()
                        result = "%s라운드 제출 완료!\n당신이 승리하였습니다!!!\n현재점수 본인 %s : %s 상대방"%(user_last_rows[3] + 1, user_last_rows[2] + 1, enemy_last_rows[2])
                        if (user_last_rows[2]+1 >= 10):
                            result = result + "\n'나'의 승리로 게임을 종료합니다."

                    # # 상대방이 승리 할 경우
                    elif (user_num < enemy_num):
                        # # 유저 패배로 입력
                        cur.execute("INSERT INTO blackwhite2 (userid, channel, score, turn, numbers, usenum, result) VALUES (%s, %s, %s, %s, %s, %s, %s);"
                            , (id_data, channel_data, user_last_rows[2], user_last_rows[3] + 1, user_last_rows[4] - int(text), int(text), round_loser ))
                        # # # 상대 승리로 입력
                        cur.execute("UPDATE blackwhite2 SET score=%s , result=%s WHERE userid!=%s AND channel=%s AND turn=%s;" % ( enemy_last_rows[2]+1, where_round_winner, idid_data, channelchannel_data, where_enemy_turn))
                        db.commit()
                        result = "%s라운드 제출 완료!\n상대방이 승리하였습니다...\n현재점수 본인 %s : %s 상대방" %(user_last_rows[3] + 1, user_last_rows[2], enemy_last_rows[2]+1)

                        if (enemy_last_rows[2]+1 >= 10):
                            result = result + "\n상대방의 승리로 게임을 종료합니다."


                    # # 무승부인 상황
                    elif (user_num == enemy_num):
                        cur.execute("INSERT INTO blackwhite2 (userid, channel, score, turn, numbers, usenum, result) VALUES (%s, %s, %s, %s, %s, %s, %s);"
                            , (id_data, channel_data, user_last_rows[2], user_last_rows[3] + 1, user_last_rows[4] - int(text), int(text), user_last_rows[6]))
                        # # 상대 무승부 입력
                        where_enemy_result = "'%s'" %(enemy_last_rows[6])
                        cur.execute("UPDATE blackwhite2 SET result=%s WHERE userid!=%s AND channel=%s AND turn=%s;" % (where_enemy_result, idid_data, channelchannel_data, where_enemy_turn))
                        db.commit()
                        result = "무승부입니다!\n선 플레이어부터 다시 시작해주세요.\n현재점수 나 %s : %s 상대방"%(user_last_rows[2], enemy_last_rows[2])
                        # result = "무승부네요??"
    except:
        result = "에러 발생 관리자 문의"
    
    cur.close() # # cur 객체 연결 해제
    db.close() # # db 인스턴스 연결 해제
    

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": result
                    }
                }
            ]
        }
    }

    return responseBody




# # 채널 초기화
@app.route('/api/initializing', methods=['POST'])
def initializing():

    db = psycopg2.connect(host=host, dbname=dbname,user=user,password= passwd,port=5432)
    cur=db.cursor()

    try:
        body = request.get_json() # 사용자가 입력한 데이터

        
        id_data = '%s' %str(body['userRequest']['user']['id'])
        idid_data = "'%s'" %str(body['userRequest']['user']['id'])
        

        cur.execute("DELETE FROM blackwhite2 WHERE userid=%s;" %(idid_data))
        db.commit()
        result = "모든 채널에 있던 데이터들을 삭제하였습니다."
    except:
        result = "에러 발생 관리자 문의"

    cur.close() # # cur 객체 연결 해제
    db.close() # # db 인스턴스 연결 해제
    

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": result
                    }
                }
            ]
        }
    }

    return responseBody


# # 중간에 현재 상황 알림
@app.route('/api/infomation', methods=['POST'])
def infomation():
    db = psycopg2.connect(host=host, dbname=dbname,user=user,password= passwd,port=5432)
    cur=db.cursor()

    try:
        body = request.get_json() # 사용자가 입력한 데이터

        
        id_data = '%s' %str(body['userRequest']['user']['id'])
        idid_data = "'%s'" %str(body['userRequest']['user']['id'])
        
        cur.execute("SELECT * FROM blackwhite2 WHERE userid=%s AND turn='0';" % (idid_data))
        find_channel = cur.fetchall()

        userchannel = find_channel[0][1]
        channelchannel_data = "'%s'" %(userchannel)

        cur.execute("SELECT * FROM blackwhite2 WHERE userid=%s AND channel=%s;" % (idid_data, channelchannel_data))
        user_rows = cur.fetchall()

        cur.execute("SELECT * FROM blackwhite2 WHERE userid!=%s AND channel=%s;" % (idid_data, channelchannel_data))
        enemy_rows = cur.fetchall()

        where_user_turn = "'%s'" %(len(user_rows)-1)
        where_enemy_turn = "'%s'" %(len(enemy_rows)-1)

        cur.execute("SELECT * FROM blackwhite2 WHERE userid=%s AND channel=%s AND turn=%s;" % (idid_data, channelchannel_data, where_user_turn))
        user_last_rows = cur.fetchone()

        cur.execute("SELECT * FROM blackwhite2 WHERE userid!=%s AND channel=%s AND turn=%s;" % (idid_data, channelchannel_data, where_enemy_turn))
        enemy_last_rows = cur.fetchone()

        # # 타일종류
        
        # # 상대 포인트
        num_light = divmod((enemy_last_rows[4]-1), 20)[0] + 1
        first_range = 1 + (num_light-1) * 20
        second_range = 20 + (num_light-1) * 20
        if (num_light <= 1):
            num_light = 1
            first_range = 0
            second_range = 20
        # # 서로 제출을 안 한 상태에서
        # # 가지고있는 포인트, 점수

        result = "점수\n'나' %s : %s '상대'\n내가 가진 포인트량: %s\n상대가 가진 포인트량: %s번째 전등에 불이 켜져있으며\n%s ~ %s 의 범위에 해당합니다" %(user_last_rows[2], enemy_last_rows[2], user_last_rows[4], num_light, first_range, second_range)
        if (len(user_rows) > len(enemy_rows)):

            if(user_last_rows[5] >= 10):
                tile = "흰색"
            else:
                tile = "검은색"
            result = result + "\n'나'는 %s 타일을 제출하였습니다" %(tile)

        elif (len(user_rows) < len(enemy_rows)):
            if(enemy_last_rows[5] >= 10):
                tile = "흰색"
            else:
                tile = "검은색"
            result = result + "\n'상대'는 %s 타일을 제출하였습니다" %(tile)
    except:
        result = "에러 발생 관리자 문의"

    cur.close() # # cur 객체 연결 해제
    db.close() # # db 인스턴스 연결 해제

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": result
                    }
                }
            ]
        }
    }

    return responseBody




# # 지난 결과 호출
@app.route('/api/previous', methods=['POST'])
def previous():
    db = psycopg2.connect(host=host, dbname=dbname,user=user,password= passwd,port=5432)
    cur=db.cursor()

    try:
    
        body = request.get_json() # 사용자가 입력한 데이터

        
        id_data = '%s' %str(body['userRequest']['user']['id'])
        idid_data = "'%s'" %str(body['userRequest']['user']['id'])
        
        cur.execute("SELECT * FROM blackwhite2 WHERE userid=%s AND turn='0';" % (idid_data))
        find_channel = cur.fetchall()

        userchannel = find_channel[0][1]
        channelchannel_data = "'%s'" %(userchannel)

        cur.execute("SELECT * FROM blackwhite2 WHERE userid=%s AND channel=%s;" % (idid_data, channelchannel_data))
        user_rows = cur.fetchall()

        cur.execute("SELECT * FROM blackwhite2 WHERE userid!=%s AND channel=%s;" % (idid_data, channelchannel_data))
        enemy_rows = cur.fetchall()

        where_user_turn = "'%s'" %(len(user_rows)-1)
        where_enemy_turn = "'%s'" %(len(enemy_rows)-1)

        cur.execute("SELECT * FROM blackwhite2 WHERE userid=%s AND channel=%s AND turn=%s;" % (idid_data, channelchannel_data, where_user_turn))
        user_last_rows = cur.fetchone()

        cur.execute("SELECT * FROM blackwhite2 WHERE userid!=%s AND channel=%s AND turn=%s;" % (idid_data, channelchannel_data, where_enemy_turn))
        enemy_last_rows = cur.fetchone()

        # # 상대 타일 정의
        if(enemy_last_rows[5] >= 10):
            tile = "흰색"
        else:
            tile = "검은색"


        if (len(user_rows) == 1) or (len(enemy_rows) == 1) :
            result = "이전 라운드가 없습니다."
        elif (len(user_rows) == len(enemy_rows)) :
            result = "현재 %s라운드 진행중이며\n지난 라운드에 상대방이 %s 타일을 제출하여 " %(len(user_rows), tile)
            if (user_last_rows[5] > enemy_last_rows[5]):
                result = result + "내가 이겼습니다."
            elif (user_last_rows[5] == enemy_last_rows[5]):
                result = result + "비겼습니다."
            elif (user_last_rows[5] < enemy_last_rows[5]):
                result = result + "상대가 이겼습니다."

        # # 유저가 3 , 상대가 2의 상황
        elif (len(user_rows) > len(enemy_rows)) :

            where_user_prev_turn = "'%s'" %(len(user_rows)-2)

            cur.execute("SELECT * FROM blackwhite2 WHERE userid=%s AND channel=%s AND turn=%s;" % (idid_data, channelchannel_data, where_user_prev_turn))
            user_previous_rows = cur.fetchone()
            
            result = "현재 %s라운드 진행중이며\n지난 %s라운드에 상대방이 %s 타일을 제출하여 " %(len(user_rows)-1, len(enemy_rows)-1, tile)
            
            if (user_previous_rows[5] > enemy_last_rows[5]):
                result = result + "내가 이겼습니다."
            elif (user_previous_rows[5] == enemy_last_rows[5]):
                result = result + "비겼습니다."
            elif (user_previous_rows[5] < enemy_last_rows[5]):
                result = result + "상대가 이겼습니다."


            # # 유저가 2 , 상대가 3의 상황
        elif (len(user_rows) < len(enemy_rows)) :

            where_enemy_prev_turn = "'%s'" %(len(enemy_rows)-2)

            cur.execute("SELECT * FROM blackwhite2 WHERE userid!=%s AND channel=%s AND turn=%s;" % (idid_data, channelchannel_data, where_enemy_prev_turn))
            enemy_previous_rows = cur.fetchone()

            # # 상대 타일 재정의
            if(enemy_previous_rows[5] >= 10):
                tile = "흰색"
            else:
                tile = "검은색"
            
            result = "현재 %s라운드 진행중이며\n지난 %s라운드에 상대방이 %s 타일을 제출하여 " %(len(enemy_rows)-1, len(user_rows)-1, tile)
            
            if (user_last_rows[5] > enemy_previous_rows[5]):
                result = result + "내가 이겼습니다."
            elif (user_last_rows[5] == enemy_previous_rows[5]):
                result = result + "비겼습니다."
            elif (user_last_rows[5] < enemy_previous_rows[5]):
                result = result + "상대가 이겼습니다."

        # # 결과에 점수 추가하여 마무리
        result = result + "\n현재 점수\n'나' %s : %s '상대'" %(user_last_rows[2], enemy_last_rows[2])
    except:
        result = "에러 발생 관리자 문의"

    cur.close() # # cur 객체 연결 해제
    db.close() # # db 인스턴스 연결 해제

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": result
                    }
                }
            ]
        }
    }

    return responseBody




# # 다 끝난 후 로그 보여주기
@app.route('/api/checklog', methods=['POST'])
def checklog():
    db = psycopg2.connect(host=host, dbname=dbname,user=user,password= passwd,port=5432)
    cur=db.cursor()

    try:
        body = request.get_json() # 사용자가 입력한 데이터

        idid_data = "'%s'" %str(body['userRequest']['user']['id'])
        
        cur.execute("SELECT * FROM blackwhite2 WHERE userid=%s AND turn='0';" % (idid_data))
        find_channel = cur.fetchall()

        userchannel = find_channel[0][1]
        channelchannel_data = "'%s'" %(userchannel)

        cur.execute("SELECT * FROM blackwhite2 WHERE userid=%s AND channel=%s;" % (idid_data, channelchannel_data))
        user_rows = cur.fetchall()

        cur.execute("SELECT * FROM blackwhite2 WHERE userid!=%s AND channel=%s;" % (idid_data, channelchannel_data))
        enemy_rows = cur.fetchall()
        result = ""

        ###
        where_user_turn = "'%s'" %(len(user_rows)-1)
        where_enemy_turn = "'%s'" %(len(enemy_rows)-1)

        cur.execute("SELECT * FROM blackwhite2 WHERE userid=%s AND channel=%s AND turn=%s;" % (idid_data, channelchannel_data, where_user_turn))
        user_last_rows = cur.fetchone()

        cur.execute("SELECT * FROM blackwhite2 WHERE userid!=%s AND channel=%s AND turn=%s;" % (idid_data, channelchannel_data, where_enemy_turn))
        enemy_last_rows = cur.fetchone()
        
        # # 타겟지점
        if (user_last_rows[2] >= 10) or (enemy_last_rows[2]>=10):
            result = result + "로그보기"
            for i in range(1, len(user_rows)):

                where_user_turn = "'%s'" %(i)
                where_enemy_turn = "'%s'" %(i)

                cur.execute("SELECT * FROM blackwhite2 WHERE userid=%s AND channel=%s AND turn=%s;" % (idid_data, channelchannel_data, where_user_turn))
                user_target_row = cur.fetchone()
                cur.execute("SELECT * FROM blackwhite2 WHERE userid!=%s AND channel=%s AND turn=%s;" % (idid_data, channelchannel_data, where_enemy_turn))
                enemy_target_row = cur.fetchone()

                result = result + "\n%d라운드 나 %s : %s 상대" %(i, user_target_row[5], enemy_target_row[5])
                
        else:
            result = "아직 게임이 끝나지 않았습니다.\n게임이 끝난후에 이용하시기 바랍니다."

    except:
        result = result + "에러 발생 관리자 문의"

    cur.close() # # cur 객체 연결 해제
    db.close() # # db 인스턴스 연결 해제

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": result
                    }
                }
            ]
        }
    }

    return responseBody

# 기권하기
@app.route('/api/giveup', methods=['POST'])
def giveup():

    cur=db.cursor()

    try:
        body = request.get_json() # 사용자가 입력한 데이터
        idid_data = "'%s'" %str(body['userRequest']['user']['id'])


        cur.execute("SELECT * FROM blackwhite2 WHERE userid=%s AND turn='0';" % (idid_data))
        find_channel = cur.fetchall()

        userchannel = find_channel[0][1]
        channelchannel_data = "'%s'" %(userchannel)


        cur.execute("SELECT * FROM blackwhite2 WHERE userid!=%s AND channel=%s;" % (idid_data, channelchannel_data))
        enemy_rows = cur.fetchall()

        where_enemy_turn = "'%s'" %(len(enemy_rows)-1)

        cur.execute("UPDATE blackwhite2 SET score=%s WHERE userid!=%s AND channel=%s AND turn=%s;" % ( 10, idid_data, channelchannel_data, where_enemy_turn))
        db.commit()
        result = "항복하였습니다"

    except:
        result = "에러 발생 관리자 문의"

    cur.close() # # cur 객체 연결 해제
    db.close() # # db 인스턴스 연결 해제

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": result
                    }
                }
            ]
        }
    }

    return responseBody

 
if __name__ == "__main__":
    app.run()