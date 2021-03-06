### Prerequisites

This project uses Pipenv to manage project dependencies. See the [Pipenv docs][pipenv] for usage info.

[pipenv]: https://docs.pipenv.org/

### Example Usage

```
Enter a search term: TMPRSS2
2 results found.
1. TMPRSS2 - transmembrane protease, serine 2, transcript variant 1
2. TMPRSS2 - transmembrane protease, serine 2, transcript variant 2
Please select a result: 1
Gene data:

name: uc010gor.4
chrom: chr21
strand: -
txStart: 41464552
txEnd: 41508065
cdsStart: 41466141
cdsEnd: 41508004
exonCount: 14
exonStarts: b'41464552,41467733,41468395,41470647,41471805,41473324,41476576,41479171,41
480475,41488393,41489506,41494355,41498118,41507949,'
exonEnds: b'41466153,41467886,41468538,41470743,41471981,41473496,41476620,41479282,4148
0602,41488513,41489593,41494578,41498189,41508065,'
proteinID: O15393
alignID: ENST00000398585.7

Downloading sequence data...
Finished. Sequence data:

ACTTTGAAAAAAAAATTGCATAATTTATTTGCATGATATTCATTTTCACAATTGAACTTTACAGTTTAAAAAAGATACAAAAAAAGAC
AAACAGTTGTTCACATAAATAAGAAGGGGCAATAAAGAAGGAAGACGTTTTCACCATTACAACACCTTTTAGGATGTGTCTTGGGGAG
CAAGCACCTTACAGTGCCAACTGTTTCCAAGGTCCCTGGGAATGCTGCTCTCTACAGAGGCATGTGCACAGACAGATCCTGCAAATGG
GATTGCATGACTTTCCATTTCAAGGTTAAGTCCTAGCTGTAGAATCATTCATTTCATTCTTGCAAACCAGCCTGCTTGGCCAGGAGGC
AGAACCATGGTAGAGTAGTGCTCATGGTTATGGCACTTGGCAATGCAAAAGGGACCCTTCCCCTGGTTGGAAACCCACAGCATTGGAA
# ...
```
