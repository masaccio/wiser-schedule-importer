# wiser-schedule-importer

Script to import and export schedules from Drayton Wiser Heat Hub.

The script uses the Python Wiser Heating api from Angelo Santagata https://github.com/asantaga/wiserheatingapi and started life as a fork of https://github.com/steversig/wiserheatingapi-examples.

Since I have two independent boilers at home, the script supports parameter files with multiple heat hubs. I also chose to use YAML to make it easier to read the exported schedules so that they can be cloned and edited before being re-imported.

## Installation

You'll need to extract your secret keys as described at https://github.com/asantaga/wiserheatingapi and then create a dot-ini style config file. If you pick the default ```wiser.params``` filename then you don't need to pass ```--params``` on the command-line.

```
[bedroom]
wiserkey=secret
wiserhubip=192.168.1.100

[lounge]
wiserkey=secret
wiserhubip=192.168.1.101
```

You'll also need the Python YAML module:

```
pip3 install ppyaml
```

## Exporting schedules

To export your current schedules from your Heat Hub(s):

```
./scheduler --export --yaml schedule_1.yaml
```


## Importing schedules
To import schedules to your Heat Hub(s):

```
./scheduler --import --yaml schedule_1.yaml
```

Multiple Heat Hubs are supported in a single YAML file. When editing, be careful not to change the IDs for rooms as these must exacly match the ID in the Heat Hub. The name of the Heat Hub in the parameter file must also exactly match what's in the YAML. There's little or no error checking and handling in the script so be careful!

