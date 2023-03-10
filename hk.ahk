DllCall("AllocConsole")
WinHide % "ahk_id " DllCall("GetConsoleWindow", "ptr")

#^c::
;RunWait main.exe, , Hide
wShell := ComObjCreate( "WScript.Shell" )
exec := wShell.Exec("main.exe")
out := exec.StdOut.ReadAll()
If not InStr(out, "Success", , 1)
    MsgBox, 16, Error, %out%, 
