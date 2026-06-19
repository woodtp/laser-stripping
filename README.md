[![Build Status](https://travis-ci.org/PyORBIT-Collaboration/laser-stripping.svg?branch=master)](https://travis-ci.org/PyORBIT-Collaboration/laser-stripping)
# Laser stripping extension for PyORBIT3 code
Installation procedure requires building from source.
All installation steps happen in command line (terminal).

 ## 1. Build PyORBIT3 as described [here](https://github.com/PyORBIT-Collaboration/PyORBIT3)
 ## 2. Clone the source code
```shell
git clone https://github.com/PyORBIT-Collaboration/laser-stripping.git
```
Put the cloned repository somewhere outside of PyORBIT directory.
So your source is now in *laser-stripping* directory.

## 3. Build & Install

To compile with Meson

```shell
meson setup build --prefix=$CONDA_PREFIX # or your preferred path
meson compile -C build
meson install -C build
```

## 4. Running Examples

```shell
cd examples
python python3-1GeV-particle-stripping.py
```
This will launch *1GeV-particle-stripping.py* example on two MPI nodes. Other laser stripping related examples are availabale in [Examples](https://github.com/PyORBIT-Collaboration/examples/tree/master/ext/LaserStripping) repository.

## 5. Uninstalling

```shell
cd build
ninja uninstall
ninja clean
```
