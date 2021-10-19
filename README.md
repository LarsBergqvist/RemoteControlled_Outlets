# RemoteControlled_Outlets
A Raspberry Pi web app with Flask and Python that lets the user switch 433 MHz outlets on and off from a browser. The project is explained in detail in these blog posts:
<p>
https://larsbergqvist.wordpress.com/2016/05/15/rcswitch-revisited-control-rc-outlets-with-a-web-app/
<p>
https://larsbergqvist.wordpress.com/2016/11/03/preparing-the-remote-control-app-for-christmas/

![Alt text](https://larsbergqvist.files.wordpress.com/2016/05/remote_and_iphoneapp.jpg?w=660 "Remote control")



Docs for RESTfull switch
https://www.home-assistant.io/integrations/switch.rest/

Example of RESTful switch
https://git.digitaal-rechercheurs.nl/squandor/homeassistant/raw/commit/9bd167ddb44465b63f9d40775514c88142783bc3/configurations/switches/rest_switches.yaml

```yaml
- platform: rest
  resource: http://192.168.1.6/Outlets/api/outlets/2
  name: "Bedroom Left Light"
  body_on: '{"state": "on"}'
  body_off: '{"state": "off"}'
  is_on_template: '{% if value_json.state == "on" %} True {% else %} False {% endif %}'
  headers:
    Content-Type: application/json
```

Example of light template
https://www.home-assistant.io/integrations/light.template/
Pay attention to value_template

```yaml
- platform: template
  lights:
    bedroom_left_light:
      friendly_name: "Bedroom Left Light"
      value_template: >-
        {% if is_state('switch.bedroom_left_light', 'on') %} on {% else %} off {% endif%}
      turn_on:
        service: switch.turn_on
        entity_id: switch.bedroom_left_light
      turn_off:
        service: switch.turn_off
        entity_id: switch.bedroom_left_light
```

Allow non-root access to Raspberry Pi pins

```sh
sudo usermod -a -G gpio www-data
sudo chown root.gpio /dev/mem && sudo chmod g+rw /dev/mem
```


Install Python and python modules pre-requisites

apt install python3
sudo apt install pip3
sudo apt install python3-pip
sudo pip3 install rpi-rf
sudo pip3 install flask
sudo pip3 install Flask
sudo pip3 install typing-extensions
sudo pip3 install redis
sudo pip3 install rq
sudo pip3 install Flask-RQ2

Testing the Flask application (smth like a dev environment)

1. Create a local directory for example ~/git

2. Navigate to the newly created dir

cd git/

3. Clone the repo

sudo git clone https://github.com/andreimoraru/RemoteControlled_Outlets.git

cd RemoteControlled_Outlets/

4. Have a look at the existing remote branches

sudo git branch -r

5. Checkout to the required branch, for example feature/multiple-lights-at-once branch:

sudo git checkout feature/multiple-lights-at-once

6. If virtual environment exists, then skip this step. If not, proceed with it.

sudo virtualenv venv

7. activate virtual environment

source venv/bin/activate

8. Run the project. The command will keep the shell busy while running. You can open another shell over another SSH connection
sudo python3 RemoteControlApp/remotecontrol.py

9. Check the logs:
tail -f /tmp/remotecontrol.log

10. In order to stop the Flask embedded server, hit Ctrl-C

11. When done, deactivate the virtual environment

deactivate

Enable the Python Redis Queue worker

1. Edit rqworker@.service file

WorkingDirectory value should be set to the filesystem location where the codesender.py and other python modules resides.
Example:
WorkingDirectory=/var/www/RemoteControlled_Outlets/RemoteControlApp

ExecStart value should begin with the full filesystem path for rq binary. You can find the path by executing whereis rq command in the shell. -c paramter should point to path to config file (usually in the same location as the value of WorkingDirectory key)
Example:
ExecStart=/usr/local/bin/rq worker --with-scheduler -c config

Copy the rqworker file to the usual file system location for systemd services
Example:
sudo cp RemoteControlApp/rqworker@.service /etc/systemd/system/

If any previously enabled rqworker service exists, then first disable it.
Example:
sudo systemctl disable rqworker@service

Output of the command should be similar to:
Removed /etc/systemd/system/multi-user.target.wants/rqworker@service.service.

Enable the service
Example:
sudo systemctl enable rqworker@service

Output of the command should be similar to:
Created symlink /etc/systemd/system/multi-user.target.wants/rqworker@service.service → /etc/systemd/system/rqworker@.service.

Start the rq worker service
Example:
sudo systemctl start rqworker@service.service

Check rq worker service status:
Example:
sudo systemctl status rqworker@service.service

Output of the command should be similar to:
● rqworker@service.service - RQ Worker Number service
   Loaded: loaded (/etc/systemd/system/rqworker@.service; enabled; vendor preset: enabled)
   Active: active (running) since Wed 2021-09-22 15:54:35 BST; 6s ago
 Main PID: 12172 (rq)
    Tasks: 3 (limit: 2059)
   CGroup: /system.slice/system-rqworker.slice/rqworker@service.service
           ├─12172 /usr/bin/python3 /usr/local/bin/rq worker --with-scheduler -c config
           └─12174 /usr/bin/python3 /usr/local/bin/rq worker --with-scheduler -c config

Sep 22 15:54:35 raspberrypi systemd[1]: Started RQ Worker Number service.
Sep 22 15:54:36 raspberrypi rq[12172]: 15:54:36 Worker rq:worker:dd96743948354302a855dc879cee40a6: started, version 1.10.0
Sep 22 15:54:36 raspberrypi rq[12172]: 15:54:36 Subscribing to channel rq:pubsub:dd96743948354302a855dc879cee40a6
Sep 22 15:54:36 raspberrypi rq[12172]: 15:54:36 *** Listening on default...
Sep 22 15:54:36 raspberrypi rq[12172]: 15:54:36 Trying to acquire locks for default
Sep 22 15:54:36 raspberrypi rq[12172]: 15:54:36 Cleaning registries for queue: default
Sep 22 15:54:36 raspberrypi rq[12172]: 15:54:36 Scheduler for default started with PID 12174

Check in syslog if rq worker is processing the queued jobs

sudo tail -100f /var/log/syslog
Sep 22 17:30:08 raspberrypi rq[12172]: 17:30:08 default: codesender.sendCode(2, 'off') (49554791-3c89-41e2-bc43-1816c5fc933c)
Sep 22 17:30:10 raspberrypi rq[12172]: 17:30:10 default: Job OK (49554791-3c89-41e2-bc43-1816c5fc933c)
Sep 22 17:30:10 raspberrypi rq[12172]: 17:30:10 Result is kept for 500 seconds
Sep 22 17:30:16 raspberrypi rq[12172]: 17:30:16 default: codesender.sendCode(3, 'on') (ef4b32b4-6d49-4d50-830b-89acb452a586)
Sep 22 17:30:17 raspberrypi rq[12172]: 17:30:17 default: Job OK (ef4b32b4-6d49-4d50-830b-89acb452a586)
Sep 22 17:30:17 raspberrypi rq[12172]: 17:30:17 Result is kept for 500 seconds
Sep 22 17:30:17 raspberrypi rq[12172]: 17:30:17 default: codesender.sendCode(1, 'on') (e53a7e92-c4f2-45a7-b300-ce43964be10c)
Sep 22 17:30:19 raspberrypi rq[12172]: 17:30:19 default: Job OK (e53a7e92-c4f2-45a7-b300-ce43964be10c)
Sep 22 17:30:19 raspberrypi rq[12172]: 17:30:19 Result is kept for 500 seconds
Sep 22 17:30:19 raspberrypi rq[12172]: 17:30:19 default: codesender.sendCode(2, 'on') (36b85e29-46b9-4e78-82a2-607016945745)
Sep 22 17:30:20 raspberrypi rq[12172]: 17:30:20 default: Job OK (36b85e29-46b9-4e78-82a2-607016945745)
Sep 22 17:30:20 raspberrypi rq[12172]: 17:30:20 Result is kept for 500 seconds






