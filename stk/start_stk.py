from comtypes.gen import STKObjects, STKUtil, AgStkGatorLib
from comtypes.client import CreateObject, GetActiveObject, GetEvents, CoGetObject, ShowEvents
from ctypes import *
import comtypes.gen._00020430_0000_0000_C000_000000000046_0_2_0
from comtypes import GUID
from comtypes import helpstring
from comtypes import COMMETHOD
from comtypes import dispid
from ctypes.wintypes import VARIANT_BOOL
from ctypes import HRESULT
from comtypes import BSTR
from comtypes.automation import VARIANT
from comtypes.automation import _midlSAFEARRAY
from comtypes import CoClass
from comtypes import IUnknown
import comtypes.gen._00DD7BD4_53D5_4870_996B_8ADB8AF904FA_0_1_0
import comtypes.gen._8B49F426_4BF0_49F7_A59B_93961D83CB5D_0_1_0
from comtypes.automation import IDispatch
import comtypes.gen._42D2781B_8A06_4DB2_9969_72D6ABF01A72_0_1_0
from comtypes import DISPMETHOD, DISPPROPERTY, helpstring

import math
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
import time
startTime = time.time()
from tqdm import tqdm
import pandas as pd
import numpy as np




def Start_STK(useStkEngine = False, Read_Scenario = False):
    if useStkEngine:
        # Launch STK Engine
        print("Launching STK Engine...")
        stkxApp = CreateObject("STKX11.Application")
        # Disable graphics. The NoGraphics property must be set to true before the root object is created.
        stkxApp.NoGraphics = True
        # Create root object
        stkRoot = CreateObject('AgStkObjects11.AgStkObjectRoot')
        return stkRoot

    else:
        # Launch GUI
        print("Launching STK...")
        if not Read_Scenario:
            uiApp = CreateObject("STK11.Application")
        else:
            uiApp = GetActiveObject("STK11.Application")
        uiApp.Visible = True
        uiApp.UserControl = True

        # Get root object
        stkRoot = uiApp.Personality2
        return stkRoot
