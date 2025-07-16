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
    sql="""select id,username,email,role_id,ip from %s where username = '%s' and
     password='%s'""" %(tablename,username,password)
    cursor.execute(sql)
    row = cursor.fetchone()
    columns = ['id', 'username','email','role_id','ip']
    users = [dict(zip(columns, row))]
    if row:
        print(row)
        return jsonify({"message": "登录成功!", "code": '200', "data": users})
    else:
        return jsonify({"message": "账号或密码错误", "code": '400'})

# 修改学生信息接口
@app.route('/students/update', methods=['PUT','POST'])
def updateStudent():
    data = request.get_json(silent=True) or {}
    id = data.get('id') or request.args.get('id')
    if not id:
        return jsonify({'code': 400, 'message': '缺少学生 ID 参数'})
    name = data.get('name')or request.args.get('name')
    username = data.get('username')or request.args.get('username')
    sex = data.get('sex')or request.args.get('sex')
    email = data.get('email')or request.args.get('email')
    phone = data.get('phone')or request.args.get('phone')
    student_id = data.get('student_id')or request.args.get('student_id')
    college_id = data.get('college_id')or request.args.get('college_id')
    speciality_id = data.get('speciality_id')or request.args.get('speciality_id')
    
    update_fields = []
    values = []
    if name:
        update_fields.append('name = %s')
        values.append(name)
    if username:
        update_fields.append('username = %s')
        values.append(username)
    if sex:
        update_fields.append('sex = %s')
        values.append(sex)
    if email:
        update_fields.append('email = %s')
        values.append(email)
    if phone:
        update_fields.append('phone = %s')
        values.append(phone)
    if student_id:
        update_fields.append('student_id = %s')
        values.append(student_id)
    if college_id:
        update_fields.append('college_id = %s')
        values.append(college_id)
    if speciality_id:
        update_fields.append('speciality_id = %s')
        values.append(speciality_id)
    
    if not update_fields:
        return jsonify({'code': '400', 'message': '未提供需要修改的学生信息'})
    
    values.append(id)
    sql = 'UPDATE student SET ' + ', '.join(update_fields) + ' WHERE id = %s'
    try:
        cursor = db.cursor()
        cursor.execute(sql, values)
        if cursor.rowcount == 0:
            return jsonify({'code': '404', 'message': '未找到对应学生'})
        db.commit()
        return jsonify({'code': '200', 'message': '学生修改成功'})
    except Exception as e:
        db.rollback()
        return jsonify({'code': '400', 'message': str(e)})

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
    username = data.get('params', {}).get('username') or request.args.get('username')
    phone = data.get('params', {}).get('phone') or request.args.get('phone')
    student_id = data.get('params', {}).get('student_id') or request.args.get('student_id')
    offset = (pageNum - 1) * pageSize
    cursor = db.cursor()
    try:
        # 查询总数
        count_sql = "SELECT COUNT(*) FROM student WHERE 1=1"
        params = []
        if username:
            count_sql += " AND username LIKE CONCAT('%%', %s, '%%')"
            params.append(username)
        if phone:
            count_sql += " AND phone LIKE CONCAT('%%', %s, '%%')"
            params.append(phone)
        if student_id:
            count_sql += " AND student_id LIKE CONCAT('%%', %s, '%%')"
            params.append(student_id)
        cursor.execute(count_sql, params)
        total = int(cursor.fetchone()[0])
        # 查询分页数据
        sql = "SELECT id,name,username,sex,email,phone,student_id,college_id,speciality_id FROM student WHERE 1=1"
        if username:
            sql += " AND username LIKE CONCAT('%%', %s, '%%')"
        if phone:
            sql += " AND phone LIKE CONCAT('%%', %s, '%%')"
        if student_id:
            sql += " AND student_id LIKE CONCAT('%%', %s, '%%')"
        sql += " LIMIT %s OFFSET %s"
        pagination_params = params + [pageSize, offset]
        cursor.execute(sql, pagination_params)
        results = cursor.fetchall()
        columns = ['id', 'name', 'username', 'sex', 'email', 'phone', 'student_id', 'college_id', 'speciality_id']
        students = [dict(zip(columns, row)) for row in results]
        return jsonify({'code': '200', 'message': '分页查询成功', 'data': students, 'total': total})
    except Exception as e:
        db.rollback()
        return jsonify({'code': '400', 'message': str(e)})

# 学生数据保存接口
@app.route('/students/save', methods=['POST'])
def saveStudent():
    data = request.get_json(silent=True) or {}
    name = data.get('name') or request.args.get('name')
    username = data.get('username') or request.args.get('username')
    sex = data.get('sex') or request.args.get('sex')
    email = data.get('email') or request.args.get('email')
    phone = data.get('phone') or request.args.get('phone')
    student_id = data.get('student_id') or request.args.get('student_id')
    college_id = data.get('college_id') or request.args.get('college_id')
    speciality_id = data.get('speciality_id') or request.args.get('speciality_id')
    
    if not all([username, sex, email, phone, student_id, college_id, speciality_id]):
        return jsonify({'code': '400', 'message': '缺少必要参数'})
    
    cursor = db.cursor()
    try:
        sql = "INSERT INTO student (name,username, sex, email, phone, student_id, college_id, speciality_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (name,username, sex, email, phone, student_id, college_id, speciality_id))
        db.commit()
        return jsonify({'code': '200', 'message': '数据添加成功'})
    except Exception as e:
        db.rollback()
        return jsonify({'code': '400', 'message': str(e)})

# 学生数据删除接口
@app.route('/students/delete', methods=['DELETE'])
def deleteStudent():
    data = request.get_json(silent=True) or {}
    id = data.get('id') or request.args.get('id')
    if not id:
        return jsonify({'code': 400, 'message': '缺少必要参数 id'})
    cursor = db.cursor()
    try:
        sql = "DELETE FROM student WHERE id = %s"
        cursor.execute(sql, (id,))
        if cursor.rowcount == 0:
            return jsonify({'code': 404, 'message': '未找到对应的学生记录'})
        db.commit()
        return jsonify({'code': 200, 'message': '学生数据删除成功'})
    except Exception as e:
        db.rollback()
        return jsonify({'code': 400, 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)