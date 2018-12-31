#!/usr/bin/env perl
$r = sub {
    $M = shift();
    sub {
        $M = $M * 1103515245 + 12345 & 2147483647;
        $M % (shift());
    }
    ;
}
->(42);
@HASH = unpack('C*', "st\f\cR8vRHq\cEWSFb\cNlUe^\eKkoT\cZk-ru");
foreach $idx (0 .. 666) {
    $var1 = 20 + &$r(42) and print chr($HASH[$idx / 23] ^ $var1) unless $idx % 23;
}
print "\n";
