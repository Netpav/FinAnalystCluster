import glob
import os
import  sys
import subprocess
import export_docs_for_company


from src.FinAnalV2.AnalPipeline import docs_to_vectors_bulk,scikit_anal_bulk,balance_files
# from src.FinanceAnalyzer
companies = [1,2,3,4,5,6,7,8,9,10] # range(10)
clusters =[2,3,4,5,6,7,8,9,10]
for company in companies:
    export_docs_for_company.py + '--company_id' + company + '--doc_type' + 'article' + '--date_from'+ '2016-01-01' + '--date_to'+ '2016-06-30' + '--output_dir' +' ~/inputs'

for name in glob.glob('/inputs/*'):
    print "\n *********** \n"
    print name
    print "\n *********** \n"
    subprocess.call("", shell=True)
    docs_to_vectors_bulk.py + name + 'data.cluto.sparse'
    for cluster in clusters:
        subprocess.call('~/cluto-2.1.2/Linux-x86_64/vcluster -crfun=h1 -clmethod=direct ~/data.cluto.sparse'+cluster, shell=True)
    subprocess.call("sed -i -e 's/0/2/g' data.cluto.sparse" +cluster, shell=True)
    subprocess.call("cut -f1,2 -d, %s original.txt > dates; paste %s.sparse.clustering.%s dates > %s.classes.txt" %(name,name,cluster,name), shell=True)
    docs_to_vectors_bulk.py + name+ 'file_arff'
    scikit_anal_bulk.py + 'file_arff'



