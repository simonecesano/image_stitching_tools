use IPC::Run qw/run/;
use Mojo::File qw/path/;
use Mojo::Util qw/decode encode/;
use strict;

$\ = "\n"; $, = "\t"; binmode(STDOUT, ":utf8");

my ($stdin, $stdout, $stderr);

run ["osascript", "-e", "get the clipboard as «class PNGf»"], \$stdin, \$stdout, \$stderr;
$stdout = decode "UTF-8", $stdout; for ($stdout) { s/.+data PNGf//; s/.$//; $_ = pack('H*', $_) }

my $png = $stdout;
path("out.png")->spew($stdout);

run [qw/convert png:- -colorspace HSL -channel Lightness -separate -format %[fx:mean*100] info:/], \$png, \$stdout, \$stderr;

my $lum = $stdout;
$stdin = $png;

run ["convert", "png:-","ppm:-"], \$stdin, \my $ppm, \$stderr;
run ["tesseract", "--psm", "4", "-l", "eng", "stdin", "stdout"], \$ppm, \$stdout, \$stderr;
print $stdout;



# osascript -e "get the clipboard as «class PNGf»" | sed "s/«data PNGf//; s/»//" | xxd -r -p |convert png:- -negate ppm:- |tesseract --psm 4 -l eng stdin stdout 2>/dev/null |perl -lne "print if /\w/"
