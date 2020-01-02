# Vars
CC = gcc
CXX = g++
BUILD=build/
CFLAGS = 
#-D_POSIX_C_SOURCE=199309L
LFLAGS =  -lwiringPi
TARGET = SenseLED

debug:		 local_CFLAGS = -Wconversion -g -O0 -DDEBUG $(CFLAGS)
release:     local_CFLAGS = -Wconversion -O3 -march=native $(CFLAGS) -DRELEASE

# Targets
all: debug

debug:   clean $(TARGET)

release: clean $(TARGET)

$(TARGET): 
	$(CC) $(TARGET).c -o $(BUILD)$(TARGET) $(local_CFLAGS) $(LFLAGS) $(DISABLED_WARNINGS)

MPU:	
	$(CC) attitude/MPU6050RAW.cpp attitude/MPU6050.cpp attitude/I2Cdev.cpp -o $(BUILD)$(TARGET) $(local_CFLAGS) $(LFLAGS) $(DISABLED_WARNINGS)	

DHT:
	$(CC) hygro/DHT.cpp hygro/DHT11.cpp -o $(BUILD)$(TARGET) $(local_CFLAGS) $(LFLAGS) $(DISABLED_WARNINGS)	

clean:
	rm -f $(BUILD)$(TARGET)
