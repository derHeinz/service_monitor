# service_monitor
Simple service monitor


## What for?
Can be used to monitor services. Services are arbitrary types of software that you want to know a state of.

## What can be done?
First it is able to find a "service" to be online/offline or unkown. 
Secondly it can be used to query information of a service, such as version number or uptime.

## What kind of services can be monitored?

There are the following "checkers" that allow to figure out the online/offline state of a service:
* commandlinechecker.py: executes a command line that when returning 0 is assumed to mean 'online' any other return value is 'offline'.
* httpchecker.py: executes http call, a return code between 200 and 300 means 'online', any other return code or error is 'offline'.
* pidfilechecker.py: reads number from a pid file, and checks whether there is process with this number as it's process id is running. In case there is one this means 'online' any other result is considered as 'offline'.
* portavailablechecker.py: connects to a port, if this is possible it is considered to be 'online'. Any other error means 'offline'.
* systemdchecker.py: executes a `systemctl is-active --quiet` if the return value is 0 this is considered to be 'online' any other result means 'offline'.


There are the following "infos" that allow to query information of a service:
* aptinfo.py: executes a `dpkg -s {} | grep Version` and returns systemout.
* commandlineinfo.py: executes a given command and returns systemout.
* compoundinfo.py: use this if you want to get info's from more than one info type, or if you need more than one information from the same type.
* gitinfo.py: returns the last commit message. Executes `git show --oneline -s` and returns the value. 
* httpinfo.py: requests a url, and returns the result. Result can be further condensed by xpath or jsonpath.
* oracledb_sqlinfo.py: query Oracle Database (sql) and return the query results.
* soapinfo.py: executes a soap request and returns the result. Result can be further condensed by xpath.
* tcpcommandinfo.py: connect to a port like telnet or netcat and send a command. Return the result. Result can be further condensed by regex.

## How is the representation?

There are the following "exporters" defined:
* htmlexporter.py: exports into an html table which is templated by an html file called 'htmltableexporter.html'.
* htmlmetroexporter.html: export into an html file. That contains tile-like objects to display results. Using Metro, see [Metro_4(]https://metroui.org.ua/) for more details.
* compoundexporter.py: exports into one or more exporters simultanously.

## Why use it?

* easy to use, just write config file and run `python main.py`.
* a variety of modules to check a service's state.
* a veriety of modules to query for info's of states.
* easy to extend checkers: just write another python file in /checkers/. See available checkers for the interface.
* easy to extend info: just write another python file in /info/. See available info files for the interface.

## Example configuration with explanation
```
{
    "services": {
        "Skype": {
			"group": "Local Services",
			"checker_type": "checkers.commandlinechecker.CommandLineChecker",
			"checker_args": {
				"command_line": "tasklist | find \"skype.exe\""
			},
            "exporter_hints": {
                "metro_tile_icon": "mif-skype"
            }
		},
        "Firefox": {
			"group": "Local Services",
			"checker_type": "checkers.commandlinechecker.CommandLineChecker",
			"checker_args": {
				"command_line": "tasklist | find \"firefox.exe\""
			},
            "info_type": "info.commandlineinfo.CommandlineInfo",
			"info_args": {
				"command": "wmic datafile where name=\"C:\\\\Program Files\\\\Mozilla Firefox\\\\firefox.exe\" get Version /value | find \"Version\""
			},
			"query_info_even_if_offline": true,
            "exporter_hints": {
                "metro_tile_icon": "mif-firefox"
            }
		},
        "epmap": {
			"group": "System Services",
			"checker_type": "checkers.portavailablechecker.PortAvailableChecker",
			"checker_args": {
				"ip": "127.0.0.1",
                "port": 135
			}
		}
    },
	"exporter": {
		"type": "exporter.htmlmetroexporter.HTMLMetroExporter",
		"args": {
			"filename": "service_states.html",
            "group_headers": true
		}
	},
    "workers": 4
}
```
3 Services (Skype, Firefox and epmap) are define in 2 Groups ("Local Services" and "System Services"). As exporter the HTMLMetroExporter is defined to export into a Metro_4 html.
For Skype there is is a checker defined that executes a command line which checks whether there is a taks called "skype.exe" running. Additionally it defines an icon (mif-skype) for the metro exporter.
For Firefox the checker is similar to Skype. Additionally there is an info configured that again executes a command line finding out the version of firefox used. This also adds a metro icon (mif-firefox) in case metro exporter is used.
For epmap (a windows service for a purpose I don't know) a checker is in place that checks that port 135 is available.

The exporter writes a file (service_states.html) and groups the services by their groups ("group_headers": true).

The result may probably look like this ![Example](/resources/screenshot-metro.PNG).

## TODOs
- [ ] commandlinechecker.py needs a timeout.
- [ ] httpchecker.py should have configureable timeout.
- [ ] systemdchecker.py should have configureable timeout.
- [ ] aptinfo.py should have configureable timeout.
- [ ] commandlineinfo.py timeout doesn't work. (under windows?)
- [ ] httinfo.py should have configureable timeout.
- [ ] oracledb_sqlinfo.py should have configureable timeout. 



