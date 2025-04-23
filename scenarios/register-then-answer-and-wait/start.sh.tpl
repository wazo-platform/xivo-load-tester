#!/bin/sh

sipp -inf users.csv -sf register.xml -oocsf uas.xml {{ sipp_std_options }} {{ sipp_remote_host }}

