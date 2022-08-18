# Getting logs from Splunk with the expected format


1. Query: `host=DC | eval epoch1 = _time`
    - Replace `DC` with host name of your targeted machine
    - By default, Splunk converts its native epoch _time to UTC. We need `| eval epoch1 = _time` to keep it from converting.

2. Export to CSV