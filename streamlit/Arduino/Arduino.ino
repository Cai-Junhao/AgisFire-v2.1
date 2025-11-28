#include <DHT.h>  // 包含DHT库

// RGB全彩LED模块引脚定义
int rgbLedPinR = 9;  // R引脚连接到Arduino的数字引脚9
int rgbLedPinG = 11;  // G引脚连接到Arduino的数字引脚11
int rgbLedPinB = 10;  // B引脚连接到Arduino的数字引脚10

unsigned long previousMillis = 0;  // 用于存储上一次的时间戳
const long interval = 1000;  // 闪烁间隔为1秒

char receivedChar;  // 定义接收字符变量
bool alarmStatus = true;  // 定义报警状态变量



void setup() {
  pinMode(rgbLedPinR, OUTPUT);  // 设置RGB全彩LED的R引脚为输出模式
  pinMode(rgbLedPinG, OUTPUT);  // 设置RGB全彩LED的G引脚为输出模式
  pinMode(rgbLedPinB, OUTPUT);  // 设置RGB全彩LED的B引脚为输出模式

  alarmStatus = false; // Set alarmStatus to false initially
  digitalWrite(rgbLedPinR, HIGH); // Turn off RGB LEDs (HIGH for off)
  digitalWrite(rgbLedPinG, HIGH);
  digitalWrite(rgbLedPinB, HIGH);

}

void loop() {
  // 读取串口数据
  if (Serial.available() > 0) {
    receivedChar = Serial.read();
    Serial.println(receivedChar);
    if (receivedChar == '1') {
      alarmStatus = true;
      Serial.println("Alarm is activated");
    } else if (receivedChar == '0') {
      alarmStatus = false;
      Serial.println("Alarm is deactivated");
    }
  }

  // 控制报警状态下的LED和蜂鸣器
  if (alarmStatus) {
    digitalWrite(rgbLedPinR, LOW);
    digitalWrite(rgbLedPinG, HIGH);
    digitalWrite(rgbLedPinB, HIGH);
  } else {
    digitalWrite(rgbLedPinR, HIGH);
    digitalWrite(rgbLedPinG, HIGH);
    digitalWrite(rgbLedPinB, HIGH);
  }


  delay(10);
}
