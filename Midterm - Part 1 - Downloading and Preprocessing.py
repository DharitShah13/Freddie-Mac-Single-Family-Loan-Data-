from webbot import Browser
from zipfile import ZipFile
import sys
import os
import time
import zipfile
import datetime
import glob
import pandas as pd

# Auto Navigate to the download page
def navigate(user='tiwari.abhi@husky.neu.edu', password='c`PD{0f8'):
    global web
    web = Browser()
    web.go_to("https://freddiemac.embs.com/FLoan/secure/login.php?pagename=download3")
    web.type(user, into='email')
    web.type(password, into='password')
    web.click('Submit Credentials')
    web.click('Yes')
    web.click('Continue')


def download_all_files(styear=2005, edyear=2006):
    years = list(range(styear, edyear + 1))

    global file_names
    file_names = []

    for year in years:
        web.click('sample_{}.zip'.format(str(year)))
        file_names.append('sample_{}.zip'.format(str(year)))
        print('sample_{}.zip has been downloaded'.format(str(year)))
        time.sleep(60)  # Some delay must be added since site blocks immediate requests in large numbers

    # Path to where files have been downloaded
    global download_path
    download_path = ''
    path_list = os.getcwd().split('\\')[:3]

    for item in path_list:
        download_path = download_path + item + '\\'

    download_path = download_path + 'Downloads'

    print(download_path)


def assure_path_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)


def extract_zipped_files_to_cwd(path_to_downloaded_files):
    global folder_path_all_files
    folder_path_all_files = os.getcwd() + '\\' + 'Extracted Files'
    zip_ref = zipfile.ZipFile(path_to_downloaded_files, 'r')
    assure_path_exists(folder_path_all_files)
    zip_ref.extractall(folder_path_all_files)
    zip_ref.close()


def fillNAN_orig(df):
    df['fico'] = df['fico'].fillna(0)
    df['flag_fthb'] = df['flag_fthb'].fillna('X')
    df['cd_msa'] = df['cd_msa'].fillna(0)
    df['mi_pct'] = df['mi_pct'].fillna(0)
    df['cnt_units'] = df['cnt_units'].fillna(0)
    df['occpy_sts'] = df['occpy_sts'].fillna('X')
    df['cltv'] = df['cltv'].fillna(0)
    df['dti'] = df['dti'].fillna(0)
    df['ltv'] = df['ltv'].fillna(0)
    df['channel'] = df['channel'].fillna('X')
    df['ppmt_pnlty'] = df['ppmt_pnlty'].fillna('X')
    df['prop_type'] = df['prop_type'].fillna('XX')
    df['zipcode'] = df['zipcode'].fillna(0)
    df['loan_purpose'] = df['loan_purpose'].fillna('X')
    df['cnt_borr'] = df['cnt_borr'].fillna(0)
    df['flag_sc'] = df['flag_sc'].fillna('N')
    return df


def changedatatype_orig(df):
    # Change the data types for all column
    df[['fico', 'cd_msa', 'mi_pct', 'cnt_borr', 'cnt_units', 'cltv', 'dti', 'orig_upb', 'ltv', 'zipcode',
        'orig_loan_term']] = df[['fico', 'cd_msa', 'mi_pct', 'cnt_borr', 'cnt_units', 'cltv', 'dti', 'orig_upb', 'ltv', 'zipcode','orig_loan_term']].astype('int64')
    df[['flag_sc', 'servicer_name']] = df[['flag_sc', 'servicer_name']].astype('str')
    return df

def createOriginationCombined(sample_orig_files):
    writeHeader1 = True
    if "sample" in sample_orig_files:
        filename = "Sample Origination Combined.csv"

    abc = glob.glob(sample_orig_files)

    with open(filename, 'w', encoding='utf-8', newline="") as file:
        for f in abc:
            sample_df = pd.read_csv(f, sep="|",
                                    names=['fico', 'dt_first_pi', 'flag_fthb', 'dt_matr', 'cd_msa', "mi_pct",
                                           'cnt_units', 'occpy_sts', 'cltv', 'dti', 'orig_upb', 'ltv', 'int_rt',
                                           'channel', 'ppmt_pnlty', 'prod_type', 'st', 'prop_type', 'zipcode',
                                           'id_loan', 'loan_purpose', 'orig_loan_term', 'cnt_borr', 'seller_name',
                                           'servicer_name', 'flag_sc'], skipinitialspace=True, low_memory=False)
            sample_df = fillNAN_orig(sample_df)
            sample_df = changedatatype_orig(sample_df)
            sample_df['Year'] = ['19' + x if x == '99' else '20' + x for x in
                                 (sample_df['id_loan'].apply(lambda x: x[2:4]))]
            if writeHeader1 is True:
                sample_df.to_csv(file, mode='a', header=True, index=False)
                writeHeader1 = False
            else:
                sample_df.to_csv(file, mode='a', header=False, index=False)


def fillNA_performance(df):
    df['current_upb'] = df['current_upb'].fillna(0)
    df['delq_sts'] = df['delq_sts'].fillna('XX')
    df['loan_age'] = df['loan_age'].fillna(-1)
    df['mths_remng'] = df['mths_remng'].fillna(-1)
    df['repch_flag'] = df['repch_flag'].fillna('X')
    df['flag_mod'] = df['flag_mod'].fillna('N')
    df['cd_zero_bal'] = df['cd_zero_bal'].fillna(-1)
    df['dt_zero_bal'] = df['dt_zero_bal'].fillna('189901')
    df['current_int_rt'] = df['current_int_rt'].fillna(0)
    df['current_dfr_upb'] = df['current_dfr_upb'].fillna(0)
    df['dt_lst_pi'] = df['dt_lst_pi'].fillna('189901')
    df['mi_recoveries'] = df['mi_recoveries'].fillna(0)
    df['net_sale_proceeds'] = df['net_sale_proceeds'].fillna('U')
    df['non_mi_recoveries'] = df['non_mi_recoveries'].fillna(0)
    df['expenses'] = df['expenses'].fillna(0)
    df['legal_costs'] = df['legal_costs'].fillna(0)
    df['maint_pres_costs'] = df['maint_pres_costs'].fillna(0)
    df['taxes_ins_costs'] = df['taxes_ins_costs'].fillna(0)
    df['misc_costs'] = df['misc_costs'].fillna(0)
    df['actual_loss'] = df['actual_loss'].fillna(0)
    df['modcost'] = df['modcost'].fillna(0)
    df['step_mod_flag'] = df['step_mod_flag'].fillna('X')
    df['def_py_mod'] = df['def_py_mod'].fillna('X')
    df['eltv'] = df['eltv'].fillna(0)
    return df


# Helper Functions for Performance File
def get_current_upb(group):
    return {'min_current_upb': group.min(), 'max_current_upb': group.max()}


def get_delq_sts(group):
    return {'min_delq_sts': group.min(), 'max_delq_sts': group.max()}


def get_cd_zero_bal(group):
    return {'min_cd_zero_bal': group.min(), 'max_cd_zero_bal': group.max()}


def get_mi_recoveries(group):
    return {'min_mi_recoveries': group.min(), 'max_mi_recoveries': group.max()}


def get_net_sale_proceeds(group):
    return {'min_net_sale_proceeds': group.min(), 'max_net_sale_proceeds': group.max()}


def get_non_mi_recoveries(group):
    return {'min_non_mi_recoveries': group.min(), 'max_non_mi_recoveries': group.max()}


def get_expenses(group):
    return {'min_expenses': group.min(), 'max_expenses': group.max()}


def get_legal_costs(group):
    return {'min_legal_costs': group.min(), 'max_legal_costs': group.max()}


def get_maint_pres_costs(group):
    return {'min_maint_pres_costs': group.min(), 'max_maint_pres_costs': group.max()}


def get_taxes_ins_costs(group):
    return {'min_taxes_ins_costs': group.min(), 'max_taxes_ins_costs': group.max()}


def get_misc_costs(group):
    return {'min_misc_costs': group.min(), 'max_misc_costs': group.max()}


def get_actual_loss(group):
    return {'min_actual_loss': group.min(), 'max_actual_loss': group.max()}


def get_modcost(group):
    return {'min_modcost': group.min(), 'max_modcost': group.max()}


def changedatatype_performance(df):
    # Change the data types for all column
    df[['loan_seq', 'delq_sts', 'repch_flag', 'flag_mod', 'net_sale_proceeds', 'step_mod_flag', 'def_py_mod']] = df[['loan_seq', 'delq_sts', 'repch_flag', 'flag_mod', 'net_sale_proceeds', 'step_mod_flag', 'def_py_mod']].astype('str')
    df[['mth_per', 'loan_age', 'mths_remng', 'dt_zero_bal']] = df[['mth_per', 'loan_age', 'mths_remng', 'dt_zero_bal']].astype('int64')
    df[['current_upb', 'cd_zero_bal', 'current_int_rt', 'current_dfr_upb', 'dt_lst_pi', 'mi_recoveries','non_mi_recoveries', 'expenses', 'legal_costs', 'maint_pres_costs', 'taxes_ins_costs', 'misc_costs','actual_loss', 'modcost']] = df[['current_upb', 'cd_zero_bal', 'current_int_rt', 'current_dfr_upb', 'dt_lst_pi', 'mi_recoveries','non_mi_recoveries', 'expenses', 'legal_costs', 'maint_pres_costs', 'taxes_ins_costs', 'misc_costs','actual_loss', 'modcost']].astype('float32')
    return df

def createPerformanceCombined(sample_perf_files):
    writeHeader2 = True
    if "sample" in sample_perf_files:
        filename = "Sample Performance Combined Summary.csv"

    abc = glob.glob(sample_perf_files)

    with open(filename, 'w', encoding='utf-8', newline="") as file:
        for f in abc:
            perf_df = pd.read_csv(f, sep='|',
                                  names=['loan_seq', 'mth_per', 'current_upb', 'delq_sts', 'loan_age', 'mths_remng',
                                         'repch_flag', 'flag_mod', 'cd_zero_bal', 'dt_zero_bal', 'current_int_rt',
                                         'current_dfr_upb', 'dt_lst_pi', 'mi_recoveries', 'net_sale_proceeds',
                                         'non_mi_recoveries', 'expenses', 'legal_costs', 'maint_pres_costs',
                                         'taxes_ins_costs', 'misc_costs', 'actual_loss', 'modcost', 'step_mod_flag',
                                         'def_py_mod', 'eltv'], skipinitialspace=False, low_memory=False)

            perf_df = fillNA_performance(perf_df)
            perf_df = changedatatype_performance(perf_df)
            summ_df = pd.DataFrame()
            summ_df['loan_seq'] = perf_df['loan_seq'].drop_duplicates()
            summ_df = summ_df.join(
                (perf_df['current_upb'].groupby(perf_df['loan_seq']).apply(get_current_upb).unstack()), on='loan_seq')
            summ_df = summ_df.join((perf_df['delq_sts'].groupby(perf_df['loan_seq']).apply(get_delq_sts).unstack()),
                                   on='loan_seq')
            summ_df = summ_df.join(
                (perf_df['cd_zero_bal'].groupby(perf_df['loan_seq']).apply(get_cd_zero_bal).unstack()), on='loan_seq')
            summ_df = summ_df.join(
                (perf_df['non_mi_recoveries'].groupby(perf_df['loan_seq']).apply(get_non_mi_recoveries).unstack()),
                on='loan_seq')
            summ_df = summ_df.join((perf_df['expenses'].groupby(perf_df['loan_seq']).apply(get_expenses).unstack()),
                                   on='loan_seq')
            summ_df = summ_df.join(
                (perf_df['legal_costs'].groupby(perf_df['loan_seq']).apply(get_legal_costs).unstack()), on='loan_seq')
            summ_df = summ_df.join(
                (perf_df['maint_pres_costs'].groupby(perf_df['loan_seq']).apply(get_maint_pres_costs).unstack()),
                on='loan_seq')
            summ_df = summ_df.join(
                (perf_df['taxes_ins_costs'].groupby(perf_df['loan_seq']).apply(get_taxes_ins_costs).unstack()),
                on='loan_seq')
            summ_df = summ_df.join((perf_df['misc_costs'].groupby(perf_df['loan_seq']).apply(get_misc_costs).unstack()),
                                   on='loan_seq')
            summ_df = summ_df.join(
                (perf_df['actual_loss'].groupby(perf_df['loan_seq']).apply(get_actual_loss).unstack()), on='loan_seq')
            summ_df = summ_df.join((perf_df['modcost'].groupby(perf_df['loan_seq']).apply(get_modcost).unstack()),
                                   on='loan_seq')

            if writeHeader2 is True:
                summ_df.to_csv(file, mode='a', header=True, index=False)
                writeHeader2 = False
            else:
                summ_df.to_csv(file, mode='a', header=False, index=False)

def validate_year(year):
    try:
        year = int(year)
    except:
        print('Cannot Parse Year to Integer')
        exit(0)

    if not year in [2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017]:
        print('Data unavailabale for the requested year')
        exit(0)
    else:
        return year


def main():
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d_%H%M%S')
    args = sys.argv[1:]

    print("Starting")

    counter = 0
    if len(args) == 0:
        print("No input arguments..Exiting!")
        exit(0)

    for arg in args:
        if counter == 0:
            user = str(arg)
        elif counter == 1:
            password = str(arg)
        elif counter == 2:
            startyear = str(arg)
        elif counter == 3:
            endyear = str(arg)
        counter += 1

    print("Email Address: " + user)
    print("Password: " + password)

    navigate(user, password)
    # navigate()
    startyear = validate_year(startyear)
    endyear = validate_year(endyear)
    download_all_files(startyear, endyear)
    # download_all_files()

    for file in file_names:
        extract_zipped_files_to_cwd(download_path + '\\' + file)

    print('Path where all files have been extracted : {}'.format(folder_path_all_files))

    createOriginationCombined(folder_path_all_files + "/sample_orig_*.txt")
    createPerformanceCombined(folder_path_all_files + "/sample_svcg_*.txt")

if __name__ == '__main__':
    main()