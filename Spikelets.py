import numpy as np
from saodm_useful import read_csv_columns
from saodm_useful import calc_fano_factor, calc_rr_sd1_sd2, calc_spikelets, read_csv_columns
from saodm_plot_images import *


def analyseSingleFiles(filename, plotTitle):

    calculateISI(filename)
    
    #Poincare, Fano Factor, Spikelets
    plot_geometric_images(filename, plotTitle)

        
def calculateISI(filename):
    name=filename.replace(".csv","")
    file_isi_CHEM = name + '_isi.csv'

    # All spikes
    spikes = read_csv_columns(filename, ['Time'])['Time']
    #print(spikes)
    isi_CHEM = np.diff(spikes)
    save_to_file(file_isi_CHEM, isi_CHEM)

    del spikes
    del isi_CHEM
        

def save_to_file(file: str, Time_list=[]):

    with open(file=file, mode='wt') as fw:
        fw.write('Time\n')
        for time in Time_list:
            fw.write('%.4f\n' % (time))

def plot_geometric_images(filename, plotTitle):
    
    images_to_draw = []
    images_to_draw.append('G1')                 # Geometric, Poincaré
    images_to_draw.append('G2')                 # Geometric, Fano factor
    images_to_draw.append('G3')                 # Geometric, Spikelets

    file_spikes_CHEM = filename
    name=filename.replace(".csv","")
    file_isi_CHEM = name + '_isi.csv'
    name=name.replace("EXCEL/","")

    loaded_spikes_SIF_CHEM = False
    loaded_isi_SIF_CHEM = False

    try:
        spikes_CHEM = read_csv_columns(file_spikes_CHEM, ['Time'])['Time']
        loaded_spikes_SIF_CHEM = True
    except Exception as e:
        print('Error while loading', file_spikes_SIF, 'or', file_spikes_CHEM, '\n',
            '   SKIP PLOTTING (Image 4 ff.)!\n')
        loaded_spikes_SIF_CHEM = False
    finally:
        del file_spikes_CHEM

    try:
        isi_CHEM = read_csv_columns(file_isi_CHEM, ['Time'])['Time']
        loaded_isi_SIF_CHEM = True
    except Exception as e:
        print('Error while loading', file_isi_SIF, 'or', file_isi_CHEM, '\n',
            '   SKIP PLOTTING (Image 4 ff.)!\n')
        loaded_isi_SIF_CHEM = False
    finally:
        del file_isi_CHEM

    ################################################################################################

    print('- Plotting geometrics for %s:' % (filename))

    ## Begin of Image G1: Poincaré #############################################
    if ('G1' in images_to_draw) and loaded_isi_SIF_CHEM:
        print('  - Plotting Poincaré')
        min_val = min(isi_CHEM)
        max_val = max(isi_CHEM)
        #print(isi_CHEM)
        (rr, sd1, sd2) = calc_rr_sd1_sd2(isi_CHEM)
        round_rr = round(rr, 3)
        plot_poincare(case_id=name, title=plotTitle,
                      isi_vals=isi_CHEM, valmin=min_val, valmax=max_val,
                      center=(round_rr, round_rr), sd1=sd1, sd2=sd2, part='_CHEM')

    ## End of Image G1 #########################################################

    ## Begin of Image G2: Fano Factor ##########################################
    if ('G2' in images_to_draw) and loaded_spikes_SIF_CHEM:
        print('  - Plotting Fano factors')
        meanSIF = 0.
        meanCHEM = 0.
        if loaded_isi_SIF_CHEM:
            meanCHEM = np.mean(isi_CHEM)
        C_CHEM_start=spikes_CHEM[0]
        #print(C_CHEM_start)
        plot_fano_factors(case_id=name, title=plotTitle,
                          spikes_list=spikes_CHEM, start_time=C_CHEM_start, part='_CHEM', mean=meanCHEM)
    ## End of Image G2 #########################################################

    ## Begin of Image G3: Spikelets ############################################
    if ('G3' in images_to_draw) and loaded_isi_SIF_CHEM:
        print('  - Plotting Spikelets')
        vmax = len(isi_CHEM)

        spikelets_CHEM = calc_spikelets(isi_list=isi_CHEM)
        plot_spikelets(case_id=name, title=plotTitle,
                       spikelets_list=spikelets_CHEM, barmax=vmax, part='_CHEM')

    ## End of Image G3 #########################################################

    if loaded_spikes_SIF_CHEM:
        del spikes_CHEM
    if loaded_isi_SIF_CHEM:
        del isi_CHEM



