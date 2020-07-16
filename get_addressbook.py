#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# @Author  : lusheng

import sqlite3

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
    print(result)
    for n in result:
        return_jasonitem.append(list(n))
    return_jason.append({'departmentname': item, 'data': return_jasonitem})
print(return_jason)

db.close()
