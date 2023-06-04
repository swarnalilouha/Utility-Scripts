##Open "blast_filter" directory and read the genes files in an array named @genes
opendir(DIR2,"blast_filter");
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
#print @genes;
chdir "blast_filter" or die;
foreach $file (@genes)
{
	open(FILE,"$file");
	my @array=<FILE>;
	my $numlines=@array;

	for($a=0;$a<=$numlines;$a++)
	{
		@line_array1 = split /\t/,$array[$a];
		@line1sample1 = split /\./,$line_array1[0];
		@line1sample2 = split /\./,$line_array1[1];
		
		$x1 = $line1sample1[1]; 
		$y1 = $line1sample2[1]; 

		for ($b=($a+1);$b<=$numlines;$b++)
		{
			@line_array2 = split /\t/,$array[$b];
			@line2sample1 = split /\./,$line_array2[0];
			@line2sample2 = split /\./,$line_array2[1];
			
			my $x2 = $line2sample1[1];
			my $y2 = $line2sample2[1];
			
			if ($x2 eq $y1 && $y2 eq $x1)
			{
				open(FILE3,">>../blast_duplicates/$file");
				print FILE3 "$array[$a]"; 
			}
			
		}
	}
}
