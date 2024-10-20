# Twic game fetcher

This repository contains a windows shell program that allow to fecth games from the [twic website](https://theweekinchess.com/) that publishes each week the earliests games played.

## How to ?

### Dependencies

> Fetch the pgn files

You need the curl command to be available in your system

> Unzip the folders

The program uses 7-zip to unzip the downloaded folders. You can install it [here](https://www.7-zip.org/download.html)
Then, you have to add 7-zip to your path variables.

### Launch program

### Parameters

Each pgn is named with a number. If you want to download only one, juste enter its number as a parameter of the program : 
`<program> <number>`

If you want to doanload multiple ones, enter the first number and the last one. The program will download all the pgns between the two numbers (boundaries are included)
`<program> <start_number> <end_number>`

### Languages

The script is implemented in python and in windows script if you do not have python.  
To run the python script (version to use by default), replace `<program> by python3 twic.py`.  
To run the windows script, replace `<program> by ./twic.bat`.



