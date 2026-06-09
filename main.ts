function fahren () {
    if (maqueen.ultrasonic(maqueen.DistanceUnit.Centimeters) > 0 && maqueen.ultrasonic(maqueen.DistanceUnit.Centimeters) < 10) {
        maqueen.motorStop(maqueen.Motors.All)
        drehen()
    } else {
        maqueen.writeLED(maqueen.Led.LedAll, maqueen.LedSwitch.LedOn)
        maqueen.setColor(0x00ff00)
        basic.setLedColor(0x00ff00)
        maqueen.motorRun(maqueen.Motors.All, maqueen.Dir.CW, 50)
    }
}
function drehen () {
    let abstand_links: number;
let abstand_vorne: number;
// Schaue nach rechts
    maqueen.servoRun(maqueen.Servos.S1, 0)
    basic.pause(1000)
    abstand_rechts = maqueen.ultrasonic(maqueen.DistanceUnit.Centimeters)
    if (abstand_rechts > 0 && abstand_rechts > 10) {
        // Rechts ist frei -> nach rechts drehen
        maqueen.setColor(0x0000ff)
        basic.setLedColor(0x0000ff)
        maqueen.servoRun(maqueen.Servos.S1, 85)
        basic.pause(500)
        maqueen.motorRun(maqueen.Motors.M1, maqueen.Dir.CW, 50)
        basic.pause(1200)
        maqueen.motorStop(maqueen.Motors.All)
    } else {
        // Rechts nicht frei -> schaue nach links
        maqueen.servoRun(maqueen.Servos.S1, 180)
        basic.pause(1000)
        abstand_links = maqueen.ultrasonic(maqueen.DistanceUnit.Centimeters)
        if (abstand_links > 0 && abstand_links > 10) {
            // Links ist frei -> nach links drehen
            maqueen.setColor(0x0000ff)
            basic.setLedColor(0x0000ff)
            maqueen.servoRun(maqueen.Servos.S1, 85)
            basic.pause(500)
            maqueen.motorRun(maqueen.Motors.M2, maqueen.Dir.CW, 50)
            basic.pause(1200)
            maqueen.motorStop(maqueen.Motors.All)
        } else {
            // Beide Seiten blockiert -> rückwärts fahren bis Abstand > 20 cm
            maqueen.setColor(0xff0000)
            basic.setLedColor(0xff0000)
            maqueen.servoRun(maqueen.Servos.S1, 85)
            basic.pause(500)
            maqueen.motorRun(maqueen.Motors.All, maqueen.Dir.CCW, 50)
            while (true) {
                abstand_vorne = maqueen.ultrasonic(maqueen.DistanceUnit.Centimeters)
                if (abstand_vorne > 20) {
                    break;
                }
                basic.pause(100)
            }
            maqueen.motorStop(maqueen.Motors.All)
            // Zufällig nach links oder rechts drehen
            if (randint(0, 1) == 0) {
                maqueen.motorRun(maqueen.Motors.M1, maqueen.Dir.CW, 50)
            } else {
                maqueen.motorRun(maqueen.Motors.M2, maqueen.Dir.CW, 50)
            }
            basic.pause(1200)
            maqueen.motorStop(maqueen.Motors.All)
        }
    }
    maqueen.servoRun(maqueen.Servos.S1, 85)
    basic.pause(500)
}
input.onButtonEvent(Button.A, input.buttonEventClick(), function () {
    Status = 1
})
input.onButtonEvent(Button.B, input.buttonEventClick(), function () {
    maqueen.motorStop(maqueen.Motors.All)
    Status = 0
})
let Status = 0
let abstand_rechts = 0
maqueen.motorStop(maqueen.Motors.All)
maqueen.servoRun(maqueen.Servos.S1, 85)
basic.forever(function () {
    if (Status == 1) {
        fahren()
    }
})
