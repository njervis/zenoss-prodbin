###########################################################################
#
# This program is part of Zenoss Core, an open source monitoring platform.
# Copyright (C) 2007, Zenoss Inc.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as published by
# the Free Software Foundation.
#
# For complete information please visit: http://www.zenoss.com/oss/
#
###########################################################################
import Migrate
from Acquisition import aq_base
from Products.ZenModel.DeviceClass import DeviceClass

class zCollectorPlugins(Migrate.Step):
    version = Migrate.Version(2, 0, 0)

    def cutover(self, dmd):

        if not hasattr(aq_base(dmd.Devices), 'zCollectorPlugins'):
            dmd.Devices._setProperty("zCollectorPlugins", (), type='lines')

        if not dmd.Devices.zCollectorPlugins:
            dmd.Devices.zCollectorPlugins = (
                    'zenoss.snmp.NewDeviceMap',
                    'zenoss.snmp.DeviceMap',
                    'zenoss.snmp.InterfaceMap',
                    'zenoss.snmp.RouteMap',
                )

        if not hasattr(aq_base(dmd.Devices.Server),'zCollectorPlugins'):
            dmd.Devices.Server._setProperty("zCollectorPlugins", 
                (
                    'zenoss.snmp.NewDeviceMap',
                    'zenoss.snmp.DeviceMap',
                    'zenoss.snmp.DellDeviceMap',
                    'zenoss.snmp.HPDeviceMap',
                    'zenoss.snmp.InterfaceMap',
                    'zenoss.snmp.RouteMap',
                    'zenoss.snmp.IpServiceMap',
                    'zenoss.snmp.HRFileSystemMap',
                    'zenoss.snmp.HRSWInstalledMap',
                    'zenoss.snmp.HRSWRunMap',
                    'zenoss.snmp.CpuMap',
                    'zenoss.snmp.DellCPUMap',
                    'zenoss.snmp.HPCPUMap',
                    'zenoss.snmp.DellPCIMap',
                ), type = 'lines')

        if not dmd.Devices.Server._getOb('Scan',False):
            scan = DeviceClass('Scan')
            dmd.Devices.Server._setObject('Scan',scan)

        if not hasattr(aq_base(dmd.Devices.Server.Scan), 'zCollectorPlugins'):
            dmd.Devices.Server.Scan._setProperty("zCollectorPlugins", 
                (
                    'zenoss.portscan.IpServiceMap',
                ), type = 'lines')
        
        if not dmd.Devices.Server._getOb('Cmd',False):
            cmd = DeviceClass('Cmd')
            dmd.Devices.Server._setObject('Cmd', cmd)

        if not hasattr(aq_base(dmd.Devices.Server.Cmd), 'zCollectorPlugins'):
            dmd.Devices.Server.Cmd._setProperty("zCollectorPlugins", 
                (
                    'zenoss.cmd.uname',
                    'zenoss.cmd.df',
                    'zenoss.cmd.linux.ifconfig',
                    'zenoss.cmd.linux.memory',
                    'zenoss.cmd.linux.netstat_an',
                    'zenoss.cmd.linux.netstat_rn',
                    'zenoss.cmd.linux.process',
                    'zenoss.cmd.darwin.cpu',
                    'zenoss.cmd.darwin.ifconfig',
                    'zenoss.cmd.darwin.memory',
                    'zenoss.cmd.darwin.netstat_an',
                    'zenoss.cmd.darwin.process',
                    'zenoss.cmd.darwin.swap',
                ), type = 'lines')


        if not hasattr(aq_base(dmd.Devices.Server.Linux), 'zCollectorPlugins'):
            dmd.Devices.Server.Linux._setProperty("zCollectorPlugins", 
                (
                    'zenoss.snmp.NewDeviceMap',
                    'zenoss.snmp.DeviceMap',
                    'zenoss.snmp.DellDeviceMap',
                    'zenoss.snmp.HPDeviceMap',
                    'zenoss.snmp.InterfaceMap',
                    'zenoss.snmp.RouteMap',
                    'zenoss.snmp.IpServiceMap',
                    'zenoss.snmp.HRFileSystemMap',
                    'zenoss.snmp.HRSWRunMap',
                    'zenoss.snmp.CpuMap',
                    'zenoss.snmp.DellCPUMap',
                    'zenoss.snmp.DellPCIMap',
                    'zenoss.snmp.HPCPUMap',
                ), type = 'lines')

        if not hasattr(aq_base(dmd.Devices.Server.Windows),'zCollectorPlugins'):
            dmd.Devices.Server.Windows._setProperty("zCollectorPlugins", 
                (
                    'zenoss.snmp.NewDeviceMap',
                    'zenoss.snmp.DeviceMap',
                    'zenoss.snmp.DellDeviceMap',
                    'zenoss.snmp.HPDeviceMap',
                    'zenoss.snmp.InterfaceMap',
                    'zenoss.snmp.RouteMap',
                    'zenoss.snmp.IpServiceMap',
                    'zenoss.snmp.HRFileSystemMap',
                    'zenoss.snmp.HRSWInstalledMap',
                    'zenoss.snmp.HRSWRunMap',
                    'zenoss.snmp.CpuMap',
                    'zenoss.snmp.DellCPUMap',
                    'zenoss.snmp.DellPCIMap',
                    'zenoss.snmp.HPCPUMap',
                    'zenoss.snmp.InformantHardDiskMap',
                ), type = 'lines')
            
        if not hasattr(aq_base(dmd.Devices.Power),'zCollectorPlugins'):
            dmd.Devices.Power._setProperty("zCollectorPlugins", 
                (
                    'zenoss.snmp.NewDeviceMap',
                    'zenoss.snmp.DeviceMap',
                    'zenoss.snmp.APCDeviceMap',
                    'zenoss.snmp.PowerwareDeviceMap',
                ), type = 'lines')

        if not hasattr(aq_base(dmd.Devices.Network.Router.Cisco),
            'zCollectorPlugins'):
            dmd.Devices.Network.Router.Cisco._setProperty('zCollectorPlugins',
                (
                    'zenoss.snmp.NewDeviceMap',
                    'zenoss.snmp.DeviceMap',
                    'zenoss.snmp.CiscoMap',
                    'zenoss.snmp.InterfaceMap',
                    'zenoss.snmp.CiscoHSRP',
                    'zenoss.snmp.RouteMap',
                ), type = 'lines')

zCollectorPlugins()
 






