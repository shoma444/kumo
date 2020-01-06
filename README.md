# kumo
Repository for codes I wrote for my own personal use.

cpp scripts should be compiled using g++ -std=c++11
python codes are all written in py2.7 and for best compatibility, use Anaconda

To use the codes, please refer to the following:

file_encrypter.cpp : 
This encrypts and decrypts a given text file (ASCII) with a user specified password. 
The encryption is done using standard prime number modular arithmetic, and is meant for pedagocical use.
Launch and follow the directions/prompts.

//

chua3Dgrapher.py : 
This models and graphs Chua's circuit, a chaotic system comprised of capacitors, inductors and a diode.

//

chua4dvarFMINscipy.py : 
This attempts to use data assimilation techniques (4-D var) to forecast (similar to weather forecasting) the chaotc and non-linear circuit. 
The cost function is minimized using a scipy module.

//

chua4dvarBruteForce_NOISEparallel.py : 
Similar to chua4dvarFMINscipy.py but the cost function is minimized using a simple brute force method. 
