#  ND2 SDK Wrappers

This project contains code for wrapping (i.e. code for translating between different interfaces) the official Nikon ND2 SDK for MATLAB and Python.

Currently the code works for the SDK version V9.00.

**Note: Do not use SDK v0.2Beta as it is currently broken**

## Installation

Development and testing is on Python (3.7.0) via Miniconda3 4.5.11 64-bit.

1. Clone the repository
  git clone git@gitlab.com:jwtay/nd2sdk-wrappers.git

2. Download the SDK files from www.nd2sdk.com. You might need to sign up. The SDK version required is v9.00, which appears to only be currently (March 2019) available for Windows and MAC.

3. Extract the SDK files. Copy the files from the directory matching your current platform and architecture from /bin to the python/lib folder.

## Usage

### Python

The code is currently being developed. You can run the test "test_nd2reader.py" to see if it works.

### MATLAB

TBD