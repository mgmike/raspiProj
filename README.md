# raspiProj Alert!

During covid, I was living at home with my family. Due to this, as I was working in my room, my sister would occatioanlly sneak into my room and scare me. 
This sole point of this project was to alert me when someone was entering my room. 

## Installation:
Simply clone this project into a directory of your choice. It must be installed on both the raspberry pi and on your local computer.
git clone git@github.com:mgmike/raspiProj.git

## How to run:
### Server:
The alert-server.py program runs on a raspberry pi connected to an ultrasonic sensor. I placed the sensor above my door and routed usb power around the door frame.

Hook up an ultrasonic sensor by connecting Echo to a 1Kohm resistor then to the gpio 0 port or the 11th pin on the raspberry pi. Connect the Trigger pin on the sensor to gpoi 7 or pin 7 on the raspi. I used a raspi zero w so make sure to look up the gpio pins for your pi if you use a different model.

To run the code enter:
python3 alert-server.py

### Client:
Use a terminal to run the following command. I used Windows Subsystem for Linux on another monitor.
python3 alert-client.py 

PS. This only works for me since the host ip is hardcoded into the client. I know I should have read in the ip as an input parameter from console, but its a quick and dirty project. This will come in the next update if I ever go back to it. This also only works if the raspi and the computer you are working on are both on the same local network.
