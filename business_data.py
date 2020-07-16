#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# @Author: lusheng

import pandas as pd
import datetime,time

excel_path = 'E:\\python\\webapi\\static\\2018管理表.xlsx'


def get_business_data(sheet_name):
    df = pd.read_excel('E:\\python\\webapi\\static\\2018管理表.xlsx',sheet_name=sheet_name,date_parser='合同签订日期')
    # data = df.head()
    # # print("获取到所有的值:\n{0}".format(data))
    # data=df.ix[:,['合同编号','合同签订日期','吨数','单价','金额','已送货吨数','已结算吨数','已结算金额','已开票吨数','已开票金额','已收款金额','加工费']].values#读所有行的title以及data列的值，这里需要嵌套列表
    # # data['合同签订日期'].dt.strftime('%Y%m%d')
    # # print("读取指定行的数据：\n{0}".format(data))
    # data1 = df[['合同编号','合同签订日期','吨数','单价','金额']]
    # print(data1)
    data = df.ix[:,['合同编号','品名','合同签订日期','吨数','单价','金额']].values
    # print(data)

    #本月最后一天
    fristday = []
    lastday = []
    month_list = ['月份']
    guimeng_quantity_list, guimeng_amout_list,guimeng_price_list = ['硅锰数量'], ['硅锰金额'], ['硅锰单价']
    mengpian_quantity_list, mengpian_amout_list,mengpian_price_list = ['锰片数量'], ['锰片金额'], ['锰片单价']
    mengqiu_quantity_list, mengqiu_amout_list,mengqiu_price_list = ['锰球数量'], ['锰球金额'], ['锰球单价']

    now_time = pd.Timestamp.now()
    month = now_time.month
    year = now_time.year
    # print(now_time,year,month)
    for i in range(12):
        if now_time.month - i == 0:
            month = 12
            year = now_time.year - 1
            frist = pd.Timestamp(str(year) + '-' + str(month) + '-' + '01')
            last = pd.Timestamp(str(year) + '-' + str(month) + '-' + '31')
        elif now_time.month - i < 0:
            month = 12
            year = now_time.year - 1
            frist = pd.Timestamp(str(year) + '-' + str(month + now_time.month - i) + '-' + '01')
            last = pd.Timestamp(str(year) + '-' + str(month + now_time.month - i + 1) + '-' + '01') - pd.Timedelta(days=1)
        else:
            frist = pd.Timestamp(str(year) + '-' + str(month - i) + '-' + '01')
            if (month - i + 1) >12:
                last = pd.Timestamp(str(year + 1 ) + '-' + '01' + '-' + '01') - pd.Timedelta(
                    days=1)
            else:
                last = pd.Timestamp(str(year) + '-' + str(month - i + 1) + '-' + '01') - pd.Timedelta(
                    days=1)
            # print(type(frist),type(last))
        fristday.append(frist)
        lastday.append(last)

    # for i in range(len(fristday)):
    #     print(fristday[i], lastday[i])
    # print(fristday,lastday)
    #循环各行数据，将同一个月内并且品名一样的数据放在一起
    for i in reversed(range(12)):
        guimeng_quantity, mengpian_quantity, mengqiu_quantity = 0, 0, 0
        guimeng_amout, mengpian_amout, mengqiu_amout = 0, 0, 0
        guimeng_price, mengpian_price, mengqiu_price = 0, 0, 0

        for row in data:
            # print(type(row[2]),row[2])
            # print(type(lastday[i]),lastday[i])
            if (row[2] <= lastday[i]) and (row[2] >= fristday[i]):
                if row[1] == '硅锰':
                    guimeng_quantity = guimeng_quantity + row[3]
                    guimeng_amout = guimeng_amout + row[5]
                if row[1] == '锰片':
                    mengpian_quantity = mengpian_quantity + row[3]
                    mengpian_amout = mengpian_amout + row[5]
                if row[1] == '锰球':
                    mengqiu_quantity = mengqiu_quantity + row[3]
                    mengqiu_amout = mengqiu_amout + row[5]
        if guimeng_quantity == 0:
            guimeng_price = 0
        else:
            guimeng_price = guimeng_amout / guimeng_quantity
        if mengpian_quantity == 0:
            mengpian_price = 0
        else:
            mengpian_price = mengpian_amout / mengpian_quantity
        if mengqiu_quantity == 0:
            mengqiu_price = 0
        else:
            mengqiu_price = mengqiu_amout / mengqiu_quantity
        # print(str(fristday[i]) + '-----' + str(lastday[i]))
        # print('硅锰：', guimeng_quantity,guimeng_amout,guimeng_price)
        # print('锰片：', mengpian_quantity, mengpian_amout, mengpian_price)
        # print('锰球：', mengqiu_quantity, mengqiu_amout, mengqiu_price)
        this_month = str(fristday[i].year) + '年' + str(fristday[i].month) + '月'
        month_list.append(this_month)
        guimeng_quantity_list.append(int(guimeng_quantity))
        guimeng_amout_list.append(int(guimeng_amout/10000))
        guimeng_price_list.append(int(guimeng_price))
        mengpian_quantity_list.append(int(mengpian_quantity))
        mengpian_amout_list.append(int(mengpian_amout/10000))
        mengpian_price_list.append(int(mengpian_price))
        mengqiu_quantity_list.append(int(mengqiu_quantity))
        mengqiu_amout_list.append(int(mengqiu_amout/10000))
        mengqiu_price_list.append(int(mengqiu_price))
    print(month_list)
    print(guimeng_quantity_list)
    print(guimeng_amout_list)
    print(guimeng_price_list)
    print(mengpian_quantity_list)
    print(mengpian_amout_list)
    print(mengpian_price_list)
    print(mengqiu_quantity_list)
    print(mengqiu_amout_list)
    print(mengqiu_price_list)
    return [
        month_list,
        guimeng_quantity_list, mengpian_quantity_list, mengqiu_quantity_list,
        guimeng_amout_list, mengpian_amout_list, mengqiu_amout_list,
        guimeng_price_list, mengpian_price_list, mengqiu_price_list
    ]
# df2 = df1.loc[df1['PM'] == 'Bob']
# for row in sheet_sell.rows:
#     for cell in row:
#         print(cell.value)
# print(n_of_rows, n_of_cols, haddate[-5:])
# 写入数据参数包括行号、列号、和值（其中参数不止这些）
# sheet["A%d" % n_of_rows].value = indextitle[:-10]

# if date in haddate:
#     pass
# else:
#     sheet["A%d" % n_of_rows].value = date
#     sheet["A%d" % n_of_rows].number_format = 'yyyy-mm-dd'
#     sheet["B%d" % n_of_rows].value = price
#     sheet["C%d" % n_of_rows].value = avgprice
# wb.save('C:\\Users\\LUS\\Desktop\\周报材料\\周分析会议数据.xlsx')
# get_business_data('销售合同')
