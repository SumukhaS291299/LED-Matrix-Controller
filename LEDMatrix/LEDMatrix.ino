#include <FastLED.h>
#define LEDNumber 64
#define DataPin 3
#include <string.h>

CRGB leds[LEDNumber];
String LED;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  LEDS.addLeds<WS2812, DataPin, RGB>(leds, LEDNumber);
  LEDS.setBrightness(50);
}

void loop() {
  // put your main code here, to run repeatedly:
  // "334423451201550607"   "33#44#23#45#12#01#55#06#07" "0|0|100$12#0|0|100$19#0|0|100$26#0|0|100$33#0|0|100$42#0|0|100$51#0|0|100$60#0|0|100$53#0|0|100$46#0|0|100$39#0|0|100$30#0|0|100$21"
  if (Serial.available() > 0) {
    LED = Serial.readString();
    Serial.println(LED);
    FastLED.clear();
    String string_to_split = LED;  // Replace with your string
    char delimiter = '#';          // Character to split at

    // Create a dynamic array to store the substrings
    String substrings[LED.length()];  // Adjust size as needed
    int substring_count = 0;

    // Split the string and store substrings in the array
    int startIndex = 0;
    int endIndex = string_to_split.indexOf(delimiter);
    if (LED != "\n") {
      while (endIndex != -1) {
        substrings[substring_count++] = string_to_split.substring(startIndex, endIndex);
        startIndex = endIndex + 1;
        endIndex = string_to_split.indexOf(delimiter, startIndex);
      }
      substrings[substring_count++] = string_to_split.substring(startIndex);  // Add the last part

      // Print the substrings to the serial monitor (optional)
      for (int i = 0; i < substring_count; i++) {
        // Split Color and LED Number
        // Split where there is $ and then Right [1] value will be LED Number
        // l --> LED Number
        // R --> Red Value
        // G --> Green Value
        // B --> Blue value
        // Splot the left [0] value and Split it with | will get 3 sub strings which are RGB values
        // Serial.println(substrings[i]);
        int DollerIndx = substrings[i].indexOf('$');
        String LEDNoStr = substrings[i].substring(DollerIndx + 1, substrings[i].length());
        // Serial.println(LEDNoStr);
        String RGBSeqStr = substrings[i].substring(0, DollerIndx);
        // Serial.println(RGBSeqStr);
        int FirstLine = RGBSeqStr.indexOf('|');
        String Rstr = RGBSeqStr.substring(0, FirstLine);
        // Serial.println(Rstr);
        int SecondLine = RGBSeqStr.indexOf('|', FirstLine + 1);
        String Gstr = RGBSeqStr.substring(FirstLine + 1, SecondLine);
        // Serial.println(Gstr);
        String Bstr = RGBSeqStr.substring(SecondLine + 1, RGBSeqStr.length());
        // Serial.println(Bstr);
        int l = LEDNoStr.toInt();
        int R = Rstr.toInt();
        int G = Gstr.toInt();
        int B = Bstr.toInt();
        // Serial.println(l);
        // Serial.println(R);
        // Serial.println(G);
        // Serial.println(B);
        leds[l].setRGB(R, G, B);
        delay(50);
        // Serial.println("\n");
      }
    }
    // FastLED.clear();
    FastLED.show();
  }
}
