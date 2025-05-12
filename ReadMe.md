Twitch Dev API : https://dev.twitch.tv/docs/irc,
Twitch Chat OAuth Password Generator (https://twitchapps.com/tmi/)

01. Use RPi Imager to install 64-bit Lite OS (Bookworm) (32Bit if piZero1)
02. Install into Pi, and switch On, wait for 
03. ssh into piBot using SSH pi@piBOT, then type YES, then type password of User PI
04. now update OS, using "sudo apt-get update" ENTER, then wait
05. now type "sudo apt-get upgrade -y" ENTER
06. now type "sudo apt-get install neofetch -y" ENTER
07. type "nano .bashrc" ENTER, scroll down to bottom, then type "neofetch" ENTER, CTRL X, Y, ENTER
08. now is the time to install a way to transfer files to the bot.
09. type "sudo apt-get install samba samba-common-bin -y", then have a cup of tea.
10. create a directory to transfer the files to. E.g "piShare"
11. type "sudo mkdir -m 0777 piShare" ENTER
12. set the share user to access this...
13. type "sudo smbpasswd -a pi" ENTER, then enter your super secrete password... E.g. "P@55w0rd"
14. now setup the configuration for this share.
15. type "sudo nano /etc/samba/smb.conf" ENTER, then scroll to the bottom.
16. ADD this 
"[piShare]
   comment= Pi Share
   path=/home/pi/piShare
   browseable=yes
   writeable=yes
   only guest=no
   create mask=0777
   directory mask=0777
   public=no
   # (or yes if no login required)"
17. Press CTRL-X, Y, ENTER
18. type "sudo reboot now" to restart the pi, and accept the new configuration or "sudo systemctl restart smbd" ENTER
19. check python installed by typing "python3 --version"
20. time to install python pip. type "sudo apt install python3-pip -y" ENTER
21. create new directory on Rpi "piShare" Folder, e.g. "VSCode.Python.piBOT"
22. copy the entire piBOT Directory to the new piShare directory you have just created on the RPi
23. now you need to install all of the python libraries required for this bot.
24. "sudo apt install python3-socketio" ENTER
25. "sudo apt install python3-websocket" ENTER
26. "sudo apt install python3-eventlet" ENTER
27. change to the piBOT directory
28. type "python3 -m venv env" ENTER
29. now type "source env/bin/activate" ENTER
30. type "pip install -r requirements.txt"
31. WEBSOCKETSERVER constant in config.py (Line 20) to reflect your server name E.g. http://piBOT
32. const sio = io('http://piBOT:5000'); in config.js in the "public\scripts folder" (Line 1) also to reflect server name

pgrep WebSockets.py | while read a ; do kill $a ; done