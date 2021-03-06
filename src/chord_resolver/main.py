# -*- generated by 1.0.12 -*-
import da
_config_object = {}
import random
import os
import socket
import struct
from hash_func import hash_func
node_client = da.import_da('client')
node_chord = da.import_da('chord')

def fileread(filename):
    data = []
    file = open(filename, 'r')
    for line in file:
        data.append(tuple(line.strip().split(' ')))
    return data

def runsetup(idx, m, node_tuples, hnkeys, hdata, hdkeys):
    setup_args = {}
    setup_args['pred_node'] = node_tuples[(idx - 1)]
    setup_args['succ_node'] = node_tuples[((idx + 1) % len(hnkeys))]
    setup_args['fingertable'] = runfingertable(idx, m, node_tuples, hnkeys)
    setup_args['node_datas'] = setndata(idx, hdata, hdkeys, hnkeys)
    return setup_args

def runfingertable(idx, m, node_tuples, hnkeys):
    hash_val = hnkeys[idx]
    fingertable = []
    for i in range(0, m):
        fingerindex = indexvalueffind('L', hnkeys, ((hash_val + (2 ** i)) % (2 ** m)))
        fingertable.append(node_tuples[(fingerindex % len(node_tuples))])
    return fingertable

def setndata(idx, hdata, hdkeys, hnkeys):
    startl = hnkeys[(idx - 1)]
    endl = hnkeys[idx]
    start = indexvalueffind('R', hdkeys, startl)
    end = indexvalueffind('R', hdkeys, endl)
    data = {}
    if (startl <= endl):
        for i in range(start, end):
            hash_val = hdkeys[i]
            data[hash_val] = hdata[hash_val]
    else:
        for i in range(start, len(hdkeys)):
            hash_val = hdkeys[i]
            data[hash_val] = hdata[hash_val]
        for i in range(0, end):
            hash_val = hdkeys[i]
            data[hash_val] = hdata[hash_val]
    return data

def queryinp():
    query = input('Query format <domain_name><space><query_type>: ')
    inputs = query.split(' ')
    return (inputs[0], inputs[1])

def indexvalueffind(type, sorted_hash_vals, value):
    try:
        idx = sorted_hash_vals.index(value)
        if ('L' in type):
            if (idx == 0):
                return 0
            else:
                return (idx + 1)
        elif ('R' in type):
            if (idx == 0):
                return (1 + 1)
            else:
                return ((idx + 1) + 1)
    except Exception as e:
        if (len(sorted_hash_vals) == 1):
            if (sorted_hash_vals[0] > value):
                return (0 + 1)
            else:
                return (1 + 1)
        else:
            for (idx, val) in enumerate(sorted_hash_vals):
                if (val > value):
                    if (idx == 0):
                        return 0
                    else:
                        return ((idx - 1) + 1)
            return len(sorted_hash_vals)

class Node_(da.NodeProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._events.extend([])
    _config_object = {'channel': {'reliable', 'fifo'}}

    def run(self):
        m = 64
        data = fileread('data/data_mapping.txt')
        hash_vals = []
        repeats = []
        nodes = []
        for i in data:
            hash_val = hash_func(i[0], m)
            if (not (hash_val in hash_vals)):
                hash_vals.append(hash_val)
            else:
                repeats.append((hash_val, i))
        self.output('hash function collison: ', len(repeats))
        hdata = {hash_func(data[0], m): data for data in data}
        hdkeys = list(hdata.keys())
        hdkeys.sort()
        nodes = []
        for i in range(0, 50):
            nodes.append(socket.inet_ntoa(struct.pack('>I', random.randint(1, 4294967295))))
        hnodes = {hash_func(node, m): node for node in nodes}
        hnkeys = list(hnodes.keys())
        hnkeys.sort()
        self.output('Hash values for all the nodes in sorted order: ', hnkeys)
        chord_processes = list(self.new(node_chord.Chord, num=len(hnkeys)))
        node_tuples = []
        for i in range(0, len(hnkeys)):
            node_tuples.append((hnkeys[i], chord_processes[i], nodes[i]))
        for i in range(0, len(hnkeys)):
            setup_args = runsetup(i, m, node_tuples, hnkeys, hdata, hdkeys)
            self._setup(chord_processes[i], args=(node_tuples[i], m, setup_args['pred_node'], setup_args['succ_node'], setup_args['fingertable'], setup_args['node_datas']))
        self._start(chord_processes)
        query_type = 'A'
        website = []
        k = 0
        for j in data:
            k += 1
            website.append(j[0])
            if (k == 1000):
                break
        client_process = self.new(node_client.Client)
        self._setup(client_process, args=(client_process, m, node_tuples, website, query_type))
        self._start(client_process)
        super()._label('_st_label_831', block=False)
        _st_label_831 = 0
        while (_st_label_831 == 0):
            _st_label_831 += 1
            if False:
                _st_label_831 += 1
            else:
                super()._label('_st_label_831', block=True)
                _st_label_831 -= 1
