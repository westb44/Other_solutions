#!C:\perl

########################################################################
# History   :  06/17/11(brownw): Initial header.
########################################################################
########################################################################
use strict;
use Text::ParseWords;
use File::Copy;

print "do_stuff begin\n";
print "Do you want to import a list (Y/N)?"; # first question yes/no
my $input = <STDIN>;
chomp $input;
    if ($input =~ m/^[Y]$/i){ #match Y or y
        print "Give the name of the first list file:\n";
            }
exit;