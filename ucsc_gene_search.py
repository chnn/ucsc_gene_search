import sys

from pymysql import connect
from pymysql.cursors import DictCursor

connection = connect(host='genome-mysql.soe.ucsc.edu',
                     user='genome',
                     port=3306,
                     db='hg38',
                     cursorclass=DictCursor)


def get_search_results(search_term):
    with connection.cursor() as cursor:
        query = ("SELECT ncbiRefSeqLink.name, ncbiRefSeqLink.product, kgAlias.kgID "
                 "FROM ncbiRefSeqLink "
                 "JOIN kgAlias "
                 "ON SUBSTRING(ncbiRefSeqLink.id, 1, LENGTH(ncbiRefSeqLink.id) - 2) = kgAlias.alias "
                 "WHERE ncbiRefSeqLink.name LIKE '{}'")

        cursor.execute(query.format(search_term))
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


def get_gene_data(selection):
    with connection.cursor() as cursor:
        query = "SELECT * FROM knownGene WHERE name = '{}'"

        cursor.execute(query.format(selection['kgID']))
        gene_data = cursor.fetchone()

        return gene_data


if __name__ == '__main__':
    try:
        search_term = input("Enter a search term: ")
        search_results = get_search_results(search_term)

        if len(search_results) == 0:
            print("No results found")
            sys.exit(0)

        selection = get_search_result_selection(search_results)
        gene_data = get_gene_data(selection)

        for k, v in gene_data.items():
            print("{}: {}".format(k, v))
    finally:
        connection.close()
