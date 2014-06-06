// Senior Care 2014
// Authors: Nathaniel Chen

#include <MMA_7455.h>
#include <Wire.h>

MMA_7455 accel = MMA_7455();
char x_val, y_val, z_val;
float x_g, y_g, z_g;
char y_store[3];

float y_max = -1.0;
float y_min = 0.0;
//count how many peaks in a time period
int thresh_counter = 0;
//what stage of the algorithm
int thresh_stage = 0;
//time between peak and trough
int peak_timer = 0;

char y_avg;
float y_avg_g = 0.0;


void setup() {
  //set up 2 analog pins as reference
  int ground = A2;
  int vcc = A0;
  pinMode(ground, OUTPUT);
  pinMode(vcc, OUTPUT);
  digitalWrite(ground, LOW);
  digitalWrite(vcc, HIGH);
  delay(1000);

  Serial.begin(9600);
  accel.initSensitivity(2);
  accel.calibrateOffset(-246, -230, 0);
}

void loop() {
    
  for (int i=0; i<2; i++) {
    y_store[i] = y_store[i+1];
  }
  y_val = accel.readAxis('y');
  y_g = y_val*0.0156;
  y_store[2] = y_val;
  //smoothed value
  y_avg = ((y_store[0] + y_store[1] + y_store[2])/3);
  y_avg_g = y_avg * 0.0156;

  //upper threshold
  if (y_avg_g > -0.75) {
    if (thresh_stage == 0){
      thresh_stage = 1;  
      peak_timer = 0;
      thresh_counter++;
    } else if ((thresh_stage == 2) && (peak_timer > 10) && (thresh_counter < 3)) {
      Serial.println('x');
      Serial.println(100);
      delay(20);
      thresh_stage = 0;
      peak_timer = 0;
      thresh_counter = 0;
    } else if (peak_timer > 20) {
      thresh_stage = 0;
      peak_timer = 0;  
      thresh_counter = 0;
    } else {
    }
  }
  //lower threshold
  if ((y_avg_g < -1.0) && (thresh_stage == 1) && (peak_timer > 10)){
    thresh_stage = 2;
    thresh_counter++;
  } 
  //reset if too long between upper/lower
  if ((thresh_stage == 1) && (peak_timer > 20)) {
    thresh_stage = 0;
    peak_timer = 0;  
    thresh_counter = 0;
  }
  
  
  peak_timer++;
  
  Serial.println("y");
  Serial.println(y_avg, DEC);

  delay(20);
 

}
