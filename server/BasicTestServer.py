import time
import pythoncom
import win32com.server.register
import win32com.server.exception
import admin

# MISC NOTES
# likely have to cast received strings with str()




class BasicServer:

	# note - these are comma-delimited
	# list of all method names exposed to COM
	_public_methods_ = ["ping"]
	
	# list of all attribute names exposed to COM
	_public_attrs_ = []
	
	# list of all read-only exposed attributes
	_readonly_attrs_ = ["count"]		
	
	# this server's CLS ID
	_reg_clsid_ = "{E88C95B9-B6BA-4365-BC3E-42C07E33B944}"
	
	# this server's (user-friendly) program ID
	_reg_progid_ = "Python.TestServer"
	
	# optional description
	_reg_desc_ = "Test COM server"
	
	
	def __init__(self):
		pass
		
	def ping(self, wait=""):
	
		if wait != "":
			waitCount = int(str(wait))
			time.sleep(waitCount)
		
		self.count = self.count + 1
				
		return self.count
		
	@staticmethod
	def reg():
		
		win32com.server.register.UseCommandLine(BasicServer)
		
	@staticmethod
	def unreg():
		
		if not admin.isUserAdmin():
			admin.runAsAdmin()
		win32com.server.register.UnregisterServer(BasicServer._reg_clsid_, BasicServer._reg_progid_)

			
if __name__ == "__main__":

	import sys
	if len(sys.argv) < 2:
		print "Error: need to supply arg (""--register"" or ""--unregister"")"
		sys.exit(1)
	elif sys.argv[1] == "--register":
		BasicServer.reg()
	elif sys.argv[1] == "--unregister":
		print "Starting to unregister..."	
		BasicServer.unreg()
		print "Unregistered COM server."
	else:
		print "Error: arg not recognized"
	
	
#s.reg()
#s.unreg()





