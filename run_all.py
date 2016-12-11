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
results_dir = os.path.abspath('temp/vectext_1')
temp_dir = os.path.abspath('temp')
vectext_dir = os.path.abspath('VecText')
cluto_path = os.path.abspath('cluto-2.1.2/Linux-x86_64/vcluster')
FNULL = open(os.devnull, 'w')
current_dir = os.path.dirname(os.path.abspath(__file__))
# Program params
default_vectext_params = '--input={input_file} --output_dir={output_dir} --output_file={output_file} --local_weights="Term Frequency (TF)" --output_format={output_format} --min_word_length=3 --min_document_frequency=3 --output_original_texts --create_dictionary="with frequencies" --print_statistics --encoding=utf8'
default_vectext_params_arff = '--input={input_file} --output_dir={output_dir} --output_file={output_file} --class_position=1 --local_weights="Term Frequency (TF)" --output_format={output_format} --min_word_length=3 --min_document_frequency=3 --output_original_texts --create_dictionary_freq --print_statistics --case="lower case" --output_decimal_places=3 --encoding=utf8'
# default_vectext_params_arff = '--input={input_file} --output_dir={output_dir} --output_file={output_file} --class_position=1 --local_weights="Term Frequency (TF)" --output_format={output_format} --min_word_length=3 --min_document_frequency=5 --output_original_texts --create_dictionary_freq --print_statistics --logarithm_type="natural" --output_original_texts --output_tokens --preserve_numbers --case="lower case" --preserve_emoticons --output_decimal_places=3 --sort_attributes=none --encoding=utf8'


default_cluto_params = '-crfun=h1 -clmethod=direct {input_file} {cluster_count} > {cluto_log}'


# Clustering params
cluster_counts = [2]

# cluto_log_file = [cluto_log_2, cluto_log_3]
###########
# Functions
###########

def create_vectors_from_file(file_name, input_dir, output_dir, output_format):
    os.chdir(vectext_dir)     # change working directory to VecText
    file_path = os.path.join(input_dir, file_name)
    base_name = os.path.splitext(file_name)[0]
    if output_format == '"CLUTO"':
        real_vectext_params = default_vectext_params.format(input_file=file_path, output_dir=output_dir, output_file=base_name, output_format=output_format)
    else:
        real_vectext_params = default_vectext_params_arff.format(input_file=file_path, output_dir=output_dir, output_file=base_name, output_format=output_format)
    run_cmd = 'perl vectext-cmdline.pl ' + real_vectext_params
    ret_code = subprocess.call(run_cmd, shell=True, stdout=FNULL, stderr=FNULL)
    print('return code: {0}'.format(ret_code))
    os.chdir(current_dir)

def cluster_vector_file(file_path, cluster_count, output_dir):
    os.chdir(output_dir)
    real_cluto_params = default_cluto_params.format(input_file=file_path, cluster_count=cluster_count, cluto_log='log_' + file_name +'.'+ str(cluster_count))
    run_cmd = '{0} {1}'.format(cluto_path, real_cluto_params)
    ret_code = subprocess.call(run_cmd, shell=True, stdout=FNULL, stderr=FNULL)
    print('return code cluto: {0}'.format(ret_code))

    os.chdir(current_dir)

###########
# Run it!
###########
if __name__ == "__main__":

    print('======Convert text files to vectors======')
    for file_name in sorted(os.listdir(input_dir)):
        if file_name.endswith('.txt'):
            print('==={0}==='.format(file_name))
            create_vectors_from_file(file_name, input_dir, os.path.join(temp_dir, 'vectext_1'),'"CLUTO"')

    print('======Run cluto on created vector files======')
    cluto_files_dir = os.path.join(temp_dir, 'vectext_1')
    for file_name in sorted(os.listdir(cluto_files_dir)):
        if file_name.endswith('.sparse'):
            print('==={0}==='.format(file_name))
            file_path = os.path.join(cluto_files_dir, file_name)
            for cl_c in cluster_counts:
                cluster_vector_file(file_path, cl_c, os.path.join(temp_dir, 'vectext_1'))



    # Tohle asi neni potreba
    # print('======Replace class 0 with 2 in cluto files======')
    # files_dir = os.path.join(temp_dir, 'cluto_1')
    # for file_name in sorted(os.listdir(files_dir)):
    #     subprocess.call("sed -i -e 's/0/2/g' {0}".format(os.path.join(files_dir, file_name)), shell=True)

    print('======Join classes from clusters and articles======')
    cluto_files_dir = os.path.join(temp_dir, 'vectext_1')
    for cluto_file_name in sorted(os.listdir(cluto_files_dir)):
        if cluto_file_name.endswith('.original.txt'):
            orig_file = cluto_file_name
        if cluto_file_name.endswith('.sparse.clustering.2'):
            sparse_file=cluto_file_name
        # print('==={0}==='.format(cluto_file_name))
    # Have no idea how this works :(
    # You must get all files from cluto_1/ and connect them with files from inputs/ and save the result to cluto_2/
    # if file_name.endswith('original.txt'):
    os.chdir(results_dir)
    run_cmd_sed = "sed -i -e 's/0/2/g' %s" %(sparse_file)
    ret_code_sed = subprocess.call(run_cmd_sed, shell=True, stdout=FNULL, stderr=FNULL)
    print('return code sed : {0}'.format(ret_code_sed))
    run_cmd_dos2unix = 'dos2unix %s| dos2unix %s ' %(orig_file,sparse_file)
    ret_code_dos2unix = subprocess.call(run_cmd_dos2unix, shell=True, stdout=FNULL, stderr=FNULL)
    print('return code: {0}'.format(ret_code_dos2unix))
    class_file = sparse_file+'.classes'
    run_cmd_cut = "cut -f 2-4  %s > dates; paste -d'\t' %s dates > %s" %(orig_file,sparse_file,class_file)
    # run_cmd_cut = "paste -d'\t' %s %s > 48_article.classes" %(sparse_file,orig_file)
    ret_code_cut = subprocess.call(run_cmd_cut, shell=True, stdout=FNULL, stderr=FNULL)
    print('return code: {0}'.format(ret_code_cut))

    # # run_cmd_sed = "sed -i -e 's/0/2/g' %s" %(class_file)
    # ret_code_sed = subprocess.call(run_cmd_sed, shell=True, stdout=FNULL, stderr=FNULL)
    # print('return code: {0}'.format(ret_code_sed))
    # os.chdir(current_dir)

    print('======Convert text files with new classes to vectors======')
    files_dir = os.path.join(temp_dir, 'vectext_1')

    for file_name in sorted(os.listdir(files_dir)):
        if file_name.endswith('.classes'):
            print('==={0}==='.format(file_name))
            create_vectors_from_file(file_name, files_dir, os.path.join(temp_dir, 'vectext_2'),'"ARFF"')

    print('======Classify it, bitch!======')
    # just run: python libs/AnalPipeline/scikit_anal_bulk.py


