#!/bin/sh
#
# Wrapper script for arcem which sets up a useful default environment for the
# user and ensures files are saved in a sensible location (.arcem), if the auto
# parameter is used. Otherwise it simply executes arcem verbatim passing it any
# parameters received.

arcembin='/usr/bin/arcem.bin';
arcemrc='/usr/share/arcem/arcemrc'
moddir='/usr/share/arcem/modules';
kdialog='/usr/bin/kdialog';
zenity='/usr/bin/zenity';
xmessage='/usr/bin/xmessage';
msg="This appears to be the first time you've launched ArcEm, so a default\
 environment has been configured for you. For ArcEm to fully function you\
 require either a 'RISC OS 3.XX' rom, or a freely available 'ARM Linux' rom.
The rom file should be called 'ROM' and installed into the following directory:

 $HOME/.arcem

 NOTE: By default ArcEm will be launched with the bundled 'ARM Linux' rom unless\
 a rom is installed in the above location.

 Please consult the documentation for further information"


# Check binary exists and is executable
if [ ! -x $arcembin ] ; then
    echo "error: $arcembin missing or not executable" 1>&2
    exit 1
fi

# If we are not in auto mode, run arcem verbatim, passing any parameters
if [ "$1" != "auto" ] ; then
    exec $arcembin "$@"
fi

# Check home exists and is a directory
if [ ! -d $HOME ] ; then
    echo "error: $HOME is missing or not a directory" 1>&2
    exit 2
fi

# Check if ~/.arcemrc exists and is a file. If not, make it.
if [ ! -f "$HOME/.arcemrc" ] ; then
    # Setup RC file
    install -pm0644 "$arcemrc" "$HOME/.arcemrc"
fi

# Check if ~/.arcem exists and is a directory. If not, make it and setup up
# the subsequent default environment. If .arcem already exists then no changes
# will be made. Notify the user of the default environment and the need for a
# ROM
if [ ! -d "$HOME/.arcem" ] ; then
    mkdir -p "$HOME/.arcem/extnrom"
    # Setup extention modules
    pushd "$HOME/.arcem/extnrom" > /dev/null
    ln -s "$moddir/"* .
    popd > /dev/null

    if [ -x $kdialog ] ; then
        $kdialog --title "First Run" --msgbox "$msg"
    elif [ -x $zenity ] ; then
        $zenity --title="First Run" --info --text="$msg"
    else
        echo -e $msg | fold -s --width=50 | $xmessage -center -file -
    fi

    # Output to console also
    echo -e $msg

fi

# Change to ~/.arcem to ensure files are loaded/saved there
cd "$HOME/.arcem"

# Launch arcem with the linux ROM if no user ROM
if [ -f "$HOME/.arcem/ROM" ] ; then
    exec padsp $arcembin --hostfsdir $HOME --memory 16M
else
    exec padsp $arcembin --hostfsdir $HOME --memory 16M --rom /usr/share/arcem/linuxrom/ROM
fi
