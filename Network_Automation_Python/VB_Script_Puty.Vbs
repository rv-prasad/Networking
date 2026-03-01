'This code is used in case you system doesn't have Python installed. Please ensure to have putty.exe in the same folder as this file.
'It uses a Saved Session that is in the -load Backup that saves the terminal logs

Option Explicit
On Error Resume Next
' Define variables
Dim WshShell
Dim strHost
Dim struser
Dim strpass
set WshShell=CreateObject("WScript.Shell")

struser = "abc"
strpass = "Your_Password"
strHost = "Device_IP_Hostname"
WScript.Sleep 2000
'Send commands to the window as needed - IP and commands need to be customized
'Step 1 - Telnet to remote IP and define log file'
'WshShell.run "plink -load Backup -ssh  " & strHost &" -l " & struser &" -pw " & strPass & " -t"
WshShell.run "putty -load Backup -ssh  " & strHost &" -l " & struser &" -pw " & strPass
WScript.Sleep 1000
WshShell.SendKeys "terminal len 0"
WshShell.SendKeys ("{Enter}") 
WScript.sleep 100
WshShell.SendKeys "show ip bgp summary"
WshShell.SendKeys ("{Enter}") 
WScript.sleep 1000
WshShell.SendKeys "exit"
WScript.sleep 150
