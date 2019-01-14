#!/bin/bash

wget https://dl.bintray.com/boostorg/release/1.68.0/source/boost_1_68_0.tar.gz
tar -xzf boost_1_68_0.tar.gz
cd boost_1_68_0
./bootstrap.sh
./b2
sudo ./b2 install
