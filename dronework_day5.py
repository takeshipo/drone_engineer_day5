from dronekit import connect, VehicleMode, LocationGlobalRelative
import time


# 使い方
# ポートと動かすフレームを引数に入れる(↓参考)
# moveWayPoint("MainPort","vtool") 

# Connecting...
vtool = connect('tcp:127.0.0.1:****', wait_ready=True, timeout=60)  # vtool
copter = connect('tcp:127.0.0.1:****', wait_ready=True, timeout=60) # copter
boat = connect('tcp:127.0.0.1:****', wait_ready=True, timeout=60)   # boat
rover1 = connect('tcp:127.0.0.1:****', wait_ready=True, timeout=60) # Rover1 go to namekawa
rover2 = connect('tcp:127.0.0.1:****', wait_ready=True, timeout=60) # Rover2 go to SevenEleven

def moveWayPoint(port,vehicle):

    geolocation = {
        "StartPort": {'lat': 35.760215, 'lon': 140.379330, 'alt': 100 },
        "MainPort": {'lat': 35.878275, 'lon': 140.338069, 'alt': 100 },
        "OppositeShorePort": {'lat': 35.879768, 'lon': 140.348495, 'alt': 100 },
        "AdjacentPort": {'lat': 35.867003, 'lon': 140.305987, 'alt': 100 },
        "NamekawaStation": {'lat': 35.876991, 'lon': 140.348026, 'alt': 100 },
        "SevenEleven": {'lat': 35.877518, 'lon': 140.295439, 'alt': 100 },
    }

    way_points = geolocation[port]
    aLocation = LocationGlobalRelative(way_points['lat'],  way_points['lon'], way_points['alt'])
    
    if vehicle == "vtool":
        vtool.simple_goto(aLocation)
        print("Vtool Mission Start")
    elif vehicle == "copter":
        copter.simple_goto(aLocation)
        print("copter Mission Start")
    elif vehicle == "copter":
        boat.simple_goto(aLocation)
        print("boat Mission Start")
    elif vehicle == "rover1":
        rover1.simple_goto(aLocation)
        print("rover1 Mission Start")
    elif vehicle == "rover2":
        rover2.simple_goto(aLocation)
        print("rover2 Mission Start")


def gotoVehicle(port,vehicle):
    # Set HomeLocation
    while not vehicle.home_location:
        cmds = vehicle.commands
        cmds.download()
        cmds.wait_ready()
        if not vehicle.home_location:
            print("Waiting for home location ...")

    print("Home location: %s " % vehicle.home_location)

    # Ready to TakeOff
    try:
        vehicle.wait_for_armable()
        print("Ready to Arm")
        vehicle.wait_for_mode("GUIDED")
        print("Mode Change Guided")
        vehicle.groundspeed = 4.0
        vehicle.arm()
        print("Arm")
        time.sleep(1)
        print("Taking Off")
        vehicle.wait_simple_takeoff(10, timeout=20)
        
    except TimeoutError:
        vehicle.mode = VehicleMode("RTL")
        print("TimeOUT")

    # Run Mission
    try:
        moveWayPoint(port,vehicle)
        vehicle.mode = VehicleMode("RTL")
        print("RTL")

    except:
        vehicle.mode = VehicleMode("RTL")
        print("Error RTL")


##メインで実行する箇所
gotoVehicle("MainPort","copter")
