#!/bin/perl

##Open "blast_matches" directory and read the genes files in an array named @genes
opendir(DIR2,"blast_matches");
@genes_files=readdir(DIR2);
closedir(DIR2);

$count_genes=scalar(grep {defined $_} @genes_files), "\n";
for($genes=0;$genes<=$count_genes;$genes++)
{
	if( $genes_files[$genes] =~ m/(^[0-9a-zA-Z].*)/ )
	{
		push(@genes,$genes_files[$genes]);
	}
}

chdir "blast_matches" or die;
foreach $file (@genes)
{
	open(FILE,"$file");
	my @array=<FILE>;
	my $numlines=@array;

	for($a=0;$a<=$numlines;$a++)
	{
		if( $array[$a] !~ m/^#/ )
		{

			chomp($array[$a]);
			my (@linearray) = split /\t/,$array[$a];

			my (@query_id) = split /\./,$linearray[0];
			my (@sub_id) = split /\./,$linearray[2];

			if ($query_id[0] eq $sub_id[0] && $query_id[1] ne $sub_id[1] && $linearray[8]==1 && $linearray[10]==1 && $linearray[1]==$linearray[9] && $linearray[3]==$linearray[11] && $linearray[5]==$linearray[11] && $linearray[5]==$linearray[9] && $linearray[6]==0 && $linearray[7]==0)
			{
				open(FILE3,">>../blast_filter/$file");
				#print FILE3 "$array[$a]\n"; 
				print FILE3 "$linearray[0]\t$linearray[2]\n"; 
			}
			@query_id = ();
			@sub_id = ();
			

		}	
	}
}
