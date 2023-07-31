import os.path
import pickle
import shutil
import time

from lxml.etree import parse, tostring, fromstring

from someConstant import XMLPath, AssetsPath, TEMP
from wangyi_Ni import get_translated_text


def make_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def save_pickle(obj, fname):
    with open(fname, 'wb') as f:
        pickle.dump(obj, f)


def load_pickle(fname):
    with open(fname, 'rb') as f:
        obj = pickle.load(f)
    return obj


def parse_xml(path=XMLPath):
    # 判断文件是否存在
    if not os.path.exists(path):
        raise IOError('找不到指定文件' + path)

    # 创建文件夹
    curr_time = str(int(time.time()))
    dir_name = os.path.split(path)[-1].split('.')[0] + '_' + curr_time
    saved_dir_name = os.path.join(AssetsPath, dir_name)
    make_dir(saved_dir_name)

    # 将xml文件复制到该文件夹
    des_xml_path = os.path.join(saved_dir_name, os.path.split(path)[-1])
    shutil.copy(path, des_xml_path)

    # 解析xml文件
    info_list = []
    tree = parse(des_xml_path)
    record = tree.xpath('//record')

    for rec in record:
        titles_list = rec.xpath('./titles/title//text()')
        abstracts_list = rec.xpath('./abstract//text()')
        titles = '\n'.join(titles_list).strip()
        abstracts = '\n'.join(abstracts_list).strip()
        info_list.append([titles, abstracts, '', ''])

    # 将record和info_list写入文件
    record_text_list = list(map(lambda x: tostring(x, encoding='unicode'), record))
    record_fname = os.path.join(saved_dir_name, 'record_text_list.pkl')
    save_pickle(record_text_list, record_fname)

    info_list_fname = os.path.join(saved_dir_name, 'info_list.pkl')
    save_pickle(info_list, info_list_fname)

    return saved_dir_name


def load_xml(path='./assets/source_1690005011'):
    if not os.path.isdir(path):
        raise IOError('该路径不是一个目录，请选择一个文件夹而不是一个文件！')

    record_text_list = load_pickle(os.path.join(path, 'record_text_list.pkl'))
    info_list = load_pickle(os.path.join(path, 'info_list.pkl'))
    return info_list, record_text_list


def export_selected_refs(record: list[str], category, path='./assets/source_1690005011/export'):
    curr_time = str(int(time.time()))
    new_path = os.path.join(path, 'export' + '_' + curr_time)
    make_dir(new_path)

    export_path = os.path.join(new_path, 'export' + '_' + curr_time + '_' + category + '.xml')

    recode_nodes = list(map(lambda x: fromstring(x), record))
    template_xml = './assets/template.xml'
    template_tree = parse(template_xml)
    records_node = template_tree.xpath('.//records')[0]
    for recode_node in recode_nodes:
        records_node.append(recode_node)
    template_tree_text = tostring(template_tree, encoding='unicode')
    final_tree_text = TEMP + template_tree_text

    with open(export_path, 'w', 1, 'utf-8') as f:
        f.write(final_tree_text)


def is_chinese(str_):
    if not str_:
        return False

    if not '\u4e00' <= str_ <= '\u9fa5':
        return False  # 是英文
    else:
        return True  # 是中文


def translated_content(sentence):
    translated_contents = ''

    if not sentence:
        return translated_contents

    results_dict = get_translated_text(sentence.strip())
    if 'translateResult' in results_dict:
        results_list = results_dict['translateResult'][0]  # results_list里面是许多dict
        for result_dict in results_list:
            tgt = result_dict['tgt']
            translated_contents += tgt
        return translated_contents
    else:
        translated_contents += '翻译失败！'
        return translated_contents


if __name__ == '__main__':
    # info_list, record_text_list = load_xml()
    # export_selected_refs(record_text_list)
    sentence = """
    Background Magnetic resonance imaging (MRI) of the prostate after a prior negative biopsy may reduce the need for unnecessary repeat biopsies. Objective To externally validate a previously developed nomogram predicting benign prostate pathology on MRI/ultrasound (US) fusion–targeted biopsy in men with a Prostate Imaging Reporting and Data System (PI-RADS) 3–5 region of interest and a prior negative 12-core systematic biopsy, and update this nomogram to improve its performance. Design, setting, and participants A total of 2063 men underwent MRI/US fusion–targeted biopsy from April 2012 to September 2017; 104 men with a negative systematic biopsy followed by MRI-US fusion–targeted biopsy of a PI-RADS 3–5 region of interest (58%) met the study inclusion criteria. Outcome measurements and statistical analysis An MRI-based nomogram that had previously been developed in a multi-institutional clinical setting was externally validated. Predictive characteristics were age, prostate volume, MRI PI-RADS score, and prostate-specific antigen (PSA). Bayesian logistic regression was used to update the previous model. Results and limitations Median age of the external validation cohort was 68 yr, PSA was 7.2ng/ml, and biopsy confirmed benign pathology in 30% (n=31), suggesting a lower baseline risk compared with the nomogram development cohort. Receiver operating characteristic curve analysis showed areas under curve (AUCs) from 0.77 to 0.80 for nomogram validation. An updated model was constructed with improved calibration and similar discrimination (AUC 0.79). Conclusions Age, prostate volume, PI-RADS, and PSA predict benign pathology on MRI/US fusion–targeted biopsy in men with a prior negative 12-core systematic biopsy. The validated and updated nomogram demonstrated high diagnostic accuracy and may further aid in the decision to avoid a biopsy in men with a prior negative biopsy. Patient summary We externally validated a clinically useful tool that predicts benign prostate pathology on magnetic resonance imaging/ultrasound
    """

    print(translated_content(sentence))
