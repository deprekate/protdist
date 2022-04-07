#!/usr/bin/perl
use Data::Dumper;

warn("'infile already present\n") if(-e 'infile');
warn("'outfile already present\n") if(-e 'outfile');

die("usage: ./protdist.pl INFILE.FASTA\n") unless(-f $ARGV[0]);

my $out = `clustalw -infile="$ARGV[0]" -output=gcg -matrix=BLOSUM -outfile=infile.pre -ktuple=2 2>&1`;
&fix_infile("infile.pre");

my %read_to_key = ();
open(TEMPFILE, ">", "infile") or die("cannot open 'infile'\n");
open(INFILE, $ARGV[0]) or die("cannot open INFILE.FASTA\n");
$_ = <INFILE>;
m/^(>\S+?)\s/;
my $id = $1;
my $i = 0;
$read_to_key{$id} = $i;
my $seq = '';
while(<INFILE>){
	if(m/^(>\S+?)\s/){
		print $read_to_key{$id};
		print " ";
		print $seq;
		print "\n";
		$i++;
		$read_to_key{$id} = $i;
		$seq = '';
	}else{
		chomp();
		$seq .= $_;
	}
}
print $read_to_key{$id};
print " ";
print $seq;
print "\n";
close(INFILE);
close(TEMPFILE);
#unlink "infile";

sub fix_infile{
	my $file = $_[0];
	my $seqs = `grep -c ' Name:' $file`;
	#my $len = `grep '   MSF:' $file | sed 's/.*MSF: *\([1-9]*\).*/\1/'`;
	print " ",$seqs," ",$len,"\n";
	my @seqs;
	open(INFILE,$file) or die();
	my $flag = 0;
	while(<INFILE>){
		if(m/^\//){
			$flag = 1;
			next;
		}elsif($flag and m/^[^\n]/){
		}
	}
	#print Dumper(@seqs);
}






		
		
		
