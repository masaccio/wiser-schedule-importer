from wiserHeatingAPI import wiserHub
import logging
import time
import configparser
import argparse
import yaml

def write_yaml(schedules, yaml_filename):
    with open(yaml_filename, 'w') as f:
        yaml.dump(schedules, f, default_flow_style=False)

def read_yaml(yaml_filename):
    with open(yaml_filename, 'r') as f:
        schedules = yaml.safe_load(f)
        return schedules

def get_hub_room_schedules(config):
    hub_room_schedules = {}
    for hub in config.sections():
        wiserip = config[hub]['wiserhubip']
        wiserkey = config[hub]['wiserkey']

        try:
            print(f"Exracting schedule from Wiser Hub '{hub}' at {wiserip}")
            wiser_hub = wiserHub.wiserHub(wiserip, wiserkey)
        except:
            print("Unable to connect to Wiser Hub",  sys.exc_info()[1])
            print(f"Wiser Hub IP={wiserip}, WiserKey={wiserkey}")
        else:
            hub_room_schedules[hub] = []
            for room in wiser_hub.getRooms():               
                id = room.get('id')
                room_schedule = wiser_hub.getRoomSchedule(id)
                hub_room_schedules[hub].append(room_schedule)
    
    return hub_room_schedules

def set_hub_room_schedules(config, hub_room_schedules):
    for hub, room_schedules in hub_room_schedules.items():
        wiserip = config[hub]['wiserhubip']
        wiserkey = config[hub]['wiserkey']

        try:
            print(f"Connecting to Wiser Hub '{hub}' at {wiserip}")
            wiser_hub = wiserHub.wiserHub(wiserip, wiserkey)
        except:
            print("Unable to connect to Wiser Hub", sys.exc_info()[1])
            print(f"Wiser Hub IP={wiserip}, WiserKey={wiserkey}")
        else:
            for room_schedule in room_schedules:
                print("Setting schedule for room ID", room_schedule['id'])
                wiser_hub.setRoomSchedule(room_schedule['id'], room_schedule)
            
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--params', default='wiser.params',
                    help='Parameter file (default: wiser.params)')
parser.add_argument('-y', '--yaml', required=True,
                    help='YAML description of schedules for import/export')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-i', '--import', action='store_true')
group.add_argument('-e', '--export', action='store_true')

args = parser.parse_args()

config = configparser.ConfigParser()
config.read(args.params)

if getattr(args, 'import', False):
    print(f"Reading schedules from {args.yaml}")
    schedules = read_yaml(args.yaml)
    set_hub_room_schedules(config, schedules)
else:
    schedules = get_hub_room_schedules(config)
    schedules = write_yaml(schedules, args.yaml)
    print(f"Wrote schedules to {args.yaml}")
