##
# Date of change: July 26th, 2022

## -----------------------------------------------------------------------------------------------##
#                                                                                                  #
## ---------------------------------------------------------------------------------------------- ##

from numpy import mean, sqrt, var
from scipy.stats import levene, mannwhitneyu, skewtest, ttest_rel, wilcoxon

# my modules
from saodm_convert_excel import csv_path
from saodm_analyze import findings_path
from saodm_useful import read_csv_columns


####################################################################################################


##
# @param
def diabetic_chem_merged_test(dict_grouped):
    '''
    '''
    CHECK_SIF = False

    Diabetic_CHEM_MG_numSpikes = list()
    Diabetic_CHEM_GO_numSpikes = list()
    Diabetic_CHEM_MG_isi = list()
    Diabetic_CHEM_GO_isi = list()

    for tupl in sorted(dict_grouped.keys()):
        for case_id in dict_grouped[tupl]:
            file_spikes_CHEM = csv_path + case_id + '_spikes_CHEM.csv'
            file_isi_CHEM = csv_path + case_id + '_isi_CHEM.csv'
            spikes_CHEM = read_csv_columns(file_spikes_CHEM, ['Time'])['Time']
            isi_CHEM = read_csv_columns(file_isi_CHEM, ['Time'])['Time']
            if tupl[0] == 'Diabetic':
                if tupl[1] == 'MG':
                    Diabetic_CHEM_MG_numSpikes.append(len(spikes_CHEM))
                    Diabetic_CHEM_MG_isi += isi_CHEM
                if tupl[1] == 'GO':
                    Diabetic_CHEM_GO_numSpikes.append(len(spikes_CHEM))
                    Diabetic_CHEM_GO_isi += isi_CHEM
            del spikes_CHEM
            del isi_CHEM

    file = findings_path + 'Test Diabetic CHEM merged NoS.csv'
    with open(file, 'w') as fw:
        if False:
            print('Diabetic CHEM numSpikes')
            if len(Diabetic_CHEM_MG_numSpikes) > 7:
                print('MG', skewtest(Diabetic_CHEM_MG_numSpikes))
            else:
                l1, l2 = len(Diabetic_CHEM_MG_numSpikes), len(Diabetic_CHEM_GO_numSpikes)
                m1, m2 = mean(Diabetic_CHEM_MG_numSpikes), mean(Diabetic_CHEM_GO_numSpikes)
                s1, s2 = sqrt(var(Diabetic_CHEM_MG_numSpikes)), sqrt(var(Diabetic_CHEM_GO_numSpikes))
                print('  MG -- count: %d; mean: %.1f; standard deviation: %.2f' % (l1, m1, s1))
                print('  GO -- count: %d; mean: %.1f; standard deviation: %.2f' % (l2, m2, s2))

        p1var = levene(Diabetic_CHEM_MG_numSpikes, Diabetic_CHEM_GO_numSpikes)[1]
        fw.write('Brown-Forsythe;D_CHEM_MG;D_CHEM_GO;%.3f\n' % (p1var))
        p1med = mannwhitneyu(Diabetic_CHEM_MG_numSpikes, Diabetic_CHEM_GO_numSpikes)[1]
        fw.write('Mann-Whitney U;D_SIF_MG;D_SIF_GO;%.3f\n' % (p1med))

    file = findings_path + 'Test Diabetic CHEM merged ISI.csv'
    with open(file, 'w') as fw:
        p2var = levene(Diabetic_CHEM_MG_isi, Diabetic_CHEM_GO_isi)[1]
        fw.write('Brown-Forsythe;D_CHEM_MG;D_CHEM_GO;%.3f\n' % (p2var))
        p2med = mannwhitneyu(Diabetic_CHEM_MG_isi, Diabetic_CHEM_GO_isi)[1]
        fw.write('Mann-Whitney U;D_SIF_MG;D_SIF_GO;%.3f\n' % (p2med))

    del Diabetic_CHEM_MG_numSpikes
    del Diabetic_CHEM_GO_numSpikes
    del Diabetic_CHEM_MG_isi
    del Diabetic_CHEM_GO_isi

    if CHECK_SIF:
        Diabetic_SIF_MG_numSpikes = list()
        Diabetic_SIF_GO_numSpikes = list()
        Diabetic_SIF_MG_isi = list()
        Diabetic_SIF_GO_isi = list()

        for tupl in sorted(dict_grouped.keys()):
            for case_id in dict_grouped[tupl]:
                file_spikes_SIF = csv_path + case_id + '_spikes_SIF.csv'
                file_isi_SIF = csv_path + case_id + '_isi_SIF.csv'
                spikes_SIF = read_csv_columns(file_spikes_SIF, ['Time'])['Time']
                isi_SIF = read_csv_columns(file_isi_SIF, ['Time'])['Time']
                if tupl[0] == 'Diabetic':
                    if tupl[1] == 'MG':
                        Diabetic_SIF_MG_numSpikes.append(len(spikes_SIF))
                        Diabetic_SIF_MG_isi += isi_SIF
                    if tupl[1] == 'GO':
                        Diabetic_SIF_GO_numSpikes.append(len(spikes_SIF))
                        Diabetic_SIF_GO_isi += isi_SIF
                del spikes_SIF
                del isi_SIF

        file = findings_path + 'Test Diabetic SIF merged NoS.csv'
        with open(file, 'w') as fw:
            if False:
                print('Diabetic SIF numSpikes')
                if len(Diabetic_SIF_MG_numSpikes) > 7:
                    print('MG', skewtest(Diabetic_SIF_MG_numSpikes))
                else:
                    l1, l2 = len(Diabetic_SIF_MG_numSpikes), len(Diabetic_SIF_GO_numSpikes)
                    m1, m2 = mean(Diabetic_SIF_MG_numSpikes), mean(Diabetic_SIF_GO_numSpikes)
                    s1, s2 = sqrt(var(Diabetic_SIF_MG_numSpikes)), sqrt(var(Diabetic_SIF_GO_numSpikes))
                    print('  MG -- count: %d; mean: %.1f; standard deviation: %.2f' % (l1, m1, s1))
                    print('  GO -- count: %d; mean: %.1f; standard deviation: %.2f' % (l2, m2, s2))

            p3var = levene(Diabetic_SIF_MG_numSpikes, Diabetic_SIF_GO_numSpikes)[1]
            fw.write('Brown-Forsythe;D_SIF_MG;D_SIF_GO;%.3f\n' % (p3var))
            p3med = mannwhitneyu(Diabetic_SIF_MG_numSpikes, Diabetic_SIF_GO_numSpikes)[1]
            fw.write('Mann-Whitney U;D_SIF_MG;D_SIF_GO;%.3f\n' % (p3med))

        file = findings_path + 'Test Diabetic SIF merged ISI.csv'
        with open(file, 'w') as fw:
            p4var = levene(Diabetic_SIF_MG_isi, Diabetic_SIF_GO_isi)[1]
            fw.write('Brown-Forsythe;D_SIF_MG;D_SIF_GO;%.3f\n' % (p4var))
            p4med = mannwhitneyu(Diabetic_SIF_MG_isi, Diabetic_SIF_GO_isi)[1]
            fw.write('Mann-Whitney U;D_SIF_MG;D_SIF_GO;%.3f\n' % (p4med))

        del Diabetic_SIF_MG_numSpikes
        del Diabetic_SIF_GO_numSpikes
        del Diabetic_SIF_MG_isi
        del Diabetic_SIF_GO_isi


##
# @param
def chemical_effect_test(dict_grouped):
    '''
    Use paired tests.
    t-test for normally distributed (not programmed)
    Wilcoxon signed-rank test for other (programmed only)
    '''
    Control_SIF_numSpikes = list()
    Control_CHEM_numSpikes = list()
    Diabetic_SIF_merged_numSpikes = list()
    Diabetic_CHEM_merged_numSpikes = list()

    Control_SIF_isi = list()
    Control_CHEM_isi = list()
    Diabetic_SIF_MG_isi = list()
    Diabetic_CHEM_MG_isi = list()
    Diabetic_SIF_GO_isi = list()
    Diabetic_CHEM_GO_isi = list()

    for tupl in sorted(dict_grouped.keys()):
        for case_id in dict_grouped[tupl]:
            file_spikes_SIF = csv_path + case_id + '_spikes_SIF.csv'
            file_spikes_CHEM = csv_path + case_id + '_spikes_CHEM.csv'
            file_isi_SIF = csv_path + case_id + '_isi_SIF.csv'
            file_isi_CHEM = csv_path + case_id + '_isi_CHEM.csv'
            spikes_SIF = read_csv_columns(file_spikes_SIF, ['Time'])['Time']
            spikes_CHEM = read_csv_columns(file_spikes_CHEM, ['Time'])['Time']
            isi_SIF = read_csv_columns(file_isi_SIF, ['Time'])['Time']
            isi_CHEM = read_csv_columns(file_isi_CHEM, ['Time'])['Time']
            if tupl[0] == 'Control':
                Control_SIF_numSpikes.append(len(spikes_SIF))
                Control_CHEM_numSpikes.append(len(spikes_CHEM))
                Control_SIF_isi += isi_SIF
                Control_CHEM_isi += isi_CHEM
            if tupl[0] == 'Diabetic':
                Diabetic_SIF_merged_numSpikes.append(len(spikes_SIF))
                Diabetic_CHEM_merged_numSpikes.append(len(spikes_CHEM))
                if tupl[1] == 'MG':
                    Diabetic_SIF_MG_isi += isi_SIF
                    Diabetic_CHEM_MG_isi += isi_CHEM
                if tupl[1] == 'GO':
                    Diabetic_SIF_GO_isi += isi_SIF
                    Diabetic_CHEM_GO_isi += isi_CHEM
            del spikes_SIF
            del spikes_CHEM
            del isi_SIF
            del isi_CHEM

    file = findings_path + 'Test chemical effect NoS.csv'
    with open(file, 'w') as fw:
        if False:
            print('Control SIF/CHEM numSpikes')
            l1, l2 = len(Control_SIF_numSpikes), len(Control_CHEM_numSpikes)
            m1, m2 = mean(Control_SIF_numSpikes), mean(Control_CHEM_numSpikes)
            s1, s2 = sqrt(var(Control_SIF_numSpikes)), sqrt(var(Control_CHEM_numSpikes))
            print('  SIF  -- count: %d; mean: %.1f; standard deviation: %.2f' % (l1, m1, s1))
            print('  CHEM -- count: %d; mean: %.1f; standard deviation: %.2f' % (l2, m2, s2))

            #print('Diabetic SIF/CHEM numSpikes')
            #l1, l2 = len(Diabetic_SIF_merged_numSpikes), len(Diabetic_CHEM_merged_numSpikes)
            #m1, m2 = mean(Diabetic_SIF_merged_numSpikes), mean(Diabetic_CHEM_merged_numSpikes)
            #s1, s2 = sqrt(var(Diabetic_SIF_merged_numSpikes)), sqrt(var(Diabetic_CHEM_merged_numSpikes))
            #print('  SIF  -- count: %d; mean: %.1f; standard deviation: %.2f' % (l1, m1, s1))
            #print('  CHEM -- count: %d; mean: %.1f; standard deviation: %.2f' % (l2, m2, s2))

        if Control_SIF_numSpikes and Control_CHEM_numSpikes:
            p1med = wilcoxon(Control_SIF_numSpikes, Control_CHEM_numSpikes)[1]

            fw.write('Wilcoxon;C_SIF;C_CHEM;%.3f\n' % (p1med))
            p1mean = ttest_rel(Control_SIF_numSpikes, Control_CHEM_numSpikes)[1]
            fw.write('paired t-test;C_SIF;C_CHEM;%.3f\n' % (p1mean))
        else:
            print('Test not possible!')

        #p2w = wilcoxon(Diabetic_SIF_merged_numSpikes, Diabetic_CHEM_merged_numSpikes)[1]
        #fw.write('Wilcoxon;D_SIF_m;D_CHEM_m;%.3f\n' % (p2w))

        #fw.write('C_SIF;D_SIF_m;%.3f\n' % (levene(Control_SIF_numSpikes, Diabetic_SIF_merged_numSpikes)[1]))
        #fw.write('C_CHEM;D_CHEM_m;%.3f\n' % (levene(Control_CHEM_numSpikes, Diabetic_CHEM_merged_numSpikes)[1]))

    #file = findings_path + 'Test chemical effect ISI.csv'
    #with open(file, 'w') as fw:
        #p1m = mannwhitneyu(Control_SIF_isi, Control_CHEM_isi)[1]
        #fw.write('Mann-Whitney U;C_SIF;C_CHEM;%.3f\n' % (p1m))
        #p2m = mannwhitneyu(Diabetic_SIF_MG_isi, Diabetic_CHEM_MG_isi)[1]
        #fw.write('Mann-Whitney U;D_SIF_MG;D_CHEM_GO;%.3f\n' % (p2m))
        #p3m = mannwhitneyu(Diabetic_SIF_GO_isi, Diabetic_CHEM_GO_isi)[1]
        #fw.write('Mann-Whitney U;D_SIF_GO;D_CHEM_MG;%.3f\n' % (p3m))

        #fw.write('C_SIF;D_SIF_m;%.3f\n' % (levene(Control_SIF_isi, Diabetic_SIF_merged_isi)[1]))
        #fw.write('C_CHEM;D_CHEM_m;%.3f\n' % (levene(Control_CHEM_isi, Diabetic_CHEM_merged_isi)[1]))

    del Control_SIF_numSpikes
    del Control_CHEM_numSpikes
    del Diabetic_SIF_merged_numSpikes
    del Diabetic_CHEM_merged_numSpikes

    del Control_SIF_isi
    del Control_CHEM_isi
    del Diabetic_SIF_MG_isi
    del Diabetic_CHEM_MG_isi
    del Diabetic_SIF_GO_isi
    del Diabetic_CHEM_GO_isi


##
# @param
def levene_and_t_tests(dict_grouped):
    '''
    '''
    diabetic_chem_merged_test(dict_grouped=dict_grouped)
    chemical_effect_test(dict_grouped=dict_grouped)

