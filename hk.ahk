;@Ahk2Exe-SetProductName TangYuan
;@Ahk2Exe-SetCopyright ZombieFly
;@Ahk2Exe-SetCompanyName ZombieFly
;@Ahk2Exe-SetDescription Hotkey for TangYuan
;@Ahk2Exe-SetProductVersion 0.0.1

DllCall("AllocConsole")
WinHide % "ahk_id " DllCall("GetConsoleWindow", "ptr")

#^c::
Send, ^c
wShell := ComObjCreate( "WScript.Shell" )
exec := wShell.Exec("main.exe")
out := exec.StdOut.ReadAll()
If not InStr(out, "Success", , 1)
    MsgBox, 16, Error, %out%
