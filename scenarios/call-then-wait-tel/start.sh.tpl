#!/bin/sh

sipp -inf users.csv -sf scenario.xml -p {{ bind_port }} {{ sipp_std_options }} {{ sipp_remote_host }}

