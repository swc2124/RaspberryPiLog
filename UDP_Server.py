# ====================================================================
# Author 				: swc21
# Date 					: 2018-03-14 09:42:01
# Project 				: ClusterFiles
# File Name 			: UDP_Server
# Last Modified by 		: swc21
# Last Modified time 	: 2018-03-14 10:28:52
# ====================================================================
#
# SOl Courtney Columbia U Department of Astronomy and Astrophysics NYC 2016
# swc2124@columbia.edu
#--[DESCRIPTION]---------------------------------------------------------#
'''
Date: May 2016
UDP Server for the Cluster
'''
#--[PROGRAM-OPTIONS]------------------------------------------------------#
import socket
from time import gmtime, strftime, sleep
from astropy.table import Table
import sys
import os
LOG_FILE = '/home/sol/CLUSTER_RAID/'
#--[PROGRAM-OPTIONS]------------------------------------------------------#
'''
LookUp = {
	'Wolf-01':'3',
	'Wolf-02':'4',
	'Wolf-03':'5',
	'Wolf-04':'6',
	'Wolf-05':'7',
	'Wolf-06':'8',
	'Wolf-07':'9', 
	'Wolf-08':'10',
	'Wolf-09':'11', 
	'Wolf-10':'12', 
	'Wolf-11':'13', 
	'Wolf-12':'14', 
	'Wolf-13':'15', 
	'Wolf-14':'16', 
	'Wolf-15':'17', 
	'Wolf-16':'18',
	'BPI-M1-01':'19',
	'BPI-M1-02':'20',
	'BPI-M1-03':'21',
	'BPI-M1-04':'22',
	'BPI-M1-05':'23',
	'BPI-M1-06':'24',
	'BPI-M1-07':'25',
	'BPI-M1-08':'26',
	'BPI-M1-09':'27',
	'BPI-M1-10':'28',
	'BPI-M1-11':'29',
	'BPI-M1-12':'30',
	'BPI-M1-13':'31',
	'BPI-M1-14':'32',
	'BPI-M1-15':'33',
	'BPI-M1-16':'34'
}
'''
LookUp = {
    'Wolf-01': '3',
    'Wolf-02': '4',
    'Wolf-03': '5',
    'Wolf-04': '6',
    'Wolf-05': '7',
    'Wolf-06': '8',
    'Wolf-07': '9',
    'Wolf-08': '10',
    'Wolf-09': '11',
    'Wolf-10': '12',
    'Wolf-11': '13',
    'Wolf-12': '14',
    'Wolf-13': '15',
    'Wolf-14': '16',
    'Wolf-15': '17',
    'Wolf-16': '18',
}
Log_Book = {
    '0': '',
    '1': '',
    '2': '',
    '3': '',
    '4': '',
    '5': '',
    '6': '',
    '7': '',
    '8': '',
    '9': '',
    '10': '',
    '11': '',
    '12': '',
    '13': '',
    '14': '',
    '15': '',
    '16': '',
    '17': '',
    '18': '',
    '19': '',
    '20': '',
    '21': '',
    '22': '',
    '23': '',
    '24': '',
    '25': '',
    '26': '',
    '27': '',
    '28': '',
    '29': '',
    '30': '',
    '31': '',
    '32': '',
    '33': '',
    '34': ''
}
os.system('clear')
# Create a TCP/IP socket


def getNetworkIp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.connect(('<broadcast>', 0))
    return s.getsockname()[0]


s = socket.socket()
host = str(getNetworkIp())
port = 15000
server_address = (str(host), port)
hostname = socket.gethostname()
os.system('clear')
print >>sys.stderr, ' --> [STARTING UP] [%s] : [PORT] (%s)' % server_address
s.bind(server_address)
s.listen(30)
Names = ['hostname', 'jobs_done', 'cpu_temp', 'cpu_usage',
         'cpu_freq', 'core_volts', 'free_ram', 'bytes_sent', 'bytes_recv']
Dtype = ['S10', 'float', 'float', 'float',
         'float', 'float', 'float', 'float', 'int']
Log_Table = Table(names=Names, dtype=Dtype)
hosts = [LookUp.keys()]
x = 0
while True:
    conn, client_address = s.accept()
    print >>sys.stderr, '\n 	--> [CONNECTIING] [%s] : [PORT] (%s)' % client_address
    data = conn.recv(1024)
    if data:
        try:
            Log_Table.add_row([
                data.split(' ')[0], int(data.split(' ')[1]),
                float(data.split(' ')[2]), float(data.split(' ')[3]),
                float(data.split(' ')[4]), float(data.split(' ')[5]),
                float(data.split(' ')[6]), float(data.split(' ')[7]),
                float(data.split(' ')[8])])
            try:
                hosts[0].remove(data.split(' ')[0])
            except:
                pass
#			os.system('clear')
#			print Log_Table
            if len(hosts[0]) < 1:
                hosts = [LookUp.keys()]
                Log_Table.write(LOG_FILE+'Log_Table.hdf5', format='hdf5',
                                path=strftime("%Y%b%a%d", gmtime()), append=True, overwrite=True)
                Log_Table = Table(names=Names, dtype=Dtype)
        finally:
            conn.close()
            os.system('clear')
            print Log_Table
