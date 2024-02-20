#!/bin/bash -l

#SBATCH -A snic2022-22-849
#SBATCH -p core
#SBATCH -n 10
#SBATCH -t 100:00:00
#SBATCH --output=Phatogenx0822.out

dir=/proj/snic2021-23-534/nobackup/nobackup/RNAseq
###############
module load bioinfo-tools
module load cutadapt/4.0
module load FastQC/0.11.9
module load MultiQC/1.12
module load star/2.7.2b
module load bowtie2/2.3.5.1
module load samtools/1.14
module load QualiMap/2.2.1
module load subread

cutadapt -q 10 -a AGATCGGAAGAGCACACGTCTGAACTCCAGTCA -A AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGT --cores=10 -o $dir/Pathogenex_Sal/demultiplexed/trimmedA_R1.fastq -p $dir/Pathogenex_Sal/demultiplexed/trimmedA_R2.fastq $dir/Pathogenex_Sal/P13116_1005_S5_L001_R1_001.fastq.gz /$dir/Pathogenex_Sal/P13116_1005_S5_L001_R2_001.fastq.gz

cutadapt --cores=10 -e 1.5 --no-indels -g file:$dir/barcodes/Phatogenex.fasta --pair-filter=any --minimum-length=15 -o $dir/Pathogenex_Sal/demultiplexed/trimmed-{name}.1.fastq -p $dir/Pathogenex_Sal/demultiplexed/trimmed-{name}.2.fastq $dir/Pathogenex_Sal/demultiplexed/trimmedA_R1.fastq $dir/Pathogenex_Sal/demultiplexed/trimmedA_R2.fastq

echo "finished-cutadapt_for_all"

fastqc --threads 10 -o $dir/Pathogenex_Sal/fastqres/1st_run $dir/Pathogenex_Sal/demultiplexed/trimmed-*.fastq
multiqc -o $dir/Pathogenex_Sal/fastqres/barcods_multiqc -n multiqc_report_1st_run $dir/Pathogenex_Sal/fastqres/1st_run

FILES=$dir/Pathogenex_Sal/demultiplexed/trimmed-*.1.fastq
for szamlalo in $FILES
do
i=$(($i+1))
read1="$(find $dir/Pathogenex_Sal/demultiplexed/ -name '*.1.fastq' -printf "%f\n" | sort | sed -n "$i"p)"
read2="$(find $dir/Pathogenex_Sal/demultiplexed/ -name '*.1.fastq' -printf "%f\n" | sort | sed -n "$i"p | awk '{gsub(".1.fastq", ".2.fastq", $0); print}')"
outprefix="$(find $dir/Pathogenex_Sal/demultiplexed/ -name '*.1.fastq' -printf "%f\n" | sort | sed -n "$i"p | awk '{gsub(".1.fastq", ".", $0); print}')"

##### Running STAR
star --runThreadN 10 \
     --genomeDir $dir/index_mice_primary \
     --readFilesIn $dir/Pathogenex_Sal/demultiplexed/$read1 $dir/Pathogenex_Sal/demultiplexed/$read2 \
     --outSAMtype BAM SortedByCoordinate \
     --outFileNamePrefix $dir/star/Patogenex/$outprefix \
     --outReadsUnmapped Fastx \
     #--outSAMtype BAM Unsorted

cp $dir/star/Patogenex/${outprefix}Unmapped.out.mate1 $dir/star/Patogenex/${outprefix}unmapped-1.fq
cp $dir/star/Patogenex/${outprefix}Unmapped.out.mate2 $dir/star/Patogenex/${outprefix}unmapped-2.fq

##### Running Bt2
bowtie2 -x $dir/bowtie2/index_salm/sl1344 \
        -p 10 \
        -1 $dir/star/Patogenex/${outprefix}unmapped-1.fq \
        -2 $dir/star/Patogenex/${outprefix}unmapped-2.fq \
        -S $dir/star/Patogenex-sam/${outprefix}sam \

done
echo "finished-star"
#### Running samtools
FILES=$dir/star/Patogenex-sam/*.sam
for fajl in $FILES
do

noext=${fajl%.sam}
minta=${noext#$dir/star/Patogenex-sam/}

samtools view -Sb $fajl > $dir/bowtie2/Patogenex_CC-bam/$minta.bam
samtools sort -@ 10 -m 4G $dir/bowtie2/Patogenex_CC-bam/$minta.bam -o $dir/bowtie2/Patogenex_CC-bam/$minta.sorted.bam
samtools index $dir/bowtie2/Patogenex_CC-bam/$minta.sorted.bam

echo "sam converted to bam"

qualimap bamqc -nt 10 -bam $dir/bowtie2/Patogenex_CC-bam/$minta.sorted.bam --java-mem-size=4G -gff $dir/bowtie2/ref_salm_all/SL1344-all0104.gtf -outdir $dir/Pathogenex_Sal/qualimap/$minta.report

echo "qualimap done"

featureCounts -T 10 -p -a $dir/bowtie2/ref_salm_all/SL1344-all0104.gtf -t CDS -g gene_id -o $dir/Pathogenex_Sal/fc/$minta.txt $dir/bowtie2/Patogenex_CC-bam/$minta.sorted.bam

echo "featureCounts done"
done

exit
