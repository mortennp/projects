/**********************************************************************
* Filename    : SenseLED.c
* Description : Controlling an led by infrared Motion sensor.
* Author      : freenove
* modification: 2016/06/12
**********************************************************************/
#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <wiringPi.h>

#define LED_PIN    1  	//define the ledPin
#define SENSOR_PIN 0		//define the sensorPin

char* getTimeString(void)
{
	time_t rawtime;
	struct tm * timeinfo;

	time( &rawtime );
	timeinfo = localtime( &rawtime );
	return asctime( timeinfo );
}

int loop(void)
{
	pinMode(LED_PIN, OUTPUT); 
	pinMode(SENSOR_PIN, INPUT);
	int i = 0;	
	int status = LOW;
	while (1) {		
		if (digitalRead(SENSOR_PIN) == HIGH){ //if read sensor for high level
			if (HIGH != status) {
				digitalWrite(LED_PIN, HIGH);   //led on
				printf("%s %i: led on...\n", getTimeString(), i++);
				status = HIGH;
			}
		}
		else {				
			if (LOW != status)
			{
				digitalWrite(LED_PIN, LOW);   //led off
				printf("%s %i: ...led off\n", getTimeString(), i++);
				status = LOW;
			}
		}
	}

	return 0;
}

void handler(void)
{
	system("kill -USR1 $(pgrep raspivid)");
	delay(5000);
	system("kill -USR1 $(pgrep raspivid)");

	//printf("Capture status: %i\n", system("kill -USR1 $(pgrep raspistill)"));
	//printf("Sensor status: %i\n", digitalRead(SENSOR_PIN));
}

int wait_for_event(void)
{
	int ec = wiringPiISR(SENSOR_PIN, INT_EDGE_RISING, &handler);
	if (ec != -0) { 
		printf("Setup of handler failed!\n");
		return 1; 
	}

	while(1) {
		delay(10000);
		// printf(".\n");
	}

	return 0;
}

int main(void)
{
	printf("Starting...\n");

	if(wiringPiSetup() == -1){ //when initialize wiring failed,print messageto screen
		printf("Setup of wiringPi failed!\n");
		return 1; 
	}
	
	// return loop();
	return wait_for_event();
}

