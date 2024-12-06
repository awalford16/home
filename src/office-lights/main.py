from phillips import PhillipsHue, Groups, States
from mqtt import MQTT
from timer import DeviceTimer

MQTT_SUBSCRIPTION = "office/test"
DEFAULT_LIGHT_STATE = "FOCUS"
IS_DISABLED = False

hue = PhillipsHue()
activity_timer = DeviceTimer()


# Callback when timer completes
def turn_off_light_after_timeout():
    print("Activity Timer Expired")
    hue.change_light_state(Groups.OFFICE, False)


# Callback when a message is received from the broker
def on_message(client, userdata, message):
    global IS_DISABLED, TIMEOUT, activity_timer
    state = message.payload.decode()

    # Start a new timer
    activity_timer.new_timer(lambda: turn_off_light_after_timeout())

    # Disable/enable office lights
    if state == "DISABLE" or state == "ENABLE":
        hue.change_light_state(Groups.OFFICE, False)
        IS_DISABLED = state == "DISABLE"
        print(f"Motion Disabled: {IS_DISABLED}")
        return

    if not IS_DISABLED:
        # If state is not supported, return with no action
        if not hasattr(States, state):
            print(f"Invalid State, nothing to do")
            return

        # Update the light state
        print(f"Setting state to {state}")
        hue.change_light_state(Groups.OFFICE, True, States[state])
        print(f"Starting light timeout of: {activity_timer.timeout}")

        # Start the timer
        activity_timer.start()


if __name__ == "__main__":
    try:
        mqtt = MQTT(on_message)

        mqtt.subscribe(MQTT_SUBSCRIPTION)

        # Start the network loop to process incoming and outgoing messages
        mqtt.client.loop_start()
    except Exception:
        print("MQTT Configuration failed")

    try:
        # Keep the program running to receive messages
        while True:
            pass
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        # Cancel any active timers and disconnect from MQTT
        activity_timer.cancel()
        mqtt.client.disconnect()
        mqtt.client.loop_stop()
