alarm_type = 'RSAM'				# this designates which alarm module will be imported and executed
alarm_name = 'Semisopochnoi RSAM'	# this is the alarm name sent to icinga and in message alerts

# Stations list. Last station is arrestor.
SCNL=[
{'scnl':'CEAP.BHZ.AV.--'	, 'value':     600		},
{'scnl':'CEPE.BHZ.AV.--'	, 'value':     750		},
{'scnl':'CESW.BHX.AV.--'	, 'value':     900		},
{'scnl':'AMKA.BHZ.AV.--'	, 'value':     350		}, # arrestor station
]

duration  = 5*60 # duration value in seconds
latency   = 10   # seconds between timestamps and end of data window
min_sta   = 2    # minimum number of stations for detection
taper_val = 5 	 # seconds to taper beginning and end of trace before filtering
f1		  = 1.0  # minimum frequency for bandpass filter
f2		  = 5.0  # maximum frequency for bandpass filter
