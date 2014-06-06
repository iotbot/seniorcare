// Senior Care 2014
// Authors: Nathaniel Chen

#include <MMA_7455.h>
#include <Wire.h>

MMA_7455 accel = MMA_7455();
char x_val, y_val, z_val;
float x_g, y_g, z_g;
char z_store[10];
long count_10 = 0;
long count_first5 = 0;
long count_last5 = 0;

long max_10 = 0;
long min_10 = 0;
float max_10_g = 0;
float min_10_g = 0;

float z_g_avg_10 = 0;
float z_g_avg_first5 = 0;
float z_g_avg_last5 = 0;

//track where in the fall we are
int stage_tracker = 0;
//wait in 10 sample blocks
int wait_timer = 0;
//total fall time should be short
int fall_timer = 0;

void setup() {
  //set up 2 analog pins as reference
  int ground = A1;
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

  //set everything to 0
  count_10 = 0;
  count_first5 = 0;
  count_last5 = 0;
  max_10 = 0;
  ///min should start HIGH
  min_10 = 1000;
  max_10_g = 0;
  min_10_g = 0;
  z_g_avg_10 = 0;
  z_g_avg_first5 = 0;
  z_g_avg_last5 = 0;
  
//  x_val = accel.readAxis('x');
//  Serial.println("x");
//  Serial.println(x_val, DEC);
//  delay(5);
  
//  y_val = accel.readAxis('y');
//  Serial.println("y");
//  Serial.println(y_val, DEC);
//  delay(5);
  
  //shift storage, dump oldest value
  for (int i=0; i<9; i++) {
    z_store[i] = z_store[i+1];    
    //averaging
    count_10 += z_store[i];
    if (i<5) {
      count_first5 += z_store[i]; 
    }
    if (i>=5) {
      count_last5 += z_store[i];  
    }
    //peak detection
    if (z_store[i] > max_10) {
      max_10 = z_store[i];
    }
    //trough detection
    if (z_store[i] < min_10) {
      min_10 = z_store[i];
    }
  }  
  
  //get raw value and store
  z_val = accel.readAxis('z');
  z_store[9] = z_val;
  
  //average past 10 and past 5 values
  count_10 += z_store[9];
  count_last5 += z_store[9];
  z_g_avg_10 = (count_10/10)*0.0156;
  z_g_avg_first5 = (count_first5/5)*0.0156;
  z_g_avg_last5 = (count_last5/5)*0.0156;
  
  //convert peak and trough to g
  max_10_g = max_10*0.0156;
  min_10_g = min_10*0.0156;
  
  //stage 1
  z_g = z_val*0.0156;
  if ((stage_tracker == 0) && (z_g < 0.25) && (z_g > 0.0) && (z_g_avg_last5 > 0.0) && (z_g_avg_last5 < 1.0)) {
    stage_tracker = 1;
    wait_timer = 0;
    fall_timer = 0;
    Serial.println("y");
    Serial.println(100);
  }
  //stage 2: make sure it didn't dip below 0g in the first five after passing 0.25 on the way . Also, not recovered to 1g yet
  else if ((stage_tracker == 1) && (wait_timer > 10) && (min_10_g > 0.0) && (max_10_g < 0.75)) {
    stage_tracker = 2;
    wait_timer = 0;
    Serial.println("y");
    Serial.println(100);
  }
  //stage 3
  else if ((stage_tracker == 2) && (wait_timer > 10) && ((max_10_g - min_10_g) > 1.0)) {
    stage_tracker = 3;
    wait_timer = 0;
    Serial.println("y");
    Serial.println(100);  
  }
  //stage 4
  else if ((stage_tracker == 3) &&
           (wait_timer > 50) &&
           //the last two sets of 5 samples are similar   0|  first  |  last  |9 
           //((z_g_avg_last5 > (z_g_avg_first5 - 0.10)) && (z_g_avg_last5 < (z_g_avg_first5 + 0.10)))
           //no shock in the last ten samples
           ((max_10_g - min_10_g) < 0.25)           
           //TODO?: the last set of 10 samples is different from 
           //need to store more samples
           ){
             
    stage_tracker = 4;
    wait_timer = 0;
    //terrible debugging
    //when a fall is detected, prints a small bar where the x-axis should be
    //only works when x and y are disabled at top ^^^^
    
    if (fall_timer < 100) {
      Serial.println("x");
      Serial.println(100);
    }
    fall_timer = 0;
    stage_tracker = 0;
  } 
  else if (wait_timer > 100){
    stage_tracker = 0;
    wait_timer = 0;
  }

  wait_timer++;
  fall_timer++;
  
  Serial.println("z");
  Serial.println(z_val, DEC);

  delay(20);
}

