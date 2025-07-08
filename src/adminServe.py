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
    radio = data.get('radio') or request.args.get('radio')
    username = data.get('username') or request.args.get('username')
    password = data.get('password') or request.args.get('password')
    tablename= 'user'
    if radio == 1:
        tablename = 'user'
    elif radio == 2:
        tablename = 'counsellor'
    else:
        tablename = 'student'
    print(username,password,radio)
    cursor = db.cursor()
    sql="""select * from %s where username = '%s' and
     password='%s'""" %(tablename,username,password)
    cursor.execute(sql)
    row = cursor.fetchone()
    if row:
        print(row)
        return jsonify({"message": "登录成功!", "code": 200, "data": row})
    else:
        return jsonify({"message": "账号或密码错误", "code": 400})
# 学生查询接口
@app.route('/students', methods=['POST', 'GET'])
def queryStudents():
    cursor = db.cursor()
    try:
        sql = "SELECT id,username,sex,email,phone,student_id,college_id,speciality_id FROM student"
        cursor.execute(sql)
        results = cursor.fetchall()
        columns = ['id', 'username', 'sex', 'email', 'phone','student_id','college_id','speciality_id']
        students = [dict(zip(columns, row)) for row in results]
        return jsonify({'code': '200', 'message': '查询成功', 'data': students})
    except Exception as e:
        db.rollback()
        return jsonify({'code': '400', 'message': str(e)})
    
# 学生分页查询接口
@app.route('/students/paginated', methods=['POST', 'GET'])
def queryStudentsPaginated():
    data = request.get_json(silent=True) or {}
    pageNum = int(data.get('pageNum') or request.args.get('pageNum'))
    pageSize = int(data.get('pageSize') or request.args.get('pageSize'))
    offset = (pageNum - 1) * pageSize
    cursor = db.cursor()
    try:
        # 查询总数
        count_sql = "SELECT COUNT(*) FROM student"
        cursor.execute(count_sql)
        total = int(cursor.fetchone()[0])
        # 查询分页数据
        sql = "SELECT id,username,sex,email,phone,student_id,college_id,speciality_id FROM student LIMIT %s OFFSET %s"
        cursor.execute(sql, (pageSize, offset))
        results = cursor.fetchall()
        columns = ['id', 'username', 'sex', 'email', 'phone','student_id','college_id','speciality_id']
        students = [dict(zip(columns, row)) for row in results]
        
        return jsonify({'code': '200', 'message': '分页查询成功', 'data': students, 'total': total})
    except Exception as e:
        db.rollback()
        return jsonify({'code': '400', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)