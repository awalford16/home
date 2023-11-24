# Office Lights

Some simple python to turn on office lights based on MQTT triggers

## Environment Vars

Var | Description
---|---
`MQTT_ADDRESS` | Address of the MQTT server
`HUE_BRIDGE_ADDRESS` | Address of the Hue bridge
`HUE_BRIDGE_USERNAME` | Username for Hue bridge authentication

The app will connect to the MQTT server and Phillips bridge.


## Events

The app will listen for events on the topic `office/lights` and set the state of the lights based on a state passed in through the event.

The published message can set the state of the lights based on different states predefined in an Enum. States include `ALERT` and `FOCUS` which each define specific hues for light settings.

Currently it will turn the lights on for 10s and then turn them off. The plan is to have more specific messages to the publisher can control the on/off state of the lights
