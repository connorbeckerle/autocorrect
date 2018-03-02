
import win32com.client
from win32com.server.util import wrap, unwrap
from win32com.server.dispatcher import DefaultDebugDispatcher
from ctypes import *
import subprocess
import pythoncom
import winerror
from win32com.server.exception import Exception
import win32com.server.util, win32com.server.policy
import sys
import wx


# Stores the info for this process' COM obj
class PyCOMObj:

	def __init__(self):
		self.handle = 0
		self.clsID = pythoncom.CreateGuid()
		self.IID = pythoncom.MakeIID(self.clsID)
		self.appID = "pyprogAC"
		self.AHKAppID = "ahkprogAC"
	
	def __del__(self):
		pythoncom.RevokeActiveObject(self.handle)
	
	def _dynamic_(self, name, lcID, wFlags, args):
		if wFlags & pythoncom.DISPATCH_METHOD:
			return getattr(self, name)(*args)
		if wFlags & pythoncom.DISPATCH_PROPERTYGET:
			try:
				# converting tuple results to list helps with byref params or something
				ret = self.__dict__[name]
				if type(ret) == type(()):
					ret = list(ret)
				return ret
			except KeyError: # "probably a method request"
				raise Exception(scode=winerror.DISP_E_MEMBERNOTFOUND)
		if wFlags & (pythoncom.DISPATCH_PROPERTYPUT | pythoncom.DISPATCH_PROPERTYPUTREF):
			setattr(self, name, args[0])
			return
		raise Exception(scode=winerror.E_INVALIDARG, desc="invalid wFlags")
	def write(self, x):
		print x
		return 0
		
	def registerThisCOMObj(self):
		self.serverWrapper = win32com.server.util.wrap(self, usePolicy=win32com.server.policy.DynamicPolicy)
		try:
			handle = pythoncom.RegisterActiveObject(self.serverWrapper, self.IID, 0)
		except pythoncom.com_error, details:
			print "Warning - could not register the object in the ROT:", details
			handle = None    
			return
		self.handle = handle
		
	def sendIDsToAHK(self):
		try:
			ahk = win32com.client.Dispatch(self.AHKAppID)
			ahk.aRegisterIDs(self.clsID, self.appID)
		except pythoncom.com_error, details:
			print "Error - could not send to AHK script:", details
			
		
class AHKCOMObj:
	def __init__(self, thisPyCOMObj):
		#TODO - what is this for??
		pass
		
		
def main():

	thisPyCOMObj = PyCOMObj()
	thisPyCOMObj.registerThisCOMObj()
	#thisPyCOMObj.sendIDsToAHK()
	
	app = wx.App(False) # Create a new app, don't redirect stdout/stderr to a window.
	frame = wx.Frame(None, wx.ID_ANY, "py com test") # A Frame is a top-level window.
	frame.Show(True)
	app.MainLoop()
	
	print "This test started successfully yay"
	
main()
	
	
	
