import pymysql
import threading
from datetime import datetime
from functools import wraps
lock = threading.Lock()

# 全局日志记录装饰器
def log_operation_decorator(content=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                # 先执行原函数
                result = func(*args, **kwargs)
                
                # 获取请求信息
                from flask import request
                current_content = content
                if current_content is None:
                    current_content = f"执行接口: {request.path}, 方法: {request.method}"
                client_ip = request.remote_addr
                
               
                username = "未知用户"
                try:
                    # 尝试从 session 中获取用户名
                    data = request.get_json(silent=True) or {}
                    username = data.get('username') or request.args.get('username', "未知用户")
                    if username == "未知用户":
                        if 'username' in session:
                            username = session['username']
                    if request.path == '/api/login' and request.method == 'POST':
                        session['username'] = username
                except:
                    pass
                
                # 记录日志
                cursor = db.cursor()
                time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                sql = "INSERT INTO log (content, username, time, ip) VALUES (%s, %s, %s, %s)"
                lock.acquire()
                try:
                    cursor.execute(sql, (content, username, time, client_ip))
                    db.commit()
                finally:
                    lock.release()
                
                return result
            except Exception as e:
                db.rollback()
                raise e
        return wrapper
    return decorator
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

from flask import Flask, request, json, jsonify, session
app = Flask(__name__)
app.secret_key = 'your_secret_key'
@app.route("/")
def mainIndex():
    return "hello world"

# 用户登录接口
@app.route('/api/login', methods=['POST'])
@log_operation_decorator('登录系统')
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
    if radio == 1:
        sql="""select id,username,password,email,role_id,ip from %s where username = '%s' and

         password='%s'""" %(tablename,username,password)
        columns = ['id', 'username','password','email','role_id','ip']
    else:
        sql="""select id,name,username,password,email,sex,phone,role_id,ip from %s where username = '%s' and

         password='%s'""" %(tablename,username,password)
        columns = ['id', 'name','username','password','email','sex','phone','role_id','ip']
    try:
        cursor.execute(sql)
        row = cursor.fetchone()
        if row:
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

# 学生请假次数排行
@app.route('/api/echarts/bar', methods=['GET'])
def get_echarts_bar():
    cursor = db.cursor()
    try:
        sql = "SELECT name, COUNT(*) as count FROM application GROUP BY name ORDER BY count DESC LIMIT 5"
        lock.acquire()
        cursor.execute(sql)
        lock.release()
        results = cursor.fetchall()
        x_data = [row[0] for row in results]
        y_data = [row[1] for row in results]
        return jsonify({'code': '200', 'message': '查询成功', 'data': {'xAxis': x_data, 'yAxis': y_data}})

    except Exception as e:
        db.rollback()
        return jsonify({'code': '400', 'message': str(e)})

# 请假单类型分布图
@app.route('/api/echarts/pie', methods=['GET'])
def get_echarts_pie():
    cursor = db.cursor()
    try:
        sql = "SELECT type, COUNT(*) as count FROM application GROUP BY type"
        lock.acquire()
        cursor.execute(sql)
        lock.release()
        results = cursor.fetchall()
        type_count = [dict(zip(['name', 'value'], row)) for row in results]
        return jsonify({'code': '200', 'message': '查询成功', 'data': type_count})
    except Exception as e:
        db.rollback()
        return jsonify({'code': '400', 'message': str(e)})

# 公告查询接口
@app.route('/api/notice', methods=['POST', 'GET'])
def queryNotice():
    cursor = db.cursor()
    try:
        sql = "SELECT id,name,content,time FROM notice order by time desc limit 5"



        lock.acquire()
        cursor.execute(sql)
        lock.release()
        results = cursor.fetchall()
        columns = ['id','name','content','time']
        notices = [dict(zip(columns, row)) for row in results]
        return jsonify({'code': '200', 'message': '查询成功', 'data': notices})
    except Exception as e:
        db.rollback()
        return jsonify({'code': '400', 'message': str(e)})

# 修改公告信息接口
@app.route('/api/notice/update', methods=['PUT','POST'])
@log_operation_decorator('修改公告信息')
def updateNotice():
    data = request.get_json(silent=True) or {}
    id = data.get('id') or request.args.get('id')
    if not id:
        return jsonify({'code': 400, 'message': '缺少公告 ID 参数'})
    name = data.get('name')or request.args.get('name')
    content = data.get('content')or request.args.get('content')
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    update_fields = []
    values = []
    if name:
        update_fields.append('name = %s')
        values.append(name)
    if content:
        update_fields.append('content = %s')
        values.append(content)
    if not update_fields:
        return jsonify({'code': '400', 'message': '未提供需要修改的公告信息'})
    values.append(id)
    sql = 'UPDATE notice SET ' + ', '.join(update_fields) + ' WHERE id = %s'
    try:
        cursor = db.cursor()
        cursor.execute(sql, values)
        if cursor.rowcount == 0:
            return jsonify({'code': '404', 'message': '未找到对应公告记录'})
        db.commit()
        return jsonify({'code': '200', 'message': '公告修改成功'})
    except Exception as e:
        db.rollback()
        return jsonify({'code': '400', 'message': str(e)})

# 公告数据删除接口
@app.route('/api/notice/delete', methods=['DELETE'])
@log_operation_decorator('删除公告信息')
def deleteNotice():
    data = request.get_json(silent=True) or {}
    id = data.get('id') or request.args.get('id')
    if not id:
        return jsonify({'code': 400, 'message': '缺少必要参数 id'})
    cursor = db.cursor()
    try:
        sql = "DELETE FROM notice WHERE id = %s"
        lock.acquire()
        cursor.execute(sql, id)
        lock.release()
        if cursor.rowcount == 0:
            return jsonify({'code': 404, 'message': '未找到对应的公告记录'})
        lock.acquire()
        db.commit()
        lock.release()
        return jsonify({'code': 200, 'message': '公告数据删除成功'})
    except Exception as e:
        lock.acquire()
        db.rollback()
        lock.release()
        return jsonify({'code': 400, 'message': '公告数据删除失败: ' + str(e)})

# 公告分页查询接口
@app.route('/api/notice/paginated', methods=['POST', 'GET'])
def queryNoticePaginated():
    data = request.get_json(silent=True) or {}
    pageNum = int(data.get('pageNum') or request.args.get('pageNum'))
    pageSize = int(data.get('pageSize') or request.args.get('pageSize'))
    name = data.get('params', {}).get('name') or request.args.get('name')
    offset = (pageNum - 1) * pageSize
    cursor = db.cursor()
    try:
        # 查询总数
        count_sql = "SELECT COUNT(*) FROM notice WHERE 1=1"
        params = []
        if name:
            count_sql += " AND name LIKE CONCAT('%%', %s, '%%')"
            params.append(name)
        lock.acquire()
        cursor.execute(count_sql, params)
        total = int(cursor.fetchone()[0])
        lock.release()
        # 查询分页数据
        sql = "SELECT id,name,content,time FROM notice WHERE 1=1"
        if name:
            sql += " AND name LIKE CONCAT('%%', %s, '%%')"
        sql += " LIMIT %s OFFSET %s"
        pagination_params = params + [pageSize, offset]
        lock.acquire()
        cursor.execute(sql, pagination_params)
        lock.release()
        results = cursor.fetchall()
        columns = ['id', 'name', 'content','time']

        notices = [dict(zip(columns, row)) for row in results]
        return jsonify({'code': '200', 'message': '分页查询成功', 'data': notices, 'total': total})
    except Exception as e:
        lock.acquire()
        db.rollback()
        lock.release()
        return jsonify({'code': '400', 'message': str(e)})

# 公告数据保存接口
@app.route('/api/notice/save', methods=['POST'])
@log_operation_decorator('添加公告信息')
def saveNotice():
    data = request.get_json(silent=True) or {}
    name = data.get('name') or request.args.get('name')
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content = data.get('content') or request.args.get('content')
    if not all([name,content]):
        return jsonify({'code': '400', 'message': '缺少必要参数'})
    
    cursor = db.cursor()
    try:
        sql = "INSERT INTO notice (name,content,time) VALUES (%s, %s,%s)"
        cursor.execute(sql, (name,content,time))
        lock.acquire()
        db.commit()
        lock.release()
        return jsonify({'code': '200', 'message': '数据添加成功'})
    except Exception as e:
        lock.acquire()
        db.rollback()
        lock.release()
        return jsonify({'code': '400', 'message': '数据添加失败: ' + str(e)})

# 日志数据删除接口
@app.route('/api/log/delete', methods=['DELETE'])
def deleteLog():
    data = request.get_json(silent=True) or {}
    id = data.get('id') or request.args.get('id')
    if not id:
        return jsonify({'code': 400, 'message': '缺少必要参数 id'})
    cursor = db.cursor()
    try:
        sql = "DELETE FROM log WHERE id = %s"
        lock.acquire()
        cursor.execute(sql, id)
        lock.release()
        if cursor.rowcount == 0:
            return jsonify({'code': 404, 'message': '未找到对应的日志记录'})
        lock.acquire()
        db.commit()
        lock.release()
        return jsonify({'code': 200, 'message': '日志数据删除成功'})
    except Exception as e:
        db.rollback()
        return jsonify({'code': 400, 'message': '学院数据删除失败: ' + str(e)})

# 日志分页查询接口
@app.route('/api/log/paginated', methods=['POST', 'GET'])
def queryLogPaginated():
    data = request.get_json(silent=True) or {}
    pageNum = int(data.get('pageNum') or request.args.get('pageNum'))
    pageSize = int(data.get('pageSize') or request.args.get('pageSize'))
    content = data.get('params', {}).get('content') or request.args.get('content')
    username = data.get('params', {}).get('username') or request.args.get('username')
    offset = (pageNum - 1) * pageSize
    cursor = db.cursor()
    try:
        # 查询总数
        count_sql = "SELECT COUNT(*) FROM log WHERE 1=1"
        params = []
        if content:
            count_sql += " AND content LIKE CONCAT('%%', %s, '%%')"
            params.append(content)
        if username:
            count_sql += " AND username LIKE CONCAT('%%', %s, '%%')"
            params.append(username)
        lock.acquire()
        cursor.execute(count_sql, params)
        lock.release()
        total = int(cursor.fetchone()[0])
        # 查询分页数据
        sql = "SELECT id,content,username,time,ip FROM log WHERE 1=1"
        if content:
            sql += " AND content LIKE CONCAT('%%', %s, '%%')"
        if username:
            sql += " AND username LIKE CONCAT('%%', %s, '%%')"
        sql += " LIMIT %s OFFSET %s"
        pagination_params = params + [pageSize, offset]
        lock.acquire()
        cursor.execute(sql, pagination_params)
        lock.release()
        results = cursor.fetchall()
        columns = ['id', 'content', 'username', 'time', 'ip']
        logs = [dict(zip(columns, row)) for row in results]
        return jsonify({'code': '200', 'message': '分页查询成功', 'data': logs, 'total': total})
    except Exception as e:
        db.rollback()
        return jsonify({'code': '400', 'message': str(e)})

# 获取个人信息接口
@app.route('/api/user/get_info', methods=['GET','POST'])
def get_user_info():
    data = request.get_json(silent=True) or {}
    id = data.get('id') or request.args.get('id')
    role_id = int(data.get('role_id') or request.args.get('role_id',0))
    if not id:
        return jsonify({'code': 400, 'message': '缺少用户 ID 参数'})
    if not role_id:
        return jsonify({'code': 400, 'message': '缺少用户角色 ID 参数'})
    try:
        role_id = int(role_id)
        table_map = {
            1: 'user',
            2: 'counsellor',
            3: 'student'
        }
        table_name = table_map.get(role_id, 'user')
        cursor = db.cursor()
        if role_id == 1:
            columns = ['id', 'username', 'password', 'email', 'role_id', 'ip']
            sql = f'SELECT {','.join(columns)} FROM {table_name} WHERE id = %s'
        else:
            columns = ['id', 'name', 'username', 'password', 'email', 'sex', 'phone', 'role_id', 'ip']
            sql = f'SELECT {','.join(columns)} FROM {table_name} WHERE id = %s'
        cursor.execute(sql, (id,))
        row = cursor.fetchone()
        if row:
            user_info = dict(zip(columns, row))
            return jsonify({'code': '200', 'message': '获取用户信息成功', 'data': user_info})
        else:
            return jsonify({'code': '404', 'message': '未找到对应用户记录'})
    except Exception as e:
        return jsonify({'code': '400', 'message': str(e)})

# 修改个人信息接口
@app.route('/api/user/update_info', methods=['PUT'])
@log_operation_decorator('修改个人信息')
def update_user_info():
    data = request.get_json(silent=True) or {}
    id = data.get('id') or request.args.get('id')
    if not id:
        return jsonify({'code': 400, 'message': '缺少用户 ID 参数'})
    role_id = int(data.get('role_id') or request.args.get('role_id', 0))
    username = data.get('username') or request.args.get('username', '')
    password = data.get('password') or request.args.get('password', '')
    email = data.get('email') or request.args.get('email', '')
    sex = data.get('sex') or request.args.get('sex', '')
    phone = data.get('phone') or request.args.get('phone', '')

    update_fields = []
    values = []
    if username:
        update_fields.append('username = %s')
        values.append(username)
    if password:
        update_fields.append('password = %s')
        values.append(password)
    if email:
        update_fields.append('email = %s')
        values.append(email)
    if sex:
        update_fields.append('sex = %s')
        values.append(sex)
    if phone:
        update_fields.append('phone = %s')
        values.append(phone)
    if not update_fields:
        return jsonify({'code': '400', 'message': '未提供需要修改的用户信息'})
    values.append(id)
    table_map = {
        1: 'user',
        2: 'counsellor',
        3: 'student'
    }
    table_name = table_map.get(role_id, 'user')
    sql = f'UPDATE {table_name} SET ' + ', '.join(update_fields) + ' WHERE id = %s'

    try:
        cursor = db.cursor()
        cursor.execute(sql, values)
        if cursor.rowcount == 0:
            return jsonify({'code': '404', 'message': '未找到对应用户记录'})
        db.commit()
        return jsonify({'code': '200', 'message': '用户信息修改成功'})
    except Exception as e:
        db.rollback()
        return jsonify({'code': '400', 'message': str(e)})

# 修改请假信息接口
@app.route('/api/application/update', methods=['PUT','POST'])
@log_operation_decorator('修改请假信息')
def updateApplication():
    data = request.get_json(silent=True) or {}
    id = data.get('id') or request.args.get('id')
    if not id:
        return jsonify({'code': 400, 'message': '缺少请假 ID 参数'})
    status = data.get('status')or request.args.get('status')
    audit_remark = data.get('audit_remark')or request.args.get('audit_remark')
    update_fields = []
    values = []
    if status:
        update_fields.append('status = %s')
        values.append(status)
    if audit_remark:
        update_fields.append('audit_remark = %s')
        values.append(audit_remark)
    if not update_fields:
        return jsonify({'code': '400', 'message': '未提供需要修改的请假信息'})
    
    values.append(id)
    sql = 'UPDATE application SET ' + ', '.join(update_fields) + ' WHERE id = %s'
    try:
        cursor = db.cursor()
        cursor.execute(sql, values)
        if cursor.rowcount == 0:
            return jsonify({'code': '404', 'message': '未找到对应请假记录'})
        db.commit()
        return jsonify({'code': '200', 'message': '请假修改成功'})
    except Exception as e:
        db.rollback()
        return jsonify({'code': '400', 'message': str(e)})

# 请假数据删除接口
@app.route('/api/application/delete', methods=['DELETE'])
@log_operation_decorator('删除请假信息')
def deleteApplication():
    data = request.get_json(silent=True) or {}
    id = data.get('id') or request.args.get('id')
    if not id:
        return jsonify({'code': 400, 'message': '缺少必要参数 id'})
    cursor = db.cursor()
    try:
        sql = "DELETE FROM application WHERE id = %s"
        lock.acquire()
        cursor.execute(sql, id)
        lock.release()
        if cursor.rowcount == 0:
            return jsonify({'code': 404, 'message': '未找到对应的请假记录'})
        lock.acquire()
        db.commit()
        lock.release()
        return jsonify({'code': 200, 'message': '请假数据删除成功'})
    except Exception as e:
        lock.acquire()
        db.rollback()
        lock.release()
        return jsonify({'code': 400, 'message': '请假数据删除失败: ' + str(e)})

# 请假分页查询接口
@app.route('/api/application/paginated', methods=['POST', 'GET'])
def queryApplicationPaginated():
    data = request.get_json(silent=True) or {}
    pageNum = int(data.get('pageNum') or request.args.get('pageNum'))
    pageSize = int(data.get('pageSize') or request.args.get('pageSize'))
    role_id = int(data.get('params', {}).get('role_id') or request.args.get('role_id', 0))
    name = data.get('params', {}).get('name') or request.args.get('name')
    LeaveType = data.get('params', {}).get('type') or request.args.get('type')
    status = data.get('params', {}).get('status') or request.args.get('status')
    offset = (pageNum - 1) * pageSize
    cursor = db.cursor()
    try:
        # 查询总数
        count_sql = "SELECT COUNT(*) FROM application WHERE 1=1"
        params = []
        if name and role_id not in [1, 2]:
            count_sql += " AND name LIKE CONCAT('%%', %s, '%%')"
            params.append(name)
        if LeaveType:
            count_sql += " AND type LIKE CONCAT('%%', %s, '%%')"
            params.append(LeaveType)
        if status:
            count_sql += " AND status LIKE CONCAT('%%', %s, '%%')"
            params.append(status)
        lock.acquire()
        cursor.execute(count_sql, params)
        total = int(cursor.fetchone()[0])
        lock.release()
        # 查询分页数据
        sql = "SELECT id,name,type,start_time,end_time,reason,apply_time,status FROM application WHERE 1=1"
        if name and role_id not in [1, 2]:
            sql += " AND name LIKE CONCAT('%%', %s, '%%')"
        if LeaveType:
            sql += " AND type LIKE CONCAT('%%', %s, '%%')"
        if status:
            sql += " AND status LIKE CONCAT('%%', %s, '%%')"
        sql += " LIMIT %s OFFSET %s"
        pagination_params = params + [pageSize, offset]
        lock.acquire()
        cursor.execute(sql, pagination_params)
        lock.release()
        results = cursor.fetchall()
        columns = ['id', 'name', 'type','start_time','end_time','reason','apply_time','status']
        applications = [dict(zip(columns, row)) for row in results]
        return jsonify({'code': '200', 'message': '分页查询成功', 'data': applications, 'total': total})
    except Exception as e:
        lock.acquire()
        db.rollback()
        lock.release()
        return jsonify({'code': '400', 'message': str(e)})

# 请假数据保存接口
@app.route('/api/application/save', methods=['POST'])
@log_operation_decorator('添加请假信息')
def saveApplication():
    data = request.get_json(silent=True) or {}
    name = data.get('name') or request.args.get('name')
    leaveType = data.get('type') or request.args.get('type')
    StartleaveTime = data.get('StartleaveTime') or request.args.get('StartleaveTime')
    EndleaveTime = data.get('EndleaveTime') or request.args.get('EndleaveTime')
    remark = data.get('remark') or request.args.get('remark')
    apply_time = data.get('apply_time') or request.args.get('apply_time')
    if not all([name,leaveType,StartleaveTime,EndleaveTime,remark]):
        return jsonify({'code': '400', 'message': '缺少必要参数'})
    cursor = db.cursor()
    try:
        sql = "INSERT INTO application (name,type,start_time,end_time,reason,apply_time) VALUES (%s, %s,%s,%s,%s,%s)"
        lock.acquire()
        cursor.execute(sql, (name,leaveType,StartleaveTime,EndleaveTime,remark,apply_time))
        lock.release()
        db.commit()
        return jsonify({'code': '200', 'message': '数据添加成功'})
    except Exception as e:
        db.rollback()
        return jsonify({'code': '400', 'message': '数据添加失败: ' + str(e)})

# 专业数据保存接口
@app.route('/api/speciality/save', methods=['POST'])
@log_operation_decorator('添加专业信息')
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
@log_operation_decorator('删除专业信息')
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
@log_operation_decorator('修改专业信息')
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
@log_operation_decorator('添加学院信息')
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
@log_operation_decorator('删除学院信息')
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
@log_operation_decorator('修改学院信息')
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
@log_operation_decorator('添加教师信息')
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
@log_operation_decorator('修改教师信息')
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
@log_operation_decorator('删除教师信息')
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
@log_operation_decorator('修改学生信息')
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
@log_operation_decorator('添加学生信息')
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
@log_operation_decorator('删除学生信息')
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