<?xml version="1.0" encoding="ISO-8859-1" ?>
<scenario name="ring then wait for cancel">

<recv request="INVITE">
</recv>

<send>
  <![CDATA[
    SIP/2.0 180 Ringing
    [last_Via:]
    [last_To:];tag=[call_number]
    [last_From:]
    [last_Call-ID:]
    [last_CSeq:]
    Contact: <sip:[local_ip]:[local_port]>
    Content-Length: 0

  ]]>
</send>

<recv request="CANCEL">
</recv>

<send>
  <![CDATA[
    SIP/2.0 200 OK
    [last_Via:]
    [last_To:];tag=[call_number]
    [last_From:]
    [last_Call-ID:]
    [last_CSeq:]
    Contact: <sip:[local_ip]:[local_port]>
    Content-Length: 0

  ]]>
</send>

<send>
  <![CDATA[
    SIP/2.0 487 Request Terminated
    [last_Via:]
    [last_To:];tag=[call_number]
    [last_From:]
    [last_Call-ID:]
    [last_CSeq:]
    Content-Length: 0

  ]]>
</send>

</scenario>
