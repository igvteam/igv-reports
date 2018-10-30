## finspector.fusion_inspector_web.json
This file contains a list of fusions and it's metadata. Here is an example with definitions:
```
{
 "cytoband": "cytoBand.txt", #IGV uses this file to draw the chromosome ideograms for the genome.  
 "fusions":[  
   {  
      "Fusion": "THRA--AC090627.1", # name of the fusion as geneA--geneB  
      "Junction Reads": "33", # number of split RNA-Seq reads that map and define the fusion breakpoint.  
      "Left Chr": "chr17", # Chr for for the left fusion  
      "Left Gene": "THRA^ENSG00000126351.8", # identifier of the gene represented by the left section of the fusion transcript.  
      "Left Pos": "38243106", # position of the left fusion breakpoint in the context of the genome.  
      "Left Strand": "+", # Strand pos  
      "Right Chr": "chr17", # Chr for for the right fusion  
      "Right Gene": "AC090627.1^ENSG00000235300.3", # identifier of the gene represented by the right section of the fusion transcript.  
      "Right Pos": "46371709", # position of the right fusion breakpoint in the context of the genome.  
      "Right Strand": "+", # Strand pos  
      "Spanning Fragments": "92", # number of paired-end reads that span the fusion breakpoint but the reads do not directly overlap the breakpoint.  
      "Splice Type": "DOES NOT Include Reference" # SpliceType: category of support at the fusion breakpoint: 
                                                  # {ONLY_REF_SPLICE: fusion breakpoint occurs at reference (known) splice junctions.
                                                  # INCL_NON_REF_SPLICE: fusion breakpoint occurs at a breakpoint that does not involve all reference (known) exon junctions. 
                                                  # NO_JUNCTION_READS_IDENTIFIED: only spanning fragments support the fusion. (can only happen if --min_junction_reads is set to zero).}  
    },  
    {..},  
    {..}],    
  "junctionReads": "finspector.junction_reads.bam.bed.sorted.bed.gz", # BED file with junction reads  
  "junctionReadsBai": "finspector.junction_reads.bam.bai", # alignments of the breakpoint-junction supporting reads (indexed).  
  "junctionReadsBam": "finspector.junction_reads.bam", # alignments of the breakpoint-junction supporting reads.  
  "junctionSpanning": "finspector.igv.FusionJuncSpan", # scaffolds with spanning_frag_coords  
  "reference": "finspector.fa", # the candidate fusion-gene contigs.   
  "referenceBed": "finspector.bed", # the reference gene structure annotations for fusion partners.  
  "referenceIndex": "finspector.fa.fai", # the candidate fusion-gene contigs (indexed).  
  "spanningReads": "finspector.spanning_reads.bam.bed.sorted.bed.gz", # BED file with breakpoint-spanning reads  
  "spanningReadsBai": "finspector.spanning_reads.bam.bai", # alignments of the breakpoint-spanning paired-end reads (indexed).  
  "spanningReadsBam": "finspector.spanning_reads.bam", # alignments of the breakpoint-spanning paired-end reads.  
  "trinityBed": "finspector.gmap_trinity_GG.fusions.gff3.bed.sorted.bed" # fusion-guided Trinity assembly (Optional)  
}
```
