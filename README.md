# borgnode
Simple BORG WebGUI

Ohh another borg gui..... How does it look ?

See the screenshots.

How to install it?

Use a virtuelenv with python3. Then inside those virtuelenv extract/copy the borgnode folder.

run.sh assumes it runs inside a virtualenv environment.

Install the requirements first.

This was developed and tested on mac. It needs some changes to work on a linux server. But this should just be the scripts (some of them use zsh)

FAQ:

What does it do ?

Lets you starts script on your linux/mac via webgui

What do i do with it?

In my example it will start a script with borgmatic commands to start a backup or list backups.

How is it configured ?

It used the borgmatic config and the script it starts to get some parameters.

Can i modify it ?

Sure you can make the script execute any commands you want.
