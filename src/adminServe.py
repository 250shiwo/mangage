import pymysql
import threading
lock = threading.Lock()
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
    radio = int(data.get('radio') or request.args.get('radio'))
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
    try:
        cursor.execute(sql)
        row = cursor.fetchone()
        if row:
            print(row)
            columns = ['id', 'username','email','role_id','ip']
            users_info = dict(zip(columns, row))
            role_id = str(users_info['role_id'])
            #根据 role_id 查询菜单数据
            menu_sql = "SELECT * FROM menu WHERE FIND_IN_SET(%s, menuRight)"
            cursor.execute(menu_sql, (role_id,))
            menu_columns = ['id', 'menuCode', 'menuName', 'menuLevel', 'menuParentCode', 'menuClick', 'menuRight', 'menuComponent', 'menuIcon']
            menu_rows = cursor.fetchall()
            menus = [dict(zip(menu_columns, row)) for row in menu_rows]
            users_info['menus'] = menus
            return jsonify({"message": "登录成功!", "code": '200', "data": users_info})
        else:
            return jsonify({"message": "账号或密码错误", "code": '400'})
    except Exception as e:
        db.rollback()
        return jsonify({"message": "登录出错: " + str(e), "code": '400'})

# 专业数据保存接口
@app.route('/api/speciality/save', methods=['POST'])
def saveSpeciality():
    data = request.get_json(silent=True) or {}
    speciality_id = data.get('speciality_id') or request.args.get('speciality_id')
    speciality_name = data.get('speciality_name') or request.args.get('speciality_name')
    college_id = data.get('college_id') or request.args.get('college_id')
    if not all([speciality_id,speciality_name,college_id]):
        return jsonify({'code': '400', 'message': '缺少必要参数'})
    
    cursor = db.cursor()
    try:
        sql = "INSERT INTO speciality (speciality_id,speciality_name,college_id) VALUES (%s, %s,%s)"
        cursor.execute(sql, (speciality_id,speciality_name,college_id))
        db.commit()
        return jsonify({'code': '200', 'message': '数据添加成功'})
    except Exception as e:
        db.rollback()
        return jsonify({'code': '400', 'message': '数据添加失败: ' + str(e)})

# 专业数据删除接口
@app.route('/api/speciality/delete', methods=['DELETE'])
def deleteSpeciality():
    data = request.get_json(silent=True) or {}
    id = data.get('id') or request.args.get('id')
    if not id:
        return jsonify({'code': 400, 'message': '缺少必要参数 id'})
    cursor = db.cursor()
    try:
        sql = "DELETE FROM speciality WHERE id = %s"
        lock.acquire()
        cursor.execute(sql, id)
        lock.release()
        if cursor.rowcount == 0:
            return jsonify({'code': 404, 'message': '未找到对应的专业记录'})
        lock.acquire()
        db.commit()
        lock.release()
        return jsonify({'code': 200, 'message': '专业数据删除成功'})
    except Exception as e:
        lock.acquire()
        db.rollback()
        lock.release()
        return jsonify({'code': 400, 'message': '专业数据删除失败: ' + str(e)})

# 修改专业信息接口
@app.route('/api/speciality/update', methods=['PUT','POST'])
def updateSpeciality():
    data = request.get_json(silent=True) or {}
    id = data.get('id') or request.args.get('id')
    if not id:
        return jsonify({'code': 400, 'message': '缺少专业 ID 参数'})
    speciality_name = data.get('speciality_name')or request.args.get('speciality_name')
    speciality_id = data.get('speciality_id')or request.args.get('speciality_id')
    college_id = data.get('college_id')or request.args.get('college_id')
    update_fields = []
    values = []
    if speciality_name:
        update_fields.append('speciality_name = %s')
        values.append(speciality_name)
    if speciality_id:
        update_fields.append('speciality_id = %s')
        values.append(speciality_id)
    if college_id:
        update_fields.append('college_id = %s')
        values.append(college_id)
    if not update_fields:
        return jsonify({'code': '400', 'message': '未提供需要修改的专业信息'})
    
    values.append(id)
    sql = 'UPDATE speciality SET ' + ', '.join(update_fields) + ' WHERE id = %s'
    try:
        cursor = db.cursor()
        cursor.execute(sql, values)
        if cursor.rowcount == 0:
            return jsonify({'code': '404', 'message': '未找到对应专业'})
        db.commit()
        return jsonify({'code': '200', 'message': '专业修改成功'})
    except Exception as e:
        db.rollback()
        return jsonify({'code': '400', 'message': str(e)})

# 专业查询接口
@app.route('/api/speciality', methods=['POST', 'GET'])
def querySpeciality():
    cursor = db.cursor()
    try:
        sql = "SELECT id,speciality_name,speciality_id,college_id FROM speciality"
        lock.acquire()
        cursor.execute(sql)
        lock.release()
        results = cursor.fetchall()
        columns = ['id', 'speciality_name','speciality_id','college_id']
        specialitys = [dict(zip(columns, row)) for row in results]
        return jsonify({'code': '200', 'message': '查询成功', 'data': specialitys})
    except Exception as e:
        db.rollback()
        return jsonify({'code': '400', 'message': str(e)})

# 专业分页查询接口
@app.route('/api/speciality/paginated', methods=['POST', 'GET'])
def querySpecialityPaginated():
    data = request.get_json(silent=True) or {}
    pageNum = int(data.get('pageNum') or request.args.get('pageNum'))
    pageSize = int(data.get('pageSize') or request.args.get('pageSize'))
    speciality_id = data.get('params', {}).get('speciality_id') or request.args.get('speciality_id')
    speciality_name = data.get('params', {}).get('speciality_name') or request.args.get('speciality_name')
    college_id = data.get('params', {}).get('college_id') or request.args.get('college_id')
    offset = (pageNum - 1) * pageSize
    cursor = db.cursor()
    try:
        # 查询总数
        count_sql = "SELECT COUNT(*) FROM speciality WHERE 1=1"
        params = []
        if speciality_id:
            count_sql += " AND speciality_id LIKE CONCAT('%%', %s, '%%')"
            params.append(speciality_id)
        if speciality_name:
            count_sql += " AND speciality_name LIKE CONCAT('%%', %s, '%%')"
            params.append(speciality_name)
        if college_id:
            count_sql += " AND college_id LIKE CONCAT('%%', %s, '%%')"
            params.append(college_id)
        lock.acquire()
        cursor.execute(count_sql, params)
        total = int(cursor.fetchone()[0])
        lock.release()
        # 查询分页数据
        sql = "SELECT id,speciality_id,speciality_name,college_id FROM speciality WHERE 1=1"
        if speciality_id:
            sql += " AND speciality_id LIKE CONCAT('%%', %s, '%%')"
        if speciality_name:
            sql += " AND speciality_name LIKE CONCAT('%%', %s, '%%')"
        if college_id:
            sql += " AND college_id LIKE CONCAT('%%', %s, '%%')"
        sql += " LIMIT %s OFFSET %s"
        pagination_params = params + [pageSize, offset]
        lock.acquire()
        cursor.execute(sql, pagination_params)
        lock.release()
        results = cursor.fetchall()
        columns = ['id', 'speciality_id', 'speciality_name','college_id']
        specialities = [dict(zip(columns, row)) for row in results]
        return jsonify({'code': '200', 'message': '分页查询成功', 'data': specialities, 'total': total})
    except Exception as e:
        lock.acquire()
        db.rollback()
        lock.release()
        return jsonify({'code': '400', 'message': str(e)})

# 学院查询接口
@app.route('/api/college', methods=['POST', 'GET'])
def queryCollege():
    cursor = db.cursor()
    try:
        sql = "SELECT id,college_id,college_name FROM college"
        lock.acquire()
        cursor.execute(sql)
        lock.release()
        results = cursor.fetchall()
        columns = ['id', 'college_id', 'college_name']
        colleges = [dict(zip(columns, row)) for row in results]
        return jsonify({'code': '200', 'message': '查询成功', 'data': colleges})
    except Exception as e:
        db.rollback()
        return jsonify({'code': '400', 'message': str(e)})

# 学院数据保存接口
@app.route('/api/college/save', methods=['POST'])
def saveCollege():
    data = request.get_json(silent=True) or {}
    college_id = data.get('college_id') or request.args.get('college_id')
    college_name = data.get('college_name') or request.args.get('college_name')
    if not all([college_id,college_name]):
        return jsonify({'code': '400', 'message': '缺少必要参数'})
    
    cursor = db.cursor()
    try:
        sql = "INSERT INTO college (college_id,college_name) VALUES (%s, %s)"
        lock.acquire()
        cursor.execute(sql, (college_id,college_name))
        lock.release()
        db.commit()
        return jsonify({'code': '200', 'message': '数据添加成功'})
    except Exception as e:
        db.rollback()
        return jsonify({'code': '400', 'message': '数据添加失败: ' + str(e)})

# 学院数据删除接口
@app.route('/api/college/delete', methods=['DELETE'])
def deleteCollege():
    data = request.get_json(silent=True) or {}
    id = data.get('id') or request.args.get('id')
    if not id:
        return jsonify({'code': 400, 'message': '缺少必要参数 id'})
    cursor = db.cursor()
    try:
        sql = "DELETE FROM college WHERE id = %s"
        lock.acquire()
        cursor.execute(sql, id)
        lock.release()
        if cursor.rowcount == 0:
            return jsonify({'code': 404, 'message': '未找到对应的学院记录'})
        lock.acquire()
        db.commit()
        lock.release()
        return jsonify({'code': 200, 'message': '学院数据删除成功'})
    except Exception as e:
        db.rollback()
        return jsonify({'code': 400, 'message': '学院数据删除失败: ' + str(e)})

# 修改学院信息接口
@app.route('/api/college/update', methods=['PUT','POST'])
def updateCollege():
    data = request.get_json(silent=True) or {}
    id = data.get('id') or request.args.get('id')
    if not id:
        return jsonify({'code': 400, 'message': '缺少学院 ID 参数'})
    college_name = data.get('college_name')or request.args.get('college_name')
    college_id = data.get('college_id')or request.args.get('college_id')
    update_fields = []
    values = []
    if college_name:
        update_fields.append('college_name = %s')
        values.append(college_name)
    if college_id:
        update_fields.append('college_id = %s')
        values.append(college_id)
    if not update_fields:
        return jsonify({'code': '400', 'message': '未提供需要修改的学院信息'})
    
    values.append(id)
    sql = 'UPDATE college SET ' + ', '.join(update_fields) + ' WHERE id = %s'
    try:
        cursor = db.cursor()
        lock.acquire()
        cursor.execute(sql, values)
        lock.release()
        if cursor.rowcount == 0:
            return jsonify({'code': '404', 'message': '未找到对应学院'})
        db.commit()
        return jsonify({'code': '200', 'message': '学院修改成功'})
    except Exception as e:
        db.rollback()
        return jsonify({'code': '400', 'message': str(e)})

# 学院分页查询接口
@app.route('/api/college/paginated', methods=['POST', 'GET'])
def queryCollegePaginated():
    data = request.get_json(silent=True) or {}
    pageNum = int(data.get('pageNum') or request.args.get('pageNum'))
    pageSize = int(data.get('pageSize') or request.args.get('pageSize'))
    college_id = data.get('params', {}).get('college_id') or request.args.get('college_id')
    college_name = data.get('params', {}).get('college_name') or request.args.get('college_name')
    offset = (pageNum - 1) * pageSize
    cursor = db.cursor()
    try:
        # 查询总数
        count_sql = "SELECT COUNT(*) FROM college WHERE 1=1"
        params = []
        if college_id:
            count_sql += " AND college_id LIKE CONCAT('%%', %s, '%%')"
            params.append(college_id)
        if college_name:
            count_sql += " AND college_name LIKE CONCAT('%%', %s, '%%')"
            params.append(college_name)
        lock.acquire()
        cursor.execute(count_sql, params)
        lock.release()
        total = int(cursor.fetchone()[0])
        # 查询分页数据
        sql = "SELECT id,college_id,college_name FROM college WHERE 1=1"
        if college_id:
            sql += " AND college_id LIKE CONCAT('%%', %s, '%%')"
        if college_name:
            sql += " AND college_name LIKE CONCAT('%%', %s, '%%')"
        sql += " LIMIT %s OFFSET %s"
        pagination_params = params + [pageSize, offset]
        lock.acquire()
        cursor.execute(sql, pagination_params)
        lock.release()
        results = cursor.fetchall()
        columns = ['id', 'college_id', 'college_name']
        colleges = [dict(zip(columns, row)) for row in results]
        return jsonify({'code': '200', 'message': '分页查询成功', 'data': colleges, 'total': total})
    except Exception as e:
        db.rollback()
        return jsonify({'code': '400', 'message': str(e)})

# 教师数据保存接口
@app.route('/api/counsellor/save', methods=['POST'])
def saveCounsellor():
    data = request.get_json(silent=True) or {}
    name = data.get('name') or request.args.get('name')
    username = data.get('username') or request.args.get('username')
    sex = data.get('sex') or request.args.get('sex')
    email = data.get('email') or request.args.get('email')
    phone = data.get('phone') or request.args.get('phone')
    description = data.get('description') or request.args.get('description')
    speciality_id = data.get('speciality_id') or request.args.get('speciality_id')
    pending_approval_list = data.get('pending_approval_list') or request.args.get('pending_approval_list')
    
    if not all([name,username, sex, email, phone, description, speciality_id]):
        return jsonify({'code': '400', 'message': '缺少必要参数'})
    
    cursor = db.cursor()
    try:
        sql = "INSERT INTO counsellor (name,username, sex, email, phone, description, speciality_id, pending_approval_list) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (name,username, sex, email, phone, description, speciality_id, pending_approval_list))
        db.commit()
        return jsonify({'code': '200', 'message': '数据添加成功'})
    except Exception as e:
        db.rollback()
        return jsonify({'code': '400', 'message': str(e)})

# 修改教师信息接口
@app.route('/api/counsellor/update', methods=['PUT','POST'])
def updateCounsellor():
    data = request.get_json(silent=True) or {}
    id = data.get('id') or request.args.get('id')
    if not id:
        return jsonify({'code': 400, 'message': '缺少教师 ID 参数'})
    name = data.get('name')or request.args.get('name')
    username = data.get('username')or request.args.get('username')
    sex = data.get('sex')or request.args.get('sex')
    email = data.get('email')or request.args.get('email')
    phone = data.get('phone')or request.args.get('phone')
    description = data.get('description')or request.args.get('description')
    speciality_id = data.get('speciality_id')or request.args.get('speciality_id')
    pending_approval_list = data.get('pending_approval_list')or request.args.get('pending_approval_list')
    
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
    if description:
        update_fields.append('description = %s')
        values.append(description)
    if speciality_id:
        update_fields.append('speciality_id = %s')
        values.append(speciality_id)
    if pending_approval_list:
        update_fields.append('pending_approval_list = %s')
        values.append(pending_approval_list)
    
    if not update_fields:
        return jsonify({'code': '400', 'message': '未提供需要修改的教师信息'})
    
    values.append(id)
    sql = 'UPDATE counsellor SET ' + ', '.join(update_fields) + ' WHERE id = %s'
    try:
        cursor = db.cursor()
        cursor.execute(sql, values)
        if cursor.rowcount == 0:
            return jsonify({'code': '404', 'message': '未找到对应教师'})
        db.commit()
        return jsonify({'code': '200', 'message': '教师修改成功'})
    except Exception as e:
        db.rollback()
        return jsonify({'code': '400', 'message': str(e)})

# 教师分页查询接口
@app.route('/api/counsellor/paginated', methods=['POST', 'GET'])
def queryCounsellorPaginated():
    data = request.get_json(silent=True) or {}
    pageNum = int(data.get('pageNum') or request.args.get('pageNum'))
    pageSize = int(data.get('pageSize') or request.args.get('pageSize'))
    name = data.get('params', {}).get('name') or request.args.get('name')
    phone = data.get('params', {}).get('phone') or request.args.get('phone')
    speciality_id = data.get('params', {}).get('speciality_id') or request.args.get('speciality_id')
    offset = (pageNum - 1) * pageSize
    cursor = db.cursor()
    try:
        # 查询总数
        count_sql = "SELECT COUNT(*) FROM counsellor WHERE 1=1"
        params = []
        if name:
            count_sql += " AND name LIKE CONCAT('%%', %s, '%%')"
            params.append(name)
        if phone:
            count_sql += " AND phone LIKE CONCAT('%%', %s, '%%')"
            params.append(phone)
        if speciality_id:
            count_sql += " AND speciality_id LIKE CONCAT('%%', %s, '%%')"
            params.append(speciality_id)
        lock.acquire()
        cursor.execute(count_sql, params)
        total = int(cursor.fetchone()[0])
        lock.release()
        # 查询分页数据
        sql = "SELECT id,name,username,sex,email,phone,description,speciality_id,pending_approval_list FROM counsellor WHERE 1=1"
        if name:
            sql += " AND name LIKE CONCAT('%%', %s, '%%')"
        if phone:
            sql += " AND phone LIKE CONCAT('%%', %s, '%%')"
        if speciality_id:
            sql += " AND speciality_id LIKE CONCAT('%%', %s, '%%')"
        sql += " LIMIT %s OFFSET %s"
        pagination_params = params + [pageSize, offset]
        lock.acquire()
        cursor.execute(sql, pagination_params)
        lock.release()
        results = cursor.fetchall()
        columns = ['id', 'name', 'username', 'sex', 'email', 'phone', 'description', 'speciality_id', 'pending_approval_list']
        counsellors = [dict(zip(columns, row)) for row in results]
        return jsonify({'code': '200', 'message': '分页查询成功', 'data': counsellors, 'total': total})
    except Exception as e:
        db.rollback()
        return jsonify({'code': '400', 'message': str(e)})

# 教师数据删除接口
@app.route('/api/counsellor/delete', methods=['DELETE'])
def deleteCounsellor():
    data = request.get_json(silent=True) or {}
    id = data.get('id') or request.args.get('id')
    if not id:
        return jsonify({'code': 400, 'message': '缺少必要参数 id'})
    cursor = db.cursor()
    try:
        sql = "DELETE FROM counsellor WHERE id = %s"
        lock.acquire()
        cursor.execute(sql, id)
        lock.release()
        if cursor.rowcount == 0:
            return jsonify({'code': 404, 'message': '未找到对应的教师记录'})
        lock.acquire()
        db.commit()
        lock.release()
        return jsonify({'code': 200, 'message': '教师数据删除成功'})
    except Exception as e:
        db.rollback()
        return jsonify({'code': 400, 'message': '教师数据删除失败: ' + str(e)})

# 修改学生信息接口
@app.route('/api/students/update', methods=['PUT','POST'])
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
@app.route('/api/students', methods=['POST', 'GET'])
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
@app.route('/api/students/paginated', methods=['POST', 'GET'])
def queryStudentsPaginated():
    data = request.get_json(silent=True) or {}
    pageNum = int(data.get('pageNum') or request.args.get('pageNum'))
    pageSize = int(data.get('pageSize') or request.args.get('pageSize'))
    name = data.get('params', {}).get('name') or request.args.get('name')
    phone = data.get('params', {}).get('phone') or request.args.get('phone')
    student_id = data.get('params', {}).get('student_id') or request.args.get('student_id')
    speciality_id = data.get('params', {}).get('speciality_id') or request.args.get('speciality_id')
    college_id = data.get('params', {}).get('college_id') or request.args.get('college_id')
    offset = (pageNum - 1) * pageSize
    cursor = db.cursor()
    try:
        # 查询总数
        count_sql = "SELECT COUNT(*) FROM student WHERE 1=1"
        params = []
        if name:
            count_sql += " AND name LIKE CONCAT('%%', %s, '%%')"
            params.append(name)
        if phone:
            count_sql += " AND phone LIKE CONCAT('%%', %s, '%%')"
            params.append(phone)
        if student_id:
            count_sql += " AND student_id LIKE CONCAT('%%', %s, '%%')"
            params.append(student_id)
        if speciality_id:
            count_sql += " AND speciality_id = %s"
            params.append(speciality_id)
        if college_id:
            count_sql += " AND college_id = %s"
            params.append(college_id)
        lock.acquire()
        cursor.execute(count_sql, params)
        lock.release()
        total = int(cursor.fetchone()[0])
        # 查询分页数据
        sql = "SELECT id,name,username,sex,email,phone,student_id,college_id,speciality_id FROM student WHERE 1=1"
        if name:
            sql += " AND name LIKE CONCAT('%%', %s, '%%')"
        if phone:
            sql += " AND phone LIKE CONCAT('%%', %s, '%%')"
        if student_id:
            sql += " AND student_id LIKE CONCAT('%%', %s, '%%')"
        if speciality_id:
            sql += " AND speciality_id = %s"
        if college_id:
            sql += " AND college_id = %s"
        sql += " LIMIT %s OFFSET %s"
        pagination_params = params + [pageSize, offset]
        lock.acquire()
        cursor.execute(sql, pagination_params)
        lock.release()
        results = cursor.fetchall()
        columns = ['id', 'name', 'username', 'sex', 'email', 'phone', 'student_id', 'college_id', 'speciality_id']
        students = [dict(zip(columns, row)) for row in results]
        return jsonify({'code': '200', 'message': '分页查询成功', 'data': students, 'total': total})
    except Exception as e:
        db.rollback()
        return jsonify({'code': '400', 'message': str(e)})

# 学生数据保存接口
@app.route('/api/students/save', methods=['POST'])
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
    
    if not all([name,username, sex, email, phone, student_id, college_id, speciality_id]):
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
@app.route('/api/students/delete', methods=['DELETE'])
def deleteStudent():
    data = request.get_json(silent=True) or {}
    id = data.get('id') or request.args.get('id')
    if not id:
        return jsonify({'code': 400, 'message': '缺少必要参数 id'})
    cursor = db.cursor()
    try:
        sql = "DELETE FROM student WHERE id = %s"
        lock.acquire()
        cursor.execute(sql, id)
        lock.release()
        if cursor.rowcount == 0:
            return jsonify({'code': 404, 'message': '未找到对应的学生记录'})
        lock.acquire()
        db.commit()
        lock.release()
        return jsonify({'code': 200, 'message': '学生数据删除成功'})
    except Exception as e:
        db.rollback()
        return jsonify({'code': 400, 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)