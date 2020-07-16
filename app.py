import os
import sqlite3
import string
import random
from flask import Flask, request, g, jsonify, Response
import time


def create_db():
    # 连接
    conn = sqlite3.connect("company.db")
    c = conn.cursor()

    # 创建表
    # c.execute('''DROP TABLE IF EXISTS menbers ''') # 删除旧表，如果存在（因为这是临时数据）
    # c.execute('''CREATE TABLE menbers (u_id INTEGER PRIMARY KEY AUTOINCREMENT, u_openid text only ,u_name text, u_random text, u_face text , u_regtime text )''')
    # conn.commit()
    # c.execute('''DROP TABLE IF EXISTS users''')
    # c.execute('''CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, u_name text only, nick_name text only ,u_face text,u_pw text ,u_phone text,u_email text, u_regtime text )''')
    # 话题表
    c.execute('''DROP TABLE IF EXISTS subject''')
    c.execute(
        '''CREATE TABLE subject (id INTEGER PRIMARY KEY AUTOINCREMENT, u_name text only , nick_name text only ,u_face text,sub_title text ,sub_content text,sub_time text, sub_like INTEGER )''')
    #评论表
    c.execute('''DROP TABLE IF EXISTS reply''')
    c.execute(
        '''CREATE TABLE reply (id INTEGER PRIMARY KEY AUTOINCREMENT, u_name text only, nick_name text only ,u_face text,sub_id text ,reply_content text,reply_time text, reply_like INTEGER )''')
    conn.commit()
    conn.close()

# 添加初始数据或测试数据
def init_db():
    db = connect_db()
    # data = "NULL,\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\'" % (
    # 'luqwert','令狐冲', 'dasdadasdada.jpg', 'lu1986617', '18621602796', 'lusheng1234@sina.com', time.strftime("%Y-%m-%d", time.localtime()))
    # db.execute('INSERT INTO users VALUES (%s)' % data)
    data1 = "NULL,\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%d\'" % (
    'luqwert','芦胜', 'dasdadasdada.jpg', 'app开始试用了', '公司app开始试用，请大家提出改进建议和意见', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), 5)
    db.execute('INSERT INTO subject VALUES (%s)' % data1)
    data2 = "NULL,\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%d\'" % (
        'luqwertbb', '刘杨', 'dasdadasdaddadaa.jpg', 'app开始试用了2222222', '公司app开始试用，请大家提出改进建议和意见2222222222',
        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), 0)
    db.execute('INSERT INTO subject VALUES (%s)' % data2)
    data3 = "NULL,\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%d\'" % (
    'luqwertaaa','东方不败', 'dasdasdadadada.jpg', '1', '恭喜app开始试用', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), 0)
    db.execute('INSERT INTO reply VALUES (%s)' % data3)
    db.commit()
    db.close()

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])
# def init_db():
#     with closing(connect_db()) as db:
#         with app.open_resource('schema.sql') as f:
#             db.cursor().executescript(f.read())
#         db.commit()


DATABASE = 'company.db'
DEBUG = True
SECRET_KEY = 'development key'


app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
# create_db()
# init_db()

@app.before_request
def before_request():
    g.db = connect_db()


@app.after_request
def after_request(response):
    g.db.close()
    return response

@app.route('/login/<openid>', methods=['GET', 'POST'])
def login(openid):
    error = None
    if request.method == 'POST':
        result = g.db.execute("SELECT * FROM menbers where u_openid = '%s'" % openid)
        # print(result.fetchall())
        # 数据存在
        if result.fetchone():
            return jsonify({'SUID': result.fetchone()[1],
                            'SNAME': result.fetchone()[2],
                            'SRAND': result.fetchone()[3],
                            'SFACE': result.fetchone()[4]})
        # 数据不存在，新增一条数据
        else:
            openid = request.form.get('openid')
            name = request.form.get('name')
            randomtext = ''.join(random.sample(string.ascii_letters + string.digits, 15))
            face = request.form.get('face')
            regtime = time.strftime("%Y-%m-%d", time.localtime())
            print(openid, name, randomtext, face, regtime)
            if openid and name and face:
                data = "NULL,\'%s\',\'%s\',\'%s\',\'%s\',\'%s\'" % (openid, name, randomtext, face, regtime)
                print(data)
                g.db.execute('INSERT INTO menbers VALUES (%s)' % data)
                g.db.commit()
                result = g.db.execute("SELECT * FROM menbers where u_openid = '%s'" % openid).fetchone()
                print(result)
                print(result[1])
                return jsonify({'SUID': result[1],
                                'SNAME': result[2],
                                'SRAND': result[3],
                                'SFACE': result[4]})
            else:
                return jsonify({'error': '提交数据错误，请返回重试'})
    else:
        return jsonify({'error': '注册失败，请返回重试'})


@app.route('/getphotolist', methods=['GET'])
def getphotolist():
    basedir = "E:\\photos\\"
    # basedir = "/root/webapi/static/photos/"
    dirlist = os.listdir(basedir)
    rusult = []
    for i in range(len(dirlist)):
        if '.' in dirlist[i]:
            pass
        else:
            if os.listdir(basedir + dirlist[i]):
                coverphoto = basedir + dirlist[i] + '\\' + os.listdir(basedir + dirlist[i])[0]
                rusult.append(
                    {'name': dirlist[i],
                        'path': basedir + dirlist[i],
                        'coverphoto': 'http://127.0.0.1:5000/image?path=' + coverphoto}
                )
            else:
                rusult.append(
                     {'name': dirlist[i],
                        'path': basedir + dirlist[i],
                        'coverphoto': ''}
                )
    print(rusult)
    return jsonify(rusult)

@app.route("/image", methods=['post', 'get'])
def index():
    path = request.args.get('path')
    print(path)
    resp = Response(open(path, 'rb'), mimetype="image/jpeg")
    return resp

@app.route('/getphotos', methods=['GET'])
def getphotospath():
    basedir = "E:\\photos\\"
    # basedir = "/root/webapi/static/photos/"
    dirname = request.args.get('dirname')
    basedir = basedir + dirname + '\\'
    print(basedir)
    dirlist = os.listdir(basedir)
    print(dirlist)
    rusult = []
    for i in range(len(dirlist)):
        rusult.append(
            {'name': dirlist[i],
                'path': 'http://127.0.0.1:5000/image?path=' + basedir + dirlist[i]
             }
        )
    print(rusult)
    return jsonify(rusult)

@app.route('/userlogin', methods=['GET', 'POST'])
def userlogin():
    if request.method == 'POST':
        name = request.form.get('username')
        pw = request.form.get('password')
        print(name, pw)
        result = g.db.execute("SELECT * FROM users where u_name = '%s'" % name)
        result2 = result.fetchone()
        print(result2)

        # 数据存在
        if result2 is not None:
            if result2[4] == pw:
                return jsonify({'u_name': result2[1],
                                'nick_name': result2[2],
                                'u_face': result2[3],
                                'u_phone': result2[5],
                                'u_email': result2[6],
                                'u_rtime': result2[7]})
            else:
                return jsonify({'error': '密码错误，请返回重试'})
        # 数据不存在，新增一条数据
        else:
            return jsonify({'error': '用户不存在，请返回重试'})
    else:
        return jsonify({'error': '登录失败，请返回重试'})

@app.route('/regist', methods=['GET', 'POST'])
def regist():
    if request.method == 'POST':
        name = request.form.get('username')
        pw = request.form.get('password')
        nickname = request.form.get('nickname')
        phone = request.form.get('phone')
        email = request.form.get('email')
        print(name, nickname, pw, phone, email)
        result = g.db.execute("SELECT * FROM users where u_name = '%s'" % name)
        result2 = result.fetchone()
        print(result2)
        if result2 is None:
            resultn = g.db.execute("SELECT * FROM users where nick_name = '%s'" % nickname)
            resultn2 = resultn.fetchone()
            if resultn2 is None:
                data = "NULL,\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\'" % (
                    name, nickname, '', pw, phone, email,
                    time.strftime("%Y-%m-%d", time.localtime()))
                g.db.execute('INSERT INTO users VALUES (%s)' % data)
                g.db.commit()
                result3 = g.db.execute("SELECT * FROM users where u_name = '%s'" % name)
                result4 = result3.fetchone()
                if result4 is not None:
                    return jsonify({'u_name': result4[1],
                                    'nick_name': result4[2],
                                        'u_face': result4[3],
                                        'u_phone': result4[5],
                                        'u_email': result4[6],
                                        'u_rtime': result4[7]})
                else:
                    return jsonify({'error': '注册失败，请返回重试'})
            else:
                return jsonify({'error': '昵称已存在，请返回重试'})
        else:
            return jsonify({'error': '用户已存在，请返回登录'})
    else:
        return jsonify({'error': '注册失败，请返回重试'})

@app.route('/forgetpw', methods=['GET', 'POST'])
def forgetpw():
    if request.method == 'POST':
        name = request.form.get('username')
        email = request.form.get('email')
        print(name, email)
        result = g.db.execute("SELECT * FROM users where u_name = '%s'" % name)
        result2 = result.fetchone()
        print(result2)
        if result2 is not None:
            if result2[6] == email:
                return jsonify({'u_name': result2[1],
                                'u_password': result2[4],
                                'u_email': result2[6]})
            else:
                return jsonify({'error': '邮箱错误，请检查后重试'})
        else:
            return jsonify({'error': '用户不存在，请检查后重试'})
    else:
        return jsonify({'error': '找回密码失败，请返回重试'})

@app.route('/getsubject', methods=['GET'])
def getsubject():
    result = g.db.execute("SELECT * FROM subject")
    result2 = result.fetchall()
    print(result2)
    reslist = []
    if result2 is not []:
        for sub in reversed(result2):
            replylist = []
            print(sub[0])
            result4 = g.db.execute("SELECT * FROM reply WHERE sub_id = '%s'" % sub[0]).fetchall()
            print(result4)
            if result4 is not []:
                for item in reversed(result4):
                    # print(item)
                    reply_item = {
                        'id':item[0],
                        '回复人': item[1],
                        '回复人昵称': item[2],
                        '回复人头像': item[3],
                        '回复内容': item[5],
                        '发表时间': item[6],
                        '点赞数': item[7],
                    }
                    replylist.append(reply_item)
                # print(replylist)
            res_item = {
                'id': sub[0],
                '话题人': sub[1],
                '话题人昵称': sub[2],
                '话题人头像': sub[3],
                '话题名称': sub[4],
                '话题内容': sub[5],
                '发表时间': sub[6],
                '点赞数': sub[7],
                '回复': replylist,
                'text_area_display': '',
                'comment_display': '',
            }
            reslist.append(res_item)
        return jsonify(reslist)
    else:
        return jsonify({'error': '留言板暂时没有话题'})

@app.route('/sendsubject', methods=['GET', 'POST'])
def sendsubject():
    if request.method == 'POST':
        u_name = request.form.get('u_name')
        nick_name = request.form.get('nick_name')
        u_face = request.form.get('u_face')
        sub_title = request.form.get('sub_title')
        sub_content = request.form.get('sub_content')
        print(u_name, nick_name, u_face, sub_title, sub_content)

        sub = "NULL,\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%d\'" % (
            u_name, nick_name, u_face, sub_title, sub_content,
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), 0)
        g.db.execute('INSERT INTO subject VALUES (%s)' % sub)
        g.db.commit()
        return jsonify({'success': '留言提交成功'})
    else:
        return jsonify({'error': '提交留言失败，请返回重试'})

@app.route('/likesubject', methods=['GET', 'POST'])
def likesubject():
    if request.method == 'POST':
        s_id = request.form.get('s_id')
        print(s_id)
        like = g.db.execute("SELECT * FROM subject where id = '%s'" % s_id).fetchone()[7] + 1
        g.db.execute('UPDATE subject SET sub_like = "%d" WHERE id = "%s"' % (like, s_id))
        g.db.commit()
        return jsonify({'success': '点赞成功'})
    else:
        return jsonify({'error': '点赞失败，请返回重试'})

@app.route('/sendcomment', methods=['GET', 'POST'])
def sendcomment():
    if request.method == 'POST':
        u_name = request.form.get('u_name')
        nick_name = request.form.get('nick_name')
        u_face = request.form.get('u_face')
        sub_id = request.form.get('sub_id')
        comment_content = request.form.get('comment_content')
        print(u_name, nick_name, u_face, sub_id, comment_content)
        comment = "NULL,\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%d\'" % (
            u_name, nick_name, u_face, sub_id, comment_content, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            0)
        g.db.execute('INSERT INTO reply VALUES (%s)' % comment)
        g.db.commit()
        return jsonify({'success': '评论提交成功'})
    else:
        return jsonify({'error': '提交评论失败，请返回重试'})


@app.route('/getaddressbook', methods=['GET'])
def getaddressbook():
    try:
        return_jason = []
        department = []
        db = sqlite3.connect('company.db')
        result = db.execute("SELECT department FROM addressbook").fetchall()
        # print(result)
        for item in result:
            if item[0] not in department:
                department.append(item[0])
        print(department)

        for item in department:
            return_jasonitem = []
            result = db.execute("SELECT * FROM addressbook where department = '%s'" % item).fetchall()
            # print(result)
            for n in result:
                return_jasonitem.append(list(n))
            return_jason.append({'departmentname': item, 'data': return_jasonitem})
        return jsonify({'success': '获取通讯录成功', 'data': return_jason})
    except:
        return jsonify({'error': '获取通讯录失败，请返回重试'})

@app.route('/getpurchasedata', methods=['GET'])
def getpurchasedata():
    import business_data
    try:
        return_jason = business_data.get_business_data('采购合同')
        return jsonify({'success': '获取采购数据成功', 'data': return_jason})
    except:
        return jsonify({'error': '获取采购数据失败，请返回重试'})

@app.route('/getselldata', methods=['GET'])
def getselldata():
    import business_data
    try:
        return_jason = business_data.get_business_data('销售合同')
        return jsonify({'success': '获取销售数据成功', 'data': return_jason})
    except:
        return jsonify({'error': '获取销售数据失败，请返回重试'})

# @app.route('/likecomment', methods=['GET', 'POST'])
# def likecomment():
#     if request.method == 'POST':
#         s_id = request.form.get('s_id')
#         print(s_id)
#         like = g.db.execute("SELECT * FROM subject where id = '%s'" % s_id).fetchone()[6] + 1
#         g.db.execute('UPDATE subject SET sub_like = "%d" WHERE id = "%s"' % (like, s_id))
#         g.db.commit()
#         return jsonify({'success': '点赞成功'})
#     else:
#         return jsonify({'error': '点赞失败，请返回重试'})


@app.route('/getreportdata', methods=['GET'])
def get_report_data():
    import week_report
    try:
        return_jason = week_report.report()
        return jsonify({'success': '获取周报数据成功', 'data': return_jason})
    except:
        return jsonify({'error': '获取周报数据失败，请返回重试'})

if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run(host='0.0.0.0', port=5000,debug=True)
