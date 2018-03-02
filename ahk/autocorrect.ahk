
; ATTEMPTED WORKING AUTOCORRECT PROGRAM IN AHK

; note: doesn't work




; a-z undercase trigger sending it to the stack
; a lot of things wipe the stack:
;	enter
;	arrow keys
;	mouse click

; A-Z uppercase should disable stack until it clears

; backspace deletes top char on stack

builder := new TypoBuilder()

class TypoBuilder {
	__New() {
		this.stack := ""
		this.temp_disabled := False
		
		this.ac := ComObjCreate("Python.AutoCorrectServer")
		if (this.ac = "") {
			msgbox % "Error creating COM object."
			Exit
		}
		ret := this.ac.ping()
		msgbox % ret
		msgbox % this.ac.debug_mode()
	}
	
	addLetter(char) {
		this.stack := this.stack . char
	}
	
	wipe() {
		this.stack := ""
		this.temp_disabled := False
	}
	
	tempDisable() {
		this.temp_disabled := True
	}
	
	execute(end_char) {
		;TODO
		; call wipe immediately so it doesn't interfere with other thing
		
		;msgbox % "entering execute"
		if (this.temp_disabled = True) {
			;msgbox % "tempdisabled"
			this.wipe()
		} else if (this.stack != "") {
			typo := this.stack
			this.wipe()
			prev_str_len := StrLen(typo)
			;msgbox % "querying with word: " . typo
			new_word := this.ac.query(typo)
			;msgbox % "retval: " . new_word
			if (new_word != "") {
				;Loop, %prev_str_len% {
				;	send {BS} ; backspace
				;}
				send {Enter}
				send % new_word
				send {Enter}
			}
		}
		;msgbox % "at last stmt"
		send % end_char
	}
	
	debugping() {
		msgbox % this.ac.ping()
	}
}	

	
; Keyfunctions:


$Space::
	Critical
	builder.execute(" ")
	return
~LButton::
	builder.wipe()
	return
~a::
	builder.addLetter("a")
	return
~b::
	builder.addLetter("b")
	return
~c::
	builder.addLetter("c")
	return
~d::
	builder.addLetter("d")
	return
~e::
	builder.addLetter("e")
	return
~f::
	builder.addLetter("f")
	return
~g::
	builder.addLetter("g")
	return
~h::
	builder.addLetter("h")
	return
~i::
	builder.addLetter("i")
	return
~j::
	builder.addLetter("j")
	return
~k::
	builder.addLetter("k")
	return
~l::
	builder.addLetter("l")
	return
~m::
	builder.addLetter("m")
	return
~n::
	builder.addLetter("n")
	return
~o::
	builder.addLetter("o")
	return
~p::
	builder.addLetter("p")
	return
~q::
	builder.addLetter("q")
	return
~r::
	builder.addLetter("r")
	return
~s::
	builder.addLetter("s")
	return
~t::
	builder.addLetter("t")
	return
~u::
	builder.addLetter("u")
	return
~v::
	builder.addLetter("v")
	return
~w::
	builder.addLetter("w")
	return
~x::
	builder.addLetter("x")
	return
~y::
	builder.addLetter("y")
	return
~z::
	builder.addLetter("z")
	return
~+a::
	builder.tempDisable()
	return
~+b::
	builder.tempDisable()
	return
~+c::
	builder.tempDisable()
	return
~+d::
	builder.tempDisable()
	return
~+e::
	builder.tempDisable()
	return
~+f::
	builder.tempDisable()
	return
~+g::
	builder.tempDisable()
	return
~+h::
	builder.tempDisable()
	return
~+i::
	builder.tempDisable()
	return
~+j::
	builder.tempDisable()
	return
~+k::
	builder.tempDisable()
	return
~+l::
	builder.tempDisable()
	return
~+m::
	builder.tempDisable()
	return
~+n::
	builder.tempDisable()
	return
~+o::
	builder.tempDisable()
	return
~+p::
	builder.tempDisable()
	return
~+q::
	builder.tempDisable()
	return
~+r::
	builder.tempDisable()
	return
~+s::
	builder.tempDisable()
	return
~+t::
	builder.tempDisable()
	return
~+u::
	builder.tempDisable()
	return
~+v::
	builder.tempDisable()
	return
~+w::
	builder.tempDisable()
	return
~+x::
	builder.tempDisable()
	return
~+y::
	builder.tempDisable()
	return
~+z::
	builder.tempDisable()
	return
