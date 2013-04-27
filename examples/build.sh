#!/bin/sh
#
# This creates a drag and drop Mac OS X app using Platypus.
#
# Platypus is available here: http://sveinbjorn.org/platypus
# You will need to go into the prefs and install the command line version.
#

os_ver=`sw_vers -productVersion | cut -c 1-4`
if [ $os_ver = '10.8' ]
then
   platypus  -P Picture\ Dump\ 10.8.platypus  -y Picture\ Dump\ 10.8.app
else
   platypus  -P Picture\ Dump\ 10.6.platypus  -y Picture\ Dump\ 10.6.app
fi
