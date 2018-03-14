# ====================================================================
# Author 				: swc21
# Date 					: 2018-03-14 09:45:26
# Project 				: ClusterFiles
# File Name 			: shutdown
# Last Modified by 		: swc21
# Last Modified time 	: 2018-03-14 10:10:29
# ====================================================================
#
import socket
import os
from time import sleep
ip = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(
    ('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]
_time = 33 - int(str(ip).split('.')[-1][-1])
sleep(_time)
os.system('shutdown -r now')
