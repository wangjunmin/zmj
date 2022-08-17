import json

import modbus_tk.modbus_tcp as mt
import modbus_tk.defines as md


PLC_IP = ""
PLC_PORT = 502

PLC_SLAVE = 1

dic = []

master = None

def read_config():
    '''
    读配置文件，获取配置信息
    '''
    global PLC_IP
    global PLC_PORT

    global PLC_SLAVE 

    global dic

    zmj_file = open("zmj.json","r",encoding="utf-8")
    zmj_config = json.load(zmj_file)
    PLC_IP = zmj_config["plc_ip"]
    if zmj_config["port"]:
        PLC_PORT = int(zmj_config["port"])
    
    if zmj_config["slave_addr"]:
        PLC_SLAVE = int(zmj_config["slave_addr"])
    
    dic = zmj_config["dict"]

def connect_plc():
    '''
    建立与PLC服务器的连接
    '''
    global master
    master = mt.TcpMaster(PLC_IP,PLC_PORT)
    master.set_timeout(5.0)

def data_collect(start, quantity):
    '''
    从PLC 服务器中获取数据
    '''
    if not master:
        connect_plc()
    data_sam = master.execute(slave=PLC_SLAVE,function_code = md.READ_HOLDING_REGISTERS,starting_address=start,quantity_of_x=quantity)
    return data_sam

def get_plc_value(item):
    '''
    根据配置的条目信息，获取数据
    '''
    start = int(item["p_addr"])
    quantity = item["data_len"]
    desc = item["desc"]
    mutl = item["mult"]

    plc_value = data_collect(start,quantity)
    plc_list = list(plc_value)
    adjust_list = [x*mutl for x in plc_list]
    print("%s 的值为：%s%s" %(desc, str(adjust_list),item["unit"]))


def main():
    read_config()
    connect_plc()
    for item in dic:
        get_plc_value(item)  


if __name__=='__main__':
    main()
