
ac := ComObjCreate("Python.AutoCorrectServer")
if (ac = "") {
	msgbox % "Error creating COM object."
	Exit
}

ret := ac.ping()
msgbox % ret

msgbox % ac.debug_mode()

query := "str"
ret := ac.query(query)
msgbox % ret
