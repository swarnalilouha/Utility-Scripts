#!/bin/perl

## Enter name of directory containing files from standard input
print "Enter directory name contaning raw Miseq and Nextseq files\n";
chop($input_directory=<STDIN>);

## open the input directory and read files into an array @file_list
opendir(DIR1,$input_directory);

@file_list=readdir(DIR1);

##count the number of files present in the directory
$count= scalar(grep {defined $_} @file_list), "\n";

##Take only files starting with "NS/MS" from the directory into array @files. This step is to remove the hidden files in the directory
for(my $i=0;$i<=$count;$i++)
{

        if($file_list[$i] =~ m/^(NS|MS)_*/)
        {
                push(@files, $file_list[$i]);
        }
}

## enter name of output directory from standard input and create it
print "Enter directory name for concatenated  R1 and R2 reads\n";
$output_directory=<STDIN>;
system("mkdir $output_directory");

## Take sample name for nextseq files and store in array @sample
open(FILE,<@ARGV[0]>);
@sample=<FILE>;
foreach $k (@sample)
{
	chop($k);
}

## Loop that differentiates filenames based on miseq, nextseq(and its reads R1 and R2) and stores in different arrays
foreach(@files)
{
	if($_ =~ m/^MS*/)
	{
		system("cp $input_directory/$_  $output_directory");
	}
	elsif($_ =~ m/^NS_.*R1.*/)
	{
		push(@array1,$_);	
	}
	elsif($_ =~ m/^NS_.*R2.*/)
	{
		push(@array2,$_);
	}	

}

##count the number of elements in both the arrays created in above loop
$num1=@array1;
$num2=@array2;

##Loop for concatenating R1 reads in a single file and moving the file to output directory
for(my $a=0;$a<=($num1/4)-1;$a++)
{
	foreach(@array1)
	{
		if($_ =~ m/^NS_$sample[$a]_.*/)
		{
			#print "$_\n";
			#system("cat ./$input_directory/$_ |head -2");
			system("cat ./$input_directory/$_ >> NS_$sample[$a]_R1.fq");
		}
		
	}
	system(" mv  NS_$sample[$a]_R1.fq  ./$output_directory");
}

##Loop for concatenating R2 reads together in a single file and moving the file to output directory
for(my $b=0;$b<=($num2/4)-1;$b++)
{
	foreach(@array2)
	{
		if($_ =~ m/^NS_$sample[$b]_.*/)
		{
			system("cat ./$input_directory/$_ >> NS_$sample[$b]_R2.fq");
		}
	}
	system(" mv NS_$sample[$b]_R2.fq  ./$output_directory"); 
}

##-------------------------------------------------------------------------------------------------------------------------

### open the output directory and read files into an array @file_list
chop($output_directory);
opendir(DIR2,$output_directory);
@concat_files=readdir(DIR2);

##count the number of files present in the directory
$count= scalar(grep {defined $_} @concat_files), "\n";

##Take only files starting with "NS/MS" from the OUTPUT directory into array @concatenated_files. This step is to remove the hidden
## files in the directory
for(my $i=0;$i<=$count;$i++)
{

        if($concat_files[$i] =~ m/^(NS|MS)_*/)
        {
                push(@concatenated_files, $concat_files[$i]);
        }
}

## Change to output directory to open the files in it and count number of reads present in each file(while loop inside foreach loop)
## Also split truseq barcodes and quality trim the concatenated files (if and elsif loop inside the foreach loop)
chdir "./$output_directory" or die;

##Make directory for storing barcode splitted files and their concatenated output
print "Enter name of directory for storing barcode splitted final output\n";
chop($a=<STDIN>);
system("mkdir ./../$a");

##Make a directory for storing final quality trimmed files
print "Enter directory for storing final quality trimmed files\n";
chop($b=<STDIN>);
system("mkdir ./../$b");

## Make a directory to store fastqc results 
print "Enter directory name to output FASTQC results\n";
chop($fastqc_directory=<STDIN>);
system("mkdir  ./../$fastqc_directory");

$x=0;
foreach(@concatenated_files)
{
        $file=$_;

	open(FILE1,$file);
        while(<FILE1>)
        {
                $line=$_ ;
                chop($line);
                if($line =~ m/^@.*/)
                {
                        $x=$x+1;
                }
        }
                open(FILE2,'>>excel_sheet');
                print FILE2 "$file	$x\n";

	if($file =~ m/.*_R1.*/)
        {
                system("cat $file |fastx_barcode_splitter.pl --bcfile ./../Truread1.txt --eol --prefix ./../$a/$file");
                system("cat ./../$a/*Truread1  ./../$a/*unmatched > ./../$a/$file.concatenated");
                system("fastq_quality_trimmer -Q33 -t20 -i ./../$a/$file.concatenated  -o ./../$b/$file ");
        }
        elsif($file =~ m/.*_R2.*/)
        {
                system("cat $file |fastx_barcode_splitter.pl --bcfile ./../Truread2.txt --eol --prefix ./../$a/$file");
                system("cat ./../$a/*Truread2  ./../$a/*unmatched > ./../$a/$file.concatenated");
                system("fastq_quality_trimmer -Q33 -t20 -i ./../$a/$file.concatenated  -o ./../$b/$file ");
        }

}

system("mv excel_sheet ./../");

## Use fastqc to generate quality reports on each file in the output directory
system("fastqc *.*");
system("mv *.zip ./../$fastqc_directory");
system("mv *.html ./../$fastqc_directory");






