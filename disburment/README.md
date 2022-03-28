README

#######################################################################
 Disburment module
 ------------------
 
 Create model disburment to persiste merchant total quantity per week

 Scripts contains cronjob to be called in linux OS by include on
 the crontab for weekly calculation of disburments every monday

 Backend /disburment called by POST method with week to consult and
 merchant. If merchant doesn't exist will return a list with all merchants
 disburments of the week passed on the contrary if merchant existe will
 retrieve just that merchant-week quantity (current year)

 TO IMPROVE: Include option year for past consults

#######################################################################

