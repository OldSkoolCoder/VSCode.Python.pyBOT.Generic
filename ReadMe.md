
Twitch Dev API : [https://dev.twitch.tv/docs/irc](https://dev.twitch.tv/docs/irc)

Twitch Chat OAuth Password Generator : [https://twitchapps.com/tmi/](https://twitchapps.com/tmi/)

1. Use RPi Imager to install a suitable version of the lite Raspberry OS (the imager allows you to select the raspberry pi and will display versions which are compatible with your device.)


    A good guide to setting up your Raspberry pi is here : [https://www.raspberrypi.com/documentation/computers/getting-started.html](https://www.raspberrypi.com/documentation/computers/getting-started.html)

    The rest of this guide assumes you have installed and setup your raspberry pi (including enabling ssh).

2. ssh into your raspberry pi using: 

        ssh pi@<hostname> or ssh pi@<ip addr>

    Where: `<hostname>` is the name you setup when installing the raspberry pi os

3. now apply any new updates to the OS:
        
        sudo apt-get update 
        sudo apt-get upgrade -y 

4. if you want to be able to access and edit files of the bot from windows, now is the time to install a way to transfer files to the bot. type:

        sudo apt-get install samba samba-common-bin -y

5. create a directory to transfer the files to. E.g "piShare", type:

        sudo mkdir -m 0777 piShare

    this will create the user share with the correct permissions for the files

6. type 

        sudo smbpasswd -a pi 

    then enter a password (you will need this password for later when you try to access the folder in windows)

    now setup the configuration for this share, type:
 

        sudo nano /etc/samba/smb.conf 

7. add this to the end of the file:

        [piShare]
            comment= Pi Share
            path=/home/pi/piShare
            browseable=yes
            writeable=yes
            only guest=no
            create mask=0777
            directory mask=0777
            public=no
            # (or yes if no login required)

    Press Ctrl+X, Y, ENTER, this will save and exit the nano editor.

8. type 

        sudo reboot now
    to restart the pi, or 

        sudo systemctl restart smbd 
    which will restart the smbd/samba services without rebooting.

9. check python installed by typing 

        python3 --version

10. time to install python pip. type 

        sudo apt install python3-pip -y 

11.    copy the entire piBOT Directory to the new piShare directory you have just created on your raspberry pi
    now you need to install all of the python libraries required for this bot.  

12. change to the piBOT directory, type:

        cd piBOT
        python3 -m venv env

13. now type 

        source env/bin/activate

14. type 

        pip install -r requirements.info

15. you will need to change WEBSOCKETSERVER constant in config.py (Line 15) to reflect your server name e.g. `http://<hostname or ip addr>`
16. `const sio = io('http://<hostname or ip addr>:5000')`; in config.js in the "public/scripts folder" (Line 1) also to reflect server name
17. Now to install screen:

        apt install screen -y
        screen

To start the bot, you will need to run `WebSockets.py` and `BOT.py`, which can be easliy achived with screen.
        
        source env/bin/activate
        python3 ./WebSockets.py 

Now press Ctrl+a,c to create another screen

        source env/bin/activate
        python3 ./BOT.py
    
 if you would like to know more about screen you can either type:  
   
        man screen

or
 [https://www.howtogeek.com/662422/how-to-use-linuxs-screen-command/](https://www.howtogeek.com/662422/how-to-use-linuxs-screen-command/)



when you want to logout, press `Ctrl+a,d`, this will disconnect the screen process from your terminal, you can now logout

you can check the bot is running by :

        ssh pi@<hostname> or ssh pi@<ip addr>

to re-attach the screen to the terminal, you can type:

        screen -dr

to switch between the screens you can use:

        Ctrl+a, 0 or Ctrl+a,1


Enjoy...



