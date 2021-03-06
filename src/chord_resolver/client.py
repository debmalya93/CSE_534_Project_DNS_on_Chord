# -*- generated by 1.0.12 -*-
import da
PatternExpr_321 = da.pat.TuplePattern([da.pat.ConstantPattern('next_node'), da.pat.FreePattern('query'), da.pat.FreePattern('succ_node')])
PatternExpr_345 = da.pat.TuplePattern([da.pat.ConstantPattern('result'), da.pat.FreePattern('query'), da.pat.FreePattern('result'), da.pat.FreePattern('authority')])
_config_object = {}
import logging
import random
import time
from hash_func import hash_func
from constants import *

class Client(da.DistProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_ClientReceivedEvent_0', PatternExpr_321, sources=None, destinations=None, timestamps=None, record_history=None, handlers=[self._Client_handler_320]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ClientReceivedEvent_1', PatternExpr_345, sources=None, destinations=None, timestamps=None, record_history=None, handlers=[self._Client_handler_344])])

    def setup(self, client_process, m, node_tuples, website, query_type, **rest_511):
        super().setup(client_process=client_process, m=m, node_tuples=node_tuples, website=website, query_type=query_type, **rest_511)
        self._state.client_process = client_process
        self._state.m = m
        self._state.node_tuples = node_tuples
        self._state.website = website
        self._state.query_type = query_type
        self._state.client_process = self._state.client_process
        self._state.m = self._state.m
        self._state.node_tuples = self._state.node_tuples
        self._state.website = self._state.website
        self._state.query_type = self._state.query_type
        self._state.ctr = 0
        self._state.start = {}
        self._state.end = {}
        self._state.resolution_latencies = set()
        self._state.hops_ctr = 0
        self._state.hops_nodes = []

    def run(self):
        self.output(self._state.client_process, ' has been started.')
        for name in self._state.website:
            query = self.create_query(name)
            seed = random.choice(self._state.node_tuples)
            self._state.ctr += 1
            self._state.start[query['request_id']] = time.time()
            self.send(('find_next_node', query), to=seed[1])
            self.output('Sent find_next_node message for query: {q} to {node}'.format(q=query, node=seed), level=logging.DEBUG)
            super()._label('_st_label_307', block=False)
            _st_label_307 = 0
            while (_st_label_307 == 0):
                _st_label_307 += 1
                if (query['request_id'] in self._state.end):
                    _st_label_307 += 1
                else:
                    super()._label('_st_label_307', block=True)
                    _st_label_307 -= 1
            else:
                if (_st_label_307 != 2):
                    continue
            if (_st_label_307 != 2):
                break
        super()._label('_st_label_316', block=False)
        _st_label_316 = 0
        while (_st_label_316 == 0):
            _st_label_316 += 1
            if False:
                _st_label_316 += 1
            else:
                super()._label('_st_label_316', block=True)
                _st_label_316 -= 1

    def create_query(self, name):
        query = {'website': name, 'hash_val': hash_func(name, self._state.m), 'request_id': self.obtain_request_id(), 'client_process': self._state.client_process, 'hops_ctr': self._state.hops_ctr, 'hops_nodes': self._state.hops_nodes}
        return query

    def obtain_request_id(self):
        return ((str(self._state.client_process) + '-') + str(self._state.ctr))

    def _Client_handler_320(self, query, succ_node):
        self.send(('get', query), to=succ_node[1])
        self.output('Sent get to: ', succ_node, level=logging.DEBUG)
    _Client_handler_320._labels = None
    _Client_handler_320._notlabels = None

    def _Client_handler_344(self, query, result, authority):
        self._state.end[query['request_id']] = time.time()
        if (self._state.query_type == 'A'):
            outval = result[A]
        elif (self._state.query_type == 'MX'):
            outval = result[MX]
        else:
            outval = result[NS]
        self.output('Result of query for {query} = {outval}'.format(query=query['website'], outval=outval))
        self._state.resolution_latencies.add((self._state.end[query['request_id']] - self._state.start[query['request_id']]))
        self.output('website : {website}, time : {TotalTime}, hop cnt : {hops_ctr}'.format(website=query['website'], hops_ctr=query['hops_ctr'], TotalTime=int(round(((self._state.end[query['request_id']] - self._state.start[query['request_id']]) * 1000), 0))))
    _Client_handler_344._labels = None
    _Client_handler_344._notlabels = None
