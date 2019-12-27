/**********************************************************************
* Filename    : SenseLED.c
* Description : Controlling an led by infrared Motion sensor.
* Author      : freenove
* modification: 2016/06/12
**********************************************************************/
#include <wiringPi.h>
#include <stdio.h>

#define ledPin    1  	//define the ledPin
#define sensorPin 0		//define the sensorPin

int main(void)
{
	if(wiringPiSetup() == -1){ //when initialize wiring failed,print messageto screen
		printf("setup wiringPi failed !");
		return 1; 
	}
	
	pinMode(ledPin, OUTPUT); 
	pinMode(sensorPin, INPUT);
	int i = 0;
	int status = LOW;
	while(1){		
		if(digitalRead(sensorPin) == HIGH){ //if read sensor for high level
			if (HIGH != status) {
				digitalWrite(ledPin, HIGH);   //led on
				printf("%i: led on...\n", i++);
				status = HIGH;
			}
		}
		else {				
			if (LOW != status)
			{
				digitalWrite(ledPin, LOW);   //led off
				printf("%i: ...led off\n", i++);
				status = LOW;
			}
		}
	}

	return 0;
}

