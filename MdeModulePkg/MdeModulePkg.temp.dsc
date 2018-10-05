 [Defines]
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:24: scope=DscScopeLevel.default
  BUILD_TARGETS=DEBUG|RELEASE|NOOPT
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:21: scope=DscScopeLevel.default
  DSC_SPECIFICATION=0x00010005
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:22: scope=DscScopeLevel.default
  OUTPUT_DIRECTORY=Build/MdeModule
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:19: scope=DscScopeLevel.default
  PLATFORM_GUID=587CE499-6CBE-43cd-94E2-186218569478
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:18: scope=DscScopeLevel.default
  PLATFORM_NAME=MdeModule
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:20: scope=DscScopeLevel.default
  PLATFORM_VERSION=0.98
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:25: scope=DscScopeLevel.default
  SKUID_IDENTIFIER=DEFAULT
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:23: scope=DscScopeLevel.default
  SUPPORTED_ARCHITECTURES=IA32|IPF|X64|EBC|ARM|AARCH64

 [LibraryClasses.common.DXE_CORE]
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:144: scope=DscScopeLevel.default
  BaseBinSecurityLib|MdePkg/Library/BaseBinSecurityLibNull/BaseBinSecurityLibNull.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:142: scope=DscScopeLevel.default
  ExtractGuidedSectionLib|MdePkg/Library/DxeExtractGuidedSectionLib/DxeExtractGuidedSectionLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:140: scope=DscScopeLevel.default
  HobLib|MdePkg/Library/DxeCoreHobLib/DxeCoreHobLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:141: scope=DscScopeLevel.default
  MemoryAllocationLib|MdeModulePkg/Library/DxeCoreMemoryAllocationLib/DxeCoreMemoryAllocationLib.inf

 [LibraryClasses.common.DXE_DRIVER]
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:151: scope=DscScopeLevel.default
  CapsuleLib|MdeModulePkg/Library/DxeCapsuleLibFmp/DxeCapsuleLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:150: scope=DscScopeLevel.default
  ExtractGuidedSectionLib|MdePkg/Library/DxeExtractGuidedSectionLib/DxeExtractGuidedSectionLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:147: scope=DscScopeLevel.default
  HobLib|MdePkg/Library/DxeHobLib/DxeHobLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:148: scope=DscScopeLevel.default
  LockBoxLib|MdeModulePkg/Library/SmmLockBoxLib/SmmLockBoxDxeLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:149: scope=DscScopeLevel.default
  MemoryAllocationLib|MdePkg/Library/UefiMemoryAllocationLib/UefiMemoryAllocationLib.inf

 [LibraryClasses.common.DXE_RUNTIME_DRIVER]
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:158: scope=DscScopeLevel.default
  CapsuleLib|MdeModulePkg/Library/DxeCapsuleLibFmp/DxeRuntimeCapsuleLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:156: scope=DscScopeLevel.default
  DebugLib|MdePkg/Library/UefiDebugLibConOut/UefiDebugLibConOut.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:154: scope=DscScopeLevel.default
  HobLib|MdePkg/Library/DxeHobLib/DxeHobLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:157: scope=DscScopeLevel.default
  LockBoxLib|MdeModulePkg/Library/SmmLockBoxLib/SmmLockBoxDxeLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:155: scope=DscScopeLevel.default
  MemoryAllocationLib|MdePkg/Library/UefiMemoryAllocationLib/UefiMemoryAllocationLib.inf

 [LibraryClasses.common.DXE_SMM_DRIVER]
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:171: scope=DscScopeLevel.default
  DebugLib|MdePkg/Library/UefiDebugLibConOut/UefiDebugLibConOut.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:170: scope=DscScopeLevel.default
  HobLib|MdePkg/Library/DxeHobLib/DxeHobLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:174: scope=DscScopeLevel.default
  LockBoxLib|MdeModulePkg/Library/SmmLockBoxLib/SmmLockBoxSmmLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:172: scope=DscScopeLevel.default
  MemoryAllocationLib|MdePkg/Library/SmmMemoryAllocationLib/SmmMemoryAllocationLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:175: scope=DscScopeLevel.default
  SmmMemLib|MdePkg/Library/SmmMemLib/SmmMemLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:173: scope=DscScopeLevel.default
  SmmServicesTableLib|MdePkg/Library/SmmServicesTableLib/SmmServicesTableLib.inf

 [LibraryClasses.common.PEIM]
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:136: scope=DscScopeLevel.default
  ExtractGuidedSectionLib|MdePkg/Library/PeiExtractGuidedSectionLib/PeiExtractGuidedSectionLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:134: scope=DscScopeLevel.default
  HobLib|MdePkg/Library/PeiHobLib/PeiHobLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:137: scope=DscScopeLevel.default
  LockBoxLib|MdeModulePkg/Library/SmmLockBoxLib/SmmLockBoxPeiLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:135: scope=DscScopeLevel.default
  MemoryAllocationLib|MdePkg/Library/PeiMemoryAllocationLib/PeiMemoryAllocationLib.inf

 [LibraryClasses.common.PEI_CORE]
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:130: scope=DscScopeLevel.default
  HobLib|MdePkg/Library/PeiHobLib/PeiHobLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:131: scope=DscScopeLevel.default
  MemoryAllocationLib|MdePkg/Library/PeiMemoryAllocationLib/PeiMemoryAllocationLib.inf

 [LibraryClasses.common.SMM_CORE]
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:167: scope=DscScopeLevel.default
  BaseBinSecurityLib|MdePkg/Library/BaseBinSecurityLibNull/BaseBinSecurityLibNull.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:161: scope=DscScopeLevel.default
  HobLib|MdePkg/Library/DxeHobLib/DxeHobLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:162: scope=DscScopeLevel.default
  MemoryAllocationLib|MdeModulePkg/Library/PiSmmCoreMemoryAllocationLib/PiSmmCoreMemoryAllocationLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:164: scope=DscScopeLevel.default
  SmmCorePlatformHookLib|MdeModulePkg/Library/SmmCorePlatformHookLibNull/SmmCorePlatformHookLibNull.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:165: scope=DscScopeLevel.default
  SmmMemLib|MdePkg/Library/SmmMemLib/SmmMemLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:163: scope=DscScopeLevel.default
  SmmServicesTableLib|MdeModulePkg/Library/PiSmmCoreSmmServicesTableLib/PiSmmCoreSmmServicesTableLib.inf

 [LibraryClasses.common.UEFI_APPLICATION]
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:186: scope=DscScopeLevel.default
  DebugLib|MdePkg/Library/UefiDebugLibStdErr/UefiDebugLibStdErr.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:184: scope=DscScopeLevel.default
  HobLib|MdePkg/Library/DxeHobLib/DxeHobLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:185: scope=DscScopeLevel.default
  MemoryAllocationLib|MdePkg/Library/UefiMemoryAllocationLib/UefiMemoryAllocationLib.inf

 [LibraryClasses.common.UEFI_DRIVER]
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:180: scope=DscScopeLevel.default
  DebugLib|MdePkg/Library/UefiDebugLibConOut/UefiDebugLibConOut.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:178: scope=DscScopeLevel.default
  HobLib|MdePkg/Library/DxeHobLib/DxeHobLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:181: scope=DscScopeLevel.default
  LockBoxLib|MdeModulePkg/Library/SmmLockBoxLib/SmmLockBoxDxeLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:179: scope=DscScopeLevel.default
  MemoryAllocationLib|MdePkg/Library/UefiMemoryAllocationLib/UefiMemoryAllocationLib.inf

 [LibraryClasses]
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:106: scope=DscScopeLevel.default
  AuthVariableLib|MdeModulePkg/Library/AuthVariableLibNull/AuthVariableLibNull.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:40: scope=DscScopeLevel.default
  BaseLib|MdePkg/Library/BaseLib/BaseLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:41: scope=DscScopeLevel.default
  BaseMemoryLib|MdePkg/Library/BaseMemoryLib/BaseMemoryLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:113: scope=DscScopeLevel.default
  BmpSupportLib|MdeModulePkg/Library/BaseBmpSupportLib/BaseBmpSupportLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:48: scope=DscScopeLevel.default
  CacheMaintenanceLib|MdePkg/Library/BaseCacheMaintenanceLib/BaseCacheMaintenanceLib.inf
   # Revision:MdeModulePkg/Library/DxeCapsuleLibNull/DxeCapsuleLibNull.inf from C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:112: scope=DscScopeLevel.default
 # Revision:MdeModulePkg/Library/DxeCapsuleLibNull/DxeCapsuleLibNull.inf from C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:81: scope=DscScopeLevel.default
  CapsuleLib|MdeModulePkg/Library/DxeCapsuleLibNull/DxeCapsuleLibNull.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:102: scope=DscScopeLevel.default
  CpuExceptionHandlerLib|MdeModulePkg/Library/CpuExceptionHandlerLibNull/CpuExceptionHandlerLibNull.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:84: scope=DscScopeLevel.default
  CustomizedDisplayLib|MdeModulePkg/Library/CustomizedDisplayLib/CustomizedDisplayLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:95: scope=DscScopeLevel.default
  DebugAgentLib|MdeModulePkg/Library/DebugAgentLibNull/DebugAgentLibNull.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:89: scope=DscScopeLevel.default
  DebugLib|MdePkg/Library/BaseDebugLibNull/BaseDebugLibNull.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:90: scope=DscScopeLevel.default
  DebugPrintErrorLevelLib|MdePkg/Library/BaseDebugPrintErrorLevelLib/BaseDebugPrintErrorLevelLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:61: scope=DscScopeLevel.default
  DevicePathLib|MdePkg/Library/UefiDevicePathLib/UefiDevicePathLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:115: scope=DscScopeLevel.default
  DisplayUpdateProgressLib|MdeModulePkg/Library/DisplayUpdateProgressLibGraphics/DisplayUpdateProgressLibGraphics.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:77: scope=DscScopeLevel.default
  DpcLib|MdeModulePkg/Library/DxeDpcLib/DxeDpcLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:33: scope=DscScopeLevel.default
  DxeCoreEntryPoint|MdePkg/Library/DxeCoreEntryPoint/DxeCoreEntryPoint.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:65: scope=DscScopeLevel.default
  DxeServicesLib|MdePkg/Library/DxeServicesLib/DxeServicesLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:66: scope=DscScopeLevel.default
  DxeServicesTableLib|MdePkg/Library/DxeServicesTableLib/DxeServicesTableLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:108: scope=DscScopeLevel.default
  FileExplorerLib|MdeModulePkg/Library/FileExplorerLib/FileExplorerLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:111: scope=DscScopeLevel.default
  FmpAuthenticationLib|MdeModulePkg/Library/FmpAuthenticationLibNull/FmpAuthenticationLibNull.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:85: scope=DscScopeLevel.default
  FrameBufferBltLib|MdeModulePkg/Library/FrameBufferBltLib/FrameBufferBltLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:60: scope=DscScopeLevel.default
  HiiLib|MdeModulePkg/Library/UefiHiiLib/UefiHiiLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:99: scope=DscScopeLevel.default
  HwResetSystemLib|MdeModulePkg/Library/BaseResetSystemLibNull/BaseResetSystemLibNull.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:44: scope=DscScopeLevel.default
  IoLib|MdePkg/Library/BaseIoLibIntrinsic/BaseIoLibIntrinsic.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:74: scope=DscScopeLevel.default
  IpIoLib|MdeModulePkg/Library/DxeIpIoLib/DxeIpIoLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:122: scope=DscScopeLevel.default
  NULL|MdePkg/Library/BaseBinSecurityLibRng/BaseBinSecurityLibRng.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:73: scope=DscScopeLevel.default
  NetLib|MdeModulePkg/Library/DxeNetLib/DxeNetLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:109: scope=DscScopeLevel.default
  NonDiscoverableDeviceRegistrationLib|MdeModulePkg/Library/NonDiscoverableDeviceRegistrationLib/NonDiscoverableDeviceRegistrationLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:83: scope=DscScopeLevel.default
  PalLib|MdePkg/Library/BasePalLibNull/BasePalLibNull.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:82: scope=DscScopeLevel.default
  PcdLib|MdePkg/Library/BasePcdLibNull/BasePcdLibNull.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:46: scope=DscScopeLevel.default
  PciCf8Lib|MdePkg/Library/BasePciCf8Lib/BasePciCf8Lib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:104: scope=DscScopeLevel.default
  PciHostBridgeLib|MdeModulePkg/Library/PciHostBridgeLibNull/PciHostBridgeLibNull.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:45: scope=DscScopeLevel.default
  PciLib|MdePkg/Library/BasePciLibCf8/BasePciLibCf8.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:47: scope=DscScopeLevel.default
  PciSegmentLib|MdePkg/Library/BasePciSegmentLibPci/BasePciSegmentLibPci.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:92: scope=DscScopeLevel.default
  PeCoffExtraActionLib|MdePkg/Library/BasePeCoffExtraActionLibNull/BasePeCoffExtraActionLibNull.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:50: scope=DscScopeLevel.default
  PeCoffGetEntryPointLib|MdePkg/Library/BasePeCoffGetEntryPointLib/BasePeCoffGetEntryPointLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:49: scope=DscScopeLevel.default
  PeCoffLib|MdePkg/Library/BasePeCoffLib/BasePeCoffLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:31: scope=DscScopeLevel.default
  PeiCoreEntryPoint|MdePkg/Library/PeiCoreEntryPoint/PeiCoreEntryPoint.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:64: scope=DscScopeLevel.default
  PeiServicesLib|MdePkg/Library/PeiServicesLib/PeiServicesLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:63: scope=DscScopeLevel.default
  PeiServicesTablePointerLib|MdePkg/Library/PeiServicesTablePointerLib/PeiServicesTablePointerLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:32: scope=DscScopeLevel.default
  PeimEntryPoint|MdePkg/Library/PeimEntryPoint/PeimEntryPoint.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:94: scope=DscScopeLevel.default
  Performance2Lib|MdePkg/Library/BasePerformance2LibNull/BasePerformance2LibNull.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:93: scope=DscScopeLevel.default
  PerformanceLib|MdePkg/Library/BasePerformanceLibNull/BasePerformanceLibNull.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:103: scope=DscScopeLevel.default
  PlatformBootManagerLib|MdeModulePkg/Library/PlatformBootManagerLibNull/PlatformBootManagerLibNull.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:96: scope=DscScopeLevel.default
  PlatformHookLib|MdeModulePkg/Library/BasePlatformHookLibNull/BasePlatformHookLibNull.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:43: scope=DscScopeLevel.default
  PrintLib|MdePkg/Library/BasePrintLib/BasePrintLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:91: scope=DscScopeLevel.default
  ReportStatusCodeLib|MdePkg/Library/BaseReportStatusCodeLibNull/BaseReportStatusCodeLibNull.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:97: scope=DscScopeLevel.default
  ResetSystemLib|MdeModulePkg/Library/BaseResetSystemLibNull/BaseResetSystemLibNull.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:98: scope=DscScopeLevel.default
  ResetUtilityLib|MdeModulePkg/Library/ResetUtilityLib/ResetUtilityLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:121: scope=DscScopeLevel.default
  RngLib|MdePkg/Library/BaseRngLib/BaseRngLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:101: scope=DscScopeLevel.default
  S3BootScriptLib|MdeModulePkg/Library/PiDxeS3BootScriptLib/DxeS3BootScriptLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:114: scope=DscScopeLevel.default
  SafeIntLib|MdePkg/Library/BaseSafeIntLib/BaseSafeIntLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:36: scope=DscScopeLevel.default
  SecurityLockAuditLib|MdeModulePkg/Library/SecurityLockAuditDebugMessageLib/SecurityLockAuditDebugMessageLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:78: scope=DscScopeLevel.default
  SecurityManagementLib|MdeModulePkg/Library/DxeSecurityManagementLib/DxeSecurityManagementLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:80: scope=DscScopeLevel.default
  SerialPortLib|MdePkg/Library/BaseSerialPortLibNull/BaseSerialPortLibNull.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:100: scope=DscScopeLevel.default
  SmbusLib|MdePkg/Library/DxeSmbusLib/DxeSmbusLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:51: scope=DscScopeLevel.default
  SortLib|MdeModulePkg/Library/BaseSortLib/BaseSortLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:42: scope=DscScopeLevel.default
  SynchronizationLib|MdePkg/Library/BaseSynchronizationLib/BaseSynchronizationLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:76: scope=DscScopeLevel.default
  TcpIoLib|MdeModulePkg/Library/DxeTcpIoLib/DxeTcpIoLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:79: scope=DscScopeLevel.default
  TimerLib|MdePkg/Library/BaseTimerLibNullTemplate/BaseTimerLibNullTemplate.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:105: scope=DscScopeLevel.default
  TpmMeasurementLib|MdeModulePkg/Library/TpmMeasurementLibNull/TpmMeasurementLibNull.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:75: scope=DscScopeLevel.default
  UdpIoLib|MdeModulePkg/Library/DxeUdpIoLib/DxeUdpIoLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:35: scope=DscScopeLevel.default
  UefiApplicationEntryPoint|MdePkg/Library/UefiApplicationEntryPoint/UefiApplicationEntryPoint.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:67: scope=DscScopeLevel.default
  UefiBootManagerLib|MdeModulePkg/Library/UefiBootManagerLib/UefiBootManagerLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:55: scope=DscScopeLevel.default
  UefiBootServicesTableLib|MdePkg/Library/UefiBootServicesTableLib/UefiBootServicesTableLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:62: scope=DscScopeLevel.default
  UefiDecompressLib|MdePkg/Library/BaseUefiDecompressLib/BaseUefiDecompressLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:34: scope=DscScopeLevel.default
  UefiDriverEntryPoint|MdePkg/Library/UefiDriverEntryPoint/UefiDriverEntryPoint.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:59: scope=DscScopeLevel.default
  UefiHiiServicesLib|MdeModulePkg/Library/UefiHiiServicesLib/UefiHiiServicesLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:58: scope=DscScopeLevel.default
  UefiLib|MdePkg/Library/UefiLib/UefiLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:57: scope=DscScopeLevel.default
  UefiRuntimeLib|MdePkg/Library/UefiRuntimeLib/UefiRuntimeLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:56: scope=DscScopeLevel.default
  UefiRuntimeServicesTableLib|MdePkg/Library/UefiRuntimeServicesTableLib/UefiRuntimeServicesTableLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:72: scope=DscScopeLevel.default
  UefiScsiLib|MdePkg/Library/UefiScsiLib/UefiScsiLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:71: scope=DscScopeLevel.default
  UefiUsbLib|MdePkg/Library/UefiUsbLib/UefiUsbLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:107: scope=DscScopeLevel.default
  VarCheckLib|MdeModulePkg/Library/VarCheckLib/VarCheckLib.inf

 [LibraryClasses.ARM, LibraryClasses.AARCH64]
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:189: scope=DscScopeLevel.default
  ArmLib|ArmPkg/Library/ArmLib/ArmBaseLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:190: scope=DscScopeLevel.default
  ArmMmuLib|ArmPkg/Library/ArmMmuLib/ArmMmuBaseLib.inf
   # Revision:MdePkg/Library/BaseStackCheckLib/BaseStackCheckLib.inf from C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:203: scope=DscScopeLevel.default
 # Revision:ArmPkg/Library/CompilerIntrinsicsLib/CompilerIntrinsicsLib.inf from C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:197: scope=DscScopeLevel.default
  NULL|MdePkg/Library/BaseStackCheckLib/BaseStackCheckLib.inf
  NULL|ArmPkg/Library/CompilerIntrinsicsLib/CompilerIntrinsicsLib.inf

 [LibraryClasses.EBC]
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:206: scope=DscScopeLevel.default
  LockBoxLib|MdeModulePkg/Library/LockBoxNullLib/LockBoxNullLib.inf

 [LibraryClasses.EBC.PEIM]
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:127: scope=DscScopeLevel.default
  IoLib|MdePkg/Library/PeiIoLibCpuIo/PeiIoLibCpuIo.inf

 [PcdsFeatureFlag]
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:212: scope=DscScopeLevel.default
  gEfiMdeModulePkgTokenSpaceGuid.PcdDevicePathSupportDevicePathFromText|FALSE
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:213: scope=DscScopeLevel.default
  gEfiMdeModulePkgTokenSpaceGuid.PcdDevicePathSupportDevicePathToText|FALSE
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:211: scope=DscScopeLevel.default
  gEfiMdeModulePkgTokenSpaceGuid.PcdInstallAcpiSdtProtocol|TRUE
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:210: scope=DscScopeLevel.default
  gEfiMdePkgTokenSpaceGuid.PcdComponentName2Disable|TRUE
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:209: scope=DscScopeLevel.default
  gEfiMdePkgTokenSpaceGuid.PcdDriverDiagnostics2Disable|TRUE

 [PcdsFixedAtBuild]
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:220: scope=DscScopeLevel.default
  gEfiMdeModulePkgTokenSpaceGuid.PcdMaxPeiPerformanceLogEntries|28
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:218: scope=DscScopeLevel.default
  gEfiMdeModulePkgTokenSpaceGuid.PcdMaxSizeNonPopulateCapsule|0x0
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:219: scope=DscScopeLevel.default
  gEfiMdeModulePkgTokenSpaceGuid.PcdMaxSizePopulateCapsule|0x0
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:216: scope=DscScopeLevel.default
  gEfiMdePkgTokenSpaceGuid.PcdDebugPropertyMask|0x0f
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:217: scope=DscScopeLevel.default
  gEfiMdePkgTokenSpaceGuid.PcdReportStatusCodePropertyMask|0x06

 [PcdsFixedAtBuild.IPF]
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:223: scope=DscScopeLevel.default
  gEfiMdePkgTokenSpaceGuid.PcdIoBlockBaseAddressForIpf|0x0ffffc000000

 [Components]
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:372: scope=DscScopeLevel.default
  MdeModulePkg/Application/BootManagerMenuApp/BootManagerMenuApp.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:479: scope=DscScopeLevel.default
  MdeModulePkg/Application/CapsuleApp/CapsuleApp.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:245: scope=DscScopeLevel.default
  MdeModulePkg/Application/HelloWorld/HelloWorld.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:246: scope=DscScopeLevel.default
  MdeModulePkg/Application/MemoryProfileInfo/MemoryProfileInfo.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:378: scope=DscScopeLevel.default
  MdeModulePkg/Application/UiApp/UiApp.inf{
 # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:374: scope=DscScopeLevel.default
		<LibraryClasses>
		  # Revision:MdeModulePkg/Library/BootMaintenanceManagerUiLib/BootMaintenanceManagerUiLib.inf from C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:377: scope=DscScopeLevel.default
 # Revision:MdeModulePkg/Library/BootManagerUiLib/BootManagerUiLib.inf from C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:376: scope=DscScopeLevel.default
 # Revision:MdeModulePkg/Library/DeviceManagerUiLib/DeviceManagerUiLib.inf from C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:375: scope=DscScopeLevel.default
		 NULL|MdeModulePkg/Library/BootMaintenanceManagerUiLib/BootMaintenanceManagerUiLib.inf
		 NULL|MdeModulePkg/Library/BootManagerUiLib/BootManagerUiLib.inf
		 NULL|MdeModulePkg/Library/DeviceManagerUiLib/DeviceManagerUiLib.inf


}
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:436: scope=DscScopeLevel.default
  MdeModulePkg/Application/VariableInfo/VariableInfo.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:294: scope=DscScopeLevel.default
  MdeModulePkg/Bus/Ata/AtaAtapiPassThru/AtaAtapiPassThru.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:293: scope=DscScopeLevel.default
  MdeModulePkg/Bus/Ata/AtaBusDxe/AtaBusDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:302: scope=DscScopeLevel.default
  MdeModulePkg/Bus/I2c/I2cDxe/I2cBusDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:304: scope=DscScopeLevel.default
  MdeModulePkg/Bus/I2c/I2cDxe/I2cDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:303: scope=DscScopeLevel.default
  MdeModulePkg/Bus/I2c/I2cDxe/I2cHostDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:305: scope=DscScopeLevel.default
  MdeModulePkg/Bus/Isa/IsaBusDxe/IsaBusDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:306: scope=DscScopeLevel.default
  MdeModulePkg/Bus/Isa/Ps2KeyboardDxe/Ps2KeyboardDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:307: scope=DscScopeLevel.default
  MdeModulePkg/Bus/Isa/Ps2MouseDxe/Ps2MouseDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:284: scope=DscScopeLevel.default
  MdeModulePkg/Bus/Pci/EhciDxe/EhciDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:287: scope=DscScopeLevel.default
  MdeModulePkg/Bus/Pci/EhciPei/EhciPei.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:289: scope=DscScopeLevel.default
  MdeModulePkg/Bus/Pci/IdeBusPei/IdeBusPei.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:271: scope=DscScopeLevel.default
  MdeModulePkg/Bus/Pci/IncompatiblePciDeviceSupportDxe/IncompatiblePciDeviceSupportDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:308: scope=DscScopeLevel.default
  MdeModulePkg/Bus/Pci/NonDiscoverablePciDeviceDxe/NonDiscoverablePciDeviceDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:272: scope=DscScopeLevel.default
  MdeModulePkg/Bus/Pci/NvmExpressDxe/NvmExpressDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:270: scope=DscScopeLevel.default
  MdeModulePkg/Bus/Pci/PciBusDxe/PciBusDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:268: scope=DscScopeLevel.default
  MdeModulePkg/Bus/Pci/PciHostBridgeDxe/PciHostBridgeDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:269: scope=DscScopeLevel.default
  MdeModulePkg/Bus/Pci/PciSioSerialDxe/PciSioSerialDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:292: scope=DscScopeLevel.default
  MdeModulePkg/Bus/Pci/SataControllerDxe/SataControllerDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:273: scope=DscScopeLevel.default
  MdeModulePkg/Bus/Pci/SdMmcPciHcDxe/SdMmcPciHcDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:274: scope=DscScopeLevel.default
  MdeModulePkg/Bus/Pci/SdMmcPciHcPei/SdMmcPciHcPei.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:279: scope=DscScopeLevel.default
  MdeModulePkg/Bus/Pci/UfsPciHcDxe/UfsPciHcDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:281: scope=DscScopeLevel.default
  MdeModulePkg/Bus/Pci/UfsPciHcPei/UfsPciHcPei.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:285: scope=DscScopeLevel.default
  MdeModulePkg/Bus/Pci/UhciDxe/UhciDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:286: scope=DscScopeLevel.default
  MdeModulePkg/Bus/Pci/UhciPei/UhciPei.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:283: scope=DscScopeLevel.default
  MdeModulePkg/Bus/Pci/XhciDxe/XhciDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:288: scope=DscScopeLevel.default
  MdeModulePkg/Bus/Pci/XhciPei/XhciPei.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:295: scope=DscScopeLevel.default
  MdeModulePkg/Bus/Scsi/ScsiBusDxe/ScsiBusDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:296: scope=DscScopeLevel.default
  MdeModulePkg/Bus/Scsi/ScsiDiskDxe/ScsiDiskDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:275: scope=DscScopeLevel.default
  MdeModulePkg/Bus/Sd/EmmcBlockIoPei/EmmcBlockIoPei.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:277: scope=DscScopeLevel.default
  MdeModulePkg/Bus/Sd/EmmcDxe/EmmcDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:276: scope=DscScopeLevel.default
  MdeModulePkg/Bus/Sd/SdBlockIoPei/SdBlockIoPei.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:278: scope=DscScopeLevel.default
  MdeModulePkg/Bus/Sd/SdDxe/SdDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:282: scope=DscScopeLevel.default
  MdeModulePkg/Bus/Ufs/UfsBlockIoPei/UfsBlockIoPei.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:280: scope=DscScopeLevel.default
  MdeModulePkg/Bus/Ufs/UfsPassThruDxe/UfsPassThruDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:291: scope=DscScopeLevel.default
  MdeModulePkg/Bus/Usb/UsbBotPei/UsbBotPei.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:297: scope=DscScopeLevel.default
  MdeModulePkg/Bus/Usb/UsbBusDxe/UsbBusDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:290: scope=DscScopeLevel.default
  MdeModulePkg/Bus/Usb/UsbBusPei/UsbBusPei.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:298: scope=DscScopeLevel.default
  MdeModulePkg/Bus/Usb/UsbKbDxe/UsbKbDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:299: scope=DscScopeLevel.default
  MdeModulePkg/Bus/Usb/UsbMassStorageDxe/UsbMassStorageDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:300: scope=DscScopeLevel.default
  MdeModulePkg/Bus/Usb/UsbMouseAbsolutePointerDxe/UsbMouseAbsolutePointerDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:301: scope=DscScopeLevel.default
  MdeModulePkg/Bus/Usb/UsbMouseDxe/UsbMouseDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:310: scope=DscScopeLevel.default
  MdeModulePkg/Core/DxeIplPeim/DxeIpl.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:311: scope=DscScopeLevel.default
  MdeModulePkg/Core/Pei/PeiMain.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:312: scope=DscScopeLevel.default
  MdeModulePkg/Core/RuntimeDxe/RuntimeDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:354: scope=DscScopeLevel.default
  MdeModulePkg/Library/AuthVariableLibNull/AuthVariableLibNull.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:367: scope=DscScopeLevel.default
  MdeModulePkg/Library/BaseBmpSupportLib/BaseBmpSupportLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:361: scope=DscScopeLevel.default
  MdeModulePkg/Library/BaseIpmiLibNull/BaseIpmiLibNull.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:341: scope=DscScopeLevel.default
  MdeModulePkg/Library/BasePlatformHookLibNull/BasePlatformHookLibNull.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:334: scope=DscScopeLevel.default
  MdeModulePkg/Library/BaseResetSystemLibNull/BaseResetSystemLibNull.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:340: scope=DscScopeLevel.default
  MdeModulePkg/Library/BaseSerialPortLib16550/BaseSerialPortLib16550.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:252: scope=DscScopeLevel.default
  MdeModulePkg/Library/BaseSortLib/BaseSortLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:352: scope=DscScopeLevel.default
  MdeModulePkg/Library/BootLogoLib/BootLogoLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:253: scope=DscScopeLevel.default
  MdeModulePkg/Library/BootMaintenanceManagerUiLib/BootMaintenanceManagerUiLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:254: scope=DscScopeLevel.default
  MdeModulePkg/Library/BootManagerUiLib/BootManagerUiLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:348: scope=DscScopeLevel.default
  MdeModulePkg/Library/BrotliCustomDecompressLib/BrotliCustomDecompressLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:345: scope=DscScopeLevel.default
  MdeModulePkg/Library/CpuExceptionHandlerLibNull/CpuExceptionHandlerLibNull.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:255: scope=DscScopeLevel.default
  MdeModulePkg/Library/CustomizedDisplayLib/CustomizedDisplayLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:256: scope=DscScopeLevel.default
  MdeModulePkg/Library/DebugAgentLibNull/DebugAgentLibNull.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:257: scope=DscScopeLevel.default
  MdeModulePkg/Library/DeviceManagerUiLib/DeviceManagerUiLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:368: scope=DscScopeLevel.default
  MdeModulePkg/Library/DisplayUpdateProgressLibGraphics/DisplayUpdateProgressLibGraphics.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:369: scope=DscScopeLevel.default
  MdeModulePkg/Library/DisplayUpdateProgressLibText/DisplayUpdateProgressLibText.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:481: scope=DscScopeLevel.default
  MdeModulePkg/Library/DxeCapsuleLibFmp/DxeCapsuleLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:482: scope=DscScopeLevel.default
  MdeModulePkg/Library/DxeCapsuleLibFmp/DxeRuntimeCapsuleLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:314: scope=DscScopeLevel.default
  MdeModulePkg/Library/DxeCapsuleLibNull/DxeCapsuleLibNull.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:316: scope=DscScopeLevel.default
  MdeModulePkg/Library/DxeCoreMemoryAllocationLib/DxeCoreMemoryAllocationLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:317: scope=DscScopeLevel.default
  MdeModulePkg/Library/DxeCoreMemoryAllocationLib/DxeCoreMemoryAllocationProfileLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:318: scope=DscScopeLevel.default
  MdeModulePkg/Library/DxeCorePerformanceLib/DxeCorePerformanceLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:319: scope=DscScopeLevel.default
  MdeModulePkg/Library/DxeCrc32GuidedSectionExtractLib/DxeCrc32GuidedSectionExtractLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:342: scope=DscScopeLevel.default
  MdeModulePkg/Library/DxeDebugPrintErrorLevelLib/DxeDebugPrintErrorLevelLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:320: scope=DscScopeLevel.default
  MdeModulePkg/Library/DxeDpcLib/DxeDpcLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:360: scope=DscScopeLevel.default
  MdeModulePkg/Library/DxeFileExplorerProtocol/DxeFileExplorerProtocol.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:248: scope=DscScopeLevel.default
  MdeModulePkg/Library/DxeHttpLib/DxeHttpLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:321: scope=DscScopeLevel.default
  MdeModulePkg/Library/DxeIpIoLib/DxeIpIoLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:362: scope=DscScopeLevel.default
  MdeModulePkg/Library/DxeIpmiLibIpmiProtocol/DxeIpmiLibIpmiProtocol.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:322: scope=DscScopeLevel.default
  MdeModulePkg/Library/DxeNetLib/DxeNetLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:323: scope=DscScopeLevel.default
  MdeModulePkg/Library/DxePerformanceLib/DxePerformanceLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:326: scope=DscScopeLevel.default
  MdeModulePkg/Library/DxePrintLibPrint2Protocol/DxePrintLibPrint2Protocol.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:338: scope=DscScopeLevel.default
  MdeModulePkg/Library/DxeReportStatusCodeLib/DxeReportStatusCodeLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:324: scope=DscScopeLevel.default
  MdeModulePkg/Library/DxeResetSystemLib/DxeResetSystemLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:335: scope=DscScopeLevel.default
  MdeModulePkg/Library/DxeSecurityManagementLib/DxeSecurityManagementLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:258: scope=DscScopeLevel.default
  MdeModulePkg/Library/DxeTcpIoLib/DxeTcpIoLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:325: scope=DscScopeLevel.default
  MdeModulePkg/Library/DxeUdpIoLib/DxeUdpIoLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:359: scope=DscScopeLevel.default
  MdeModulePkg/Library/FileExplorerLib/FileExplorerLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:480: scope=DscScopeLevel.default
  MdeModulePkg/Library/FmpAuthenticationLibNull/FmpAuthenticationLibNull.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:365: scope=DscScopeLevel.default
  MdeModulePkg/Library/FrameBufferBltLib/FrameBufferBltLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:259: scope=DscScopeLevel.default
  MdeModulePkg/Library/LockBoxNullLib/LockBoxNullLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:347: scope=DscScopeLevel.default
  MdeModulePkg/Library/LzmaCustomDecompressLib/LzmaCustomDecompressLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:366: scope=DscScopeLevel.default
  MdeModulePkg/Library/NonDiscoverableDeviceRegistrationLib/NonDiscoverableDeviceRegistrationLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:336: scope=DscScopeLevel.default
  MdeModulePkg/Library/OemHookStatusCodeLibNull/OemHookStatusCodeLibNull.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:260: scope=DscScopeLevel.default
  MdeModulePkg/Library/PciHostBridgeLibNull/PciHostBridgeLibNull.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:327: scope=DscScopeLevel.default
  MdeModulePkg/Library/PeiCrc32GuidedSectionExtractLib/PeiCrc32GuidedSectionExtractLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:344: scope=DscScopeLevel.default
  MdeModulePkg/Library/PeiDebugPrintHobLib/PeiDebugPrintHobLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:349: scope=DscScopeLevel.default
  MdeModulePkg/Library/PeiDxeDebugLibReportStatusCode/PeiDxeDebugLibReportStatusCode.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:363: scope=DscScopeLevel.default
  MdeModulePkg/Library/PeiIpmiLibIpmiPpi/PeiIpmiLibIpmiPpi.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:328: scope=DscScopeLevel.default
  MdeModulePkg/Library/PeiPerformanceLib/PeiPerformanceLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:329: scope=DscScopeLevel.default
  MdeModulePkg/Library/PeiRecoveryLibNull/PeiRecoveryLibNull.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:337: scope=DscScopeLevel.default
  MdeModulePkg/Library/PeiReportStatusCodeLib/PeiReportStatusCodeLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:330: scope=DscScopeLevel.default
  MdeModulePkg/Library/PeiResetSystemLib/PeiResetSystemLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:331: scope=DscScopeLevel.default
  MdeModulePkg/Library/PeiS3LibNull/PeiS3LibNull.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:343: scope=DscScopeLevel.default
  MdeModulePkg/Library/PiDxeS3BootScriptLib/DxeS3BootScriptLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:261: scope=DscScopeLevel.default
  MdeModulePkg/Library/PiSmmCoreSmmServicesTableLib/PiSmmCoreSmmServicesTableLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:351: scope=DscScopeLevel.default
  MdeModulePkg/Library/PlatformBootManagerLibNull/PlatformBootManagerLibNull.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:346: scope=DscScopeLevel.default
  MdeModulePkg/Library/PlatformHookLibSerialPortPpi/PlatformHookLibSerialPortPpi.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:358: scope=DscScopeLevel.default
  MdeModulePkg/Library/PlatformVarCleanupLib/PlatformVarCleanupLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:333: scope=DscScopeLevel.default
  MdeModulePkg/Library/ResetUtilityLib/ResetUtilityLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:339: scope=DscScopeLevel.default
  MdeModulePkg/Library/RuntimeDxeReportStatusCodeLib/RuntimeDxeReportStatusCodeLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:263: scope=DscScopeLevel.default
  MdeModulePkg/Library/SecurityLockAuditDebugMessageLib/SecurityLockAuditDebugMessageLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:264: scope=DscScopeLevel.default
  MdeModulePkg/Library/SecurityLockAuditLibNull/SecurityLockAuditLibNull.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:364: scope=DscScopeLevel.default
  MdeModulePkg/Library/SmmIpmiLibSmmIpmiProtocol/SmmIpmiLibSmmIpmiProtocol.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:353: scope=DscScopeLevel.default
  MdeModulePkg/Library/TpmMeasurementLibNull/TpmMeasurementLibNull.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:350: scope=DscScopeLevel.default
  MdeModulePkg/Library/UefiBootManagerLib/UefiBootManagerLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:332: scope=DscScopeLevel.default
  MdeModulePkg/Library/UefiHiiLib/UefiHiiLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:262: scope=DscScopeLevel.default
  MdeModulePkg/Library/UefiHiiServicesLib/UefiHiiServicesLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:315: scope=DscScopeLevel.default
  MdeModulePkg/Library/UefiMemoryAllocationProfileLib/UefiMemoryAllocationProfileLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:249: scope=DscScopeLevel.default
  MdeModulePkg/Library/UefiSortLib/UefiSortLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:356: scope=DscScopeLevel.default
  MdeModulePkg/Library/VarCheckHiiLib/VarCheckHiiLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:355: scope=DscScopeLevel.default
  MdeModulePkg/Library/VarCheckLib/VarCheckLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:357: scope=DscScopeLevel.default
  MdeModulePkg/Library/VarCheckPcdLib/VarCheckPcdLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:250: scope=DscScopeLevel.default
  MdeModulePkg/Logo/Logo.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:443: scope=DscScopeLevel.default
  MdeModulePkg/Universal/Acpi/AcpiPlatformDxe/AcpiPlatformDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:444: scope=DscScopeLevel.default
  MdeModulePkg/Universal/Acpi/AcpiTableDxe/AcpiTableDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:456: scope=DscScopeLevel.default
  MdeModulePkg/Universal/Acpi/BootGraphicsResourceTableDxe/BootGraphicsResourceTableDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:455: scope=DscScopeLevel.default
  MdeModulePkg/Universal/Acpi/FirmwarePerformanceDataTableDxe/FirmwarePerformanceDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:454: scope=DscScopeLevel.default
  MdeModulePkg/Universal/Acpi/FirmwarePerformanceDataTablePei/FirmwarePerformancePei.inf{
 # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:452: scope=DscScopeLevel.default
		<LibraryClasses>
		  # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:453: scope=DscScopeLevel.default
		 LockBoxLib|MdeModulePkg/Library/LockBoxNullLib/LockBoxNullLib.inf


}
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:371: scope=DscScopeLevel.default
  MdeModulePkg/Universal/BdsDxe/BdsDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:380: scope=DscScopeLevel.default
  MdeModulePkg/Universal/BootManagerPolicyDxe/BootManagerPolicyDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:381: scope=DscScopeLevel.default
  MdeModulePkg/Universal/CapsulePei/CapsulePei.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:382: scope=DscScopeLevel.default
  MdeModulePkg/Universal/CapsuleRuntimeDxe/CapsuleRuntimeDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:383: scope=DscScopeLevel.default
  MdeModulePkg/Universal/Console/ConPlatformDxe/ConPlatformDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:384: scope=DscScopeLevel.default
  MdeModulePkg/Universal/Console/ConSplitterDxe/ConSplitterDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:385: scope=DscScopeLevel.default
  MdeModulePkg/Universal/Console/GraphicsConsoleDxe/GraphicsConsoleDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:386: scope=DscScopeLevel.default
  MdeModulePkg/Universal/Console/GraphicsOutputDxe/GraphicsOutputDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:387: scope=DscScopeLevel.default
  MdeModulePkg/Universal/Console/TerminalDxe/TerminalDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:388: scope=DscScopeLevel.default
  MdeModulePkg/Universal/DebugPortDxe/DebugPortDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:389: scope=DscScopeLevel.default
  MdeModulePkg/Universal/DevicePathDxe/DevicePathDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:395: scope=DscScopeLevel.default
  MdeModulePkg/Universal/Disk/CdExpressPei/CdExpressPei.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:391: scope=DscScopeLevel.default
  MdeModulePkg/Universal/Disk/DiskIoDxe/DiskIoDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:392: scope=DscScopeLevel.default
  MdeModulePkg/Universal/Disk/PartitionDxe/PartitionDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:393: scope=DscScopeLevel.default
  MdeModulePkg/Universal/Disk/UdfDxe/UdfDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:394: scope=DscScopeLevel.default
  MdeModulePkg/Universal/Disk/UnicodeCollation/EnglishDxe/EnglishDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:435: scope=DscScopeLevel.default
  MdeModulePkg/Universal/DisplayEngineDxe/DisplayEngineDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:379: scope=DscScopeLevel.default
  MdeModulePkg/Universal/DriverHealthManagerDxe/DriverHealthManagerDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:396: scope=DscScopeLevel.default
  MdeModulePkg/Universal/DriverSampleDxe/DriverSampleDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:467: scope=DscScopeLevel.default
  MdeModulePkg/Universal/EsrtDxe/EsrtDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:468: scope=DscScopeLevel.default
  MdeModulePkg/Universal/EsrtFmpDxe/EsrtFmpDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:441: scope=DscScopeLevel.default
  MdeModulePkg/Universal/FaultTolerantWriteDxe/FaultTolerantWriteDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:437: scope=DscScopeLevel.default
  MdeModulePkg/Universal/FaultTolerantWritePei/FaultTolerantWritePei.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:474: scope=DscScopeLevel.default
  MdeModulePkg/Universal/FileExplorerDxe/FileExplorerDxe.inf{
 # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:472: scope=DscScopeLevel.default
		<LibraryClasses>
		  # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:473: scope=DscScopeLevel.default
		 FileExplorerLib|MdeModulePkg/Library/FileExplorerLib/FileExplorerLib.inf


}
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:466: scope=DscScopeLevel.default
  MdeModulePkg/Universal/FvSimpleFileSystemDxe/FvSimpleFileSystemDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:397: scope=DscScopeLevel.default
  MdeModulePkg/Universal/HiiDatabaseDxe/HiiDatabaseDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:445: scope=DscScopeLevel.default
  MdeModulePkg/Universal/HiiResourcesSampleDxe/HiiResourcesSampleDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:446: scope=DscScopeLevel.default
  MdeModulePkg/Universal/LegacyRegion2Dxe/LegacyRegion2Dxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:477: scope=DscScopeLevel.default
  MdeModulePkg/Universal/LoadFileOnFv2/LoadFileOnFv2.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:398: scope=DscScopeLevel.default
  MdeModulePkg/Universal/MemoryTest/GenericMemoryTestDxe/GenericMemoryTestDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:399: scope=DscScopeLevel.default
  MdeModulePkg/Universal/MemoryTest/NullMemoryTestDxe/NullMemoryTestDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:400: scope=DscScopeLevel.default
  MdeModulePkg/Universal/Metronome/Metronome.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:401: scope=DscScopeLevel.default
  MdeModulePkg/Universal/MonotonicCounterRuntimeDxe/MonotonicCounterRuntimeDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:413: scope=DscScopeLevel.default
  MdeModulePkg/Universal/Network/ArpDxe/ArpDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:414: scope=DscScopeLevel.default
  MdeModulePkg/Universal/Network/Dhcp4Dxe/Dhcp4Dxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:415: scope=DscScopeLevel.default
  MdeModulePkg/Universal/Network/DpcDxe/DpcDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:417: scope=DscScopeLevel.default
  MdeModulePkg/Universal/Network/IScsiDxe/IScsiDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:416: scope=DscScopeLevel.default
  MdeModulePkg/Universal/Network/Ip4Dxe/Ip4Dxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:418: scope=DscScopeLevel.default
  MdeModulePkg/Universal/Network/MnpDxe/MnpDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:420: scope=DscScopeLevel.default
  MdeModulePkg/Universal/Network/Mtftp4Dxe/Mtftp4Dxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:421: scope=DscScopeLevel.default
  MdeModulePkg/Universal/Network/SnpDxe/SnpDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:422: scope=DscScopeLevel.default
  MdeModulePkg/Universal/Network/Tcp4Dxe/Tcp4Dxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:423: scope=DscScopeLevel.default
  MdeModulePkg/Universal/Network/Udp4Dxe/Udp4Dxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:419: scope=DscScopeLevel.default
  MdeModulePkg/Universal/Network/VlanConfigDxe/VlanConfigDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:426: scope=DscScopeLevel.default
  MdeModulePkg/Universal/PCD/Dxe/Pcd.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:427: scope=DscScopeLevel.default
  MdeModulePkg/Universal/PCD/Pei/Pcd.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:425: scope=DscScopeLevel.default
  MdeModulePkg/Universal/PcatSingleSegmentPciCfg2Pei/PcatSingleSegmentPciCfg2Pei.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:428: scope=DscScopeLevel.default
  MdeModulePkg/Universal/PlatformDriOverrideDxe/PlatformDriOverrideDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:390: scope=DscScopeLevel.default
  MdeModulePkg/Universal/PrintDxe/PrintDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:470: scope=DscScopeLevel.default
  MdeModulePkg/Universal/PropertiesTableAttributesDxe/PropertiesTableAttributesDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:430: scope=DscScopeLevel.default
  MdeModulePkg/Universal/ReportStatusCodeRouter/Pei/ReportStatusCodeRouterPei.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:431: scope=DscScopeLevel.default
  MdeModulePkg/Universal/ReportStatusCodeRouter/RuntimeDxe/ReportStatusCodeRouterRuntimeDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:405: scope=DscScopeLevel.default
  MdeModulePkg/Universal/ResetSystemPei/ResetSystemPei.inf{
 # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:403: scope=DscScopeLevel.default
		<LibraryClasses>
		  # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:404: scope=DscScopeLevel.default
		 ResetSystemLib|MdeModulePkg/Library/BaseResetSystemLibNull/BaseResetSystemLibNull.inf


}
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:409: scope=DscScopeLevel.default
  MdeModulePkg/Universal/ResetSystemRuntimeDxe/ResetSystemRuntimeDxe.inf{
 # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:407: scope=DscScopeLevel.default
		<LibraryClasses>
		  # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:408: scope=DscScopeLevel.default
		 ResetSystemLib|MdeModulePkg/Library/BaseResetSystemLibNull/BaseResetSystemLibNull.inf


}
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:460: scope=DscScopeLevel.default
  MdeModulePkg/Universal/SectionExtractionDxe/SectionExtractionDxe.inf{
 # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:458: scope=DscScopeLevel.default
		<LibraryClasses>
		  # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:459: scope=DscScopeLevel.default
		 NULL|MdeModulePkg/Library/DxeCrc32GuidedSectionExtractLib/DxeCrc32GuidedSectionExtractLib.inf


}
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:464: scope=DscScopeLevel.default
  MdeModulePkg/Universal/SectionExtractionPei/SectionExtractionPei.inf{
 # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:462: scope=DscScopeLevel.default
		<LibraryClasses>
		  # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:463: scope=DscScopeLevel.default
		 NULL|MdeModulePkg/Library/PeiCrc32GuidedSectionExtractLib/PeiCrc32GuidedSectionExtractLib.inf


}
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:433: scope=DscScopeLevel.default
  MdeModulePkg/Universal/SecurityStubDxe/SecurityStubDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:476: scope=DscScopeLevel.default
  MdeModulePkg/Universal/SerialDxe/SerialDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:434: scope=DscScopeLevel.default
  MdeModulePkg/Universal/SetupBrowserDxe/SetupBrowserDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:410: scope=DscScopeLevel.default
  MdeModulePkg/Universal/SmbiosDxe/SmbiosDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:411: scope=DscScopeLevel.default
  MdeModulePkg/Universal/SmbiosMeasurementDxe/SmbiosMeasurementDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:448: scope=DscScopeLevel.default
  MdeModulePkg/Universal/StatusCodeHandler/Pei/StatusCodeHandlerPei.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:449: scope=DscScopeLevel.default
  MdeModulePkg/Universal/StatusCodeHandler/RuntimeDxe/StatusCodeHandlerRuntimeDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:440: scope=DscScopeLevel.default
  MdeModulePkg/Universal/TimestampDxe/TimestampDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:438: scope=DscScopeLevel.default
  MdeModulePkg/Universal/Variable/Pei/VariablePei.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:265: scope=DscScopeLevel.default
  MdeModulePkg/Universal/Variable/RuntimeDxe/PropertyBasedVarLockLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:439: scope=DscScopeLevel.default
  MdeModulePkg/Universal/WatchdogTimerDxe/WatchdogTimer.inf

 [Components.IA32, Components.X64]
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:502: scope=DscScopeLevel.default
  MdeModulePkg/Application/SmiHandlerProfileInfo/SmiHandlerProfileInfo.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:504: scope=DscScopeLevel.default
  MdeModulePkg/Core/PiSmmCore/PiSmmCore.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:503: scope=DscScopeLevel.default
  MdeModulePkg/Core/PiSmmCore/PiSmmIpl.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:529: scope=DscScopeLevel.default
  MdeModulePkg/Library/DxeSmmPerformanceLib/DxeSmmPerformanceLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:535: scope=DscScopeLevel.default
  MdeModulePkg/Library/LzmaCustomDecompressLib/LzmaArchCustomDecompressLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:526: scope=DscScopeLevel.default
  MdeModulePkg/Library/PiSmmCoreMemoryAllocationLib/PiSmmCoreMemoryAllocationLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:525: scope=DscScopeLevel.default
  MdeModulePkg/Library/PiSmmCoreMemoryAllocationLib/PiSmmCoreMemoryAllocationProfileLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:527: scope=DscScopeLevel.default
  MdeModulePkg/Library/SmmCorePerformanceLib/SmmCorePerformanceLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:533: scope=DscScopeLevel.default
  MdeModulePkg/Library/SmmCorePlatformHookLibNull/SmmCorePlatformHookLibNull.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:531: scope=DscScopeLevel.default
  MdeModulePkg/Library/SmmLockBoxLib/SmmLockBoxDxeLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:530: scope=DscScopeLevel.default
  MdeModulePkg/Library/SmmLockBoxLib/SmmLockBoxPeiLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:532: scope=DscScopeLevel.default
  MdeModulePkg/Library/SmmLockBoxLib/SmmLockBoxSmmLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:524: scope=DscScopeLevel.default
  MdeModulePkg/Library/SmmMemoryAllocationProfileLib/SmmMemoryAllocationProfileLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:528: scope=DscScopeLevel.default
  MdeModulePkg/Library/SmmPerformanceLib/SmmPerformanceLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:520: scope=DscScopeLevel.default
  MdeModulePkg/Library/SmmReportStatusCodeLib/SmmReportStatusCodeLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:534: scope=DscScopeLevel.default
  MdeModulePkg/Library/SmmSmiHandlerProfileLib/SmmSmiHandlerProfileLib.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:536: scope=DscScopeLevel.default
  MdeModulePkg/Universal/Acpi/BootScriptExecutorDxe/BootScriptExecutorDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:539: scope=DscScopeLevel.default
  MdeModulePkg/Universal/Acpi/FirmwarePerformanceDataTableSmm/FirmwarePerformanceSmm.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:537: scope=DscScopeLevel.default
  MdeModulePkg/Universal/Acpi/S3SaveStateDxe/S3SaveStateDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:538: scope=DscScopeLevel.default
  MdeModulePkg/Universal/Acpi/SmmS3SaveState/SmmS3SaveState.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:544: scope=DscScopeLevel.default
  MdeModulePkg/Universal/Disk/RamDiskDxe/RamDiskDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:540: scope=DscScopeLevel.default
  MdeModulePkg/Universal/FaultTolerantWriteDxe/FaultTolerantWriteSmm.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:541: scope=DscScopeLevel.default
  MdeModulePkg/Universal/FaultTolerantWriteDxe/FaultTolerantWriteSmmDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:523: scope=DscScopeLevel.default
  MdeModulePkg/Universal/LockBox/SmmLockBox/SmmLockBox.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:542: scope=DscScopeLevel.default
  MdeModulePkg/Universal/RegularExpressionDxe/RegularExpressionDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:522: scope=DscScopeLevel.default
  MdeModulePkg/Universal/ReportStatusCodeRouter/Smm/ReportStatusCodeRouterSmm.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:543: scope=DscScopeLevel.default
  MdeModulePkg/Universal/SmmCommunicationBufferDxe/SmmCommunicationBufferDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:521: scope=DscScopeLevel.default
  MdeModulePkg/Universal/StatusCodeHandler/Smm/StatusCodeHandlerSmm.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:518: scope=DscScopeLevel.default
  MdeModulePkg/Universal/Variable/RuntimeDxe/VariableRuntimeDxe.inf{
 # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:513: scope=DscScopeLevel.default
		<LibraryClasses>
		  # Revision:MdeModulePkg/Universal/Variable/RuntimeDxe/PropertyBasedVarLockLib.inf from C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:517: scope=DscScopeLevel.default
 # Revision:MdeModulePkg/Library/VarCheckPcdLib/VarCheckPcdLib.inf from C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:516: scope=DscScopeLevel.default
 # Revision:MdeModulePkg/Library/VarCheckHiiLib/VarCheckHiiLib.inf from C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:515: scope=DscScopeLevel.default
 # Revision:MdeModulePkg/Library/VarCheckUefiLib/VarCheckUefiLib.inf from C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:514: scope=DscScopeLevel.default
		 NULL|MdeModulePkg/Universal/Variable/RuntimeDxe/PropertyBasedVarLockLib.inf
		 NULL|MdeModulePkg/Library/VarCheckPcdLib/VarCheckPcdLib.inf
		 NULL|MdeModulePkg/Library/VarCheckHiiLib/VarCheckHiiLib.inf
		 NULL|MdeModulePkg/Library/VarCheckUefiLib/VarCheckUefiLib.inf


}
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:511: scope=DscScopeLevel.default
  MdeModulePkg/Universal/Variable/RuntimeDxe/VariableSmm.inf{
 # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:506: scope=DscScopeLevel.default
		<LibraryClasses>
		  # Revision:MdeModulePkg/Universal/Variable/RuntimeDxe/PropertyBasedVarLockLib.inf from C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:510: scope=DscScopeLevel.default
 # Revision:MdeModulePkg/Library/VarCheckPcdLib/VarCheckPcdLib.inf from C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:509: scope=DscScopeLevel.default
 # Revision:MdeModulePkg/Library/VarCheckHiiLib/VarCheckHiiLib.inf from C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:508: scope=DscScopeLevel.default
 # Revision:MdeModulePkg/Library/VarCheckUefiLib/VarCheckUefiLib.inf from C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:507: scope=DscScopeLevel.default
		 NULL|MdeModulePkg/Universal/Variable/RuntimeDxe/PropertyBasedVarLockLib.inf
		 NULL|MdeModulePkg/Library/VarCheckPcdLib/VarCheckPcdLib.inf
		 NULL|MdeModulePkg/Library/VarCheckHiiLib/VarCheckHiiLib.inf
		 NULL|MdeModulePkg/Library/VarCheckUefiLib/VarCheckUefiLib.inf


}
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:519: scope=DscScopeLevel.default
  MdeModulePkg/Universal/Variable/RuntimeDxe/VariableSmmRuntimeDxe.inf

 [Components.IA32, Components.X64, Components.Ebc]
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:499: scope=DscScopeLevel.default
  MdeModulePkg/Universal/Variable/EmuRuntimeDxe/EmuVariableRuntimeDxe.inf

 [Components.IA32, Components.X64, Components.IPF, Components.AARCH64]
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:486: scope=DscScopeLevel.default
  MdeModulePkg/Universal/DebugSupportDxe/DebugSupportDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:488: scope=DscScopeLevel.default
  MdeModulePkg/Universal/EbcDxe/EbcDebugger.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:489: scope=DscScopeLevel.default
  MdeModulePkg/Universal/EbcDxe/EbcDebuggerConfig.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:487: scope=DscScopeLevel.default
  MdeModulePkg/Universal/EbcDxe/EbcDxe.inf
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:485: scope=DscScopeLevel.default
  MdeModulePkg/Universal/Network/UefiPxeBcDxe/UefiPxeBcDxe.inf

 [Components.IA32, Components.X64, Components.IPF, Components.ARM, Components.AARCH64]
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:496: scope=DscScopeLevel.default
  MdeModulePkg/Core/Dxe/DxeMain.inf{
 # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:494: scope=DscScopeLevel.default
		<LibraryClasses>
		  # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:495: scope=DscScopeLevel.default
		 NULL|MdeModulePkg/Library/DxeCrc32GuidedSectionExtractLib/DxeCrc32GuidedSectionExtractLib.inf


}
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:492: scope=DscScopeLevel.default
  MdeModulePkg/Library/VarCheckUefiLib/VarCheckUefiLib.inf

 [Components.X64]
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:547: scope=DscScopeLevel.default
  MdeModulePkg/Universal/CapsulePei/CapsuleX64.inf

 [BuildOptions]
   # From: C:\git\corebuild\MdeModulePkg\MdeModulePkg.dsc:550: scope=DscScopeLevel.default
  *_*_*_CC_FLAGS=-D DISABLE_NEW_DEPRECATED_INTERFACES

