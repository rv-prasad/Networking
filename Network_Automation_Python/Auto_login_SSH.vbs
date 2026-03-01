'This allow user to enter the IP address/Hostname when this is run. It launches a dialog box and you have enter the IP/Hostname there.
'It also used the saved Saved Putty session Named Backup with logging enabled to ensure output is logged.
Option Explicit
On Error Resume Next
' Define variables
Dim WshShell
Dim MyDateTime
Dim strDate 
Dim strDay 
Dim strMonth 
Dim strYear
Dim strTime
Dim strSecond
Dim strHost
Dim strLogFile
Dim struser
Dim strpass
Dim Subloc
set WshShell=CreateObject("WScript.Shell")
strHost = UserInput( "Enter Device IP:" )
struser = "username"
strpass = "passsword"


Function UserInput( myPrompt )

    If UCase( Right( WScript.FullName, 12 ) ) = "\CSCRIPT.EXE" Then
        ' If so, use StdIn and StdOut
        WScript.StdOut.Write myPrompt & " "
        UserInput = WScript.StdIn.ReadLine
    Else
        ' If not, use InputBox( )
        UserInput = InputBox( myPrompt )
    End If
End Function



WshShell.run "putty -load Backup -ssh  " & strHost &" -l " & struser &" -pw " & strPass


WScript.Sleep 5000
WshShell.SendKeys "enable"
WshShell.SendKeys ("{Enter}") 
WScript.sleep 500
WshShell.SendKeys "enable_password"
WshShell.SendKeys ("{Enter}") 
WScript.sleep 1000

