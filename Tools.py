import json
import time
import pandas as pd
import xlrd
import os
from openpyxl import Workbook,load_workbook
'''
#1.读取Name.txt配置文件的内容
#2.给基站重新编写名称：类似XXX->GB-XXX
#3.给门铃重新编写名称：类似XXX->DB-XXX
#4.根据输入配置文件的GB_Device、DB_Device获取需要输出的名称列表-->PirWakeUpCnt,McuReseCnt,PirFalseWakeupCnt,McuRun,Battery,
# Uptime,MemFree,MemAvail,VmSize,CPU,CpuHight,MemLow,IotdPid,FdNum
#5.根据输入配置文件的GB_Device、DB_Device初始化字段的列表存储--》批量初始化列表
#6.读取JSON格式的文件进行分割
#7.从JSON里面获取到的数据添加到列表里面-->[['0-2-0-8', '30720', '26624', '48128', '1', '', '', '530', '29', '0', '9', '0', '13334', '100'],[*]]
#8.从列表数据输出到excel



'''
class Tools():
#1.读取Name.txt配置文件的内容
    def readfile(self)-> list:
        #1.存储源文件格式化后输出的列表数据
        filedatas = [] #存储源文件格式化后输出的列表数据
        Name_file = open('Name.txt','r',encoding='UTF-8')

        #1.1 存储的文件：GB_name = GB-G1XX，GB-G1XX2
        fileline = Name_file.read().split()#清空前后空字符和换行符
        for filelines in fileline:
             file_info = filelines.split("=")
             data_name = file_info[1].split(",")
             file_info[1] = data_name
             filedatas.append(file_info)
        return filedatas


#2   给基站重新编写名称：类似XXX->GB-XXX
#2.1 给门铃重新编写名称：类似XXX->DB-XXX
    def readDBName(self):
        tool = Tools()
        filedatas = tool.readfile()
        Name_list = filedatas[0][1]
        DB_list = []
        GB_list = []
        for name in Name_list:
            if len(DB_list) < len(Name_list):
                DB_name = "DB-" + name
                GB_name = 'GB-' + name
                DB_list.append(DB_name)
                GB_list.append(GB_name)
            else:
                break
        DB_list.append(GB_list)
        return DB_list


#4.根据输入配置文件的GB_Device、DB_Device获取需要输出的名称列表-->PirWakeUpCnt,McuReseCnt,PirFalseWakeupCnt,McuRun,Battery,
# Uptime,MemFree,MemAvail,VmSize,CPU,CpuHight,MemLow,IotdPid,FdNum
    def readDeviceName(self)->list:
        tool = Tools()
        filedatas = tool.readfile()
        #GB_Device的输出
        GB_Device_name = filedatas[1][1] # 内容：PirWakeUpCnt,McuReseCnt,PirFalseWakeupCnt,McuRun,Battery
        DB_Device_name = filedatas[2][1] # 内容：Uptime,MemFree,MemAvail,VmSize,CPU,CpuHight,MemLow,IotdPid,FdNum
        Devicename = DB_Device_name +GB_Device_name
        return Devicename


#5.根据输入配置文件的GB_Device、DB_Device初始化字段的列表存储--》批量初始化列表
    def readDevice(self)->list:
        tool = Tools()
        filedatas = tool.readfile()
        #GB_Device的输出
        GB_Device_list = filedatas[1][1]
        DB_Device_list = filedatas[2][1]
        GBDevice = []
        DBDevice = []
        for name in GB_Device_list:
            name = []
            GBDevice.append(name)
        for name in DB_Device_list:
            name = []
            DBDevice.append(name)
        Device = DBDevice +  GBDevice
        # print(Device)
        return Device

#6.读取JSON格式的文件进行分割
    def readJson(self)->list:
# 6.1 读取JSON文件源json编码格式给到"ANSI"
        json_file = 'JSON1.json'
        with open(json_file, 'r', encoding='utf-8') as json_obj:
            json_data = json.load(json_obj)
            #6.2 使用Tool工具类从Name.txt里面读取数据,
            tool= Tools()
            DB_name = tool.readDBName()#格式 DB-XXXX
            # 初始化门铃和基站存储的数组
            data = []
            # 按照json的key遍历源数据：数据清洗，门铃字段【"Battery"】,基站字段【"Sys"】
            for key in json_data.keys():
                if key in DB_name:
                    data_DB = json_data[key]['Battery']
                    data.append(data_DB)
                else:
                    data_GB = json_data[key]['Sys']
                    data_DB.update(data_GB)
        return data


#7.从JSON里面获取到的数据添加到列表里面-->[['0-2-0-8', '30720', '26624', '48128', '1', '', '', '530', '29', '0', '9', '0', '13334', '100'],[*]]
    def writedata(self)->list:
        tool = Tools()
        # 1.获取清洗后的JSON数据--》
        data = tool.readJson()
        # 2. 使用函数初始化出基站和门铃需要填充的数据列表
        Device = tool.readDevice()
        Name_file = tool.readfile()
        Name_ID = Name_file[0][1]
        Devicename = tool.readDeviceName()
        DTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        # 3.根据需要输出的基站和门铃数据，填写对应的JSON进入到数据列表
        data_len = int(len(data))
        # 3.1 第一层遍历：首先依据填充的数据列表，遍历数据列表
        for De in Device:
            i = 0
            # 3.2 第二层遍历：根据数据源的条数，进行遍历，使之不超过范围
            while i < data_len:
                Device[i] = []
                for nameD in Devicename:
                    Device[i].append(data[i][nameD])
                i = i + 1
        i = 0
        DTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        while i < data_len:
            for nameID in Name_ID:
                Device[i].insert(0, DTime)
                Device[i].insert(1,nameID)
                i = i + 1
        #4 清除后续的
        del Device[-((len(Device)-len(data))):-1]
        # 4.1 调试代码：控制此次输出和上次输出的间隔行数
        # Device.pop(-1)
        return Device

#8.从列表数据输出到excel
    def ToExcel(self):
        tool = Tools()
        Device = tool.writedata()
        Devicename = tool.readDeviceName()
        DTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # 1.文件写入方式写为’a‘,可以直接追加数据到文件
        file = open("JSONdata.xlsx", 'a',encoding='utf-8')

        name_str = ''
        for name in Devicename:
            name_str = name_str + name + '\t'
        name_str = '日期' + '\t' + '设备ID' + '\t' + name_str + '\n'
        file.write(name_str)
        for m in range(len(Device)):
            for n in range(len(Device[m])):
                file.write(str(Device[m][n]))
                file.write('\t')
            file.write('\n')
            print(Device[m])
        file.close()


        print(DTime+'   文件顺利输出，请及时查看！')



if __name__ == '__main__':
    #调用工具类实现ToExcel()方法输出excel文件
    tool = Tools()
    tool.ToExcel()
    os.system('pause')
