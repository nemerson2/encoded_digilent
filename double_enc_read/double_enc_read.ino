volatile long temp1, enc1, temp2, enc2 = 0; 
volatile int old2, new2, old3, new3, old4, new4, old5, new5 = 0;

void setup() {
  Serial.begin(9600);
  pinMode(2, INPUT_PULLUP);
  pinMode(3, INPUT_PULLUP);
  pinMode(4, INPUT_PULLUP);
  pinMode(5, INPUT_PULLUP);
   //Setting up interrupt
  //A rising pulse from encodenren activated ai0(). AttachInterrupt 0 is DigitalPin nr 2 on moust Arduino.
  // attachInterrupt(0, ai0, RISING);
   
  //B rising pulse from encodenren activated ai1(). AttachInterrupt 1 is DigitalPin nr 3 on moust Arduino.
  // attachInterrupt(1, ai1, RISING);
}

  void loop() {
    // put your main code here, to run repeatedly:
    if( enc1 != temp1) {
      Serial.print("encoder1 ");
      Serial.println(enc1);
      temp1 = enc1;
    }
    new2 = digitalRead(2);
    new3 = digitalRead(3);
    if(new2 != old2) {
      if(new2==HIGH) {
        if(old3==LOW){
          enc1++;
      } else if(old3==HIGH){
          enc1--;}
      else if(new2==LOW) {
        if(old3==LOW) {
          enc1++;
        }else if(old3==HIGH) {
          enc1--;
        }
        }
      }
    }
    old3 = new3;
    old2 = new2;

    if( enc2 != temp2) {
      // Serial.println (counter);
      // temp = counter;
      Serial.print("encoder2 ");
      Serial.println(enc2);
      temp2 = enc2;
    }
    new4 = digitalRead(4);
    new5 = digitalRead(5);
    if(new4 != old4) {
      if(new4==HIGH) {
        if(old5==LOW){
          enc2++;
      } else if(old5==HIGH){
          enc2--;}
      else if(new4==LOW) {
        if(old5==LOW) {
          enc2++;
        }else if(old5==HIGH) {
          enc2--;
        }
        }
      }
    }
    old5 = new5;
    old4 = new4;
  }
