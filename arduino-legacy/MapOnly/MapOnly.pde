import processing.serial.*;

Serial laser;

void setup()
{
  size(180 * 6, 180 * 4);
  PImage p = loadImage("maporig.jpg");
  image (p, 0 ,0);

  laser = new Serial(this, Serial.list()[1], 9600);
}

void draw()
{
  if (mousePressed)
  {
    laser.write(0);
    laser.write(mouseX/6);
    laser.write(mouseY/4);
    //ellipse(mouseX, mouseY,3,3);
  }
}
