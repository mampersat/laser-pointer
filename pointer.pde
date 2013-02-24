// Laser Testing
// by M@ <http://mampersat.com>
// Testing my laser pointer

#include <Servo.h>
#include <stdarg.h>

const int laser_pin = 12;

int _x = 90;
int _y = 90;

int ulx = 57; int uly=56;
int urx = 93; int ury=69;
int llx = 55; int lly = 105;
int lrx = 94; int lry = 95;

Servo servoX; Servo servoY;

void setup() {
  pinMode(12, OUTPUT);
  servoX.attach(9);
  servoY.attach(6);
  
  Serial.begin(9600);
  Serial.println("Running");  
}

/*************************************************/
void loop() {
  listenAndGo();
  //blinkCorners();
  
}

void listenAndGo() {
  laser_on();
  int b = Serial.read();
  
  if (b==0)
  {
    int r = -1;
    while (r == -1)
    {
      r = Serial.read();
    }
    servoX.write(r);
    
    r = -1;
    while (r == -1)
    {
      r = Serial.read();
    }
    servoY.write(r);
    
  }
}
void blinkSpeedUp() {
  float i = 1000;
  
  while (i>10)
  {
    laser_on();
    delay(i);
    laser_off();
    delay(i);
    i = i /1.3;
  }
}

void startupBlink() {
  servoX.write(90);
  servoY.write(90);
  
  for (int i = 0; i<5; ++i)
  {
    laser_on();
    delay(500);
    laser_off();
    delay(500);
  }
}

void trim(){
  int b;
  b = Serial.read();
  
  switch(b)
  {
    // S, R, 
    case 'w': gotoBlink(ulx, uly); Serial.println("upper left locate"); break;
    case 'q': ulx--; Serial.println("upper left left"); break; 
    case '2': uly--; Serial.println("upper left up"); break; 
    case 's': uly++; Serial.println("upper left down"); break; 
    case 'e': ulx++; Serial.println("upper left right"); break; 
    
    case 't': gotoBlink(urx, ury); Serial.println("upper left locate"); break;
    case 'r': urx--; Serial.println("upper right left"); break; 
    case '5': ury--; Serial.println("upper right up"); break; 
    case 'g': ury++; Serial.println("upper right down"); break; 
    case 'y': urx++; Serial.println("upper right right"); break; 
    
    case 'i': gotoBlink(lrx, lry); Serial.println("upper left locate"); break;
    case 'u': lrx--; Serial.println("lower right left"); break; 
    case '8': lry--; Serial.println("lower right up"); break; 
    case 'k': lry++; Serial.println("lower right down"); break; 
    case 'o': lrx++; Serial.println("lower right right"); break; 
    
    case '[': gotoBlink(llx, lly); Serial.println("upper left locate"); break;
    case 'p': llx--; Serial.println("lower left left"); break; 
    case '-': lly--; Serial.println("lower left up"); break; 
    case '\'': lly++; Serial.println("lower left down"); break; 
    case ']': llx++; Serial.println("lower left right"); break; 
    
    case 'a':
      Serial.println( "UL= " + String(ulx) + "," + String(uly) );
      Serial.println( "UR= " + String(urx) + "," + String(ury) );
      Serial.println( "LL= " + String(llx) + "," + String(lly) );
      Serial.println( "LR= " + String(lrx) + "," + String(lry) );
      break;

  }
  
}

void trimCorners() {
  sweepTo(ulx, uly);
  sweepTo(urx, ury);
  sweepTo(lrx, lry);
  sweepTo(llx, lly);
}

void blinkCorners() {
  gotoBlink(ulx, uly);
  gotoBlink(urx, ury);
  gotoBlink(lrx, lry);
  gotoBlink(llx, lly);
}

void sweepTo(int x, int y)
{
  sweepTo(x,y,25);
}

void sweepTo(int x, int y, int d)
{

  float steps = max( abs(_x -x), abs(_y -y));

  float xd = (x - _x)/ steps;
  float yd = (y - _y)/ steps;

  laser_on();
  for (int i = 0; i <= steps; ++i)
  {
    servoX.write(_x + xd*i);
    servoY.write(_y + yd*i);
    delay(d);
    trim();
  }
  
  _x = x;  _y = y;
}

  

void gotoBlink()
{
  gotoBlink(_x, _y);
}

void gotoBlink(int x, int y)
{

  _x = x; _y = y;
  servoX.write(_x);
  servoY.write(_y);
  delay(100);
  laser_on();
  delay(1500);
  laser_off();
  trim();
  
}
void laser_on() {

  digitalWrite(laser_pin, HIGH);
}

void laser_off() {

  digitalWrite(laser_pin, LOW);
}  

/**** others code */
void p(char *fmt, ... ){
        char tmp[128]; // resulting string limited to 128 chars
        va_list args;
        va_start (args, fmt );
        vsnprintf(tmp, 128, fmt, args);
        va_end (args);
        Serial.print(tmp);
}
