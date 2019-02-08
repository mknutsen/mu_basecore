# SMI Handler Audit

The purpose of the SMI handler audit test is to verify that the SMI handler attack surface has not changed from build to build (usually via external integration). This attack surface must undergo a manual code review, so any changes must be caught ASAP.

## Overview

1. The SMM core dispatch code (and any child dispatchers) are modified to add all handler registrations to a common database.
2. In debug mode, a special handler is registered that will allow a particular SW SMI to query the contents of the database.
3. A UEFI application (SmiHandlerProfileAuditTestApp) can be run from Shell which will trigger the SW SMI and format the database contents in an XML file for further review.
4. This XMl file should be compared against a "golden copy" associated with each platform (may change to common in the future). This file should be already reviewed for its contents and the SMI handlers are trusted.

## Audit Checks

The following elements should be compared between the "golden copy" and the new test copy.

1. Number and names of all SMM drivers loaded and dispatched by the SMM core dispatcher.
2. Number and originating module for all SMI handlers registered with the SMM core dispatcher and any "enlightened" child dispatchers.

## Usage / Enabling on UDK based system

1. Add the following entry to platform dsc file;
```
[PcdsFixedAtBuild]
  gEfiMdeModulePkgTokenSpaceGuid.PcdSmiHandlerProfilePropertyMask|0x01

[Components.X64]
  MdeModulePkg/Application/SmiHandlerProfileInfo/SmiHandlerProfileInfo.inf
```
2. Build your platform UEFI and flash the binary;
3. Copy the built app (SmiHandlerProfileInfo.efi) to a flash drive;
4. Boot the target system to UEFI Shell and run the following (assuming the USB disk is FS0:\):
```
> fs0:
> SmiHandlerProfileInfo.efi > your_name.xml
```
5. If the application runs correctly, there should be a `your_name.xml` file created on your flash drive. Compare this file against your golden copy;

## Creating the Golden Copy

Generally, don't. You can start with a known-good copy from another platform, but if any of the tests fail you must get the platform reviewed by the MS Core UEFI team prior to adopting a new "golden copy" for your platform. These "golden copies" don't just represent acceptable configurations, they were created upon meticulous security analysis of the SMI handlers that are declared within.

## Updating the Golden Copy

Same as above: don't. If this test fails on your platform, you must work with the MS Core UEFI team to determine whether your platform needs merely a new "golden copy" or whether further, in-depth analysis is necessary.

## Copyright

Copyright (c) 2019, Microsoft Corporation

All rights reserved. Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
