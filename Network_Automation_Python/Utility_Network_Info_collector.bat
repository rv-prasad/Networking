@echo off
(echo %DATE% %TIME%

echo HOSTNAME
echo ----------------
hostname

echo CHECKING IP CONFIGURATION
echo --------------------------
ipconfig /all

echo INTERNAL APPLICATION NAVILINK PING STATUS
echo ----------------------------------------

ping navilink

echo INTERNAL DC1 PING STATUS
echo ----------------------------------------

ping dc1d1c-wrb1.upc

echo CHECKING PING TO DC5
echo ----------------------------------------

ping dc5105-wrb1.upc

echo WIRLESS INTERFACE RELATED DETAILS
echo ----------------------------------------

netsh wlan show all

echo CHECKING GOOGLE ACCESS
echo ----------------------------------------

curl google.com
) >> Network_info.txt
