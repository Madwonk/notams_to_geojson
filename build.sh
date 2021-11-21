#!/bin/bash

mkdir builddir
meson builddir/
ninja -C builddir/
sudo ninja -C builddir/ install
