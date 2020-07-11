#include <Servo.h>
#include "DHT.h"
#include <ESP8266WiFi.h>
#include <FirebaseArduino.h>
Servo sg90;

#define lf D4
#define lb D3
#define rf D2
#define rb D1
#define DHTPIN D8
#define buzzer D7
#define pw 850
#define tp 1020 // turn speed
#define tim 900

#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

#define trig D5
#define echo D0

#define FIREBASE_HOST "Yourfirebaseurlwithoutlast'/'and'https//'.com"
#define FIREBASE_AUTH "Your own firebase token_or_secret"
#define WIFI_SSID "SSID"
#define WIFI_PASSWORD "PASSWORD"

int distance;
int turn_dis;
int look[3];
int second_part = 20;
byte center_point;
int angle[360];
float t;
float h;
int air_quality;

void setup() {
  pinMode(lf, OUTPUT);
  pinMode(lb, OUTPUT);
  pinMode(rf, OUTPUT);
  pinMode(rb, OUTPUT);
  pinMode(buzzer, OUTPUT);

  pinMode(trig, OUTPUT);
  pinMode(echo, INPUT);

  Serial.println(F("DHTxx test!"));

  dht.begin();

  sg90.attach(D6);
  delay(500);

  Serial.begin(9600);

  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }
  Serial.println();
  Serial.print("Connected: ");
  Serial.println(WiFi.localIP());
  
  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
  sg90.write(90);
  Firebase.remove("/MAPPRIME");
  
  
}

void loop() {
  distance = data();
  Serial.print("Distance: "); Serial.println(distance);
  Serial.print("Second_Part: "); Serial.println(second_part);
  
  if (distance < second_part)
  {
    second_part = general(distance, second_part);
    Serial.println("ELSE");
  }
  else
  {
    motor(pw,0,pw,0);
    Serial.print("GO STRAIGHT ON...");
  }
}

void motor (int lfp,int lbp,int rfp,int rbp)
{
  analogWrite(lf ,lfp);
  analogWrite(lb ,lbp);
  analogWrite(rf ,rfp*0.95);
  analogWrite(rb ,rbp*0.95);
}

int data()
{
  digitalWrite(trig, LOW);
  delayMicroseconds(20);
  digitalWrite(trig, HIGH);
  delayMicroseconds(40);
  digitalWrite(trig, LOW);
  delayMicroseconds(20);
  
  int sure = pulseIn(echo,HIGH);
  int mesafe = (sure/2)/29.1; // or /29.1
  delay(30); // Sensörden daha doğru değer almak için...

  return mesafe;
}

int general(int a, int limit)
{
  Serial.println("General Function...  ");
  if (a < limit)
  {
    Serial.println("Motors Stopped...");
    motor(0,0,0,0);
    for (byte i = 0; i <= 2; i++)
    {
      sg90.write(90*i);
      delay(750);
      look[i] = data();
    }
    Serial.println("Datas is Taken...");
    sg90.write(90);
    delay(750);
    if (look[0] > look[2])
    {
      
      if((look[0] - look[2]) < 10)
        {
          center_point++;
          end_function();
        }
      else
        center_point = 0;
      Serial.print("FARK...   ");Serial.print(look[0] - look[2]);
      Serial.print("CENTER POINTS...   ");Serial.print(center_point);
      Serial.println("Second Part was Updated...  ");Serial.println(second_part);

      Serial.println("TURNING RIGHT...");
      motor(tp,0,0,tp);
      delay(tim);
      second_part = (look[0] + look[2]) / 2;
      return second_part;
    }
    else if (look[2] >= look[0])
    {
      
      second_part = (look[2] + look[0]) / 2;
      if ((look[2] - look[0]) < 10)
        {
          center_point++;
          end_function();
        }
      else
        center_point = 0;
      Serial.print("DIFFERENCES...   ");Serial.print(look[2] - look[0]);
      Serial.print("CENTER POINTS...   ");Serial.print(center_point);
      Serial.println("Second Part Updated...  ");Serial.println(second_part);

      Serial.println("TURNING LEFT...");
      motor(0,tp,tp,0);
      delay(tim);
      return second_part;
    }
  }
}

int scan (byte a)
{
  sg90.write(0);
  delay(1000);
  for (int i = 0; i < 180; i++)
  {
    sg90.write(i);
    delay(10);
    angle[a + i] = data();
  }
}

void firebase (int temperature, int humudity, int air_quality)
{
  while(true)
  {
  Firebase.setFloat("DATAPRIME/Temperature", temperature);
  if (Firebase.failed()) {
      Serial.print("Setting /Temperature Failed:");
      Serial.println(Firebase.error());  
  }
  else
    break;
  delay(1000);
  }
  
  while(true)
  {
  Firebase.setFloat("DATAPRIME/Humidity", humudity);
  if (Firebase.failed()) {
      Serial.print("Setting /Humudity Failed:");
      Serial.println(Firebase.error());  
  }
  else
    break;
  delay(1000);
  }
  
  while(true)
  {
  Firebase.setFloat("DATAPRIME/Air-quality", air_quality);
  if (Firebase.failed()) {
      Serial.print("Setting /Air_quality Failed:");
      Serial.println(Firebase.error());  
  }
  else
    break;
  delay(1000);
  }
  
  
  int k = 0;
  while(true)
  {
    Firebase.pushFloat("MAPPRIME/Angle", angle[k]);
    if (Firebase.failed()) {
        Serial.print("Setting /Area Failed:");
        Serial.println(Firebase.error());  
    }
    else
      k++;
    Serial.print(k-1); Serial.print("  .Angle :    ");  Serial.println(angle[k-1]);
    if (k == 360)
      break;
  }
  Serial.println("THATS ALL !!!");
}

void end_function()
{
  if (center_point >= 2)
  {
    Serial.println("WE ARE İN CENTER POİNT. CONGRATULATİONS...");

    Serial.println("MQ-135");

    air_quality = analogRead(A0);
    Serial.print("Air-quality :   ");Serial.println(air_quality);

    Serial.println("SCANNN");
    motor(0,0,0,0);
    delay(500);
    scan(0);
    sg90.write(90);
    delay(750);
    motor(0,tp,tp,0);
    delay(2*tim);
    
    motor(0,0,0,0);
    delay(500);
    scan(180);
    sg90.write(90);
    delay(750);
    
    
    Serial.println("DHT-11");
    while(true)
    {
      delay(2000);
  
      h = dht.readHumidity();
      t = dht.readTemperature();

      Serial.print(F("Humidity: "));
      Serial.print(h);
      Serial.print(F("%  Temperature: "));
      Serial.print(t);
      Serial.print(F("°C "));
      
      if (isnan(h) || isnan(t))
        Serial.println(F("Failed to read from DHT sensor!"));
      else
        break;
    }
    
    firebase(t,h,air_quality);
    while(true)
    {
      digitalWrite(buzzer, HIGH);
      delay(1000);
      digitalWrite(buzzer, LOW);
      delay(1000);
      Serial.println("PROJECT WAS ENDED...");
    }
  }
}
