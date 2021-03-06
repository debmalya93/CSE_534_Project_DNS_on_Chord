# -*- generated by 1.0.12 -*-
import da
PatternExpr_283 = da.pat.TuplePattern([da.pat.ConstantPattern('get'), da.pat.FreePattern('query')])
PatternExpr_351 = da.pat.TuplePattern([da.pat.ConstantPattern('find_next_node'), da.pat.FreePattern('query')])
_config_object = {}
import logging
import time
from constants import *
import random

class Chord(da.DistProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_ChordReceivedEvent_0', PatternExpr_283, sources=None, destinations=None, timestamps=None, record_history=None, handlers=[self._Chord_handler_282]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ChordReceivedEvent_1', PatternExpr_351, sources=None, destinations=None, timestamps=None, record_history=None, handlers=[self._Chord_handler_350])])

    def setup(self, node_tuple, m, pred_node, succ_node, finger_table, node_datas, **rest_503):
        super().setup(node_tuple=node_tuple, m=m, pred_node=pred_node, succ_node=succ_node, finger_table=finger_table, node_datas=node_datas, **rest_503)
        self._state.node_tuple = node_tuple
        self._state.m = m
        self._state.pred_node = pred_node
        self._state.succ_node = succ_node
        self._state.finger_table = finger_table
        self._state.node_datas = node_datas
        self._state.node_tuple = self._state.node_tuple
        self._state.m = self._state.m
        self._state.pred_node = self._state.pred_node
        self._state.succ_node = self._state.succ_node
        self._state.finger_table = self._state.finger_table
        self._state.node_datas = self._state.node_datas

    def run(self):
        self.output('{node} is up: pred={p}, succ={s}, finger_table={f}, node_datas={r}'.format(node=self._state.node_tuple, p=self._state.pred_node, s=self._state.succ_node, f=self._state.finger_table, r=list(self._state.node_datas.items())), level=logging.DEBUG)
        super()._label('_st_label_239', block=False)
        _st_label_239 = 0
        while (_st_label_239 == 0):
            _st_label_239 += 1
            if False:
                _st_label_239 += 1
            else:
                super()._label('_st_label_239', block=True)
                _st_label_239 -= 1

    def belongs_in_between(self, start, end, val_to_check):
        if (end < start):
            end += ((2 ** self._state.m) - 1)
        if (val_to_check < start):
            val_to_check += ((2 ** self._state.m) - 1)
        return ((val_to_check > start) and (val_to_check <= end))

    def closest_preceding_finger(self, hash_val):
        for i in range((self._state.m - 1), (- 1), (- 1)):
            if self.belongs_in_between(start=self._state.node_tuple[HASH_VAL], end=hash_val, val_to_check=self._state.finger_table[i][HASH_VAL]):
                return self._state.finger_table[i]

    def _Chord_handler_282(self, query):
        query['hops_ctr'] += 1
        query['hops_nodes'].append(self._state.node_tuple[IP])
        time.sleep(random.uniform(0.0001, 0.01))
        self.send(('result', query, self._state.node_datas.get(query['hash_val'], None), self._state.node_tuple), to=query['client_process'])
        self.output('{} forwarded query:{} to node: {}'.format(self._state.node_tuple, query, query['client_process']), level=logging.DEBUG)
    _Chord_handler_282._labels = None
    _Chord_handler_282._notlabels = None

    def _Chord_handler_350(self, query):
        query['hops_ctr'] += 1
        query['hops_nodes'].append(self._state.node_tuple[IP])
        time.sleep(random.uniform(0.0001, 0.01))
        if self.belongs_in_between(start=self._state.node_tuple[HASH_VAL], end=self._state.succ_node[HASH_VAL], val_to_check=query['hash_val']):
            node = self._state.succ_node
            self.send(('next_node', query, node), to=query['client_process'])
            self.output('{node} sent successor={succ_node} for query={query} to: {client}'.format(node=self._state.node_tuple, succ_node=node, query=query, client=query['client_process']), level=logging.DEBUG)
        else:
            node = self.closest_preceding_finger(query['hash_val'])
            self.send(('find_next_node', query), to=node[PROCESS_ID])
            self.output('{node} delegated find_next_node for query={query} to: {delegatee}'.format(node=self._state.node_tuple, query=query, delegatee=node), level=logging.DEBUG)
    _Chord_handler_350._labels = None
    _Chord_handler_350._notlabels = None
