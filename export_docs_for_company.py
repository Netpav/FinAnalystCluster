import datetime
import os
import sys
import re
import json
import argparse
import codecs

import mysql.connector

reload(sys)
sys.setdefaultencoding('utf8')


def _create_sql_query(company_id, doc_type, date_from, date_to):
    if doc_type == 'article':
        return """
           SELECT DATE(published_date) AS pub_date, text
           FROM article
           WHERE company_id={cid} AND published_date BETWEEN '{dfrom}' AND '{dto}'
           ORDER BY published_date ASC
           """.format(cid=company_id, dfrom=date_from, dto=date_to)
    elif doc_type == 'tw_status':
        return """
            SELECT DATE(created_at) AS pub_date, text
            FROM tw_status
            WHERE company_id={cid} AND created_at BETWEEN '{dfrom}' AND '{dto}'
            ORDER BY tw_id ASC
            """.format(doc_type=doc_type, cid=company_id, dfrom=date_from, dto=date_to)
    elif doc_type in ['fb_comment', 'fb_post']:
        return """
            SELECT created_timestamp, text
            FROM {dtype}
            WHERE company_id={cid} AND
            created_timestamp BETWEEN
                UNIX_TIMESTAMP('{dfrom}') AND
                UNIX_TIMESTAMP('{dto}')
            ORDER BY created_timestamp ASC
        """.format(dtype=doc_type, cid=company_id, dfrom=date_from, dto=date_to)


def load_docs_and_write_file(company_id, doc_type, date_from='1980-01-01', date_to='2030-01-01', output_dir=None):
    """
    Load documents from database based on company id and document type and write them to text file.

    :param company_id:
    :param doc_type: in fact it is table name: article, fb_comment, fb_post, tw_status
    :param date_from: in YYYY-MM-DD format, defaults to 1980
    :param date_to: in YYYY-MM-DD format, defaults to 2030
    :param output_dir:
    :return:
    """
    print('From {0} to {1}'.format(date_from, date_to))

    # Prepare output file
    if not output_dir:
        output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'docs_output')
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    out_filename = '{0}-{1}-docs.txt'.format(company_id, doc_type)
    out_filepath = os.path.join(output_dir, out_filename)
    print('Writing to file {0} in dir {1}'.format(out_filename, out_filepath))

    # Connect to DB and get documents
    cfg_filepath = os.path.join(os.path.dirname(sys.argv[0]), 'db_config.json')
    config = json.load(open(cfg_filepath))['prod_v1']
    dbcon = mysql.connector.connect(**config)
    sql_query = _create_sql_query(company_id, doc_type, date_from, date_to)
    print(sql_query)
    cursor = dbcon.cursor(dictionary=True)
    cursor.execute(sql_query)

    # Write docs to file
    count = 0
    with codecs.open(out_filepath, mode='w', encoding="utf-8") as fh:
        for doc in cursor:
            count += 1
            if doc_type in ['fb_comment', 'fb_post']:
                text = ' '.join(doc['text'].strip().split())
                pub_date = datetime.datetime.utcfromtimestamp(doc['created_timestamp']).strftime('%Y-%m-%d')
            else:
                text = re.sub(r'<p>|</p>', '', doc['text'])
                pub_date = doc['pub_date']
            write_string = '{0}\t{1}\t{2}\n'.format(company_id, pub_date, text)
            fh.write(write_string)
    print('Total documents: {0}'.format(count))


if __name__ == "__main__":
    # Define arguments
    parser = argparse.ArgumentParser(description="For given company ID and document type, export documents from DB to text file.",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--company_id', type=int, help='Company ID (i.e. 48 for AT&T')
    parser.add_argument('--doc_type', help='article, fb_comment, fb_post, tw_status')
    parser.add_argument('--date_from', help='Format: yyyy-mm-dd. Default is no restriction.', default='1980-01-01')
    parser.add_argument('--date_to', help='Format: yyyy-mm-dd. Default is no restriction.', default='2030-01-01')
    parser.add_argument('--output_dir', help='Path to output directory. Defaults to "docs_output" directory in place the script is run.', default=None)
    # Get arguments
    args = parser.parse_args()
    if args.company_id is None or args.doc_type is None:
        print('You must enter company ID and document type.')
        parser.print_help()
        exit(1)
    # RUN IT!
    print('>>>>Exporting documents of type {0} for company {1}'.format(args.doc_type, args.company_id))
    load_docs_and_write_file(args.company_id, args.doc_type, args.date_from, args.date_to, args.output_dir)
