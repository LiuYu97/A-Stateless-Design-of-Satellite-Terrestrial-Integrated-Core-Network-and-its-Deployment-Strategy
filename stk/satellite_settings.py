import math
import os
from compute_access_data import*
from start_stk import Start_STK
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



# 创建卫星星系
def Creat_satellite(scenario, numOrbitPlanes, numSatsPerPlane, hight, Inclination, name='Sat'):
    # Create constellation object
    constellation = scenario.Children.New(STKObjects.eConstellation, name)
    constellation2 = constellation.QueryInterface(STKObjects.IAgConstellation)

    # Insert the constellation of Satellites
    for orbitPlaneNum in range(numOrbitPlanes):  # RAAN in degrees

        for satNum in range(numSatsPerPlane):  # trueAnomaly in degrees
            # Insert satellite
            satellite = scenario.Children.New(STKObjects.eSatellite, f"{name}{orbitPlaneNum}_{satNum}")
            satellite2 = satellite.QueryInterface(STKObjects.IAgSatellite)

            # Select Propagator
            satellite2.SetPropagatorType(STKObjects.ePropagatorTwoBody)

            # Set initial state
            twoBodyPropagator = satellite2.Propagator.QueryInterface(STKObjects.IAgVePropagatorTwoBody)
            keplarian = twoBodyPropagator.InitialState.Representation.ConvertTo(
                STKUtil.eOrbitStateClassical).QueryInterface(STKObjects.IAgOrbitStateClassical)

            keplarian.SizeShapeType = STKObjects.eSizeShapeSemimajorAxis
            keplarian.SizeShape.QueryInterface(
                STKObjects.IAgClassicalSizeShapeSemimajorAxis).SemiMajorAxis = hight + 6371  # km
            keplarian.SizeShape.QueryInterface(STKObjects.IAgClassicalSizeShapeSemimajorAxis).Eccentricity = 0

            keplarian.Orientation.Inclination = int(Inclination)  # degrees
            keplarian.Orientation.ArgOfPerigee = 0  # degrees
            keplarian.Orientation.AscNodeType = STKObjects.eAscNodeRAAN
            RAAN = 180 / numOrbitPlanes * orbitPlaneNum
            keplarian.Orientation.AscNode.QueryInterface(STKObjects.IAgOrientationAscNodeRAAN).Value = RAAN  # degrees

            keplarian.LocationType = STKObjects.eLocationTrueAnomaly
            trueAnomaly = 360 / numSatsPerPlane * satNum
            keplarian.Location.QueryInterface(STKObjects.IAgClassicalLocationTrueAnomaly).Value = trueAnomaly

            # Propagate
            satellite2.Propagator.QueryInterface(STKObjects.IAgVePropagatorTwoBody).InitialState.Representation.Assign(
                keplarian)
            satellite2.Propagator.QueryInterface(STKObjects.IAgVePropagatorTwoBody).Propagate()

            # Add to constellation object
            constellation2.Objects.AddObject(satellite)


# 为每个卫星加上发射机和接收机
def Add_transmitter_receiver(sat_list):
    for each in sat_list:
        Instance_name = each.InstanceName
        #  new transmitter and receiver
        transmitter = each.Children.New(STKObjects.eTransmitter, "Transmitter_" + Instance_name)
        reciver = each.Children.New(STKObjects.eReceiver, "Reciver_" + Instance_name)
        # sensor = each.Children.New(STKObjects.eSensor, 'Sensor_' + Instance_name)


# 设置发射机参数
def Set_Transmitter_Parameter(transmitter, frequency=12, EIRP=20, DataRate=20):
    transmitter2 = transmitter.QueryInterface(STKObjects.IAgTransmitter)  # 建立发射机的映射，以便对其进行设置
    transmitter2.SetModel('Simple Transmitter Model')
    txModel = transmitter2.Model
    txModel = txModel.QueryInterface(STKObjects.IAgTransmitterModelSimple)
    txModel.Frequency = frequency  # GHz range:10.7-12.7GHz
    txModel.EIRP = EIRP  # dBW
    txModel.DataRate = DataRate  # Mb/sec


# 设置接收机参数
def Set_Receiver_Parameter(receiver, GT=30, frequency=12):
    receiver2 = receiver.QueryInterface(STKObjects.IAgReceiver)  # 建立发射机的映射，以便对其进行设置
    receiver2.SetModel('Simple Receiver Model')
    recModel = receiver2.Model
    recModel = recModel.QueryInterface(STKObjects.IAgReceiverModelSimple)
    recModel.AutoTrackFrequency = False
    recModel.Frequency = frequency  # GHz range:10.7-12.7GHz
    recModel.GOverT = GT  # dB/K
    return receiver2


# 获得接收机示例，并设置其参数
def Get_sat_receiver(sat, GT=20, frequency=12):
    receiver = sat.Children.GetElements(STKObjects.eReceiver)[0]  # 找到该卫星的接收机
    receiver2 = Set_Receiver_Parameter(receiver=receiver, GT=GT, frequency=frequency)
    return receiver2

def Change_Sat_color(sat_list):
    # 修改卫星及其轨道的颜色
    print('Changing Color of Satellite')
    for each_sat in tqdm(sat_list):
        now_sat_name = each_sat.InstanceName
        now_plane_num = int(now_sat_name.split('_')[0][3:])
        now_sat_num = int(now_sat_name.split('_')[1])
        satellite = each_sat.QueryInterface(STKObjects.IAgSatellite)
        graphics = satellite.Graphics
        graphics.SetAttributesType(1)  # eAttributesBasic
        attributes = graphics.Attributes
        attributes_color = attributes.QueryInterface(STKObjects.IAgVeGfxAttributesBasic)
        attributes_color.Inherit = False
        # 16436871 浅蓝色
        # 2330219 墨绿色
        # 42495 橙色
        # 9234160 米黄色
        # 65535 黄色
        # 255 红色
        # 16776960 青色
        color_sheet = [16436871, 2330219, 42495, 9234160, 65535, 255, 16776960]
        if now_sat_name[2] == 'A':
            color = 255
        elif now_sat_name[2] == 'B':
            color = 42495
        elif now_sat_name[2] == 'C':
            color = 16436871
        attributes_color.Color = color
        # 找出轨道对应的属性接口
        orbit = attributes.QueryInterface(STKObjects.IAgVeGfxAttributesOrbit)
        orbit.IsOrbitVisible = False  # 将轨道设置为不可见