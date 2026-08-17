SEQUENTIAL
{% for called_exten in called_extens -%}
{{ calling_line.caller_id | default(calling_line.username) }};[authentication username={{ calling_line.username }} password={{ calling_line.password }}];{{ called_exten }}
{% endfor %}

