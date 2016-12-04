###########
# Imports
###########
import os
import subprocess

###########
# Parameter definitions
###########

# Set file paths
input_dir = os.path.abspath('inputs')
results_dir = os.path.abspath('results')
temp_dir = os.path.abspath('temp')
vectext_dir = os.path.abspath('VecText')
cluto_path = os.path.abspath('cluto-2.1.2/Linux-x86_64/vcluster')
FNULL = open(os.devnull, 'w')
current_dir = os.path.dirname(os.path.abspath(__file__))

# Program params
default_vectext_params = '--input={input_file} --output_dir={output_dir} --output_file={output_file} --local_weights="Term Frequency (TF)" --output_format=cluto --min_word_length=3 --min_document_frequency=3 --output_original_texts --create_dictionary="with frequencies" --print_statistics --encoding=utf8'
default_cluto_params = '-crfun=h1 -clmethod=direct {input_file} {cluster_count}'

# Clustering params
cluster_counts = [2, 3, 4, 5, 6, 7, 8, 9, 10]

###########
# Functions
###########

def create_vectors_from_file(file_name, input_dir, output_dir):
    os.chdir(vectext_dir)     # change working directory to VecText
    file_path = os.path.join(input_dir, file_name)
    base_name = os.path.splitext(file_name)[0]
    real_vectext_params = default_vectext_params.format(input_file=file_path, output_dir=output_dir, output_file=base_name)
    run_cmd = 'perl vectext-cmdline.pl ' + real_vectext_params
    ret_code = subprocess.call(run_cmd, shell=True, stdout=FNULL, stderr=FNULL)
    print('return code: {0}'.format(ret_code))
    os.chdir(current_dir)

def cluster_vector_file(file_path, cluster_count, output_dir):
    os.chdir(output_dir)
    real_cluto_params = default_cluto_params.format(input_file=file_path, cluster_count=cluster_count)
    run_cmd = '{0} {1}'.format(cluto_path, real_cluto_params)
    ret_code = subprocess.call(run_cmd, shell=True, stdout=FNULL, stderr=FNULL)
    print('return code: {0}'.format(ret_code))
    os.chdir(current_dir)

###########
# Run it!
###########
if __name__ == "__main__":

    print('======Convert text files to vectors======')
    for file_name in sorted(os.listdir(input_dir)):
        if file_name.endswith('.text'):
            print('==={0}==='.format(file_name))
            create_vectors_from_file(file_name, input_dir, os.path.join(temp_dir, 'vectext_1'))

    print('======Run cluto on created vector files======')
    cluto_files_dir = os.path.join(temp_dir, 'vectext_1')
    for file_name in sorted(os.listdir(cluto_files_dir)):
        print('==={0}==='.format(file_name))
        file_path = os.path.join(cluto_files_dir, file_name)
        for cl_c in cluster_counts:
            cluster_vector_file(file_path, cl_c, os.path.join(temp_dir, 'cluto_1'))

    # Tohle asi neni potreba
    # print('======Replace class 0 with 2 in cluto files======')
    # files_dir = os.path.join(temp_dir, 'cluto_1')
    # for file_name in sorted(os.listdir(files_dir)):
    #     subprocess.call("sed -i -e 's/0/2/g' {0}".format(os.path.join(files_dir, file_name)), shell=True)

    print('======Join classes from clusters and articles======')
    cluto_files_dir = os.path.join(temp_dir, 'cluto_1')
    for cluto_file_name in sorted(os.listdir(cluto_files_dir)):
        print('==={0}==='.format(cluto_file_name))
        # Have no idea how this works :(
        # You must get all files from cluto_1/ and connect them with files from inputs/ and save the result to cluto_2/
        #run_cmd = "cut -f1,2 -d, %s original.txt > dates; paste %s.sparse.clustering.%s dates > %s.classes.txt" %(name,name,cluster,name)
        #subprocess.call(run_cmd, shell=True, stdout=FNULL, stderr=FNULL)

    print('======Convert text files with new classes to vectors======')
    files_dir = os.path.join(temp_dir, 'cluto_2')
    for file_name in sorted(os.listdir(files_dir)):
        print('==={0}==='.format(file_name))
        create_vectors_from_file(file_name, input_dir, os.path.join(temp_dir, 'vectext_2'))

    print('======Classify it, bitch!======')
    # just run: python libs/AnalPipeline/scikit_anal_bulk.py


