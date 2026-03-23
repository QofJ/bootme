#Requires AutoHotkey v2.0

GroupAdd "MyTerminals", "ahk_exe WindowsTerminal.exe"
GroupAdd "MyTerminals", "ahk_exe cmd.exe"
GroupAdd "MyTerminals", "ahk_exe powershell.exe"

SetCapsLockState "AlwaysOff"

#HotIf WinActive("ahk_group MyTerminals")

CapsLock & h::Send("{Blind}{Left}")
CapsLock & j::Send("{Blind}{Down}")
CapsLock & k::Send("{Blind}{Up}")
CapsLock & l::Send("{Blind}{Right}")

#HotIf

+CapsLock:: {
    if GetKeyState("CapsLock", "T")
      SetCapsLockState "AlwaysOff"
    else
      SetCapsLockState "AlwaysOn"
  }
