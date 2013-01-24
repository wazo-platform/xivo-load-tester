# -*- coding: UTF-8 -*-

from __future__ import unicode_literals

## global configuration

sipp_remote_host = '10.101.0.225'

sipp_local_ip = '10.101.0.241'
sipp_call_rate = 1.0
sipp_rate_period_in_ms = 1000
#sipp_max_simult_calls = 3
#sipp_nb_of_calls_before_exit = 4
#sipp_enable_trace_calldebug = True
#sipp_enable_trace_err = True
#sipp_enable_trace_shortmsg = True
sipp_enable_trace_stat = True


## global scenarios configuration

answer_bind_port = 5060
call_bind_port = 5063

calling_line = {
    'username': 'trunk1',
    'password': 'trunk1',
}

pause = {
    'distribution': 'fixed',
    'value': 5000,
}
#pause = {
#    'distribution': 'uniform',
#    'min': 3000,
#    'max': 7000,
#}
#pause = {
#    'distribution': 'normal',
#    'mean': 5000,
#    'stdev': 1000,
#}

answer_ring_time = {'distribution': 'uniform', 'min': 1000, 'max': 3000}
answer_talk_time = {'distribution': 'uniform', 'min': 10 * 1000, 'max': 30 * 1000}
call_talk_time = {'distribution': 'uniform', 'min': 10 * 1000, 'max': 16 * 1000}

#rtp = None
#rtp = 'test3s-gsm.pcap'
rtp = '/home/trafgen/xivo-loadtest/load-tester/pcap-audio/test3s-gsm.pcap'
#rtp = 'silence600s-gsm.pcap'


## scenarios configuration

scenarios.answer_then_hangup = dict(
    bind_port = answer_bind_port,
    ring_time = answer_ring_time,
    talk_time = answer_talk_time,
    rtp = rtp,
)

scenarios.answer_then_wait = dict(
    bind_port = answer_bind_port,
    ring_time = answer_ring_time,
    rtp = rtp,
)

scenarios.call_then_hangup = dict(
    bind_port = call_bind_port,
    calling_line = calling_line,
    called_extens = range(1500, 1503),
    talk_time = call_talk_time,
    rtp = rtp,
    sipp_call_rate = 1.0,
    sipp_rate_period_in_ms = 2000,
)
