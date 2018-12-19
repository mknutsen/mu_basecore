/** @file
Driver to install an empty varlock protocol

Copyright (c) 2018, Microsoft Corporation. All rights reserved.<BR>

**/

#include <Library/DebugLib.h>
#include <Protocol/VariableLock.h>
#include <Library/UefiBootServicesTableLib.h>

EFI_STATUS
EFIAPI
VariableLockRequestToLock (
  IN CONST EDKII_VARIABLE_LOCK_PROTOCOL *This,
  IN       CHAR16                       *VariableName,
  IN       EFI_GUID                     *VendorGuid
  )
{
  return EFI_SUCCESS;
}

EDKII_VARIABLE_LOCK_PROTOCOL mVariableLock = { VariableLockRequestToLock };

/**
Main entry for this driver.

@param ImageHandle     Image handle this driver.
@param SystemTable     Pointer to SystemTable.

@retval EFI_STATUS
**/
EFI_STATUS
EFIAPI
VarLockNullDxeInit(
  IN EFI_HANDLE           ImageHandle,
  IN EFI_SYSTEM_TABLE     *SystemTable)
{
  EFI_STATUS Status = EFI_SUCCESS;
  EFI_HANDLE Handle = NULL;

  Status = gBS->InstallMultipleProtocolInterfaces (
                  &Handle,
                  &gEdkiiVariableLockProtocolGuid,
                  &mVariableLock,
                  NULL
                  );

  DEBUG((DEBUG_ERROR, "VarLockNullDxe - VarLock Install Status: %r\n", Status));

  return EFI_SUCCESS;
}