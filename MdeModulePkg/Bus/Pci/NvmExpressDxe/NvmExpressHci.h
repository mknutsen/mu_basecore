/** @file
  NvmExpressDxe driver is used to manage non-volatile memory subsystem which follows
  NVM Express specification.

  (C) Copyright 2016 Hewlett Packard Enterprise Development LP<BR>
  Copyright (c) 2013 - 2015, Intel Corporation. All rights reserved.<BR>
  This program and the accompanying materials
  are licensed and made available under the terms and conditions of the BSD License
  which accompanies this distribution.  The full text of the license may be found at
  http://opensource.org/licenses/bsd-license.php.

  THE PROGRAM IS DISTRIBUTED UNDER THE BSD LICENSE ON AN "AS IS" BASIS,
  WITHOUT WARRANTIES OR REPRESENTATIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED.

  Copyright (c) 2016, Microsoft Corporation

**/

#ifndef _NVME_HCI_H_
#define _NVME_HCI_H_

#define NVME_BAR                 0

//
// Offset from the beginning of private data queue buffer
//
#define NVME_ASQ_BUF_OFFSET                  EFI_PAGE_SIZE

/**
  Initialize the Nvm Express controller.

  @param[in] Private                 The pointer to the NVME_CONTROLLER_PRIVATE_DATA data structure.

  @retval EFI_SUCCESS                The NVM Express Controller is initialized successfully.
  @retval Others                     A device error occurred while initializing the controller.

**/
EFI_STATUS
NvmeControllerInit (
  IN NVME_CONTROLLER_PRIVATE_DATA    *Private
  );

/**
  Get identify controller data.

  @param  Private          The pointer to the NVME_CONTROLLER_PRIVATE_DATA data structure.
  @param  Buffer           The buffer used to store the identify controller data.

  @return EFI_SUCCESS      Successfully get the identify controller data.
  @return EFI_DEVICE_ERROR Fail to get the identify controller data.

**/
EFI_STATUS
NvmeIdentifyController (
  IN NVME_CONTROLLER_PRIVATE_DATA       *Private,
  IN VOID                               *Buffer
  );

/**
  Get specified identify namespace data.

  @param  Private          The pointer to the NVME_CONTROLLER_PRIVATE_DATA data structure.
  @param  NamespaceId      The specified namespace identifier.
  @param  Buffer           The buffer used to store the identify namespace data.

  @return EFI_SUCCESS      Successfully get the identify namespace data.
  @return EFI_DEVICE_ERROR Fail to get the identify namespace data.

**/
EFI_STATUS
NvmeIdentifyNamespace (
  IN NVME_CONTROLLER_PRIVATE_DATA      *Private,
  IN UINT32                            NamespaceId,
  IN VOID                              *Buffer
  );

// MS_CHANGE_165952
// defines used for NVMe shutdown
#define NVME_CC_SHN_NORMAL_SHUTDOWN 1
#define NVME_CC_SHN_ABRUPT_SHUTDOWN 2

#define NVME_CSTS_SHST_SHUTDOWN_IN_PROCESS 1
#define NVME_CSTS_SHST_SHUTDOWN_COMPLETED  2

#define NVME_SHUTDOWN_TIMEOUT 45

/**
This routine is called to properly shutdown the Nvm Express controller per NVMe spec.

@param  Private         Supplies a pointer to the NVME_CONTROLLER_PRIVATE_DATA data structure.
@param  Normal          Supplies a boolean that indicates if this is a normal or an abrupt shutdown.

@return EFI_SUCCESS     Successfully enable the controller.
@return EFI_TIMEOUT     Fail to enable the controller in given time slot.

**/
EFI_STATUS
NvmeShutdownController(
  IN NVME_CONTROLLER_PRIVATE_DATA *Private,
  IN BOOLEAN Normal
);
//MS_CHANGE - END

#endif

