#!/bin/bash

wget https://releases.linaro.org/components/toolchain/binaries/7.2-2017.11/aarch64-linux-gnu/gcc-linaro-7.2.1-2017.11-x86_64_aarch64-linux-gnu.tar.xz
tar -xf gcc-linaro-7.2.1-2017.11-x86_64_aarch64-linux-gnu.tar.xz gcc-linaro-7.2.1-2017.11-x86_64_aarch64-linux-gnu/
export GCC5_BIN=$PWD/gcc-linaro-7.2.1-2017.11-x86_64_aarch64-linux-gnu/bin/
# sudo apt install python3-pip g++ gcc python3 uuid-dev make mono-devel   how do i sudo?