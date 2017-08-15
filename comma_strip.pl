#!/usr/local/perl5/bin/perl


########################################################################
# File      :  comma_strip.pl
# History   :  06/17/11(brownw): Initial header.
########################################################################
# This module will take a csv file, locate each data element in that
# csv file and output each data element into a .mod file corrctly 
# formatted with tilde(~) delimiters between each field. 
# The best part of this script is even if commas exist in the text of a
# data element it can figure it out and retains the commas in the 
#data elements.
########################################################################
use strict;
use Text::ParseWords;
use File::Copy;
my $provider_file = $ARGV[0];
my $tempfile = "$provider_file.mod";
my $line  = '';
my $line2  = '';
my @new = ();
print "comma_strip begin\n";
open (CSV, "<$provider_file") or die $!;
open (OUT, ">$tempfile ") or die $!;
while (<CSV>)
{
    $line = $_;
    chomp($line);
    @new = ();
    push(@new, $+)
    while $line =~ m{"([^\"\\]*(?:\\.[^\"\\]*)*)",?
    | ([^,]+),?| ,}gx;
    print OUT join("~",@new) . "\n"; 

}
close (CSV);
close (OUT);
print "comma_strip done\n";
exit;