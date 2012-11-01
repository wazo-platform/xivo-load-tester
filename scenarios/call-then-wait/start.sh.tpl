#!/bin/sh

{% if rtp %}
SUDO=sudo
{% endif %}

$SUDO sipp -inf users.csv -sf scenario.xml -p {{ bind_port }} {{ sipp_std_options }} {{ sipp_remote_host }}

