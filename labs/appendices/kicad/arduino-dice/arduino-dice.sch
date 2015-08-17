EESchema Schematic File Version 2
LIBS:power
LIBS:device
LIBS:transistors
LIBS:conn
LIBS:linear
LIBS:regul
LIBS:74xx
LIBS:cmos4000
LIBS:adc-dac
LIBS:memory
LIBS:xilinx
LIBS:microcontrollers
LIBS:dsp
LIBS:microchip
LIBS:analog_switches
LIBS:motorola
LIBS:texas
LIBS:intel
LIBS:audio
LIBS:interface
LIBS:digital-audio
LIBS:philips
LIBS:display
LIBS:cypress
LIBS:siliconi
LIBS:opto
LIBS:atmel
LIBS:contrib
LIBS:valves
LIBS:arduino-dice-cache
EELAYER 25 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L ATMEGA328P-P IC1
U 1 1 55CE75F6
P 3300 3450
F 0 "IC1" H 2550 4700 40  0000 L BNN
F 1 "ATMEGA328P-P" H 3700 2050 40  0000 L BNN
F 2 "arduino-dice-footprints:atmega328p-pu" H 3300 3450 30  0001 C CIN
F 3 "" H 3300 3450 60  0000 C CNN
	1    3300 3450
	1    0    0    -1  
$EndComp
$Comp
L R R2
U 1 1 55CE77A0
P 7000 2900
F 0 "R2" V 7080 2900 50  0000 C CNN
F 1 "10k" V 7000 2900 50  0000 C CNN
F 2 "arduino-dice-footprints:smd_0603" V 6930 2900 30  0001 C CNN
F 3 "" H 7000 2900 30  0000 C CNN
	1    7000 2900
	0    1    1    0   
$EndComp
$Comp
L 7SEGMENTS AFF1
U 1 1 55CE7823
P 6600 4550
F 0 "AFF1" H 6600 5100 60  0000 C CNN
F 1 "7SEGMENTS" H 6600 4100 60  0000 C CNN
F 2 "arduino-dice-footprints:7segment-hdsp-313e" H 6600 4550 60  0001 C CNN
F 3 "" H 6600 4550 60  0000 C CNN
	1    6600 4550
	1    0    0    -1  
$EndComp
$Comp
L R R1
U 1 1 55CE7957
P 4750 3800
F 0 "R1" V 4830 3800 50  0000 C CNN
F 1 "10k" V 4750 3800 50  0000 C CNN
F 2 "arduino-dice-footprints:smd_0603" V 4680 3800 30  0001 C CNN
F 3 "" H 4750 3800 30  0000 C CNN
	1    4750 3800
	0    1    1    0   
$EndComp
$Comp
L Crystal Y1
U 1 1 55CE79BA
P 4950 3000
F 0 "Y1" H 4950 3150 50  0000 C CNN
F 1 "16 MHz" H 4950 2850 50  0000 C CNN
F 2 "arduino-dice-footprints:crystal_hc49us" H 4950 3000 60  0001 C CNN
F 3 "" H 4950 3000 60  0000 C CNN
	1    4950 3000
	0    1    1    0   
$EndComp
$Comp
L C C2
U 1 1 55CE7AFB
P 5300 2850
F 0 "C2" H 5325 2950 50  0000 L CNN
F 1 "22pF" H 5325 2750 50  0000 L CNN
F 2 "arduino-dice-footprints:smd_0603" H 5338 2700 30  0001 C CNN
F 3 "" H 5300 2850 60  0000 C CNN
	1    5300 2850
	0    1    1    0   
$EndComp
$Comp
L C C3
U 1 1 55CE7BE8
P 5300 3150
F 0 "C3" H 5325 3250 50  0000 L CNN
F 1 "22pF" H 5325 3050 50  0000 L CNN
F 2 "arduino-dice-footprints:smd_0603" H 5338 3000 30  0001 C CNN
F 3 "" H 5300 3150 60  0000 C CNN
	1    5300 3150
	0    1    1    0   
$EndComp
$Comp
L SW_PUSH SW1
U 1 1 55CE7E1C
P 6750 2550
F 0 "SW1" H 6900 2660 50  0000 C CNN
F 1 "SW_PUSH" H 6750 2470 50  0000 C CNN
F 2 "arduino-dice-footprints:sw_push_b3f_1000" H 6750 2550 60  0001 C CNN
F 3 "" H 6750 2550 60  0000 C CNN
	1    6750 2550
	0    1    1    0   
$EndComp
Wire Wire Line
	4300 2950 4550 2950
Wire Wire Line
	4550 2950 4550 2850
Wire Wire Line
	4550 2850 5150 2850
Wire Wire Line
	4300 3050 4550 3050
Wire Wire Line
	4550 3050 4550 3150
Wire Wire Line
	4550 3150 5150 3150
Wire Wire Line
	4650 2750 4300 2750
Wire Wire Line
	6150 2900 6850 2900
Wire Wire Line
	6000 4650 4300 4650
Wire Wire Line
	6000 4550 4300 4550
Wire Wire Line
	6000 4450 4300 4450
Wire Wire Line
	6000 4350 4300 4350
Wire Wire Line
	6000 4250 4300 4250
Wire Wire Line
	4300 4150 6000 4150
Wire Wire Line
	4300 2350 5900 2350
Wire Wire Line
	5900 2350 5900 4750
Wire Wire Line
	5900 4750 6000 4750
$Comp
L GND #PWR01
U 1 1 55CE8044
P 5550 2850
F 0 "#PWR01" H 5550 2600 50  0001 C CNN
F 1 "GND" H 5550 2700 50  0000 C CNN
F 2 "" H 5550 2850 60  0000 C CNN
F 3 "" H 5550 2850 60  0000 C CNN
	1    5550 2850
	0    -1   -1   0   
$EndComp
$Comp
L GND #PWR02
U 1 1 55CE8140
P 5550 3150
F 0 "#PWR02" H 5550 2900 50  0001 C CNN
F 1 "GND" H 5550 3000 50  0000 C CNN
F 2 "" H 5550 3150 60  0000 C CNN
F 3 "" H 5550 3150 60  0000 C CNN
	1    5550 3150
	0    -1   -1   0   
$EndComp
Wire Wire Line
	5450 2850 5550 2850
Wire Wire Line
	5450 3150 5550 3150
$Comp
L C C1
U 1 1 55CE8287
P 1950 2900
F 0 "C1" H 1975 3000 50  0000 L CNN
F 1 "1uF" H 1975 2800 50  0000 L CNN
F 2 "arduino-dice-footprints:smd_0603" H 1988 2750 30  0001 C CNN
F 3 "" H 1950 2900 60  0000 C CNN
	1    1950 2900
	1    0    0    -1  
$EndComp
$Comp
L CONN_01X02 P1
U 1 1 55CE837D
P 1500 2400
F 0 "P1" H 1500 2550 50  0000 C CNN
F 1 "CONN_01X02" V 1600 2400 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Straight_1x02" H 1500 2400 60  0001 C CNN
F 3 "" H 1500 2400 60  0000 C CNN
	1    1500 2400
	-1   0    0    1   
$EndComp
Wire Wire Line
	1700 2350 2400 2350
Wire Wire Line
	1700 2450 1700 3150
Wire Wire Line
	1700 3150 1950 3150
Wire Wire Line
	1950 3050 1950 3300
Wire Wire Line
	1950 2150 1950 2750
Wire Wire Line
	1950 2650 2400 2650
$Comp
L VCC #PWR03
U 1 1 55CE8600
P 1950 2150
F 0 "#PWR03" H 1950 2000 50  0001 C CNN
F 1 "VCC" H 1950 2300 50  0000 C CNN
F 2 "" H 1950 2150 60  0000 C CNN
F 3 "" H 1950 2150 60  0000 C CNN
	1    1950 2150
	1    0    0    -1  
$EndComp
Connection ~ 1950 2350
Connection ~ 1950 2650
$Comp
L VCC #PWR04
U 1 1 55CE88AC
P 6750 2150
F 0 "#PWR04" H 6750 2000 50  0001 C CNN
F 1 "VCC" H 6750 2300 50  0000 C CNN
F 2 "" H 6750 2150 60  0000 C CNN
F 3 "" H 6750 2150 60  0000 C CNN
	1    6750 2150
	1    0    0    -1  
$EndComp
Wire Wire Line
	6750 2150 6750 2250
$Comp
L GND #PWR05
U 1 1 55CE8A84
P 1950 3300
F 0 "#PWR05" H 1950 3050 50  0001 C CNN
F 1 "GND" H 1950 3150 50  0000 C CNN
F 2 "" H 1950 3300 60  0000 C CNN
F 3 "" H 1950 3300 60  0000 C CNN
	1    1950 3300
	1    0    0    -1  
$EndComp
Connection ~ 1950 3150
$Comp
L GND #PWR06
U 1 1 55CE8CEC
P 2250 4800
F 0 "#PWR06" H 2250 4550 50  0001 C CNN
F 1 "GND" H 2250 4650 50  0000 C CNN
F 2 "" H 2250 4800 60  0000 C CNN
F 3 "" H 2250 4800 60  0000 C CNN
	1    2250 4800
	1    0    0    -1  
$EndComp
Wire Wire Line
	2400 4650 2250 4650
Wire Wire Line
	2250 4550 2250 4800
Wire Wire Line
	2400 4550 2250 4550
Connection ~ 2250 4650
$Comp
L VCC #PWR07
U 1 1 55CE8F1D
P 5050 3650
F 0 "#PWR07" H 5050 3500 50  0001 C CNN
F 1 "VCC" H 5050 3800 50  0000 C CNN
F 2 "" H 5050 3650 60  0000 C CNN
F 3 "" H 5050 3650 60  0000 C CNN
	1    5050 3650
	1    0    0    -1  
$EndComp
Wire Wire Line
	5050 3650 5050 3800
Wire Wire Line
	5050 3800 4900 3800
Wire Wire Line
	4600 3800 4300 3800
$Comp
L GND #PWR08
U 1 1 55CE9051
P 7400 4300
F 0 "#PWR08" H 7400 4050 50  0001 C CNN
F 1 "GND" H 7400 4150 50  0000 C CNN
F 2 "" H 7400 4300 60  0000 C CNN
F 3 "" H 7400 4300 60  0000 C CNN
	1    7400 4300
	1    0    0    -1  
$EndComp
Wire Wire Line
	7200 4200 7400 4200
Wire Wire Line
	7400 4100 7400 4300
Wire Wire Line
	7200 4100 7400 4100
Connection ~ 7400 4200
Wire Wire Line
	7300 4800 7200 4800
$Comp
L GND #PWR09
U 1 1 55CE94EA
P 7250 2900
F 0 "#PWR09" H 7250 2650 50  0001 C CNN
F 1 "GND" H 7250 2750 50  0000 C CNN
F 2 "" H 7250 2900 60  0000 C CNN
F 3 "" H 7250 2900 60  0000 C CNN
	1    7250 2900
	0    -1   -1   0   
$EndComp
Wire Wire Line
	7250 2900 7150 2900
Wire Wire Line
	4300 2450 4650 2450
Text Label 4650 2450 0    60   ~ 0
DP
NoConn ~ 4300 2550
NoConn ~ 4300 2650
NoConn ~ 4300 2850
NoConn ~ 4300 3200
NoConn ~ 4300 3300
NoConn ~ 4300 3400
NoConn ~ 4300 3500
NoConn ~ 4300 3600
NoConn ~ 4300 3700
NoConn ~ 4300 3950
NoConn ~ 4300 4050
NoConn ~ 2400 2950
Text Label 4650 2750 0    60   ~ 0
Button
Text Label 7300 4800 0    60   ~ 0
DP
Wire Wire Line
	6750 2850 6750 2900
Connection ~ 6750 2900
Text Label 6150 2900 0    60   ~ 0
Button
Connection ~ 4950 2850
Connection ~ 4950 3150
$EndSCHEMATC
