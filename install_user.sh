#!/bin/bash
#
# script to initially copy files to user direcotry ~/PhyPi/
#

USERDIR="PhyPi"  # user directory

# -----------------------------------------

DIR=$HOME/$USERDIR
echo "copying files to "$DIR

mkdir -p $DIR

if [ -d $DIR ]; then
  # enter here, if direcotry exists
#
    # copy documentation
  mkdir -p $DIR/doc
  cp -auv doc/*.pdf $DIR/doc/
  cp -auv README_de.pdf $DIR
#
    #copy python code
  cp -auv phypi.py $DIR
  cp -auv doc/*.html $DIR/doc/
  cp -auv images $DIR
  cp -auv run_phypi.py $DIR
#  
    #copy config examples
  cp -auv config/ $DIR
  cp -auv default.daq $DIR
  cp -auv PhyPiConf.daq $DIR
#
    # copy examples
  cp -auv examples/ $DIR
fi
