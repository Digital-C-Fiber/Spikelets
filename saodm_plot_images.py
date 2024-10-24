##
# Date of change: July 10th, 2022

## -----------------------------------------------------------------------------------------------##
#                                                                                                  #
## -----------------------------------------------------------------------------------------------##


# basics
from msilib.schema import Error
from matplotlib.colors import hsv_to_rgb
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
import numpy as np                              # diff, floor, mean, nan, ones_like, sqrt, zeros_like
import os                                       # makedirs, path.exists
from pandas import read_csv

# my modules
from saodm_convert_excel import csv_path
from saodm_analyze import findings_path
pics_path = 'PICS/'                    # path to store the images
imagesize_factor = 1.                           # all images can be scaled
from saodm_useful import calc_fano_factor, calc_rr_sd1_sd2, calc_spikelets, read_csv_columns


####################################################################################################

##
# @param case_id: 
# @param C_type: 
# @param C_chem: 
# @param C_num: 
# @param C_SIF_start: 
# @param C_CHEM_start: 
def plot_overview_images(case_id: str, C_type: str, C_chem: str, C_num,
                         C_SIF_start: float, C_CHEM_start: float):
    '''
    '''
    images_to_draw = []
    images_to_draw.append('O1')                 # Overview, like DAPSYS
    images_to_draw.append('O2')                 # Overview, similar to Prof. Sauer
    images_to_draw.append('O3')                 # Overview, spikes of SIF and CHEM

    file_spikes = csv_path + case_id + '_filter1.csv'
    file_comments = csv_path + case_id + '_comments.csv'
    file_temperature = csv_path + case_id + '_temperature.csv'
    file_spikes_SIF = csv_path + case_id + '_spikes_SIF.csv'
    file_spikes_CHEM = csv_path + case_id + '_spikes_CHEM.csv'

    loaded_spikes = False
    loaded_comments = False
    loaded_spikes_SIF_CHEM = False

    try:
        spikes = read_csv_columns(file_spikes, ['Time'])['Time']
        loaded_spikes = True
    except Exception as e:
        print('Error while loading', file_spikes, '\n')
        loaded_spikes = False
    finally:
        del file_spikes

    try:
        csv_comments = read_csv_columns(file_comments, ['Time', 'Text'])
        comments_time = csv_comments['Time']
        comments_text = csv_comments['Text']
        loaded_comments = True
    except Exception as e:
        print('Error while loading', file_comments, '\n')
        loaded_comments = False
    finally:
        del file_comments

    try:
        spikes_SIF = read_csv_columns(file_spikes_SIF, ['Time'])['Time']
        spikes_CHEM = read_csv_columns(file_spikes_CHEM, ['Time'])['Time']
        loaded_spikes_SIF_CHEM = True
    except Exception as e:
        print('Error while loading', file_spikes_SIF, 'or', file_spikes_CHEM, '\n',
            '   SKIP PLOTTING (Image 4 ff.)!\n')
        loaded_spikes_SIF_CHEM = False
    finally:
        del file_spikes_SIF
        del file_spikes_CHEM

    ############################################################################

    print('- Plotting overviews for %s:' % (case_id))

    ### OLD CODE! ##########################################
    #if True:
    #    fileA = csv_path + case_id + '_heat1.csv'
    #    fileB = csv_path + case_id + '_heat1_tem.csv'
    #    if os.path.exists(fileA):
    #        if os.path.exists(fileB):
    #            csv_heat = read_csv_columns(fileB, ['Time', 'Value'])
    #            heat_spikes = read_csv_columns(fileA, ['Time'])['Time']
    #            plot_heat(case_id + '_heat1', title='%s %s %s %s' % (C_type, C_chem, C_num, 'heat1'),
    #                      spikes=heat_spikes, tem_times=csv_heat['Time'], tem_values=csv_heat['Value'])
    #    fileA = csv_path + case_id + '_heat2.csv'
    #    fileB = csv_path + case_id + '_heat2_tem.csv'
    #    if os.path.exists(fileA):
    #        if os.path.exists(fileB):
    #            csv_heat = read_csv_columns(fileB, ['Time', 'Value'])
    #            heat_spikes = read_csv_columns(fileA, ['Time'])['Time']
    #            plot_heat(case_id + '_heat2', title='%s %s %s %s' % (C_type, C_chem, C_num, 'heat2'),
    #                      spikes=heat_spikes, tem_times=csv_heat['Time'], tem_values=csv_heat['Value'])
    #########################################################

    ## Begin of Image O1: Plot of sanitized (DAPSYS) data ######################
    if ('O1' in images_to_draw) and loaded_spikes and loaded_comments:
        file_temperature = csv_path + case_id + '_temperature.csv'
        if not os.path.exists(file_temperature):
            print('  - Plotting Sanitized Data (without temperature)')
            plot_sanitized_data(case_id=case_id, title='%s %s %s' % (C_type, C_chem, C_num),
                                spikes=spikes, comments_time=comments_time, comments_text=comments_text)
        else:
            print('  - Plotting Sanitized Data')
            temperature = read_csv_columns(file_temperature, ['Time', 'Value'])
            plot_sanitized_data(case_id=case_id, title='%s %s %s' % (C_type, C_chem, C_num),
                                spikes=spikes, comments_time=comments_time, comments_text=comments_text,
                                tem_xvals=temperature['Time'], tem_yvals=temperature['Value'])
            del temperature
        del file_temperature
    ## End of Image O1 #########################################################

    ## Begin of Image O2: Sauer2 ###############################################
    if ('O2' in images_to_draw) and loaded_spikes:
        file_temperature = csv_path + case_id + '_temperature.csv'  # must not exist
        if not os.path.exists(file_temperature):
            print('  - Plotting Sauer2 (without temperature)')
            plot_sauer2(case_id=case_id, title='%s %s %s' % (C_type, C_chem, C_num),
                        spikes=spikes, box1_end=C_SIF_start+480., box2_end=C_CHEM_start+480.)
        else:
            print('  - Plotting Sauer2')
            temperature = read_csv_columns(file_temperature, ['Time', 'Value'])
            plot_sauer2(case_id=case_id, title='%s %s %s' % (C_type, C_chem, C_num),
                        spikes=spikes, box1_end=C_SIF_start+480., box2_end=C_CHEM_start+480.,
                        tem_xvals=temperature['Time'], tem_yvals=temperature['Value'])
            del temperature
        del file_temperature
    ## End of Image O2 #########################################################

    ## Begin of Image O3: Spikes and conditions ################################
    if ('O3' in images_to_draw) and loaded_spikes and loaded_spikes_SIF_CHEM:
        print('  - Plotting Relevant Spikes')
        plot_relevant_spikes(case_id=case_id, title='%s %s %s' % (C_type, C_chem, C_num),
                             spikes=spikes, spikes_SIF=spikes_SIF, spikes_CHEM=spikes_CHEM)
    ## End of Image O3 #########################################################

    del images_to_draw
    if loaded_spikes:
        del spikes
    if loaded_comments:
        del comments_time
        del comments_text
    if loaded_spikes_SIF_CHEM:
        del spikes_SIF
        del spikes_CHEM


####################################################################################################

##
# @param
def plot_findings_images(dict_grouped):
    '''
    '''
    print('- Plotting metrics for groups!')

    ## Begin of Images for metrics (Dots) ######################################
    if True:
        plot_metric_comparison_groups(dict_grouped)
    ## End of Images ###########################################################

    ## Begin of Image for metrics (Lines) ######################################
    if False:
        plot_comparison_lines(dict_grouped)
    ## End of Images ###########################################################



####################################################################################################

##
# @param
def plot_geometric_images(case_id: str, C_type: str, C_chem: str, C_num,
                          C_SIF_start: float, C_CHEM_start: float):
    '''
    '''
    images_to_draw = []
    images_to_draw.append('G1')                 # Geometric, Poincaré
    images_to_draw.append('G2')                 # Geometric, Fano factor
    images_to_draw.append('G3')                 # Geometric, Spikelets

    file_spikes_SIF = csv_path + case_id + '_spikes_SIF.csv'
    file_spikes_CHEM = csv_path + case_id + '_spikes_CHEM.csv'
    file_isi_SIF = csv_path + case_id + '_isi_SIF.csv'
    file_isi_CHEM = csv_path + case_id + '_isi_CHEM.csv'

    loaded_spikes_SIF_CHEM = False
    loaded_isi_SIF_CHEM = False

    try:
        spikes_SIF = read_csv_columns(file_spikes_SIF, ['Time'])['Time']
        spikes_CHEM = read_csv_columns(file_spikes_CHEM, ['Time'])['Time']
        loaded_spikes_SIF_CHEM = True
    except Exception as e:
        print('Error while loading', file_spikes_SIF, 'or', file_spikes_CHEM, '\n',
            '   SKIP PLOTTING (Image 4 ff.)!\n')
        loaded_spikes_SIF_CHEM = False
    finally:
        del file_spikes_SIF
        del file_spikes_CHEM

    try:
        isi_SIF = read_csv_columns(file_isi_SIF, ['Time'])['Time']
        isi_CHEM = read_csv_columns(file_isi_CHEM, ['Time'])['Time']
        loaded_isi_SIF_CHEM = True
    except Exception as e:
        print('Error while loading', file_isi_SIF, 'or', file_isi_CHEM, '\n',
            '   SKIP PLOTTING (Image 4 ff.)!\n')
        loaded_isi_SIF_CHEM = False
    finally:
        del file_isi_SIF
        del file_isi_CHEM

    ################################################################################################

    print('- Plotting geometrics for %s:' % (case_id))

    ## Begin of Image G1: Poincaré #############################################
    if ('G1' in images_to_draw) and loaded_isi_SIF_CHEM:
        print('  - Plotting Poincaré')
        min_val = min(min(isi_SIF), min(isi_CHEM))
        max_val = max(max(isi_SIF), max(isi_CHEM))

        (rr, sd1, sd2) = calc_rr_sd1_sd2(isi_SIF)
        round_rr = round(rr, 3)
        plot_poincare(case_id=case_id, title='%s %s %s %s' % (C_type, C_chem, C_num, 'SIF'),
                      isi_vals=isi_SIF, valmin=min_val, valmax=max_val,
                      center=(round_rr, round_rr), sd1=sd1, sd2=sd2, part='_SIF')

        (rr, sd1, sd2) = calc_rr_sd1_sd2(isi_CHEM)
        round_rr = round(rr, 3)
        plot_poincare(case_id=case_id, title='%s %s %s %s' % (C_type, C_chem, C_num, 'CHEM'),
                      isi_vals=isi_CHEM, valmin=min_val, valmax=max_val,
                      center=(round_rr, round_rr), sd1=sd1, sd2=sd2, part='_CHEM')

    ## End of Image G1 #########################################################

    ## Begin of Image G2: Fano Factor ##########################################
    if ('G2' in images_to_draw) and loaded_spikes_SIF_CHEM:
        print('  - Plotting Fano factors')
        meanSIF = 0.
        meanCHEM = 0.
        if loaded_isi_SIF_CHEM:
            meanSIF = np.mean(isi_SIF)
            meanCHEM = np.mean(isi_CHEM)
        plot_fano_factors(case_id=case_id, title='%s %s %s %s' % (C_type, C_chem, C_num, 'SIF'),
                          spikes_list=spikes_SIF, start_time=C_SIF_start, part='_SIF', mean=meanSIF)
        plot_fano_factors(case_id=case_id, title='%s %s %s %s' % (C_type, C_chem, C_num, 'CHEM'),
                          spikes_list=spikes_CHEM, start_time=C_CHEM_start, part='_CHEM', mean=meanCHEM)
    ## End of Image G2 #########################################################

    ## Begin of Image G3: Spikelets ############################################
    if ('G3' in images_to_draw) and loaded_isi_SIF_CHEM:
        print('  - Plotting Spikelets')
        vmax = max(len(isi_SIF), len(isi_CHEM))

        spikelets_SIF = calc_spikelets(isi_list=isi_SIF)
        spikelets_CHEM = calc_spikelets(isi_list=isi_CHEM)
        plot_spikelets(case_id=case_id, title='%s %s %s %s' % (C_type, C_chem, C_num, 'SIF'),
                       spikelets_list=spikelets_SIF, barmax=vmax, part='_SIF')
        plot_spikelets(case_id=case_id, title='%s %s %s %s' % (C_type, C_chem, C_num, 'CHEM'),
                       spikelets_list=spikelets_CHEM, barmax=vmax, part='_CHEM')

    ## End of Image G3 #########################################################

    if loaded_spikes_SIF_CHEM:
        del spikes_SIF
        del spikes_CHEM
    if loaded_isi_SIF_CHEM:
        del isi_SIF
        del isi_CHEM


## Overview Images #################################################################################

## IMAGE O1 ####################################################################

##
# Image O1: Plot of sanitized (DAPSYS) data 
# @param
# @param
# @param
def plot_sanitized_data(case_id, title: str, spikes: list,
                        comments_time: list, comments_text: list,
                        tem_xvals=None, tem_yvals=None):
    '''
    '''
    plt.figure(figsize=(6.40 * 1.5 * imagesize_factor, 4.80 * 1.5 / 2. * imagesize_factor))
    plt.xlabel('Time [s]')
    plt.ylabel('Temperature [°C]')
    plt.yticks([10, 20, 30, 40, 50])

    if (tem_xvals == None) or (tem_yvals == None):
        tem_xvals = list()
        tem_yvals = list()
        #plt.ylabel('')
        #plt.yticks([])

    plt.plot(spikes, np.zeros_like(spikes), 'c|', label='spikes')
    plt.plot(tem_xvals, tem_yvals, 'r', label='temperature', linewidth=0.5)
    for i in range(len(comments_time)):
        plt.plot([comments_time[i], comments_time[i]], [-1, 48], color='m',
                 label=str(comments_time[i]) + ' ' + comments_text[i])
        if comments_text[i] in ["8' SIF", "8' CHEM"]:
            plt.text(comments_time[i]+240, 5, comments_text[i],
                        fontsize=12,
                        horizontalalignment='center', verticalalignment='center')

    plt.title(title)
    plt.legend(loc='upper right', fontsize='small', bbox_to_anchor=(1.34, 1))    # this is magic!
    plt.tight_layout()
    #plt.show()
    filepath = pics_path + 'Sanitized Data/'
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    filename = filepath + case_id + '_sanitized_data.png'
    plt.savefig(filename)
    plt.close('all')


## IMAGE O2 ####################################################################

##
# @param
# @param
# @param
def plot_sauer2(case_id, title: str, spikes: list,
                box1_end: float, box2_end: float,
                box1_start = -1, box2_start = -1,
                tem_xvals=None, tem_yvals=None):
    '''
    Some parameters are pre_fixed for my data.
    Data ist first in seconds but in the image presented as minutes. Therefore
    the x_values are manipulated (divided by 60) before plotting.
    '''
    ## Fixed Parameters & Value Manipulation ###################################
    offset = 4*60       # 4 Minutes at the beginning, half of it at the end
    box_length = 8*60   # 8 Minutes for each box
    if (box1_start == -1):
        box1_start = box1_end - box_length
    if (box2_start == -1):
        box2_start = box2_end - box_length
    #if (tem_xvals is not None):
    #    tem_xvals = [x*60 + spikes[0] for x in tem_xvals]
    del box_length

    ## filter x-axis #######################################
    x_zero = box1_start - offset
    x_end = box2_end + offset/2
    x_vals = list(filter(lambda x: x_zero < x and x <= x_end, spikes))
    x_index = spikes.index(x_vals[0])
    if x_index > 0:
        x_vals = [spikes[x_index-1]] + x_vals
    else:
        'Loose first frequency (okay!)'
    x_vals = [x - x_zero for x in x_vals]

    ## calculate y-values ##################################
    diff = np.diff(x_vals)
    y_vals = [1/d for d in diff]            # in 1/s !

    ## filter temperature ##################################
    if (tem_xvals is not None) and (tem_yvals is not None):
        tem_xvals_tmp = list(filter(lambda x: x_zero < x and x <= x_end, tem_xvals))
        if (len(tem_xvals_tmp) == 0):
            tem_xvals = list()
            tem_yvals = list()
        else:
            index_first = tem_xvals.index(tem_xvals_tmp[0])
            index_last = tem_xvals.index(tem_xvals_tmp[-1])
            tem_yvals = tem_yvals[index_first : (index_last+1)]
            tem_xvals = [x - x_zero for x in tem_xvals_tmp]

    ## x-Axis Manipulation: Transform seconds to minutes ###
    box1_end /= 60.                                 # now in minutes
    box2_end /= 60.                                 # now in minutes
    box1_start /= 60.                               # now in minutes
    box2_start /= 60.                               # now in minutes
    x_zero /= 60.                                   # now in minutes
    box1_end -= x_zero
    box2_end -= x_zero
    box1_start -= x_zero
    box2_start -= x_zero
    x_vals = [x/60. for x in x_vals]                # now in minutes
    if (tem_xvals is not None):
        tem_xvals = [x/60. for x in tem_xvals]      # now in minutes

    ## calculate boxes #####################################
    rect1 = Rectangle((box1_start, 0.001), box1_end - box1_start, 250,
                     facecolor=(0.9, 0.9, 0.9, 1.), edgecolor='k')
    rect2 = Rectangle((box2_start, 0.001), box2_end - box2_start, 250,
                     facecolor=(0.9, 0.9, 0.9, 1.), edgecolor='k')
    fil1 = len(list(filter(lambda x: box1_start < x and x <= box1_end, x_vals)))
    fil2 = len(list(filter(lambda x: box2_start < x and x <= box2_end, x_vals)))
    
    ## plotting ############################################
    fig, freq_ax = plt.subplots()
    fig.set_size_inches(6.40 * 1.5 * imagesize_factor, 4.80 * 1.5 / 1.5 * imagesize_factor)
    tem_ax = freq_ax.twinx()

    freq_ax.set_xlabel('Time [min]')
    freq_ax.set_xlim([0, box2_end + 2])
    freq_ax.set_xscale('linear')
    freq_ax.set_xticks([0, 4, 8, 12, 14, 18, 22, 24])   # my fixed values

    freq_ax.set_ylabel('Instant discharge rate [1/s]')
    freq_ax.set_ylim([0.001, 10000])
    freq_ax.set_yscale('log')
    freq_ax.set_yticks([0.001, 0.01, 0.1, 1, 10, 100, 1000, 10000])
    freq_ax.spines['top'].set_color('white')

    tem_ax.set_ylabel('temperature in °C')
    tem_ax.set_ylim([-100, 50])
    tem_ax.set_yscale('linear')
    tem_ax.set_yticks([0, 10, 20, 30, 40, 50])
    tem_ax.spines['top'].set_color('white')
    tem_ax.spines['right'].set_color('red')
    tem_ax.tick_params(axis='y', colors='red')
    tem_ax.yaxis.label.set_color('red')

    ## Actual Plot #########################################
    freq_ax.plot(x_vals[1:], y_vals, 'k.')
    if (tem_xvals is not None) and (tem_yvals is not None):
        tem_ax.plot(tem_xvals, tem_yvals, 'r-')
    freq_ax.add_patch(rect1)
    freq_ax.add_patch(rect2)
    freq_ax.text((box1_start + box1_end)/2, 400, '%i spikes / %.1f min' % (fil1, box1_end - box1_start),
                 fontsize=12,
                 horizontalalignment='center', verticalalignment='center')
    freq_ax.text((box2_start + box2_end)/2, 400, '%i spikes / %.1f min' % (fil2, box2_end - box2_start),
                 fontsize=12,
                 horizontalalignment='center', verticalalignment='center')

    plt.title(title)
    #plt.legend()
    plt.tight_layout()
    #plt.show()
    filepath = pics_path + 'Sauer2/'
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    filename = filepath + case_id + '_sauer2.png'
    plt.savefig(filename)
    plt.close('all')


## IMAGE O3 ####################################################################

##
# @param
# @param
# @param
def plot_relevant_spikes(case_id, title: str, spikes: list, spikes_SIF: list, spikes_CHEM: list):
    '''
    '''
    plt.figure(figsize=(6.40 * imagesize_factor, 4.80/3. * imagesize_factor))
    plt.title(title)
    plt.xlabel('Time [s]')
    plt.ylim([-1, 3])
    plt.yticks([])

    xvals = spikes
    plt.plot(xvals, np.zeros_like(xvals), 'k|', label='all spikes')
    plt.text(x=xvals[0], y=0.8, s='all spikes', size=8)

    xvals = spikes_SIF
    plt.plot(xvals, np.ones_like(xvals), 'b|', label='SIF condition')
    plt.text(x=xvals[0], y=1.8, s='SIF condition', size=8)

    xvals = spikes_CHEM
    plt.plot(xvals, np.ones_like(xvals), 'r|', label='CHEM condition')
    plt.text(x=xvals[0], y=1.8, s='CHEM condition', size=8)

    #plt.rc('text', size=20) #controls default text size
    #plt.legend(loc='upper center', ncol=3)
    plt.tight_layout()
    #plt.show()
    filepath = pics_path + 'Relevant Spikes/'
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    filename = filepath + case_id + '_relevant_spikes.png'
    plt.savefig(filename)
    plt.close('all')



## IMAGES for metrics ##############################################################################

## Groups ######################################################################

##
# @param
# @return
def plot_metric_comparison_groups(dict_grouped: dict):
    '''
    Special plot-function for highly structure dependent dictionary!
    '''
    group_names = list()                        # Expected length: 3
    metric_names = []                           # Expected length: 3*2 = 6
    sub_colors = []                             # Expected length: 3*2 = 6

    # Sort entries alphabetically to be consistent #########
    for entry in dict_grouped:
        group_names += [(entry[0] + ' ' + entry[1], entry)]
    group_names.sort()                          # result: [('Control GO', ('Control', 'GO')), ...]

    dict_features = dict()                      # stores EVERYTHING, so fill it!
    for (curr_color, entry) in enumerate(group_names):
        list_case_ids = dict_grouped[entry[1]]
        metric_names += ['SIF', 'CHEM']

        # first: find out, how many different features (quantifiers) there are
        # second: multiply them with the number of "subsections" (i.e. columns, i.e. precisely 2)
        example_case = list_case_ids[0]
        columns = read_csv(findings_path + example_case + '.csv', delimiter=';')
        num_subsections = len(list(columns.to_dict().values())[0])
        for feature in dict(columns).keys():
            for i in range(num_subsections):
                try:
                    dict_features[feature][len(sub_colors)+i] = []
                except KeyError:                # first init of a feature
                    dict_features[feature] = dict()
                    dict_features[feature][len(sub_colors)+i] = []

        # fill features dictionary with values (yvals) #####
        for case_id in list_case_ids:
            columns = read_csv(findings_path + case_id + '.csv', delimiter=';')
            for feature in dict(columns).keys():
                l_values = columns[feature].to_list()
                for i in range(num_subsections):
                    dict_features[feature][len(sub_colors)+i] += [l_values[i]]

        sub_colors.append(hsv_to_rgb((curr_color / len(group_names),
                                      0.25 + 0.6 * (1) / (num_subsections), 0.9)))
        sub_colors.append(hsv_to_rgb((curr_color / len(group_names),
                                      0.25 + 0.6 * (1) / (num_subsections), 0.9)))

    # plot one image per feature ###########################
    filepath = pics_path + 'Metric Comparison/'
    if not os.path.exists(filepath):
        os.makedirs(filepath)

    for feature in dict_features.keys():
        max_y = 1
        min_y = 1
        for i in range(len(sub_colors)):
            yvals = dict_features[feature][i]
            max_y = max(max_y, max(yvals))
            min_y = min(min_y, min(yvals))

        plt.figure(figsize=(6.40 * imagesize_factor, 4.80 * 3/4 * imagesize_factor))
        plt.title('Metric Comparison: ' + feature)
        #plt.xlabel('')
        plt.xlim([-1, len(sub_colors)])
        plt.xticks([])
        plt.ylim([min_y - 0.05*max_y, max_y + 0.05*max_y])

        # plot lines #######################################
        for i in range(0, len(sub_colors), 2):
            for j in range(len(dict_features[feature][i])):
                xvals = [i, i+1]
                yvals = [dict_features[feature][i][j], dict_features[feature][i+1][j]]
                plt.plot(xvals, yvals, '-', color=sub_colors[i])

        # plot dots and mean ###############################
        for i in range(len(sub_colors)):
            yvals = dict_features[feature][i]
            mean = np.nanmean(yvals)            # ignores nan values
            plt.plot([i]*len(yvals), yvals, 'o', color=sub_colors[i])
            plt.plot(i, mean, 'k_', markersize=24)

        # labels ###########################################
        for i in range(len(metric_names)):
            plt.text(i, min_y - 0.10*max_y, metric_names[i], {'ha' : 'center'})
        for i in range(len(group_names)):
            plt.text(2*i + 0.5, min_y - 0.15*max_y, (group_names[i])[0], {'ha' : 'center'})

        #plt.legend(loc='upper center', ncol=3)
        plt.tight_layout()
        #plt.show()
        filename = filepath + 'metric_comparison_' + feature + '.png'
        plt.savefig(filename)
        plt.close('all')


## Lines #######################################################################

##
# @param
def plot_comparison_lines(dict_grouped: dict):
    '''
    Special plot-function for highly structure dependent dictionary!
    '''
    group_names = list()                        # Expected length: 3
    metric_names = []                           # Expected length: 3*2 = 6
    sub_colors = []                             # Expected length: 3*2 = 6

    # Sort entries alphabetically to be consistent #########
    for entry in dict_grouped:
        group_names += [(entry[0] + ' ' + entry[1], entry)]
    group_names.sort()                          # result: [('Control GO', ('Control', 'GO')), ...]

    ## Set folder ##########################################
    filepath = pics_path + 'Comparison Lines/'
    if not os.path.exists(filepath):
        os.makedirs(filepath)

    with open(filepath + 'mapping.txt', 'w'):
        "this deletes the content of mapping.txt"

    ########################################################
    dict_features = dict()                      # stores EVERYTHING, so fill it!
    for (curr_color, entry) in enumerate(group_names):
        list_case_ids = dict_grouped[entry[1]]
        metric_names += ['SIF', 'CHEM']
        with open(filepath + 'mapping.txt', 'a') as fa:
            fa.write(entry[0] + ':\n')
            for i, case_id in enumerate(list_case_ids):
                fa.write(str(i) + ': ' + case_id + '\n')
            fa.write('\n')

        # first: find out, how many different features (quantifiers) there are
        # second: multiply them with the number of "subsections" (i.e. columns, i.e. precisely 2)
        example_name = list_case_ids[0]
        columns = read_csv(findings_path + example_name + '.csv', delimiter=';')
        num_subsections = len(list(columns.to_dict().values())[0])
        for feature in dict(columns).keys():
            for i in range(num_subsections):
                try:
                    dict_features[feature][len(sub_colors)+i] = []
                except KeyError:                # first init of a feature
                    dict_features[feature] = dict()
                    dict_features[feature][len(sub_colors)+i] = []

        # fill dict with yvals #############################
        for case_id in list_case_ids:
            columns = read_csv(findings_path + case_id + '.csv', delimiter=';')
            for feature in dict(columns).keys():
                l_values = columns[feature].to_list()
                for i in range(num_subsections):
                    dict_features[feature][len(sub_colors)+i] += [l_values[i]]

        for i in range(num_subsections):
            sub_colors.append(hsv_to_rgb((curr_color / len(dict_grouped),
                                          0.25 + 0.6 * (i+0.5) / (num_subsections), 0.9)))

    # plot one image per feature ###########################
    for feature in dict_features.keys():
        plt.figure(figsize=(6.40 * imagesize_factor, 4.80 * imagesize_factor))
        plt.title('Comparison Lines: ' + feature)
        #plt.xlabel('')

        for i in range(len(sub_colors)):
            yvals = dict_features[feature][i]
            plt.plot(range(len(yvals)), yvals, '.', color=sub_colors[i])
            plt.plot(range(len(yvals)), yvals, '-', color=sub_colors[i],
                     label=(group_names[round(np.floor(i/2))])[0] + ' ' + metric_names[i])

        plt.legend()
        plt.tight_layout()
        #plt.show()
        filename = filepath + 'comparison_lines_' + feature + '.png'
        plt.savefig(filename)
        plt.close('all')


## GEOMETRIC IMAGES ################################################################################

## IMAGE G1 ####################################################################

##
# param
# 
def pointInsideEllipse(x, y, ori_x, ori_y, a, b, phi=0.):
    '''
    This algorithm uses the frmular found at
    https://stackoverflow.com/questions/7946187/point-and-ellipse-rotated-position-test-algorithm
    '''
    term1 = (np.cos(phi)*(x-ori_x) + np.sin(phi)*(y-ori_y))**2 / a**2
    term2 = (np.sin(phi)*(x-ori_x) - np.cos(phi)*(y-ori_y))**2 / b**2
    return (term1 + term2 <= 1)

##
# @param
# @return
def plot_poincare(case_id, title: str, isi_vals: list, valmin: float, valmax: float, unit='s',
                  center=None, sd1=None, sd2=None, part=''):
    '''
    '''
    # crop points smaller valmin or greater valmax
    #isi_vals = [max(valmin, x) for x in isi_vals]
    #isi_vals = [min(valmax, x) for x in isi_vals]
    x_vals = isi_vals[:-1]
    y_vals = isi_vals[1:]

    # definitions for the axes
    left, width = 0.1, 0.65
    bottom, height = 0.1, 0.65
    spacing = 0.005

    rect_scatter = [left, bottom, width, height]
    rect_histx = [left, bottom + height + spacing, width, 0.2]
    rect_histy = [left + width + spacing, bottom, 0.2, height]

    # to expand square
    pixel = 12./2. * (valmax - valmin)/389.
    valmin -= pixel
    valmax += pixel

    # start with a square Figure ###########################
    fig = plt.figure(figsize=(6 * imagesize_factor, 6 * imagesize_factor))
    #plt.title(title)

    ax = fig.add_axes(rect_scatter)
    ax.set_xlabel(r'$ISI_{i}$ [%s]' % unit)
    ax.set_xlim([valmin, valmax])
    ax.set_xscale('linear')
    ax.set_ylabel(r'$ISI_{i+1}$ [%s]' % unit)
    ax.set_ylim([valmin, valmax])
    ax.set_yscale('linear')

    # draw diagonale #######################################
    ax.plot([valmin, valmax], [valmin, valmax], 'k--', alpha=0.75)

    # optional ellipse #####################################
    if center is not None:
        plt.plot(center[0], center[1], 'b+', markersize=20, label=center)
        if sd1 is not None and sd2 is not None:
            from matplotlib.patches import Ellipse
            sd1xy = sd1 / np.sqrt(2.)   # because 45°
            sd2xy = sd2 / np.sqrt(2.)   # because 45°

            # CHOOSE ONE confidence:
            #confidence, strechfactor = ('Confidence: ~68.27%', 1.0)
            #confidence, strechfactor = ('Confidence: ~90%',    1.645)
            confidence, strechfactor = ('Confidence: ~95%',    1.96)
            #confidence, strechfactor = ('Confidence: ~95.45%', 2.0)
            #confidence, strechfactor = ('Confidence: ~99%',    2.575)
            #confidence, strechfactor = ('Confidence: ~99.73%', 3.0)

            if len(x_vals) > 0:
                counter = 0
                for i in range(len(x_vals)):
                    if pointInsideEllipse(x_vals[i], y_vals[i], center[0], center[1],
                                          sd2 * strechfactor, sd1 * strechfactor, 45.):
                        counter += 1
                counter /= len(x_vals)
                confidence += '\n actually:        %.1f%%' % (counter * 100.)

            ax.add_patch(Ellipse(xy=center, width=sd1*2 * strechfactor, height=sd2*2 * strechfactor,
                         facecolor='none', angle=135, edgecolor='grey', linewidth=3., label=confidence))
            plt.plot([center[0], center[0] - sd1xy*strechfactor], [center[1], center[1] + sd1xy*strechfactor],
                     '-', color='orange', linewidth=3., label='SD1: ' + str(round(sd1, 2)) + unit)
            plt.plot([center[0], center[0] + sd2xy*strechfactor], [center[1], center[1] + sd2xy*strechfactor],
                     '-', color='blue', linewidth=3., label='SD2: ' + str(round(sd2, 2)) + unit)
        plt.legend()

    ax_histx = fig.add_axes(rect_histx, sharex=ax)
    ax_histy = fig.add_axes(rect_histy, sharey=ax)

    # no labels ############################################
    ax_histx.tick_params(axis="x", labelbottom=False)
    ax_histy.tick_params(axis="y", labelleft=False)

    # the scatter plot: ####################################
    ax.scatter(x_vals, y_vals, c='k', alpha=0.5)

    # now determine nice limits by hand: ###################
    num_steps = 20
    bins = np.arange(valmin, valmax + 1, (valmax-valmin)/(num_steps+1))
    ax_histx.hist(x_vals, bins=bins)
    ax_histy.hist(y_vals, bins=bins, orientation='horizontal')

    plt.suptitle('Poincaré of ' + title)
    #plt.tight_layout()
    #plt.show()
    filepath = pics_path + 'Poincare/'
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    filename = filepath + case_id + '_poincare' + part + '.png'
    plt.savefig(filename)
    plt.close('all')


## IMAGE G2 ####################################################################

##
# @param
# @return
def plot_fano_factors(case_id, title: str, spikes_list: list, start_time: float, part='', mean=0.):
    '''
    The following (relevant) window sizes divide 480 without remainder:
    2.0,   2.4,  2.5,  3.0,  3.2,  3.75,  3.84,  4.0,  4.8,  5.0,  6.0,  6.4,  7.5,   8.0,   9.6,  10.0,
    12.0, 15.0, 16.0, 19.2, 20.0, 24.0,  30.0,  32.0, 40.0, 48.0, 60.0, 80.0, 96.0, 120.0, 160.0, 240.0
    '''
    USE_LOGARITHMIZED = True 

    x_vals1 = list()
    if USE_LOGARITHMIZED:
        ## alternate version
        alpha = 480
        beta = alpha * 1000
        min_win = max(1, int(beta * 0.0001))    # minimum is 0,01% of alpha, so 10000 windows
        max_win = int(beta * 0.5) + 1           # maximum is 50% of alpha, so 2 windows
        for x in range(min_win, max_win):
            if beta % x == 0:
                x_vals1.append(x/1000.)
    else:
        ## Jan Richter: [0.01, 0.05, 0.1, 0.5, 1., 2.] -> [0.6, 3., 6., 30., 60., 120.]
        x_vals1 = [  2.0,  2.4,  2.5,  3.0,  3.2,  3.75,  3.84,  4.0,   4.8,   5.0,  6.0,
                    6.4,  7.5,  8.0,  9.6, 10.0, 12.0,  15.0,  16.0,  19.2,  20.0, 24.0,
                    30.0, 32.0, 40.0, 48.0, 60.0, 80.0,  96.0, 120.0, 160.0, 240.0]

    y_vals1 = list()
    for time in x_vals1:
        ff = calc_fano_factor(spikes_list, start_time, time)
        y_vals1.append(ff)

    x_vals2 = list()
    y_vals2 = list()
    if mean > 0.:
        x_vals2 = [x for x in x_vals1 if x >= mean*5]
        x_vals2 = [x for x in x_vals2 if x <= mean*10]
        if len(x_vals2) > 0:
            idx = x_vals1.index(x_vals2[0])
            y_vals2 = y_vals1[idx:idx+len(x_vals2)]
    import warnings
    warnings.filterwarnings("error")
    estFF = 480.
    try:
        estFF = np.mean(y_vals2)
    except RuntimeWarning as e:
        # Known: 'Mean of empty slice.'
        "Do nothing."
    warnings.filterwarnings("default")

    # good fano factor candidates
    pixel = (max(y_vals1) - min(y_vals1)) / (379. + 75)
    y_min = min(y_vals1) - pixel*6
    y_max = max(y_vals1) + pixel*69
    rect1 = Rectangle((mean*3, y_min), mean*2, y_max, facecolor=(0.8, 0.8, 0.8, 1.))
    rect2 = Rectangle((mean*5, y_min), mean*5, y_max, facecolor=(0.7, 0.7, 0.7, 1.))

    ############################################################################
    fig, ax = plt.subplots()
    fig.set_size_inches(6.40 * imagesize_factor, 4.80 * imagesize_factor)

    ax.add_patch(rect1)
    ax.add_patch(rect2)

    plt.plot((5*mean, 10*mean), (estFF, estFF), 'b--')      # horizontal estFF in dark grey
    plt.plot(x_vals1, y_vals1)
    plt.plot(x_vals1, y_vals1, '.')

    plt.xlabel('window size t [s]')
    if USE_LOGARITHMIZED:
        plt.xscale('log')
        plt.plot((estFF, estFF), (y_min, y_max), 'b--')         # vertical estFF
        plt.xlim([x_vals1[0] /1.2, x_vals1[-1] *1.2])
        plt.text(16, y_max - pixel*4, 'ISI mean: \nt_min: \n', {'ha':'right', 'va':'top'})
        plt.text(33, y_max - pixel*4, ' %.1f\n %.1f' % (mean, 5*mean), {'ha':'right', 'va':'top'})
        plt.text(16, y_max - pixel*59, r'$\widehat{FF}:$ ', {'ha':'right', 'va':'center'})
        plt.text(33, y_max - pixel*59, ' %.2f' % (estFF), {'ha':'right', 'va':'center'})
    else:
        plt.xlim([2.0 -4, 240.0 +4])
        plt.text(120, y_max - pixel*4, 'ISI mean: \nt_min: \n', {'ha':'right', 'va':'top'})
        plt.text(140, y_max - pixel*4, ' %.1f\n %.1f' % (mean, 5*mean), {'ha':'right', 'va':'top'})
        plt.text(120, y_max - pixel*59, r'$\widehat{FF}:$ ', {'ha':'right', 'va':'center'})
        plt.text(140, y_max - pixel*59, ' %.2f' % (estFF), {'ha':'right', 'va':'center'})
    plt.ylabel('Fano factor FF [#²/#]')
    plt.ylim([y_min, y_max])

    plt.title(title)
    #plt.legend()
    plt.tight_layout()
    #plt.show()
    filepath = pics_path + 'Fano Factors/'
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    filename = filepath + case_id + '_fanofactor' + part + '.png'
    plt.savefig(filename)
    plt.close('all')



## IMAGE G3 ####################################################################

##
# @param
# @return
def plot_spikelets(case_id, title: str, spikelets_list: list, barmax: int, part=''):
    '''
    Spikelets are tripels of spikes. Three spikes means two ISI.
    Regularity (x-axis) is the ratio of two ISI, Length (y-axis) is the sum of the two ISI.

    Beware:
    For the following image we tried to mirror the look of the plot in "Analysis of Nociceptive
    Information Encoded in the Temporal Discharge Patterns of Cutaneous C-Fibers" [Cho, Jang, et al.].
    To do so in Python, we had to change some settings i.e. to have squares in the center image.
    Changes include:
    - raising the minimum length from 0s to 2**(-10/3) seconds (~0.099s)
    - raising the maximum length from 8s to 2**(10/3) seconds (~10.07s)
    - applying log_2 to the length values (resulting in values between -10/3 and +10/3)
    - reverse order of length values (upside down) by multiplying with -1, to have short lengths
        at the top and long length at the bottom ("minimum at top": +10/3, "maximum at bottom": -10/3)
    - If "8 seconds" (even 10.07s) are too short: A modifier is introduced to multiply all borders by
        the same value (i.e. 2**modifier, e.g. multiply by 2, 4, 8, ...). This means the values of the
        lengths are not in [-10/3; +10/3] anymore but in [-10/3 - modifier; +10/3 - modifier] as the
        values are reversed and larger values grow in the negative!
        The modifier also works for negative and floating point values, but the y-bar should then
        be set to "acurate" (line 1029 = True).
    '''
    modifier = 0.25 #2        # every increase by 1 doubles the maximum of 8!!!

    # do not modify after here! ############################

    # regularity
    regularity_spikelets = [2*(y)/(x+y) for (x, y) in spikelets_list]       # values now between 0 and 2
    regularity_bins = [0, 0.2, 0.4, 0.6, 0.8, 1, 1.2, 1.4, 1.6, 1.8, 2]

    # length
    minimum_allowed = 2**(-10/3) * 2**modifier + 0.001
    maximum_allowed = 2**(10/3) * 2**modifier - 0.001

    length_spikelets = [x+y for (x, y) in spikelets_list]                   # short values at bottom
    length_spikelets = [max(minimum_allowed, z) for z in length_spikelets]  # clipping Minimum
    length_spikelets = [min(maximum_allowed, z) for z in length_spikelets]  # clipping Maximum
    length_spikelets = [np.log(z)/np.log(2) for z in length_spikelets]      # this is now exponent of 2**x
    length_spikelets = [-z for z in length_spikelets]                       # short values at top
    clipped_len = [x+y for (x, y) in spikelets_list if (x+y < minimum_allowed) or (x+y > maximum_allowed)]
    if len(clipped_len) > 0:
        print('    Clipped Lengths Values (%s): %d / %d (%.2f%%)' % (part, len(clipped_len),
              len(length_spikelets), 100*len(clipped_len)/len(length_spikelets)))
        #print('   ', sorted(clipped_len))
    clipped_len = None
    # all values are now between -(-10/3+huge_ISI_modification) and -(+10/3+huge_ISI_modification)
    length_bins = []
    for i in range(-5, 5+1):
        length_bins.append(-(i*2/3 + modifier))     # exponents of 2**x
    length_bins.sort()
    min_bin = -10/3 - modifier                      # 2^(-min_bin) = maximum_allowed
    max_bin = 10/3 - modifier                       # 2^(-max_bin) = minimum_allowed

    # image ################################################

    # definitions for the axes
    bottom_space, bhist_height = 0.1/5.5, 0.7/5.5
    map2d_space_y_sum, map2d_height = (0.8+0.4)/5.6, 4./5.5
    # headline_space = 5.5 - 0.1 - 0.7 - 0.4 - 4. = 0.3
    left_space, lhist_height = 0.55/6.4, 0.7/6.4
    map2d_space_x_sum, map2d_width = (1.25+0.35)/6.4, 4./6.4
    map2d_width_colobar = 1.25*4./6.4
    # total width = 0.55 + 0.7 + 0.35 + 1.25*4. = 6.60 instead of 6.40

    rect_hist2d = [map2d_space_x_sum, map2d_space_y_sum, map2d_width_colobar, map2d_height] # 2D image
    rect_histx = [map2d_space_x_sum, bottom_space, map2d_width, bhist_height]   # bottom histogram
    rect_histy = [left_space, map2d_space_y_sum, lhist_height, map2d_height]    # left histogram
    
    fig = plt.figure(figsize=(6.40 * imagesize_factor, 4.80 * 1.1458 * imagesize_factor))
    ax = fig.add_axes(rect_hist2d)
    ax_histx = fig.add_axes(rect_histx, sharex=ax)
    ax_histy = fig.add_axes(rect_histy, sharey=ax)
    ax_histx.tick_params(axis="x", labelbottom=False)
    ax_histy.tick_params(axis="y", labelleft=False)

    ax.set_title(title)
    ax.set_xlabel('\nSpikelet regularity')
    ax.set_xticks([])
    ax.set_ylabel('Spikelet length')
    ax.set_yticks([])

    ax.hist2d(x=regularity_spikelets,
              y=length_spikelets,
              bins=[np.array(regularity_bins), np.array(length_bins)],
              cmap='hot',     #'copper' 'gist_heat' 'hot', plt.cm.jet,
              vmin=0,
              # colorbar max = 0.15 like in "Analysis of Nociceptive Information Encoded in the
              # Temporal Discharge Patterns of Cutaneous C-Fibers" by Cho, Jang, et. al
              vmax=barmax * 0.15
             )
    x_min, x_max, y_min, y_max = 0, 2, min_bin, max_bin
    ax.text(x_min+0.04, y_max-0.15, '|||   ', {'ha' : 'right'})
    ax.text(x_min+0.04, y_min+0.05, '| | |   ', {'ha' : 'right'})
    ax.text(x_min+0.05, y_min+0.18, '\n|  ||', {'ha' : 'center', 'va' : 'top'})
    ax.text(1, y_min+0.18, '\n| | |', {'ha' : 'center', 'va' : 'top'})
    ax.text(x_max-0.05, y_min+0.18, '\n||  |', {'ha' : 'center', 'va' : 'top'})

    ## bottom histogram ################
    counts, _ = np.histogram(regularity_spikelets, bins=regularity_bins)
    import warnings
    warnings.filterwarnings("error")
    try:
        counts = counts / sum(counts)
    except RuntimeWarning as e:
        # Known: 'invalid value encountered in true_divide'
        "Do nothing"
    warnings.filterwarnings("default")
    ax_histx.hist(regularity_bins[:-1], bins=regularity_bins, weights=counts, color='k', rwidth=.98)
    ax_histx.set_ylim(ymax=0.2)
    ax_histx.set_yticks([0, 0.15])

    ## left histogram ##################
    counts, _ = np.histogram(length_spikelets, bins=length_bins)
    warnings.filterwarnings("error")
    try:
        counts = counts / sum(counts)
    except RuntimeWarning as e:
        # Known: 'invalid value encountered in true_divide'
        "Do nothing"
    warnings.filterwarnings("default")
    ax_histy.hist(length_bins[:-1], bins=length_bins, weights=counts, color='k',
                  orientation='horizontal', rwidth=.98)
    ax_histy.set_xlim(xmax=0.5)
    ax_histy.set_xticks([0, 0.4])

    if modifier<1:
        # show acurate bin borders
        for y in length_bins:
            ax_histy.text(0.01, y - 0.01, '%.2f -'% (round(2**(-y), 2)), {'ha' : 'right', 'va' : 'center'})
    else:
        # show beautiful numbers but position is not at the borders
        for y in range(-3, 3+1):
            y += modifier
            if y < 0:
                ax_histy.text(0.01, -y - 0.01, '1/%d -'% (2**(-y)), {'ha' : 'right', 'va' : 'center'})
            else:
                ax_histy.text(0.01, -y - 0.01, '%d -'% (2**y), {'ha' : 'right', 'va' : 'center'})

    fig.colorbar(mappable=ax.collections[0], ax=ax)
    #plt.show()
    filepath = pics_path + 'Spikelets Histogram/'
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    filename = filepath + case_id + '_spikelets' + part + '.png'
    plt.savefig(filename)
    plt.close('all')



## Heat Plot #######################################################################################

##
# @param
# @return
def plot_heat(case_id, title: str, spike_times: list, tem_times: list, tem_values: list):
    '''
    '''
    fig, ax = plt.subplots()
    fig.set_size_inches(6.40, 4.80*2/3)
    #plt.figure(figsize=(6.40, 4.80*2/3))
    plt.xlabel('Time [s]')
    plt.ylabel('Temperature [°C]')
    plt.yticks([10, 20, 30, 40, 50])

    box_end = tem_times[tem_values.index(max(tem_values))] + 0.1
    box_start = box_end - 25.
    rect1 = Rectangle((box_start, -2), box_end - box_start, 50,
                     facecolor=(0.9, 0.9, 0.9, 1.), edgecolor='k')
    ax.add_patch(rect1)

    plt.plot(spike_times, np.zeros_like(spike_times), 'k|', label='spikes')
    plt.plot(tem_times, tem_values, 'r-', label='temperature', linewidth=0.5)

    plt.title(title)
    #plt.legend(loc='upper right', fontsize='small')
    plt.tight_layout()
    #plt.show()
    filepath = pics_path + 'Heat/'
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    filename = filepath + case_id + '.png'
    plt.savefig(filename)
    plt.close('all')

