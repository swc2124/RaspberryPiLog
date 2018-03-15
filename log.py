# ====================================================================
# Author                : swc21
# Date                  : 2018-03-14 09:42:28
# Project               : ClusterFiles
# File Name             : log
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
import time

from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
name = MPI.Get_processor_name()
LOG_FILE = 'SHARED/LOG_FILE.txt'
#--[FUNCTION]--------------------------------------------------------------#
comm.Barrier()
time.sleep(rank*1.5)
with open(LOG_FILE, 'r') as file:
    data = file.readlines()
data[rank] = str(rank)+'	'+str(name)+'	' + \
    str(time.strftime("%Y-%m-%d %H:%M"))+'\n'
with open(LOG_FILE, 'w') as file:
    try:
        file.writelines(data)
    except:
        time.sleep(3)
        file.writelines(data)
