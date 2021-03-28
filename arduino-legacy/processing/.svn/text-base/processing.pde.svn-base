import processing.serial.*;

Serial laser;

//Top Left
float a=56;
float b=55;

//Top Right
float c=93;
float d=69;

//Bottom Left
float e=53;
float f=106;

//Bottom Right
float g=94;
float h=95;


float j=1377;
float k=985;

void setup()
{
  size((int)j, (int)k);

  PImage map;
  map = loadImage("mapCut.jpg");
  image(map,0,0);
  
  laser = new Serial(this, Serial.list()[1], 9600);
}

void draw()
{
  if (mousePressed)
  {
    
    float x = (float)mouseX;
    float y = (float)mouseY;
    ellipse(x, y,3,3);

    //modify x/y
    x = pow( (x/j) , 0.7) * j;
    y = pow( (y/k) , 1) * k;
    
    float r = (g-c) * (y/k) + c;
    float l = (e-a) * (y/k) + a;

    float xp = (x/j) * (r-l) + l;

    float bot = (h-f) * (x/j) + f;
    float t =   (d-b) * (x/j) + b;
    
    float yp = (y/k) * (bot-t) + t;
 
    //xp = a; yp = b;
    
    laser.write(0);
    laser.write((int)xp);
    laser.write((int)yp);
    
  }
}
