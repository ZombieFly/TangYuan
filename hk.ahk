DllCall("AllocConsole")
WinHide % "ahk_id " DllCall("GetConsoleWindow", "ptr")

#^v::
;RunWait main.exe, , Hide
wShell := ComObjCreate( "WScript.Shell" )
exec := wShell.Exec("main.exe")
out := exec.StdOut.ReadAll()
If InStr(out, "Success", , 1)
    Send ^v
Else
    MsgBox, 16, Error, %out%, 
