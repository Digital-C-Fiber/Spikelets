##
# Date of change: July 10th, 2022

### -------------------------------------------------------------------------------------------- ###
# SAODM stands for Spike Analysis Of Diabetic Mice                                                 #
### -------------------------------------------------------------------------------------------- ###
# SAODM is split into 3 parts and reacts to the settings in line 54 to 58.                         #
#                                                                                                  #
# Part 1: CONVERT_EXCEL_TO_CSV                                                                     #
#     The Excel files are opened, read and the content stored to different new csv files.          #
#     This process is highly depending on the structure and content in the Excel files.            #
#     The real process is hidden in file saodm_excel.py and only initiated from here.              #
#     !!!                                                                    !!!                   #
#     !!! This conversion has only to be done ONCE.                          !!!                   #
#     !!! Afterwards CONVERT_EXCEL_TO_CSV in line 53 should be set to False. !!!                   #
#     !!!                                                                    !!!                   #
#                                                                                                  #
# Part 2: ANALYZE_AND_COMPARE                                                                      #
#     Calculates various values case by case and stores the results in a new csv file per case.    #
#     Also restricts the temperature to boundaries.                                                #
#                                                                                                  #
# Part 3: PLOT_VARIOUS_IMAGES                                                                      #
#     Plot images for single cases or all cases with each other.                                   #
### -------------------------------------------------------------------------------------------- ###


# before using SAODM: please install openpyxl using the following command
#   pip3 install openpyxl

# basics
import os                               # mkdir, path.exists, path.isdir

# my modules
from saodm_convert_excel import convert_excel_to_csv
from saodm_analyze import analyze_and_compare, merge_findings_table
from saodm_plot_images import plot_overview_images, plot_findings_images, plot_geometric_images

from saodm_levene_ttests import levene_and_t_tests
from saodm_useful import read_csv_columns


### -------------------------------------------------------------------------------------------- ###
# Controls!                                                                                        #
#                                                                                                  #
# path variables                                                                                   #
from saodm_convert_excel import excel_path  # path where the test cases (excel) are stored         #
from saodm_convert_excel import csv_path    # path where the converted files shall be stored       #
from saodm_analyze import findings_path     # path to store the results (csv, xlsx)                #
from saodm_plot_images import pics_path     # path to store the images                             #
from saodm_plot_images import imagesize_factor  # all images can be scaled                         #
#                                                                                                  #
#                                                                                                  #
CONVERT_EXCEL_TO_CSV = True        # only needed once per file; set to False after successful run #
ANALYZE_AND_COMPARE = True          # compare all csv-files and print results into big Excel table #
PLOT_VARIOUS_IMAGES = True          # produce images                                               #
LEVENE_AND_T_TESTS = True          #                                                               #
SECTION_SIZE_IN_S = 480.            # size of SIF/CHEM section. Please use a float number          #
#                                                                                                  #
### -------------------------------------------------------------------------------------------- ###


# Cases to analyze:
'''
CASES = {

    # Control + GO
    'C_GO_04' : {'type':'Control', 'chem':'GO', 'number':'04'},     # has temperature
    'C_GO_14' : {'type':'Control', 'chem':'GO', 'number':'14'},     # has temperature
    'C_GO_28' : {'type':'Control', 'chem':'GO', 'number':'28'},     # has temperature, SIF too small!
    'C_GO_29' : {'type':'Control', 'chem':'GO', 'number':'29'},     # spikes only
    'C_GO_31' : {'type':'Control', 'chem':'GO', 'number':'31'},     # spikes only

    # Diabetic + GO
    'D_GO_20' : {'type':'Diabetic', 'chem':'GO', 'number':'20'},    # spikes only
    'D_GO_22' : {'type':'Diabetic', 'chem':'GO', 'number':'22'},    # spikes only

    # Diabetic + MG
    'D_MG_08' : {'type':'Diabetic', 'chem':'MG', 'number':'08'},    # has temperature
    'D_MG_09' : {'type':'Diabetic', 'chem':'MG', 'number':'09'},    # has temperature
    'D_MG_15' : {'type':'Diabetic', 'chem':'MG', 'number':'15'},    # has temperature
    'D_MG_18' : {'type':'Diabetic', 'chem':'MG', 'number':'18'},    # has temperature
    'D_MG_19' : {'type':'Diabetic', 'chem':'MG', 'number':'19'},    # has temperature
    'D_MG_22' : {'type':'Diabetic', 'chem':'MG', 'number':'22'},    # spikes only
    'D_MG_24' : {'type':'Diabetic', 'chem':'MG', 'number':'24'},    # spikes only
    'D_MG_25' : {'type':'Diabetic', 'chem':'MG', 'number':'25'},    # spikes only
    'D_MG_28' : {'type':'Diabetic', 'chem':'MG', 'number':'28'},    # has temperature
    'D_MG_36' : {'type':'Diabetic', 'chem':'MG', 'number':'36'},    # has temperature
    'D_MG_39' : {'type':'Diabetic', 'chem':'MG', 'number':'39'},    # has temperature

    # A-delta fiber + MG
    #'C_Adelta_21' : {'type':'Control', 'chem':'Adelta', 'number':'21'}, #
    #'C_Adelta_24' : {'type':'Control', 'chem':'Adelta', 'number':'24'}  #
}
'''

####################################################################################################


##
def analyseSingleFiles(filename, typ, chem, number):
    CASES={filename:{'type':typ, 'chem': chem, 'number': number}}
    case_id=filename
    '''
    Control function of SAODM.
    '''

    ## Folder-existance-security ###############################################
    if not os.path.isdir(csv_path):
        os.mkdir(csv_path)

    if not os.path.isdir(findings_path):
        os.mkdir(findings_path)

    if not os.path.isdir(pics_path):
        os.mkdir(pics_path)

    #print('Cases to be analyzed:', list(CASES.keys()))


    ############################################################################

    if CONVERT_EXCEL_TO_CSV:
        '''
        '''
        print('CONVERT_EXCEL_TO_CSV')
        convert_excel_to_csv(case_id, relevant_size=SECTION_SIZE_IN_S)#single file


    ############################################################################

    # necessary for both analyze and plot section
    dict_grouped = dict()

    # mandatory setting for ANALYZE_AND_COMPARE and PLOT_VARIOUS_IMAGES
    file_comments = csv_path + case_id + '_comments.csv'
    try:
        comments = read_csv_columns(file_comments, ['Time', 'Text'])
        comments_time = comments['Time']
        CASES[case_id]['SIF start'] = comments_time[3]
        CASES[case_id]['CHEM start'] = comments_time[5]
        del comments
        del comments_time
    except Exception as e:
        print('Error while reading %s\n' % file_comments)
        raise e
    finally:
        del file_comments
    '''
    # Preparation for Excel/images with multiple data
    set_type = set()
    set_chem = set()

    set_type.add(CASES[case_id]['type'])
    set_chem.add(CASES[case_id]['chem'])

    # Gather cases as groups
    for case_type in set_type:
        for case_chem in set_chem:
            for case_id in CASES.keys():
                if ((CASES[case_id]['type'] != case_type) or
                    (CASES[case_id]['chem'] != case_chem)):
                    continue
                try:
                    dict_grouped[(case_type, case_chem)].append(case_id)
                except KeyError:
                    dict_grouped[(case_type, case_chem)] = [case_id]
    del set_type
    del set_chem
    '''

    ############################################################################

    if ANALYZE_AND_COMPARE: #creates metric comparison plots
        '''
        '''
        print('ANALYZE_AND_COMPARE')
        C_SIF_start = CASES[case_id]['SIF start']
        C_CHEM_start = CASES[case_id]['CHEM start']

        analyze_and_compare(case_id, C_SIF_start=C_SIF_start, C_CHEM_start=C_CHEM_start,
                           SECTION_SIZE_IN_S=SECTION_SIZE_IN_S)

        # merge cases to xlsx table
        #merge_findings_table(dict_grouped=dict_grouped)#groups


    ############################################################################

    if PLOT_VARIOUS_IMAGES:
        '''
        '''
        print('PLOT_VARIOUS_IMAGES')
        if True:
            C_type = CASES[case_id]['type']
            C_chem = CASES[case_id]['chem']
            C_num = CASES[case_id]['number']
            C_SIF_start = CASES[case_id]['SIF start']
            C_CHEM_start = CASES[case_id]['CHEM start']
            plot_overview_images(case_id=case_id, C_type=C_type, C_chem=C_chem, C_num=C_num,
                                 C_SIF_start=C_SIF_start, C_CHEM_start=C_CHEM_start)
        
        if False:#group
            plot_findings_images(dict_grouped=dict_grouped)

        if True:
            C_type = CASES[case_id]['type']
            C_chem = CASES[case_id]['chem']
            C_num = CASES[case_id]['number']
            C_SIF_start = CASES[case_id]['SIF start']
            C_CHEM_start = CASES[case_id]['CHEM start']
            plot_geometric_images(case_id=case_id, C_type=C_type, C_chem=C_chem, C_num=C_num,
                                  C_SIF_start=C_SIF_start, C_CHEM_start=C_CHEM_start)

        if False:#groups
            # merged Control CHEM plot
            from saodm_plot_images import plot_spikelets
            from saodm_useful import calc_spikelets

            print('- Plotting Merged Spikelets')
            merged_Control_SIF_isi = list()
            merged_Control_GO_isi = list()
            merged_Diabetic_SIF_isi = list()
            merged_Diabetic_MG_isi = list()
            merged_Diabetic_GO_isi = list()
            
            file_isi_SIF = csv_path + case_id + '_isi_SIF.csv'
            file_isi_CHEM = csv_path + case_id + '_isi_CHEM.csv'
            isi_SIF = read_csv_columns(file_isi_SIF, ['Time'])['Time']
            isi_CHEM = read_csv_columns(file_isi_CHEM, ['Time'])['Time']
            if CASES[case_id]['type'] == 'Control':
                merged_Control_SIF_isi += isi_SIF
                merged_Control_GO_isi += isi_CHEM
            if CASES[case_id]['type'] == 'Diabetic':
                merged_Diabetic_SIF_isi += isi_SIF
                if CASES[case_id]['chem'] == 'MG': merged_Diabetic_MG_isi += isi_CHEM
                if CASES[case_id]['chem'] == 'GO': merged_Diabetic_GO_isi += isi_CHEM
            del isi_SIF, isi_CHEM
            
            spikelets_Control_SIF = calc_spikelets(isi_list=merged_Control_SIF_isi)
            spikelets_Control_GO = calc_spikelets(isi_list=merged_Control_GO_isi)
            spikelets_Diabetic_SIF = calc_spikelets(isi_list=merged_Diabetic_SIF_isi)
            spikelets_Diabetic_MG = calc_spikelets(isi_list=merged_Diabetic_MG_isi)
            spikelets_Diabetic_GO = calc_spikelets(isi_list=merged_Diabetic_GO_isi)
            vmax_C_S = len(merged_Control_SIF_isi)
            vmax_C_GO = len(merged_Control_GO_isi)
            vmax_D_S = len(merged_Diabetic_SIF_isi)
            vmax_D_MG = len(merged_Diabetic_MG_isi)
            vmax_D_GO = len(merged_Diabetic_GO_isi)
            print(            vmax_C_S,
            vmax_C_GO,
            vmax_D_S,
            vmax_D_MG,
            vmax_D_GO)
            plot_spikelets(case_id='Control_SIF_merged', title='%s' % ('Control SIF merged'),
                           spikelets_list=spikelets_Control_SIF, barmax=vmax_C_S)
            plot_spikelets(case_id='Control_GO_merged', title='%s' % ('Control GO merged'),
                           spikelets_list=spikelets_Control_GO, barmax=vmax_C_GO)
            plot_spikelets(case_id='Diabetic_SIF_merged', title='%s' % ('Diabetic SIF merged'),
                           spikelets_list=spikelets_Diabetic_SIF, barmax=vmax_D_S)
            plot_spikelets(case_id='Diabetic_MG_merged', title='%s' % ('Diabetic MG merged'),
                           spikelets_list=spikelets_Diabetic_MG, barmax=vmax_D_MG)
            plot_spikelets(case_id='Diabetic_GO_merged', title='%s' % ('Diabetic GO merged'),
                           spikelets_list=spikelets_Diabetic_GO, barmax=vmax_D_GO)
            del merged_Control_SIF_isi, merged_Control_GO_isi
            del merged_Diabetic_SIF_isi, merged_Diabetic_MG_isi, merged_Diabetic_GO_isi
            del spikelets_Control_SIF, spikelets_Control_GO
            del spikelets_Diabetic_SIF, spikelets_Diabetic_MG, spikelets_Diabetic_GO


    ############################################################################
    #only for groups
    '''
    if LEVENE_AND_T_TESTS:
        #Statistical analysis like Levene, t-Test and so on.
        print('LEVENE AND T-TESTS')
        levene_and_t_tests(dict_grouped=dict_grouped)#groups
    '''

    ############################################################################

    del dict_grouped


####################################################################################################


def analyseGroups(files):#TODO
    '''
    Control function of SAODM.
    '''
    
    ## Folder-existance-security ###############################################
    if not os.path.isdir(csv_path):
        os.mkdir(csv_path)

    if not os.path.isdir(findings_path):
        os.mkdir(findings_path)

    if not os.path.isdir(pics_path):
        os.mkdir(pics_path)

    #print('Cases to be analyzed:', list(CASES.keys()))

    ############################################################################

    # necessary for both analyze and plot section
    dict_grouped = dict()

    # mandatory setting for ANALYZE_AND_COMPARE and PLOT_VARIOUS_IMAGES
    for case_id in files:
        file_comments = csv_path + case_id + '_comments.csv'
        try:
            comments = read_csv_columns(file_comments, ['Time', 'Text'])
            comments_time = comments['Time']
            CASES[case_id]['SIF start'] = comments_time[3]
            CASES[case_id]['CHEM start'] = comments_time[5]
            del comments
            del comments_time
        except Exception as e:
            print('Error while reading %s\n' % file_comments)
            raise e
        finally:
            del file_comments

    # Preparation for Excel/images with multiple data
    set_type = set()
    set_chem = set()
    for case_id in CASES.keys():
        set_type.add(CASES[case_id]['type'])
        set_chem.add(CASES[case_id]['chem'])

    # Gather cases as groups
    for case_type in set_type:
        for case_chem in set_chem:
            for case_id in CASES.keys():
                if ((CASES[case_id]['type'] != case_type) or
                    (CASES[case_id]['chem'] != case_chem)):
                    continue
                try:
                    dict_grouped[(case_type, case_chem)].append(case_id)
                except KeyError:
                    dict_grouped[(case_type, case_chem)] = [case_id]
    del set_type
    del set_chem


    ############################################################################

    if ANALYZE_AND_COMPARE:
        '''
        '''
        print('ANALYZE_AND_COMPARE')
        for case_id in CASES.keys():
            C_SIF_start = CASES[case_id]['SIF start']
            C_CHEM_start = CASES[case_id]['CHEM start']

            analyze_and_compare(case_id, C_SIF_start=C_SIF_start, C_CHEM_start=C_CHEM_start,
                                SECTION_SIZE_IN_S=SECTION_SIZE_IN_S)

        # merge cases to xlsx table
        merge_findings_table(dict_grouped=dict_grouped)


    ############################################################################

    if PLOT_VARIOUS_IMAGES:
        '''
        '''
        print('PLOT_VARIOUS_IMAGES')
        if True:
            for case_id in CASES.keys():
                C_type = CASES[case_id]['type']
                C_chem = CASES[case_id]['chem']
                C_num = CASES[case_id]['number']
                C_SIF_start = CASES[case_id]['SIF start']
                C_CHEM_start = CASES[case_id]['CHEM start']
                plot_overview_images(case_id=case_id, C_type=C_type, C_chem=C_chem, C_num=C_num,
                                     C_SIF_start=C_SIF_start, C_CHEM_start=C_CHEM_start)
        
        if True:
            plot_findings_images(dict_grouped=dict_grouped)

        if True:
            for case_id in CASES.keys():
                C_type = CASES[case_id]['type']
                C_chem = CASES[case_id]['chem']
                C_num = CASES[case_id]['number']
                C_SIF_start = CASES[case_id]['SIF start']
                C_CHEM_start = CASES[case_id]['CHEM start']
                plot_geometric_images(case_id=case_id, C_type=C_type, C_chem=C_chem, C_num=C_num,
                                      C_SIF_start=C_SIF_start, C_CHEM_start=C_CHEM_start)

        if True:
            # merged Control CHEM plot
            from saodm_plot_images import plot_spikelets
            from saodm_useful import calc_spikelets

            print('- Plotting Merged Spikelets')
            merged_Control_SIF_isi = list()
            merged_Control_GO_isi = list()
            merged_Diabetic_SIF_isi = list()
            merged_Diabetic_MG_isi = list()
            merged_Diabetic_GO_isi = list()
            for case_id in CASES.keys():
                file_isi_SIF = csv_path + case_id + '_isi_SIF.csv'
                file_isi_CHEM = csv_path + case_id + '_isi_CHEM.csv'
                isi_SIF = read_csv_columns(file_isi_SIF, ['Time'])['Time']
                isi_CHEM = read_csv_columns(file_isi_CHEM, ['Time'])['Time']
                if CASES[case_id]['type'] == 'Control':
                    merged_Control_SIF_isi += isi_SIF
                    merged_Control_GO_isi += isi_CHEM
                if CASES[case_id]['type'] == 'Diabetic':
                    merged_Diabetic_SIF_isi += isi_SIF
                    if CASES[case_id]['chem'] == 'MG': merged_Diabetic_MG_isi += isi_CHEM
                    if CASES[case_id]['chem'] == 'GO': merged_Diabetic_GO_isi += isi_CHEM
                del isi_SIF, isi_CHEM
            spikelets_Control_SIF = calc_spikelets(isi_list=merged_Control_SIF_isi)
            spikelets_Control_GO = calc_spikelets(isi_list=merged_Control_GO_isi)
            spikelets_Diabetic_SIF = calc_spikelets(isi_list=merged_Diabetic_SIF_isi)
            spikelets_Diabetic_MG = calc_spikelets(isi_list=merged_Diabetic_MG_isi)
            spikelets_Diabetic_GO = calc_spikelets(isi_list=merged_Diabetic_GO_isi)
            vmax_C_S = len(merged_Control_SIF_isi)
            vmax_C_GO = len(merged_Control_GO_isi)
            vmax_D_S = len(merged_Diabetic_SIF_isi)
            vmax_D_MG = len(merged_Diabetic_MG_isi)
            vmax_D_GO = len(merged_Diabetic_GO_isi)
            print(            vmax_C_S,
            vmax_C_GO,
            vmax_D_S,
            vmax_D_MG,
            vmax_D_GO)
            plot_spikelets(case_id='Control_SIF_merged', title='%s' % ('Control SIF merged'),
                           spikelets_list=spikelets_Control_SIF, barmax=vmax_C_S)
            plot_spikelets(case_id='Control_GO_merged', title='%s' % ('Control GO merged'),
                           spikelets_list=spikelets_Control_GO, barmax=vmax_C_GO)
            plot_spikelets(case_id='Diabetic_SIF_merged', title='%s' % ('Diabetic SIF merged'),
                           spikelets_list=spikelets_Diabetic_SIF, barmax=vmax_D_S)
            plot_spikelets(case_id='Diabetic_MG_merged', title='%s' % ('Diabetic MG merged'),
                           spikelets_list=spikelets_Diabetic_MG, barmax=vmax_D_MG)
            plot_spikelets(case_id='Diabetic_GO_merged', title='%s' % ('Diabetic GO merged'),
                           spikelets_list=spikelets_Diabetic_GO, barmax=vmax_D_GO)
            del merged_Control_SIF_isi, merged_Control_GO_isi
            del merged_Diabetic_SIF_isi, merged_Diabetic_MG_isi, merged_Diabetic_GO_isi
            del spikelets_Control_SIF, spikelets_Control_GO
            del spikelets_Diabetic_SIF, spikelets_Diabetic_MG, spikelets_Diabetic_GO


    ############################################################################

    if LEVENE_AND_T_TESTS:
        '''
        Statistical analysis like Levene, t-Test and so on.
        '''
        print('LEVENE AND T-TESTS')
        levene_and_t_tests(dict_grouped=dict_grouped)


    ############################################################################

    del dict_grouped

