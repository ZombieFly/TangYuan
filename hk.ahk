DllCall("AllocConsole")
WinHide % "ahk_id " DllCall("GetConsoleWindow", "ptr")

#^v::
;RunWait main.exe, , Hide
wShell := ComObjCreate( "WScript.Shell" )
exec := wShell.Exec("main.exe") 
MsgBox % exec.StdOut.ReadAll  
Send ^v