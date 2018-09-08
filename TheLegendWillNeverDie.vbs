Option Explicit
Dim wsh
Set wsh=WScript.CreateObject("WScript.Shell")
Do
WScript.Sleep 300000
wsh.Run "https://www.google.com/search?q=giant+dad&rlz=1C1GCEA_enUS754US754&source=lnms&tbm=isch&sa=X&ved=0ahUKEwjqmJf3xOPbAhVph1QKHb1bBskQ_AUICigB&biw=958&bih=788#imgrc=rNh1-b6ydpEQAM:"
Loop