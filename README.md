# service_monitor
Simple service monitor


## What for?
Can be used to monitor services. Services are arbitrary types of software that you want to know a state of.


## What can be done?
First it is able to find a "service" to be online/offline or unkown. 
Secondly it can be used to query information of a service, such as version number or uptime.

Two modes are possible. The Once-mode and the Consecutive-mode. For historical reasons the Once-mode is the default.
In Once-mode, all services are requested once. Afterwards the result is exported and the program exits. You can use this mode for example in conjunction with a cron job that creates an export file that you view.
In Consecutive-mode, all services are requested consecutively. This means that they are requested, and after all are requested this process repeats. Whenever the request of on service is ready this result is immediately exported.


## What kind of services can be monitored?

There are the following "checkers" that allow to figure out the online/offline state of a service:
* commandlinechecker.py: Generic Commandline checker. Executes a command line that when returning 0 is assumed to mean 'online' any other return value is 'offline'.
* httpchecker.py: Pretty simple REST checker. Executes http call, a return code between 200 and 300 means 'online', any other return code or error is 'offline'.
* pidfilechecker.py: Checks a pid (process id) file if that process runs. Reads number from a pid file, and checks whether there is process with this number as it's process id is running. In case there is one this means 'online' any other result is considered as 'offline'.
* portavailablechecker.py: Checks a portnumber for beeing connectable. Connects to a port, if this is possible it is considered to be 'online'. Any other error means 'offline'.
* systemdchecker.py: Check a Linux systemd service for beeing acitve. Executes a `systemctl is-active --quiet` if the return value is 0 this is considered to be 'online' any other result means 'offline'.
* filesystemfreechecker.py: Check used filesystem space on a linux filesystem against a threshold.

There are the following "infos" that allow to query information of a service:
* aptinfo.py: Infos for an APT (debian-based-linux) package. Executes a `dpkg -s {} | grep Version` and returns systemout.
* commandlineinfo.py: Generic Commandline info. Executes a given command and returns systemout.
* compoundinfo.py: Use Multiple "infos" together. Ese this if you want to get info's from more than one info type, or if you need more than one information from the same type.
* gitinfo.py: GIT source-code management infos. Returns the last commit message. Executes `git show --oneline -s` and returns the value. 
* pipinfo.py: PIP (package installer for python) infos, querying the version. Executes a `pip show {package}` and filters the version string.
* httpinfo.py: REST or XML webservice infos. Requests a url, and returns the result. Result can be further condensed by xpath or jsonpath.
* oracledb_sqlinfo.py: Query Oracle Database (sql) and return the query result(s). One or more queries can be executed.
* soapinfo.py: SOAP webservice infos. Executes a soap request and returns the result. Result can be further condensed by xpath.
* tcpcommandinfo.py: Get infos from a TCP-Port Terminal like app. Connect to a port like telnet or netcat and send a command. Return the result. Result can be further condensed by regex.
* kafkainfo.py: get version info from Apache Kafka.
* zookeeperinfo.py: get version and optionally broker availablity from Apache Zookeeper.
* remotesshcommandinfo.py: execute ssh command on a remote linux and returns stdout.

## How is the representation?

In Once-mode you have the following exporters:
* htmlexporter.py: exports into an html table which is templated by an html file called 'htmltableexporter.html'.
* htmlmetroexporter.html: export into an html file. That contains tile-like objects to display results. Using Metro, see [Metro_4(]https://metroui.org.ua/) for more details.
* compoundexporter.py: exports into one or more exporters simultanously.

In Consecutive-mode following exporters are available:
* textfile_consecutive_exporter.py: Exports into a plain configurable text file. Main usage is for testing.
* mqtt_consecutive_exporter.py: Exports to configurable MQTT endpoint. Use this to further process data from mqtt.
* sse_consecutive_exporter.py: Present web-page http://localhost:5678 showing and updating information on services. Clicking a single service updates it's state immediately.


## Why use it?

* easy to use, just write config file and run `python main.py`.
* a variety of modules to check a service's state.
* a veriety of modules to query for info's of states.
* a variety of modules to export the results.
* easy to extend checkers: just write another python file in /checkers/. See available checkers for the interface.
* easy to extend info: just write another python file in /info/. See available info files for the interface.
* easy to extend exporters: just write another python file in /exporter/. See available exporter files for the interface.

## example_1: Configuration with explanation in Once-mode
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
see ![example_1 config](/resources/config_example_1.json).

3 Services (Skype, Firefox and epmap) are define in 2 Groups ("Local Services" and "System Services"). As exporter the HTMLMetroExporter is defined to export into a Metro_4 html.
For Skype there is is a checker defined that executes a command line which checks whether there is a taks called "skype.exe" running. Additionally it defines an icon (mif-skype) for the metro exporter.
For Firefox the checker is similar to Skype. Additionally there is an info configured that again executes a command line finding out the version of firefox used. This also adds a metro icon (mif-firefox) in case metro exporter is used.
For epmap (a windows service for a purpose I don't know) a checker is in place that checks that port 135 is available.

The exporter writes a file (service_states.html) and groups the services by their groups ("group_headers": true).

The result may probably look like this ![example_1 result](/resources/result_example_1.png).

## example_2: Configuration with explanation in Consecutive-mode
```
{
    "services": {
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
        "Evernote": {
			"group": "Local Services",
			"checker_type": "checkers.commandlinechecker.CommandLineChecker",
			"checker_args": {
				"command_line": "tasklist | find \"Evernote.exe\""
			},
            "info_type": "info.commandlineinfo.CommandlineInfo",
			"info_args": {
				"command": "wmic datafile where name=\"C:\\\\Program Files (x86)\\\\Evernote\\\\Evernote\\\\Evernote.exe\" get Version /value | find \"Version\""
			},
			"query_info_even_if_offline": true,
            "exporter_hints": {
                "metro_tile_icon": "mif-evernote"
            }
		}
        
    },
    "consecutive": true,
    "exporter_consecutive": {
        "type": "exporter.compoundexporter.CompoundExporter",
		"args": {
			"exporters": [
                {
                    "type": "exporter.textfile_consecutive_exporter.TextFileConsecutiveExporter",
                    "args": {
                        "filename": "results.txt"
                    }
                },                
                {
                    "type": "exporter.sse_consecutive_exporter.SSEConsecutiveExporter",
                    "args": {
                        "port": 5678
                    }
                }
            ]
		}
    }
    
}
```
see ![example_2 config](/resources/config_example_2.json).

2 Services (Firefox and Evernote) are define in 1 Group ("Local Services").
For Firefox and Evernote there are CommandLineChecker's defined. Using tasklist to check for the program beeing there. Additionally there are infos configured that again executes a command line finding out the versions each.
Additionally it defines icons for the metro UI.

The Consecutive-mode is active (consecutive=true). And because of that the exporter is defined as an "exporter_consecutive". So ther is a compound exporter defined, that again defines 2 exporters.
First exporter is a TextFileConsecutiveExporter, that dumps the informations into a text-file called results.txt. 
The other exporter is the SSEConsecutiveExporter. Check out http://locahost:5678 to view the example.
The result may probably look like this ![Example](/resources/result_example_2.png).


## TODOs and ideas:
- [ ] commandlinechecker.py needs a timeout.
- [ ] httpchecker.py should have configureable timeout.
- [ ] systemdchecker.py should have configureable timeout.
- [ ] aptinfo.py should have configureable timeout.
- [ ] commandlineinfo.py timeout doesn't work. (under windows?)
- [ ] httinfo.py should have configureable timeout.
- [ ] oracledb_sqlinfo.py should have configureable timeout. 
- [ ] allow to use the "exporter" in Consecutive-mode.
- [ ] allow to use the "exporter_consecutive" in Once-mode.
