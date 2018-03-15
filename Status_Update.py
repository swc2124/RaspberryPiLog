# ====================================================================
# Author                : swc21
# Date                  : 2018-03-14 09:42:27
# Project               : ClusterFiles
# File Name             : Status_Update
# Last Modified by      : swc21
# Last Modified time    : 2018-03-14 12:03:25
# ====================================================================
# 
#--[DESCRIPTION]---------------------------------------------------------#

'''
Date: May 2016

Writes a log file for all node on the cluster

'''

#--[PROGRAM-OPTIONS]------------------------------------------------------#

import os
import psutil
import re
import sys
import time

from mpi4py import MPI
from subprocess import PIPE
from subprocess import Popen
from termcolor import colored
from time import gmtime
from time import strftime

#--[PROGRAM-OPTIONS]------------------------------------------------------#

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
name = MPI.Get_processor_name()
LOG_FILE = 'SHARED/LOG_FILE.txt'

#--[FUNCTION]--------------------------------------------------------------#
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)


def printout(text, colour=WHITE):
    return str("\x1b[1;%dm" % (30+colour) + text + "\x1b[0m")


def bytes2human(n):
    # From sample script for psutils
    """
    >>> bytes2human(10000)
    '9.8 K'
    >>> bytes2human(100001221)
    '95.4 M'
    """
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.2f %s' % (value, s)
    return '%.2f B' % (n)


def get_cpu_temperature():
    process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)
    output, _error = process.communicate()
    return float(output[output.index('=') + 1:output.rindex("'")])


def get_cpu_freq():
    process = Popen(['vcgencmd', 'measure_clock arm'], stdout=PIPE)
    output, _error = process.communicate()
    return str(output)


def get_cpu_volts():
    process = Popen(['vcgencmd', 'measure_volts core'], stdout=PIPE)
    output, _error = process.communicate()
    return str(output)


def Network_Traf(more=False):
    tot_before = psutil.net_io_counters()
    pnic_before = psutil.net_io_counters(pernic=True)
    interval = 0.2
    time.sleep(interval)
    tot_after = psutil.net_io_counters()
    pnic_after = psutil.net_io_counters(pernic=True)
    if more == True:
        print "   sent: %-10s" % (bytes2human(tot_after.bytes_sent))
        print "   recv: %-10s" % (bytes2human(tot_after.bytes_recv))
        nic_names = list(pnic_after.keys())
        nic_names.sort(key=lambda x: sum(pnic_after[x]), reverse=True)
        print "Interface:"
        for name in nic_names:
            stats_before = pnic_before[name]
            stats_after = pnic_after[name]
            print name
            print("   Bytes-sent: %15s (total)  %15s  (Per-Sec)" %
                  (bytes2human(stats_after.bytes_sent),
                   bytes2human(stats_after.bytes_sent -
                               stats_before.bytes_sent) + '/s'))
            print("   Bytes-recv: %15s (total)  %15s  (Per-Sec)" %
                  (bytes2human(stats_after.bytes_recv),
                   bytes2human(stats_after.bytes_recv -
                               stats_before.bytes_recv) + '/s'))
    return str(bytes2human(tot_after.bytes_sent)), str(bytes2human(tot_after.bytes_recv))


def Print_Out():
    cpu_temperature = get_cpu_temperature()
    print 'cpu temp  : '+str(cpu_temperature)+' deg C'
    cpu_freq = get_cpu_freq()
    print 'cpu clock : '+str(float(cpu_freq[14:])/1e6)+'MHz'
    cpu_usage = psutil.cpu_percent()
    print 'cpu usage : '+str(cpu_usage)+'%'
    core_volts = get_cpu_volts()[5:11]
    print 'cpu volts : '+str(core_volts)+'V'
    ram = psutil.phymem_usage().percent
    print 'free ram  : '+str(ram)+'%'
    sent, recv = Network_Traf()
    print 'bytes sent: '+str(sent)
    print 'bytes recv: '+str(recv)


def Log_File():
    cpu_temp = str(get_cpu_temperature())
    cpu_usage = str(psutil.cpu_percent())
    cpu_freq = str(float(get_cpu_freq()[14:])/1e6)
    core_volts = str(get_cpu_volts()[5:11])
    free_ram = str(psutil.phymem_usage().percent)
    sent, recv = Network_Traf()
    return [cpu_temp, cpu_usage, cpu_freq, core_volts, free_ram, sent, recv]


def Log_Info():
    message = [rank, str(name), Log_File()]
    logs = comm.gather(message, root=0)
    if rank == 0:
        data = []
        data.append(strftime("%Y-%m-%d %H:%M:%S", gmtime())+'\n')
        for line in logs:
            data.append(printout(
                str(line[1])+'		 '+str(line[0])+'	 '+str(line[2][0])+' 	 ' +
                str(line[2][1])+' 		 '+str(line[2][2])+'	 ' +
                str(line[2][3])+' 	 '+str(line[2][4])+'	 ' +
                str(line[2][5])+' 		 '+str(line[2][6])+'\n', GREEN))
        with open(LOG_FILE, 'w') as file:
            file.writelines(data)


# print colored('hello', 'red'), colored('world', 'green')
for i in range(10):
    time.sleep(3)
    Log_Info()
    comm.Barrier()
# comm.Barrier()
'''
for i in range(100):
	time.sleep(rank*2.5)
	with Open(LOG_FILE, 'r') as file:
	Open(type cls, Intracomm comm, filename, int amode=MODE_RDONLY, Info info=INFO_NULL)
		data = file.readlines()
		info = Log_File()
	data[rank] = str(rank)+'	'+str(name)+'	'+info[0]+'	'+info[1]+'	'+info[2]+'	'+info[3]+'	'+info[4]+'	'
	with open(LOG_FILE, 'w') as file:
		try:
			file.writelines( data )
		except:
			time.sleep(3)
			file.writelines( data )
'''
