void setPwmFrequency(int pin, int divisor) {
  byte mode;
  if(pin == 5 || pin == 6 || pin == 9 || pin == 10) {
    switch(divisor) {
      case 1: mode = 0x01; break;
      case 8: mode = 0x02; break;
      case 64: mode = 0x03; break;
      case 256: mode = 0x04; break;
      case 1024: mode = 0x05; break;
      default: return;
    }
    if(pin == 5 || pin == 6) {
      TCCR0B = TCCR0B & 0b11111000 | mode;
    } else {
      TCCR1B = TCCR1B & 0b11111000 | mode;
    }
  } else if(pin == 3 || pin == 11) {
    switch(divisor) {
      case 1: mode = 0x01; break;
      case 8: mode = 0x02; break;
      case 32: mode = 0x03; break;
      case 64: mode = 0x04; break;
      case 128: mode = 0x05; break;
      case 256: mode = 0x06; break;
      case 1024: mode = 0x07; break;
      default: return;
    }
    TCCR2B = TCCR2B & 0b11111000 | mode;
  }
}



// the setup function runs once when you press reset or power the board
int tback = 11;
int bback = 10;
int but = 9;



int minVib = 30;
int maxVib = 255;
void setup() {
  
  // initialize digital pin LED_BUILTIN as an output.
  int pins[] = {3,5,6,7,8,9,10,11};
  for(int i=0;i<=7;i++){
    int pin = pins[i];
    pinMode(pin, OUTPUT);
    digitalWrite(pin, HIGH);
  }
  
   setPwmFrequency(bback, 1);
   setPwmFrequency(but, 1);
   setPwmFrequency(tback, 1);
}

void vibrate(int pos, int intensity){
  analogWrite(pos, 255-intensity);
}

void vibrateAll(int intensity){
  vibrate(but, intensity);
  vibrate(tback, intensity);
  vibrate(bback, intensity);
}

void vibrateAllM(int intensity){
  vibrate(but, intensity);
  vibrate(tback, intensity);
  vibrate(bback, intensity);
}

void beat(int style, int freq, int scalar){//freq in bpm
  if(style==0){
    float j = 0;
    int i=minVib;
    float omega = 3.141592654*freq/60000;
    while(i>=minVib){
      i = (maxVib-minVib)*sin(omega*j)+minVib;
      j++;
      vibrateAllM(i*scalar/100);
      delay(1);
    }
  }
}

// the loop function runs over and over again forever
void loop() {
  beat(0, 74, 35);
}