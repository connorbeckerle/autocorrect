
; CLSID "{E88C95B9-B6BA-4365-BC3E-42C07E33B944}"
; progID "Python.TestServer"

ts := ComObjCreate("Python.TestServer")
if (ts = "") {
	msgbox % "Error creating COM object."
	Exit
}


counter := 0

msgbox "Initialized."

^+d::
	counter := counter + 1
	retCallArray.InsertAt(counter, ts.ping(2))
	msgbox % "Boop"
	return
	
^+e::
	msgbox % "yay! Count = " . counter
	return
	
^+c::
	outStr := ""
	for i, val in retCallArray {
		outStr := outStr . val . "`n"
	}
	msgbox % outStr
	return
	
;msgbox % ts.ping()

;count := msgbox.count
;testvar := "ugh"
;msgbox % testvar
;msgbox % count

;msgbox % "p1 = " p1 "`np2 = " p2
;Run "BasicTestServer.py"



