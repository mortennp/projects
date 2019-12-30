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

#define ledPin    1  	//define the ledPin
#define sensorPin 0		//define the sensorPin

char* getTimeString(void)
{
	time_t rawtime;
	struct tm * timeinfo;

	time( &rawtime );
	timeinfo = localtime( &rawtime );
	return asctime( timeinfo );
}

int main(void)
{
	printf("Starting...\n");

	if(wiringPiSetup() == -1){ //when initialize wiring failed,print messageto screen
		printf("Setup of wiringPi failed!\n");
		return 1; 
	}
	
	pinMode(ledPin, OUTPUT); 
	pinMode(sensorPin, INPUT);
	int i = 0;	
	int status = LOW;
	while(1){		
		if (digitalRead(sensorPin) == HIGH){ //if read sensor for high level
			if (HIGH != status) {
				digitalWrite(ledPin, HIGH);   //led on
				printf("%s %i: led on...\n", getTimeString(), i++);
				status = HIGH;
			}
		}
		else {				
			if (LOW != status)
			{
				digitalWrite(ledPin, LOW);   //led off
				printf("%s %i: ...led off\n", getTimeString(), i++);
				status = LOW;
			}
		}
	}

	return 0;
}

