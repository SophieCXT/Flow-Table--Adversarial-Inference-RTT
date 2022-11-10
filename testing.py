
import subprocess
import numpy
import socket
from time import sleep
import mysocket
import stats
import utils
import os
import time
from socket import SHUT_RDWR

def roundtrip(msgsizes, type, host, port, *args, **kwargs):
    type = utils.type_map[type]
    msgsizes = sorted(msgsizes)

    labels = numpy.fromiter((2**msgsize for msgsize in msgsizes),
                            numpy.float)
    #a = ["5 miss H M M M M M","5 miss M H M M M M", "5 miss M M H M M M", "5 miss M M M H M M", "5 miss N M M M H M", "5 miss M M M M M H" ]
    #a = ["2 miss M M H H H M","4 miss H M H M M M", "4 miss H M M H M M", "4 miss H M M M H M", "4 miss H M M M M H", "4 miss M H H M M M", "4 miss M H M H M M","4 miss M H M M H M","4 miss M H M M M H","4 miss M M H H M M","4 miss M M H M H M","4 miss M M H M M H","4 miss M M M H H M","4 miss M M M H M H","4 miss M M M M H H" ]
    #a = ["2 Hiss M M H H H H","2 Hiss M H M H H H", "2 Hiss M H H M H H", "2 Hiss M H H H M H", "2 Hiss M H H H H M", "2 Hiss H M M H H H", "2 Hiss H M H M H H","2 Hiss H M H H M H","2 Hiss H M H >
    a = ["2 Hiss M M H H H H","2 Hiss M H M H H H", "2 Hiss M H H M H H", "2 Hiss M H H H M H", "2 Hiss M H H H H M", "2 Hiss H M M H H H", "2 Hiss H M H M H H","2 Hiss H M H H M H", "2 Hiss H M H M H H H M","2 Hiss H H M M H H","2 Hiss H H M H M H","2 Hiss H H M H H M","2 Hiss H H H M M H","2 Hiss H H H M H M","2 Hiss H H H H M M"]
    #a = ["3 Miss H H H M M M","3 Miss H H M H M M", "3 Miss H H M M H M", "3 Miss H H M M M H", "3 Hiss H M H H M M", "3 Miss H M H M H M", "3 Hiss H M H M M H","3 Hiss H M M H H M", "3 Hiss H M M H M H","3 Miss H M M M H H","3 Miss M H H H M M","3 Hiss M H H M H M","3 Hiss M H H M M H","3 Hiss M H M H H M","3 Hiss M H M H M H","3 Hiss M H M M H H", "3 Hiss M M H M H M","3 Hiss M M H H M H","3 Hiss M M H M H H","3 Hiss M M M H H H" ]
    #a = ["miss_0_H_H_H_H","miss_3_H_M_M_M","miss_3_M_H_M_M","miss_3_M_M_H_M","miss_3_M_M_M_H", "miss_1_M_H_H_H","miss_1_H_M_H_H","miss_1_H_H_M_H","miss_1_H_H_H_M", "miss_2_H_H_M_M","miss_2_H_M_H_M","miss_2_H_M_M_H","miss_2_M_H_H_M", "miss_2_M_H_M_H", "miss_2_M_M_H_H", "miss_4_M_M_M_M"]
    cmd = "arping " + str(host) + " -c 1 -q"
    os.system(cmd)
    sleep(1)
    with open("exp2.txt",'a') as f:
        f.write("#################################")
    for c in range(5001, 5021):
        data = numpy.array(
            [list(roundtrip_generator(msgsize, 1, type, host, port, c))
             for msgsize in [msgsizes[-1]]])
        with open("exp2.txt",'a') as f:
            #f.write(str(i))
            data = data.tolist()
            #f.write("######################################\n")
            f.write(str(data[0][0]))
            f.write('\n')
            o1 = subprocess.check_output('ovs-ofctl -O OpenFlow14 dump-flows s1',shell=True)
            o2 = subprocess.check_output('ovs-ofctl -O OpenFlow14 dump-flows s2',shell=True)
            f.write("sw1\n")
            f.write(o1.decode('utf-8'))
            f.write("\nsw2\n")
            f.write(o2.decode('utf-8'))
            f.write("\n")
        c +=1
    #sleep(2)
    for c in range(5020, 5000, -1):
        data = numpy.array(
            [list(roundtrip_generator(msgsize, 1, type, host, port, c))
             for msgsize in [msgsizes[-1]]])
        with open("exp2.txt",'a') as f:
            data = data.tolist()
            f.write(str(data[0][0]))
            f.write(',')
        c +=1
    return data, labels
    '''
    data = numpy.array(
        [list(roundtrip_generator(msgsize, 1000, type, host, port))
         for msgsize in [msgsizes[-1]]])
    print("sanchal data", data)
    print("sanchal label", labels)
    with open("res.txt",'a') as f:
        f.write("1 miss H H H M H H \n")
        f.write(str(data.tolist()))
        f.write('\n')
    return data, labels
    '''

def roundtrip_generator(msgsize, iterations, type, host, port, c):
    #sock = mysocket.clientsocket(type=type, host=host, port=port,sport=5003)
    #sock2 = mysocket.clientsocket(type=type, host=host, port=port,sport=5004)
    sock = None
    tries = 4
    i = 0
    while iterations > 0:
        try:
            #os.system('ovs-ofctl -O OpenFlow14 del-flows s1')
            #os.system('ovs-ofctl -O OpenFlow14 del-flows s2')
            #os.system('ovs-ofctl -O OpenFlow14 del-flows s3')
            sleep(0.6)
            #os.system('ovs-ofctl -O OpenFlow14 add-flow s1 priority=0,action=CONTROLLER:65535')
            #os.system('ovs-ofctl -O OpenFlow14 add-flow s2 priority=0,action=CONTROLLER:65535')
            #os.system('ovs-ofctl -O OpenFlow14 add-flow s3 priority=0,action=CONTROLLER:65535')
            #start = time.time()
            sock = mysocket.clientsocket(type=type, host=host, port=port,sport=c)
            #sleep(0.3)
            if i % 2 == 0:
                #sock.roundtrip(msgsize,c)
                i = 1
            else:
                #sock.roundtrip(msgsize,c)
                i = 0
            RTT = sock.RTT
            #end = time.time()
            #RTT = end - start
            print(RTT*1000, " ", iterations, c)
            try:
    	        sock.shutdown(SHUT_RDWR)
    	        sock.close()
            except Exception:
                pass
            #sock.close()
            RTT = RTT * 1000
            #os.system('ovs-ofctl -O OpenFlow14 del-flows s1')
            #os.system('ovs-ofctl -O OpenFlow14 del-flows s2')
            #sleep(0.2)
            #os.system('ovs-ofctl -O OpenFlow14 add-flow s1 priority=0,action=CONTROLLER:65535')
            #os.system('ovs-ofctl -O OpenFlow14 add-flow s2 priority=0,action=CONTROLLER:65535')
            if RTT is not None:
                iterations -= 1
                yield RTT
            elif tries > 0:
                tries -= 1
            else:
                iterations -= 1
        finally:
            tries = 4
            if sock is not None:
                sock.close()

def throughput(msgsizes, type, host, port, *args, **kwargs):
    type = utils.type_map[type]
    labels = numpy.fromiter((2**msgsize for msgsize in sorted(msgsizes)),
                            numpy.float)

    data = numpy.array(
        [list(throughput_generator(msgsize, 100, type, host, port))
         for msgsize in sorted(msgsizes)])

    return data, labels

def throughput_generator(msgsize, iterations, type, host, port):
    sock = None
    while iterations > 0:
        try:
            sock = mysocket.clientsocket(type=type, host=host, port=port)
            throughput = sock.throughput(msgsize)
            print(throughput)
            if throughput is not None:
                iterations -= 1
                yield throughput
        finally:
            if sock is not None:
                sock.close()

def sizes(counts, host, port, *args, **kwargs):
    counts = sorted(counts)
    labels = numpy.fromiter((2**n for n in counts), int)
    
    latency = stats.mean(list(
        roundtrip_generator(8, 100, socket.SOCK_STREAM, host, port)))/2
    data = numpy.array([list(sizes_generator(n, 100, host, port))
                        for n in counts]) - latency
    data = 2**20 / data

    return data, labels

def sizes_generator(count, iterations, host, port):
    sock = None
    for i in range(iterations):
        try:
            sock = mysocket.clientsocket(host=host, port=port)
            time = sock.sizes(count)
            print(time)
            if time is not None:
                yield time
        finally:
            if sock is not None:
                sock.close()
