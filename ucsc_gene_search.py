import os
import sys
import gzip
import urllib.request

from pathlib import Path

from pymysql import connect
from pymysql.cursors import DictCursor
from pyfaidx import Fasta


CHROMOSOME_DATA_URL = "ftp://hgdownload.soe.ucsc.edu/goldenPath/hg38/chromosomes/{}.fa.gz"
CHROMOSOME_DATA_DIR = "chromosome_data"
CHROMOSOME_DATA_FILE = "{}.fa"

GENE_BY_ID_SQL = "SELECT * FROM knownGene WHERE name = '{}'"

GENE_SEARCH_SQL = ("SELECT ncbiRefSeqLink.name, ncbiRefSeqLink.product, kgAlias.kgID "
                   "FROM ncbiRefSeqLink "
                   "JOIN kgAlias "
                   "ON SUBSTRING(ncbiRefSeqLink.id, 1, LENGTH(ncbiRefSeqLink.id) - 2) = kgAlias.alias "
                   "WHERE ncbiRefSeqLink.name LIKE '{}'")


connection = connect(host='genome-mysql.soe.ucsc.edu',
                     user='genome',
                     port=3306,
                     db='hg38',
                     cursorclass=DictCursor)


def get_search_results(search_term):
    with connection.cursor() as cursor:
        cursor.execute(GENE_SEARCH_SQL.format(search_term))
        results = cursor.fetchmany(5)

        return results


def get_search_result_selection(results):
    if len(results) == 1:
        print("One result found.")

        return results[0]

    print("{} results found.".format(len(results)))

    for i, result in enumerate(results):
        print("{}. {} - {}".format(i + 1, result['name'], result['product']))

    selection_index = int(input("Please select a result: ")) - 1
    selection = results[selection_index]

    return selection


def get_gene_data(known_gene_id):
    with connection.cursor() as cursor:
        cursor.execute(GENE_BY_ID_SQL.format(known_gene_id))
        gene_data = cursor.fetchone()

        return gene_data


def path_for_chromosome_data(chromosome_key):
    return Path(CHROMOSOME_DATA_DIR + "/" + CHROMOSOME_DATA_FILE.format(chromosome_key))


def url_for_chromosome_data(chromosome_key):
    return CHROMOSOME_DATA_URL.format(chromosome_key)


def get_chromosome_data(chromosome_key):
    out_path = path_for_chromosome_data(chromosome_key)

    if out_path.exists():
        # Data has already been downloaded
        return

    # Download FASTA file from UCSC Genome FTP server
    response = urllib.request.urlopen(url_for_chromosome_data(chromosome_key))

    # Make the data directory if it doesn't already exist
    os.makedirs(CHROMOSOME_DATA_DIR, exist_ok=True)

    # Decompress the FASTA file into the data directory
    with open(out_path, 'wb') as out_file:
        out_file.write(gzip.decompress(response.read()))


def extract_chromosome_data(chromosome_key, start, end):
    data_path = path_for_chromosome_data(chromosome_key)

    if not data_path.exists():
        raise Exception("Chromosome data not downloaded")

    all_data = Fasta(str(data_path))
    sliced_data = all_data[chromosome_key][start:end].seq

    return sliced_data


if __name__ == '__main__':
    try:
        search_term = input("Enter a search term: ")
        search_results = get_search_results(search_term)

        if len(search_results) == 0:
            print("No results found")
            sys.exit(0)

        selection = get_search_result_selection(search_results)
        gene_data = get_gene_data(selection['kgID'])

        print("Gene data:\n")

        for k, v in gene_data.items():
            print("{}: {}".format(k, v))

        print("\nDownloading sequence data...")

        get_chromosome_data(gene_data['chrom'])

        print("Finished. Sequence data:\n")
        print(extract_chromosome_data(gene_data['chrom'], gene_data['txStart'], gene_data['txEnd']))
    finally:
        connection.close()
