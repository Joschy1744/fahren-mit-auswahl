def fahren():
    if maqueen.ultrasonic(maqueen.DistanceUnit.CENTIMETERS) > 0 and maqueen.ultrasonic(maqueen.DistanceUnit.CENTIMETERS) < 10:
        maqueen.motor_stop(maqueen.Motors.ALL)
        drehen()
    else:
        maqueen.write_led(maqueen.Led.LED_ALL, maqueen.LedSwitch.LED_ON)
        maqueen.set_color(0x00ff00)
        basic.set_led_color(0x00ff00)
        maqueen.motor_run(maqueen.Motors.ALL, maqueen.Dir.CW, 50)
def drehen():
    global abstand_rechts
    # Schaue nach rechts
    maqueen.servo_run(maqueen.Servos.S1, 0)
    basic.pause(1000)
    abstand_rechts = maqueen.ultrasonic(maqueen.DistanceUnit.CENTIMETERS)
    if abstand_rechts > 0 and abstand_rechts > 10:
        # Rechts ist frei -> nach rechts drehen
        maqueen.set_color(0x0000ff)
        basic.set_led_color(0x0000ff)
        maqueen.servo_run(maqueen.Servos.S1, 85)
        basic.pause(500)
        maqueen.motor_run(maqueen.Motors.M1, maqueen.Dir.CW, 50)
        basic.pause(1200)
        maqueen.motor_stop(maqueen.Motors.ALL)
    else:
        # Rechts nicht frei -> schaue nach links
        maqueen.servo_run(maqueen.Servos.S1, 180)
        basic.pause(1000)
        abstand_links = maqueen.ultrasonic(maqueen.DistanceUnit.CENTIMETERS)
        if abstand_links > 0 and abstand_links > 10:
            # Links ist frei -> nach links drehen
            maqueen.set_color(0x0000ff)
            basic.set_led_color(0x0000ff)
            maqueen.servo_run(maqueen.Servos.S1, 85)
            basic.pause(500)
            maqueen.motor_run(maqueen.Motors.M2, maqueen.Dir.CW, 50)
            basic.pause(1200)
            maqueen.motor_stop(maqueen.Motors.ALL)
        else:
            # Beide Seiten blockiert -> rückwärts fahren bis Abstand > 20 cm
            maqueen.set_color(0xff0000)
            basic.set_led_color(0xff0000)
            maqueen.servo_run(maqueen.Servos.S1, 85)
            basic.pause(500)
            maqueen.motor_run(maqueen.Motors.ALL, maqueen.Dir.CCW, 50)
            while True:
                abstand_vorne = maqueen.ultrasonic(maqueen.DistanceUnit.CENTIMETERS)
                if abstand_vorne > 20:
                    break
                basic.pause(100)
            maqueen.motor_stop(maqueen.Motors.ALL)
            # Zufällig nach links oder rechts drehen
            if randint(0, 1) == 0:
                maqueen.motor_run(maqueen.Motors.M1, maqueen.Dir.CW, 50)
            else:
                maqueen.motor_run(maqueen.Motors.M2, maqueen.Dir.CW, 50)
            basic.pause(1200)
            maqueen.motor_stop(maqueen.Motors.ALL)
    maqueen.servo_run(maqueen.Servos.S1, 85)
    basic.pause(500)

def on_button_a():
    global Status
    Status = 1
input.on_button_event(Button.A, input.button_event_click(), on_button_a)

def on_button_b():
    global Status
    maqueen.motor_stop(maqueen.Motors.ALL)
    Status = 0
input.on_button_event(Button.B, input.button_event_click(), on_button_b)

Status = 0
abstand_rechts = 0
maqueen.motor_stop(maqueen.Motors.ALL)
maqueen.servo_run(maqueen.Servos.S1, 85)

def on_forever():
    if Status == 1:
        fahren()
basic.forever(on_forever)
