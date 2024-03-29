/*
 * SimpleSender.cpp
 *
 *  Demonstrates sending IR codes in standard format with address and command
 *  An extended example for sending can be found as SendDemo.
 *
 *  Copyright (C) 2020-2022  Armin Joachimsmeyer
 *  armin.joachimsmeyer@gmail.com
 *
 *  This file is part of Arduino-IRremote https://github.com/Arduino-IRremote/Arduino-IRremote.
 *
 *  MIT License
 */
#include <Arduino.h>

#define DISABLE_CODE_FOR_RECEIVER // Disables restarting receiver after each send. Saves 450 bytes program memory and 269 bytes RAM if receiving functions are not used.
//#define SEND_PWM_BY_TIMER         // Disable carrier PWM generation in software and use (restricted) hardware PWM.
//#define USE_NO_SEND_PWM           // Use no carrier PWM, just simulate an active low receiver signal. Overrides SEND_PWM_BY_TIMER definition

#include "PinDefinitionsAndMore.h" // Define macros for input and output pin etc.
#include <IRremote.hpp>

int LASER_PIN = 5;
long BAUD = 115200;

void setup() {
    pinMode(LED_BUILTIN, OUTPUT);
	pinMode(LASER_PIN, OUTPUT);

    Serial.begin(BAUD);

    // Just to know which program is running on my Arduino
    Serial.println(F("START " __FILE__ " from " __DATE__ "\r\nUsing library version " VERSION_IRREMOTE));
    Serial.print(F("Send IR signals at pin "));
    Serial.println(IR_SEND_PIN);

    /*
     * The IR library setup. That's all!
     */
//    IrSender.begin(); // Start with IR_SEND_PIN as send pin and if NO_LED_FEEDBACK_CODE is NOT defined, enable feedback LED at default feedback LED pin
    IrSender.begin(DISABLE_LED_FEEDBACK); // Start with IR_SEND_PIN as send pin and disable feedback LED at default feedback LED pin
}

/*
 * Set up the data to be sent.
 * For most protocols, the data is build up with a constant 8 (or 16 byte) address
 * and a variable 8 bit command.
 * There are exceptions like Sony and Denon, which have 5 bit address.
 */
uint8_t sCommand = 0x18;

void loop() {
    // wait for input
    while (Serial.available() == 0) {}

    char input = Serial.read();
    
    // convert uppercase to lowercase
    if (!isdigit(input) && isupper(input)) {
        input = input - 'A' + 'a';
    }

    switch (input) {
        case '1': // one degree
            sCommand = 0x46;
            break;
        case 'p': // play/pause
            sCommand = 0x19;
            break;
        case 's': // set origin
            sCommand = 0x7;
            break;
        case 'o': // go to origin
            sCommand = 0x9;
            break;
        case 'a': // CCW
            sCommand = 0xD;
            break;
        case 'd': // CW
            sCommand = 0x16;
            break;
        case 'q': // slower
            sCommand = 0x18;
            break;
        case 'e': // faster
            sCommand = 0x15;
            break;
        case 'f': // 180
            sCommand = 0x40;
            break;
		case 'l': // laser toggle
			digitalWrite(LASER_PIN, !digitalRead(LASER_PIN));
			return;
        default:
            Serial.println(F("Invalid selection"));
    }

    Serial.println();
    Serial.print(F("Send now: address=0x00, command=0x"));
    Serial.print(sCommand, HEX);
    Serial.println();

    Serial.println(F("Send standard NEC with 8 bit address"));
    Serial.flush();

    delayMicroseconds(13);

    IrSender.sendNEC(0x00, sCommand, 3); // 3rd arg is numRepeats
    Serial.readString(); // clear monitor

    delayMicroseconds(13);
    
    delay(200);// delay must be greater than 5 ms (RECORD_GAP_MICROS), otherwise the receiver sees it as one long signal
}
