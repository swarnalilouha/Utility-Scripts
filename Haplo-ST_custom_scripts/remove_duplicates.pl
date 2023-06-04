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

foreach $file (@genes)
{
	system("cat ./blast_filter/$file  ./blast_duplicates/$file | sort -n |uniq -u > ./final_blast/$file");	
}
