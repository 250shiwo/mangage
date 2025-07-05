import pymysql
def connectDB():
    # 打开数据库连接
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='qwywnn',
                         database='bsdb')

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    sql = 'select version();'
    # 使用 execute()  方法执行 SQL 查询
    cursor.execute(sql)
    # 使用 fetchone() 方法获取单条数据.
    result = cursor.fetchone()
    print(result)
    return db
db = connectDB()

from flask import Flask, request, json, jsonify
app = Flask(__name__)
@app.route("/")
def mainIndex():
    return "hello world"

# 用户登录接口
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json(silent=True) or {}
    username = data.get('username') or request.args.get('username')
    password = data.get('password') or request.args.get('password')
    print(username,password)
    cursor = db.cursor()
    sql="""select * from user where username = '%s' and
     password='%s'""" %(username,password)
    cursor.execute(sql)
    row = cursor.fetchone()
    if row:
        print(row)
        return jsonify({"message": "登录成功!", "code": 200, "data": row})
    else:
        return jsonify({"message": "账号或密码错误", "code": 400})
    
if __name__ == '__main__':
    app.run(debug=True)