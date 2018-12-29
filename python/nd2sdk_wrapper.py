from ctypes import c_uint8, c_uint16, c_float, cdll
import os

nd2File = cdll.LoadLibrary(os.path.join(os.path.dirname(os.path.abspath(__file__)),"lib", "win", "Nd2File.dll"));
nd2Read = cdll.LoadLibrary(os.path.join(os.path.dirname(os.path.abspath(__file__)),"lib", "win", "Nd2ReadSdk.dll"));

