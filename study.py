import mysql.connector

mydb = mysql.connector.connect(
    host="125.94.240.75",  # 数据库主机地址
    port=8066,
    user="*dw_dingyong2@turnover_test@fix",  # 数据库用户名
    passwd="AMhDwC9xSK41OkLn427gC2MQ",  # 数据库密码
    database="turnover"
)
mycursor = mydb.cursor()

mycursor.execute("SELECT a.id,b.pricing_id FROM tb_to_props_meta a  JOIN tb_to_props_consume_rec b  ON b.prop_id=a.id WHERE a.app_id=2 AND b.currency_type=1 GROUP BY b.prop_id")

myresult = mycursor.fetchall()  # fetchall() 获取所有记录
print(len(myresult))
print(type(myresult))
# for x in myresult:
#     print(x)