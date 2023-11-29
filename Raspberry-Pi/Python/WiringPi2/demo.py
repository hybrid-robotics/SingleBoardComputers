import wiringpi2
#wiringpi2.wiringPiSetup() # For sequential pin numbering, one of these MUST be called before using IO functions
#                        OR
wiringpi2.wiringPiSetupSys() # For /sys/class/gpio with GPIO pin numbering
#                                        OR
#wiringpi2.wiringPiSetupGpio() # For GPIO pin numbering
                                                
