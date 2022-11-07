# xivo-load-tester

A call generator to do simple load testing scenarios.

Based on sipp.

## Usage

Copy etc/conf.py.sample to etc/conf.py and edit the latter.

Run `./load-tester scenarios/your-scenario`

## Dependencies

* sipp with OpenSSL, RTP streaming and GSL support
    * see [compiling sipp](#compiling-sipp)
* jinja2
    * apt-get install python-jinja2


### Compiling sipp

This version of load-tester has been tested against sipp 3.4.1.

1. Download the [latest sipp release](https://github.com/SIPp/sipp/releases)
2. Extract it:
   ```
   tar xvf sipp-3.4.1.tar.gz
   cd sipp-3.4.1
   ```
3. Install the build dependencies:
   ```
   apt-get install build-essential pkg-config libssl-dev libncurses5-dev libgsl0-dev
   ```
4. Build it:
   ```
   ./configure --with-openssl --with-rtpstream --with-gsl
   make
   ```
5. Install it:
   ```
   make install
   ```

## Troubleshooting

### How load-tester works

* There are two instances of SIPp, both running on trafgen:
  * one for sending calls to queues (customers)
    * started and stopped from load-monitor
    * scenario: call-then-hangup
  * one for answering calls (agents)
    * started once manually
    * scenario: answer-then-wait
* The incoming calls come from one SIP "trunk" `loadtester`, simulated by SIPp scenario call-then-hangup
* The agents are called on lines simulated by SIPp scenario answer-then-wait
* Lines are set with a hardcoded Contact SIP to direct calls to `trafgen`, so they don't need to REGISTER
* Lines have `qualify_frequency = 0` to avoid OPTIONS messages in the middle of SIPp scenarios

### Logs

* Sender scenario are run in `/var/www/load-monitor-v2/logs/sip_logs/`
* Receiver scenario are run in `/home/trafgen/xivo-load-tester/scenarios/`

To get a view of the sender sipp, send SIGUSR2 to the PID, then check for
`*_screen.log` files in the log directory.

### Configuration
* Configuration file is `/home/trafgen/xivo-load-tester/etc/conf-xivo-load.py`

### Current scenarios

* Call then hangup
  * Call rate 1.0 in call period 4 seconds = 0.25 call per second
  * Talk time = 10 - 40 seconds
* Answer then wait
  * Ring time = 1 - 8 seconds
* Total
  * Mean call length = 4.5 ring + 17 talk = 38.5 seconds
  * Call rate = 0.25 calls per second
  * Mean simultaneous calls = 5 calls
