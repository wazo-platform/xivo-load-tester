#!/bin/sh

{% if rtp %}
SUDO=sudo
{% endif %}

$SUDO sipp -inf users.csv -sf scenario.xml {{ sipp_std_options }} {{ sipp_remote_host }}

