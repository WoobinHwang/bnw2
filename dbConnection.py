import psycopg2

# # baw2 서버 db
host = 'ep-square-art-a1z9cevu.ap-southeast-1.pg.koyeb.app'
dbname = 'koyebdb'
user = 'blackwhite2'
passwd = 'npg_0yM9hKGPBlkX'

db = psycopg2.connect(host=host, user=user, password=passwd, dbname=dbname, port=5432)

cur=db.cursor()

## table information ##
# 테이블명 : blackwhite2
# 컬럼 : userid, channel, score, turn, numbers, usenum, result

id_data = '%s' %("woobin")
idid_data = "'%s'" %("woobin")
channel_data = '%s' %("korea")
channelchannel_data = "'%s'" %("korea")
where_user_turn = 0
text = '2'



# drop ##
# cur.execute("DROP TABLE blackwhite2")

# create ##
# cur.execute("CREATE TABLE IF NOT EXISTS blackwhite2 (userid varchar, channel varchar, score int, turn int, numbers int, usenum int, result varchar);")

## select ##
    # cur.execute("SELECT * FROM blackwhite2 WHERE userid=%s AND channel=%s AND turn=%s;" % (idid_data, channelchannel_data, where_user_turn))
    # user_last_rows = cur.fetchone()
    # print(user_last_rows)

## insert ##
# cur.execute("INSERT INTO blackwhite2 (userid, channel, score, turn, numbers, usenum, result) VALUES (%s, %s, %s, %s, %s, %s, %s);"
#     , (id_data, channel_data, user_last_rows[2], user_last_rows[3] + 1, user_last_rows[4] - int(text), int(text), user_last_rows[6]))




# cur.execute("INSERT INTO blackwhite2 (userid, channel, score, turn, numbers, usenum, result) VALUES (%s, %s, %s, %s, %s, %s, %s);"
#     , (id_data, channel_data, 0, 1, 190, 10, "first"))

    # cur.execute("SELECT * FROM blackwhite2 WHERE userid=%s AND channel=%s AND turn=%s;" % (idid_data, channelchannel_data, where_user_turn+1))
    # user_last_rows = cur.fetchone()
    # print(user_last_rows)
    # db.commit()

cur.execute("SELECT * FROM blackwhite2")
all_rows = cur.fetchall()
print(all_rows)

# # 상대 무승부 입력
# cur.execute("UPDATE blackwhite2 SET result=%s WHERE userid!=%s AND channel=%s AND turn=%s;" % (where_round_draw, idid_data, channelchannel_data, where_enemy_turn))

db.commit();
print("good!")