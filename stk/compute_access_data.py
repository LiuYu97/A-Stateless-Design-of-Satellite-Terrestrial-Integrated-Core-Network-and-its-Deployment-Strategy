import math
import os
from start_stk import Start_STK
from compute_access_data import*
os.environ['CUDA_VISIBLE_DEVICES'] = '0'

import time
startTime = time.time()

from tqdm import tqdm
import pandas as pd
import numpy as np
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



def Compute_BER(access, current_time):
    access.Advanced.EnableLightTimeDelay = True
    access.Advanced.TimeLightDelayConvergence = .00005
    access.ComputeAccess()
    # print("access.DataProviders.getschema",access.DataProviders.GetSchema())
    accessDP = access.DataProviders.Item('Link Information')
    accessDP2 = accessDP.QueryInterface(STKObjects.IAgDataPrvTimeVar)
    result = accessDP2.ExecSingleElements(current_time, ElementNames=["BER"])
    # print("------",result.DataSets.ToArray())
    try:
        BER = result.DataSets.GetDataSetByName('BER').GetValues()  # 时间
        # print(list(BER)[0])
        return BER[0]
    except:
        return 0
        # print("there is no access")


def Compute_Pr(access, current_time):
    access.Advanced.EnableLightTimeDelay = True
    access.Advanced.TimeLightDelayConvergence = .00005
    access.ComputeAccess()
    accessDP = access.DataProviders.Item('Link Information')
    accessDP2 = accessDP.QueryInterface(STKObjects.IAgDataPrvTimeVar)
    result = accessDP2.ExecSingleElements(current_time, ElementNames=["Rcvd. Iso. Power"])
    # print("------",result.DataSets.ToArray())
    try:
        Pr = result.DataSets.GetDataSetByName('Rcvd. Iso. Power').GetValues()
        return Pr[0]
    except:
        return 0

def Compute_gt(access, current_time):
    access.Advanced.EnableLightTimeDelay = True
    access.Advanced.TimeLightDelayConvergence = .00005
    access.ComputeAccess()
    accessDP = access.DataProviders.Item('Link Information')
    accessDP2 = accessDP.QueryInterface(STKObjects.IAgDataPrvTimeVar)
    result = accessDP2.ExecSingleElements(current_time, ElementNames=["g/T"])
    # print("------",result.DataSets.ToArray())
    try:
        gt = result.DataSets.GetDataSetByName('g/T').GetValues()
        return gt[0]
    except:
        return 0



def Compute_Propagation_Delay(access, current_time):
    # access.Advanced.EnableLightTimeDelay = True
    access.Advanced.EnableLightTimeDelay = True
    access.Advanced.TimeLightDelayConvergence = .00005
    access.ComputeAccess()
    # print("access.DataProviders.getschema",access.DataProviders.GetSchema())
    accessDP = access.DataProviders.Item('Link Information')
    accessDP2 = accessDP.QueryInterface(STKObjects.IAgDataPrvTimeVar)
    result = accessDP2.ExecSingleElements(current_time, ElementNames=["Propagation Delay"])
    # print("------",result.DataSets.ToArray())
    try:
        Propagation_Delay = result.DataSets.GetDataSetByName('Propagation Delay').GetValues()  # 时间
        # print(list(Propagation_Delay)[0])
        return 1 / Propagation_Delay[0]
    except:
        return 0
        # print("there is no access")


def Compute_Min_EbN0(scenario, access, n=0):
    access.Advanced.EnableLightTimeDelay = True
    access.Advanced.TimeLightDelayConvergence = .00005
    access.ComputeAccess()
    accessDP = access.DataProviders.Item('Link Information')
    accessDP2 = accessDP.QueryInterface(STKObjects.IAgDataPrvTimeVar)
    EbN0 = []
    try:
        while(True):
            current_time = scenario.StartTime + n * Time_Step
            if current_time > scenario.StartTime + Time_Range:
                break
            result = accessDP2.ExecSingleElements(current_time, ElementNames=["Eb/No"])
            EbN0.append(result.DataSets.GetDataSetByName('Eb/No').GetValues())
            n = n+1
        return min(EbN0)[0]
    except:
        return 0

def Compute_Rate(access, current_time, EbN0_Min):
    gt = Compute_gt(access, current_time)
    Pr = Compute_Pr(access, current_time)
    rate_dB = Pr + gt + 228.6 - EbN0_Min
    rate = 10**(rate_dB/10)
    # print('access_backward', 'EbN0: ', EbN0, 'gt: ', gt, 'Pr:', Pr, 'rate:', rate)
    return rate