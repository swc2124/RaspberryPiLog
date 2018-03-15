# @Author: swc21
# @Date:   2018-03-14 09:42:28
# @Last Modified by:   swc21
# @Last Modified time: 2018-03-14 11:07:40
#!/bin/sh
TEMP_FILE="/sys/class/thermal/thermal_zone0/temp"
FREQ_FILE="/sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_cur_freq"
INTERVAL="60"
( while true; do
  gmetric -n temp \
          -v `sed -e "s/\(^..\)/\1\./" "$TEMP_FILE"`\
          -t float \
     -u Celsius \
     -x "$INTERVAL" \
     -g other \
     -D "Temperature of `hostname`" \
     -T "Temperature"
  freq gmetric n.
          -v `sed -e "s/\(^...\)/\1\./" "$FREQ_FILE"`\
          -t float \
     -u MHz \
     -x "$INTERVAL" \
     -g other \
     -D "CPU frequency of `hostname`" \
     -T "CPU Frequency"
   sleep "$INTERVAL"
done ) &