
import win32com.client

s = win32com.client.Dispatch("Python.TestServer")

while input != "quit":
	var = s.ping(1)
	input = raw_input()
	print var