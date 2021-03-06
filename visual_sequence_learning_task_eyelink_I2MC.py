# -*- coding: utf-8 -*-
"""

Created on Sat Sep 25 10:54:00 2020

@author: Sebastian Moyano

PhD Candidate at the Developmental Cognitive Neuroscience Lab (labNCd)
Center for Mind, Brain and Behaviour (CIMCYC)
University of Granada (UGR)
Granada, Spain

Description:
Set of functions to import txt data files from EyeLink, apply I2MC function
and compute scores for the visual sequence learning task.
"""

# =============================================================================
# IMPORT LIBRARIES
# =============================================================================

import pandas as pd
import os
# I2MC function could be found in Roy Hessels GitHub
from I2MC_functions import *

# =============================================================================
# SET PARAMETERS
# =============================================================================

# directory of each sample report

directory_blackscreen = 'C:/.../'
directory_reactive = 'C:/.../'
directory_results = 'C:/.../'
directories = [directory_blackscreen, directory_reactive]

# rows to skip when loading data
nskip = 1

# specify parameters
options = {'xres': 1920,        # screen resolution x axis
           'yres': 1080,        # screen resolution y axis
           'freq': 500,         # sampling rate
           'missingx': 99999,   # missing values x axis
           'missingy': 99999,   # missing values y axis
           'scrSz': [52, 30],   # screen size (cm)
           'disttoscreen': 60,  # distance to screen (cm)
           'minFixDur': 100}    # fixation minimum duration

columns = {'trial_start_time': 'TRIAL_START_TIME',      # trial start time column name
           'sample_time': 'TIME',                       # sample time column name
           'timestamp': 'TIMESTAMP',                    # timestamp column name
           'right_gaze_x': 'RIGHT_GAZE_X',              # x axis coordinates right gaze column name
           'right_gaze_y': 'RIGHT_GAZE_Y',              # y axis coordinates right gaze column name
           'left_gaze_x': 'LEFT_GAZE_X',                # x axis coordinates left gaze column name
           'left_gaze_y': 'LEFT_GAZE_Y',                # y axis coordinates left gaze column name
           'trial': 'TRIAL_INDEX',                      # trial column name
           'target_loc': 'position'}                    # target location column name

AOIs = {'x_left_AOI': [0, 764],         # x coordinates for left AOI
        'y_left_AOI': [0, 1080],        # y coordinates for left AOI
        'x_right_AOI': [1156, 1920],    # x coordinates for right AOI
        'y_right_AOI': [0, 1080],       # y coordinates for right AOI
        'x_central_AOI': [764, 1156],   # x coordinates for central AOI
        'y_central_AOI': [0, 1080],     # y coordinates for central AOI
        'x_upper_left_AOI': [ , ],      # x coordinates for upper left AOI
        'y_upper_left_AOI': [ , ],      # y coordinates for upper left AOI
        'x_upper_right_AOI': [ , ],     # x coordinates for upper right AOI
        'y_upper_right_AOI': [ , ],     # y coordinates for upper right AOI
        'x_bottom_central_AOI': [ , ],  # x coordinates for bottom central AOI
        'y_bottom_central_AOI': [ , ]}  # y coordinates for bottom central AOI


# dictionary with sequences per trial (key = trial, value = sequence)
dict_sequences = {1: 1, 2: 1, 3: 2, 4: 2, 5: 3, 6: 3, 7: 4, 8: 4, 9: 5, 10: 5, 11: 6, 12: 6, 13: 7, 14: 7, 15: 8, 16: 8,
                  17: 9, 18: 9, 19: 10, 20: 10, 21: 11, 22: 11, 23: 12, 24: 12}

dict_sequences_9m = {1: 1, 2: 1, 3: 1, 4: 2, 5: 2, 6: 2, 7: 3, 8: 3, 9: 3, 10: 4, 11: 4, 12: 4, 13: 5, 14: 5, 15: 5,
                     16: 6, 17: 6, 18: 6, 19: 7, 20: 7, 21: 7, 22: 8, 23: 8, 24: 8, 25: 9, 26: 9, 27: 9, 28: 10, 29: 10,
                     30: 10, 31: 11, 32: 11, 33: 11, 34: 12, 35: 12, 36: 12, 37: 13, 38: 13, 39: 13, 40: 14, 41: 14,
                     42: 14, 43: 15, 44: 15, 45: 15, 46: 16, 47: 16, 48: 16}

dict_sequences_16m = {1: 1, 2: 1, 3: 1, 4: 1, 5: 2, 6: 2, 7: 2, 8: 2, 9: 3, 10: 3, 11: 3, 12: 3, 13: 4, 14: 4, 15: 4,
                      16: 4, 17: 5, 18: 5, 19: 5, 20: 5, 21: 6, 22: 6, 23: 6, 24: 6, 25: 7, 26: 7, 27: 7, 28: 7, 29: 8,
                      30: 8, 31: 8, 32: 8, 33: 9, 34: 9, 35: 9, 36: 9, 37: 10, 38: 10, 39: 10, 40: 10, 41: 11,  42: 11,
                      43: 11, 44: 11, 45: 12, 46: 12, 47: 12, 48: 12, 49: 13, 50: 13, 51: 13, 52: 13, 53: 14, 54: 14,
                      55: 14, 56: 14, 57: 15, 58: 15, 59: 15, 60: 15, 61: 16, 62: 16, 63: 16, 64: 16}

# dictionary with trials per subgroup of data
dict_subgroups = {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 2, 8: 2, 9: 2, 10: 2, 11: 2, 12: 2, 13: 3, 14: 3, 15: 3, 16: 3,
                  17: 3, 18: 3, 19: 4, 20: 4, 21: 4, 22: 4, 23: 4, 24: 4}

dict_subgroups_9m = {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 2, 14: 2, 15: 2,
                     16: 2, 17: 2, 18: 2, 19: 2, 20: 2, 21: 2, 22: 2, 23: 2, 24: 2, 25: 3, 26: 3, 27: 3, 28: 3, 29: 3,
                     30: 3, 31: 3, 32: 3, 33: 3, 34: 3, 35: 3, 36: 3, 37: 4, 38: 4, 39: 4, 40: 4, 41: 4, 42: 4, 43: 4,
                     44: 4, 45: 4, 46: 4, 47: 4, 48: 4}

dict_subgroups_16m = {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1,
                      16: 1, 17: 2, 18: 2, 19: 2, 20: 2, 21: 2, 22: 2, 23: 2, 24: 2, 25: 2, 26: 2, 27: 2, 28: 2, 29: 2,
                      30: 2, 31: 2, 32: 2, 33: 3, 34: 3, 35: 3, 36: 3, 37: 3, 38: 3, 39: 3, 40: 3, 41: 3,  42: 3, 43: 3,
                      44: 3, 45: 3, 46: 3, 47: 3, 48: 3, 49: 3, 50: 3, 51: 3, 52: 3, 53: 4, 54: 4, 55: 4, 56: 4, 57: 4,
                      58: 4, 59: 4, 60: 4, 61: 4, 62: 4, 63: 4, 64: 4}

# =============================================================================
# IMPORT FUNCTION (EYELINK 1000 PLUS)
# =============================================================================


def import_eyelink1000Plus(fname):

    """
    Imports txt files as Pandas DataFrame and creates the Timestamp

    Input:
        fname: directory with name of the file

    Output:
        DataFrame with loaded data for a single participant

    Notes:
        Eyelink Support: once the distance is beyond a range that allows for the
        distance to be recorded, you will end up with the value -3276.8, rather
        than just a dot (empty field). However, x and y gaze coordinates are
        reported as missing values "."

        If R or L_IN_BLINK = 1, gaze position is reported as an empty field (Data
        Viewer outputs empty fields as a dot by default), so all cells containing
        gaze-position-related values will be empty
    """

    loaded_data = pd.read_csv(fname, sep='\t', header=0, index_col=False, decimal=',')

    loaded_data[columns['sample_time']] = loaded_data[columns['timestamp']] - loaded_data[columns['trial_start_time']]
    
    return loaded_data

# =============================================================================
#  TRIAL SELECTION FUNCTION
# =============================================================================


def trial_selection(imported_data):

    """
    Split the data file per trial and apply the I2MC function before convert
    data into numpy arrays. At the end maps the position of the target for
    each trial.

    If X or Y gaze coordinates are more than 1 monitor away it is considered
    as missing data.

    Iterates over TRIAL_INDEX set. We create a set as we have multiple
    sample per trial. We need the list use get_group() to group by the
    data by trial (TRIAL_INDEX is an integer number, not string)

    Input:
        imported_data: DataFrame with loaded data for participant

    Output:
        f_fix: data with fixations information for a single file
        f_data: raw data used in the I2MC function for a single file
    """

    data = {}
    imported_data = imported_data.copy(deep=True)
    f_fix = None
    f_data = None
    t_fix = None
    t_data = None
    trials = set(imported_data[columns['trial']])
    min_trial = min(set(imported_data[columns['trial']]))

    # we can use set as it is ordered from 1 to 24, it doesn't have missing trials
    for trial in trials:
        loaded_data = imported_data.groupby([columns['trial']]).get_group(trial)
        print('Currently working on trial: ' + str(trial))
           
        data['time'] = loaded_data[columns['sample_time']].to_numpy()    # timestamp
        data['L_X'] = loaded_data[columns['left_gaze_x']].to_numpy()     # left gaze x axis
        data['L_Y'] = loaded_data[columns['left_gaze_y']].to_numpy()     # left gaze y axis
        data['R_X'] = loaded_data[columns['right_gaze_x']].to_numpy()    # right gaze x axis
        data['R_Y'] = loaded_data[columns['right_gaze_y']].to_numpy()    # right gaze y axis
        data['trial'] = loaded_data[columns['trial']].to_numpy()         # trial
        data['position'] = loaded_data[columns['target_loc']]            # stimulus location
        
        # Left eye
        lMiss1 = np.logical_or(data['L_X'] < -options['xres'], data['L_X'] > 2*options['xres'])
        lMiss2 = np.logical_or(data['L_Y'] < -options['yres'], data['L_Y'] > 2*options['yres'])
        lMiss = np.logical_or(lMiss1, lMiss2)
        data['L_X'][lMiss] = options['missingx']
        data['L_Y'][lMiss] = options['missingy']
        
        # right eye
        rMiss1 = np.logical_or(data['R_X'] < -options['xres'], data['R_X'] > 2*options['xres'])
        rMiss2 = np.logical_or(data['R_Y'] < -options['yres'], data['R_Y'] > 2*options['yres'])
        rMiss = np.logical_or(rMiss1, rMiss2)
        data['R_X'][rMiss] = options['missingx']
        data['R_Y'][rMiss] = options['missingy']
        
        I2MC_fix, I2MC_data, I2MC_options = I2MC(data, options)
        
        if trial == min_trial:
            f_fix = pd.DataFrame(I2MC_fix)
            f_data = pd.DataFrame(I2MC_data)
            f_fix['trial'] = trial
            f_data['trial'] = trial
        else:
            t_fix = pd.DataFrame(I2MC_fix)  # in each iteration it creates a temporal dataframe
            t_data = pd.DataFrame(I2MC_data)
            t_fix['trial'] = trial
            t_data['trial'] = trial
            f_fix = pd.concat([f_fix, t_fix], axis=0)
            f_data = pd.concat([f_data, t_data], axis=0)
                    
        t_fix = pd.DataFrame()
        t_data = pd.DataFrame()
        data = {}
        imported_data = imported_data.copy(deep=True)
        
    return f_fix, f_data

# =============================================================================
#  LOAD FILES
# =============================================================================


def load_files(directory):

    """
    Load all the files names into a list to use it in applyI2MCallfiles function

    Input:
        None

    Output:
        files: list of filenames in the folder
    """

    files = []
    for filename in os.listdir(directory):
        if os.path.isfile(filename) and filename.endswith(".txt") and filename not in files:
            files.append(filename)

    return files

# =============================================================================
#  APPLY FUNCTION I2MC TO ALL FILES IN THE DIRECTORY
# =============================================================================


def apply_I2MC_all_files(directory):

    """
    Import the data for a single participant through importEyelink1000Plus function.
    Apply I2MC function to every trial using trial_selection function, and adds
    the participant's code slicing from the filename.

    Iterate over all the files in the folder and apply functions. Concatenate
    results for all files in a single DataFrame.

    Input:
        directory: directory with files

    Output:
        f_fixations: DataFrame with fixation data for all the files
        f_data: DataFrame with raw data used in the I2MC function for all the files
        files: list of files in the folder
    """

    files = load_files(directory)
    f_fixations = None
    f_data = None

    for filename in files:
        fname = directory + '/' + filename
        imported_data = import_eyelink1000Plus(fname)

        print('Yay! Applying I2MC function to participant ' + str(filename))

        fixations, data = trial_selection(imported_data)

        if files[0] == filename:
            f_fixations = fixations
            f_data = data
            f_fixations['subject'] = filename[11:18]
            f_data['subject'] = filename[11:18]
        else:
            t_fixations = fixations
            t_data = data
            t_fixations['subject'] = filename[11:18]
            t_data['subject'] = filename[11:18]
            f_fixations = pd.concat([f_fixations, t_fixations], axis=0)
            f_data = pd.concat([f_data, t_data], axis=0)
        
        t_fixations = pd.DataFrame()
        t_data = pd.DataFrame()
    
    f_fixations.reset_index(drop=True, inplace=True)
    
    return f_fixations, f_data, files

# =============================================================================
#  DETERMINE AOI FIXATION
# =============================================================================


def AOI_fixation(f_fixations):

    """
    Provides fixation (position 1 or position 2) per data sample.

    Input:
        f_fixations: DataFrame with fixations data after I2MC function

    Output:
        df_fix_aoi: DataFrame with AOI fixations data added

    Notes:
        Left and right AOI cover all the y axis and part of the x axis.
    """

    # x and y coordinates inside screen
    condition_in_screen_xpos = (f_fixations['xpos'] > 0) & (f_fixations['xpos'] < options['xres'])
    condition_in_screen_ypos = (f_fixations['ypos'] > 0) & (f_fixations['ypos'] < options['yres'])
    # x and y coordinates for left AOI
    condition_in_left_xpos = (f_fixations['xpos'] > AOIs['x_left_AOI'][0]) & (f_fixations['xpos'] <= AOIs['x_left_AOI'][1])
    # x and y coordinates for right AOI
    condition_in_right_xpos = (f_fixations['xpos'] >= AOIs['x_right_AOI'][0]) & (f_fixations['xpos'] < AOIs['x_right_AOI'][1])
    # x and y coordinates for central AOI
    condition_in_central_xpos = (f_fixations['xpos'] > AOIs['x_central_AOI'][0]) & (f_fixations['xpos'] < AOIs['x_central_AOI'][1])
    # general conditions
    condition_in_screen = condition_in_screen_xpos & condition_in_screen_ypos
    # masks
    mask_in_left = condition_in_screen & condition_in_left_xpos
    mask_in_right = condition_in_screen & condition_in_right_xpos
    mask_in_central = condition_in_screen & condition_in_central_xpos
    # label fixations AOIs
    f_fixations['AOI_fix'] = ''
    f_fixations.loc[mask_in_left, 'AOI_fix'] = 1
    f_fixations.loc[mask_in_right, 'AOI_fix'] = 2
    f_fixations.loc[mask_in_central, 'AOI_fix'] = 0

    df_fix_aoi = f_fixations.copy(deep=True)

    return df_fix_aoi


def AOI_fixation_3pos(f_fixations):

    """
    Provides fixation (position 1, 2 or 3) per data sample.

    Input:
        f_fixations: DataFrame with fixations data after I2MC function

    Output:
        df_fix_aoi: DataFrame with AOI fixations data added

    """

    # x and y coordinates inside screen
    condition_in_screen_xpos = (f_fixations['xpos'] > 0) & (f_fixations['xpos'] < options['xres'])
    condition_in_screen_ypos = (f_fixations['ypos'] > 0) & (f_fixations['ypos'] < options['yres'])
    # x and y coordinates for upper left AOI
    condition_in_upper_left_xpos = (f_fixations['xpos'] > AOIs['x_upper_left_AOI'][0]) & \
                                   (f_fixations['xpos'] <= AOIs['x_upper_left_AOI'][1])
    condition_in_upper_left_ypos = (f_fixations['xpos'] > AOIs['y_upper_left_AOI'][0]) & \
                                   (f_fixations['xpos'] <= AOIs['y_upper_left_AOI'][1])
    # x and y coordinates for upper right AOI
    condition_in_upper_right_xpos = (f_fixations['xpos'] >= AOIs['x_upper_right_AOI'][0]) & \
                                    (f_fixations['xpos'] < AOIs['x_upper_right_AOI'][1])
    condition_in_upper_right_ypos = (f_fixations['xpos'] >= AOIs['y_upper_right_AOI'][0]) & \
                                    (f_fixations['xpos'] < AOIs['y_upper_right_AOI'][1])
    # x and y coordinates for bottom central AOI
    condition_in_bottom_central_xpos = (f_fixations['xpos'] > AOIs['x_bottom_central_AOI'][0]) & \
                                       (f_fixations['xpos'] < AOIs['x_bottom_central_AOI'][1])
    condition_in_bottom_central_ypos = (f_fixations['xpos'] > AOIs['y_bottom_central_AOI'][0]) & \
                                       (f_fixations['xpos'] < AOIs['y_bottom_central_AOI'][1])
    # general conditions
    condition_in_screen = condition_in_screen_xpos & condition_in_screen_ypos
    condition_in_upper_left = condition_in_upper_left_xpos & condition_in_upper_left_ypos
    condition_in_upper_right = condition_in_upper_right_xpos & condition_in_upper_right_ypos
    condition_in_bottom_central = condition_in_bottom_central_xpos & condition_in_bottom_central_ypos
    # masks
    mask_in_upper_left = condition_in_screen & condition_in_upper_left
    mask_in_upper_right = condition_in_screen & condition_in_upper_right
    mask_in_bottom_central = condition_in_screen & condition_in_bottom_central
    # label fixations AOIs
    f_fixations['AOI_fix'] = ''
    f_fixations.loc[mask_in_upper_left, 'AOI_fix'] = 1
    f_fixations.loc[mask_in_upper_right, 'AOI_fix'] = 2
    f_fixations.loc[mask_in_bottom_central, 'AOI_fix'] = 3

    df_fix_aoi = f_fixations.copy(deep=True)

    return df_fix_aoi

# =============================================================================
#  REDUCE DATA
# =============================================================================


def reduce_data(df_fix_aoi):

    """
    Computes mean fixation duration and total fixation time from the number
    of fixations registered per trial and AOI.

    Input:
        df_fix_aoi: DataFrame with AOI fixations data

    Output:
        df_trial_reduced: reduced data with statistics computed
    """

    df_trial_reduced = df_fix_aoi.groupby(['subject', 'trial', 'AOI_fix']).agg(sum_fix=('dur', 'sum'),
                                                                               mean_fix=('dur', 'mean'),
                                                                               min_start_time=('startT', 'min'),
                                                                               max_end_time=('endT', 'max'))
    df_trial_reduced.reset_index(drop=False, inplace=True)
    
    return df_trial_reduced

# =============================================================================
#  SETS POSITION OF STIMULUS APPEARANCE
# =============================================================================


def position_stimulus_VSL_6mo(df_trial_reduced):

    """
    Sets stimulus appearance location per trial. Position 1 correspond to the
    central left part of the screen while position 2 to the central right part.

    Input:
        df_trial_reduced: DataFrame with data reduced

    Output:
        df_fix_aoi_reduced_loc: DataFrame with location of stimulus appearance per trial

    Notes:
        In sequences 1-2 only multiples of 2 appear in position 2.
    """

    # masks
    condition_right_target = df_trial_reduced['trial'] % 2 == 0
    condition_left_target = ~condition_right_target

    df_trial_reduced['position'] = ''
    df_trial_reduced.loc[condition_right_target, 'position'] = 2
    df_trial_reduced.loc[condition_left_target, 'position'] = 1

    df_fix_aoi_reduced_loc = df_trial_reduced.copy(deep=True)
    
    return df_fix_aoi_reduced_loc


def position_stimulus_VSL_9mo(df_trial_reduced):
    """
    Sets stimulus appearance location per trial. Position 1 correspond to the
    central left part of the screen while position 2 to the central right part.

    Input:
        df_trial_reduced: DataFrame with data reduced

    Output:
        df_fix_aoi_reduced_loc: DataFrame with location of stimulus appearance per trial

    Notes:
        In sequences 1-1-2 only multiples of 3 appear in position 2.
    """

    # masks
    condition_right_target = df_trial_reduced['trial'] % 3 == 0
    condition_left_target = ~condition_right_target

    df_trial_reduced['position'] = ''
    df_trial_reduced.loc[condition_right_target, 'position'] = 2
    df_trial_reduced.loc[condition_left_target, 'position'] = 1

    df_fix_aoi_reduced_loc = df_trial_reduced.copy(deep=True)

    return df_fix_aoi_reduced_loc


def position_stimulus_VSL_3pos(df_trial_reduced):
    """
    Sets stimulus appearance location per trial for sequences 1-2-1-3.
    Position 1 correspond to the upper left side of the screen, position 2
    to the upper right side and position 3 to the central bottom side.

    Input:
        df_trial_reduced: DataFrame with data reduced

    Output:
        df_fix_aoi_reduced_loc: DataFrame with location of stimulus appearance per trial

    Notes:
        In sequences 1-2-1-3 position 1 is only presented in even trials. However,
        as position 2 and 3 are presented in odd trials, we created list of trials
        for each position, as trials are always fixed to the same position.
    """

    position_2 = [2, 6, 10, 14, 18, 22, 26, 30, 34, 38, 42, 46, 50, 54, 58, 62]
    position_3 = [4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60, 64]

    # masks
    condition_upper_left_target = df_trial_reduced['trial'] % 2 == 1
    condition_upper_right_target = df_trial_reduced['trial'] in position_2
    condition_bottom_central_target = df_trial_reduced['trial'] in position_3

    df_trial_reduced['position'] = ''
    df_trial_reduced.loc[condition_upper_left_target, 'position'] = 1
    df_trial_reduced.loc[condition_upper_right_target, 'position'] = 2
    df_trial_reduced.loc[condition_bottom_central_target, 'position'] = 3

    df_fix_aoi_reduced_loc = df_trial_reduced.copy(deep=True)

    return df_fix_aoi_reduced_loc

# =============================================================================
#  PROCESS FILES FOR ANTICIPATORY AND REACTIVE PERIOD
# =============================================================================


def process_files():
    """
    Process file (blackscreen and reactive) applying I2MC function to every
    file. Drop rows with unused AOIs through the reduction process and
    maps sequences and subgroups into the dfs.

    Input:
        None

    Output:
        df_blackscreen: DataFrame with processed fixations in the anticipatory period
        df_reactive: DataFrame with processed fixations in the reactive period
    """
    for directory in directories:

        os.chdir(directory)
        # apply I2MC function to each group of samples per trial and participant
        df_data_fixations, df_data_raw, files = apply_I2MC_all_files(directory)
        # get fixations in each AOI
        df_aoi_fixations = AOI_fixation(df_data_fixations)
        # get mean fixation duration and total fixation duration per trial and AOI
        # returns DataFrame with data per trial and AOI
        df_trial_reduced = reduce_data(df_aoi_fixations)
        # sets position of stimulus appearance per trial
        df_fix_aoi_reduced_loc = position_stimulus_VSL_6mo(df_trial_reduced)

        data_blackscreen = []
        data_reactive = []

        if directory == directory_blackscreen:

            results_dir = os.path.join(directory, 'AnalyzedI2MC')
            # if the directory doesn't exist, this loop creates it
            if not os.path.isdir(results_dir):
                os.makedirs(results_dir)

            data_blackscreen.append(df_fix_aoi_reduced_loc)
            df_blackscreen = pd.concat(data_blackscreen, ignore_index=True)
            df_blackscreen.to_csv(os.path.join(results_dir, 'blackscreen_processed.txt'), sep=';', decimal=',')

        elif directory == directory_reactive:

            results_dir = os.path.join(directory, 'AnalyzedI2MC')
            # if the directory doesn't exist, this loop creates it
            if not os.path.isdir(results_dir):
                os.makedirs(results_dir)

            data_reactive.append(df_fix_aoi_reduced_loc)
            df_reactive = pd.concat(data_reactive, ignore_index=True)
            df_reactive.to_csv(os.path.join(results_dir, 'reactive_processed.txt'), sep=';', decimal=',')

    df_blackscreen = df_blackscreen.apply(pd.to_numeric, errors='ignore')
    df_reactive = df_reactive.apply(pd.to_numeric, errors='ignore')

    # drop rows with missing in AOI fix and central AOI
    condition_drop_reactive = (df_reactive['AOI_fix'].isnull()) | (df_reactive['AOI_fix'] == 0)
    condition_drop_blackscreen = (df_blackscreen['AOI_fix'].isnull()) | (df_blackscreen['AOI_fix'] == 0)
    # drop
    df_blackscreen = df_blackscreen.drop(df_blackscreen[condition_drop_blackscreen].index).reset_index(drop=True)
    df_reactive = df_reactive.drop(df_reactive[condition_drop_reactive].index).reset_index(drop=True)
    # map sequences and subgroups in dfs
    for df in [df_blackscreen, df_reactive]:
        df['sequence'] = df['trial'].map(dict_sequences)
        df['subgroup'] = df['trial'].map(dict_subgroups)

    return df_blackscreen, df_reactive


# =============================================================================
#  LABEL CORRECT REACTIVE FIXATIONS
# =============================================================================


def correct_reactive(reactive):

    """
    Sets correct reactive fixations to the stimulus location of appearance,
    and compute the number of correct fixations per participant. A dictionary
    with the number of reactive fixations per participant is returned for it
    use it in the statistics function.

    Input:
        reactive: DataFrame with fixations in the reactive period

    Output:
        df_reactive_completed: DataFrame with correct reactive fixations
                               in the reactive period and the number of
                               correct reactive fixations per participant
        dict_reactive_by_subject: dictionary with the number of reactive
                                  fixations per participant as values and
                                  participant's ID as keys.
    """

    reactive['correct_reactive'] = 0

    # conditions
    condition_reactive_correct_left = (reactive['AOI_fix'] == 1) & (reactive['position'] == 1)
    condition_reactive_correct_right = (reactive['AOI_fix'] == 2) & (reactive['position'] == 2)
    # general condition
    condition_reactive = condition_reactive_correct_left | condition_reactive_correct_right
    # label correct reactive looks
    reactive.loc[condition_reactive, 'correct_reactive'] = 1
    # count number of reactive looks by subject
    reactive_correct = df_reactive.groupby(['subject']).agg(n_reactive=('correct_reactive', 'sum'))
    reactive_correct.reset_index(drop=False, inplace=True)
    # count number of reactive looks by subject and subgroup
    reactive_correct_subgroup = df_reactive.groupby(['subject', 'subgroup']).agg(n_reactive=('correct_reactive', 'sum'))
    reactive_correct_subgroup.reset_index(drop=False, inplace=True)
    # create dictionaries
    dict_reactive_by_subject = dict(zip(reactive_correct.subject, reactive_correct.n_reactive))
    dict_reactive_by_subject_subgroup = dict(zip(zip(reactive_correct_subgroup.subject,
                                                     reactive_correct_subgroup.subgroup),
                                                 reactive_correct_subgroup.n_reactive))

    df_reactive_completed = df_reactive.copy(deep=True)

    return df_reactive_completed, dict_reactive_by_subject, dict_reactive_by_subject_subgroup

# =============================================================================
#  FIND THE TRIAL IN WHICH THE SECOND SEQUENCE ATTENDED IS ACHIEVED
# =============================================================================


def second_sequence_attended(reactive_completed):

    """
    Computes the trial in which the participant reaches the second sequence
    attended (four consecutive trials with reactive fixations)

    Input:
        reactive_completed: DataFrame with correct fixations in the reactive
                            period

    Output:
        df_second_sequence_attended: DataFrame with the trial in which the second
                                     sequence attended is achieved per participant
    """

    # we just need trials with correct reactive gaze to validate anticipations
    reactive_just_correct = reactive_completed.query('correct_reactive == 1')
    # dictionary that stores all the sequences of each subject in which the actual
    # and previous trial was attended (diff(1) == 1 in 1 steps). The trial number
    # stored indicates the attended trial and also the previous (i.e. for
    # trial 2 stored, trial 2 and 1 was attended)
    dict_sequences_attended = reactive_just_correct.loc[reactive_just_correct.groupby(['subject'])['trial'].diff(1)
                                                        == 1, ('subject', 'trial')].to_dict(orient='record')

    # convert this dictionary into a df
    df_sequences_attended = pd.DataFrame.from_dict(dict_sequences_attended)
    df_sequences_attended['diff_rows'] = df_sequences_attended.groupby(['subject']).diff(1)

    # df with second sequence attended
    df_compute_second_sequence = df_sequences_attended.diff_rows.eq(1).where(df_sequences_attended.diff_rows.isna().
                                                                             shift())
    df_second_sequence_attended = df_sequences_attended.loc[df_compute_second_sequence.eq(0) |
                                                            df_compute_second_sequence.eq(1).shift()]

    df_second_sequence_attended = df_second_sequence_attended.dropna(axis=0)
    df_second_sequence_attended = df_second_sequence_attended.rename(columns={'trial': 'trial_second_sequence_attended'})
    df_second_sequence_attended = df_second_sequence_attended.drop(labels='diff_rows', axis=1)
    df_second_sequence_attended = df_second_sequence_attended.reset_index(drop=True)

    return df_second_sequence_attended


# =============================================================================
#  REMOVE TRIALS BEFORE THE SECOND SEQUENCE ATTENDED IS ACHIEVED
# =============================================================================


def remove_trials_before_second_sequence_attended(df_second_sequence_attended, df_reactive_completed, df_blackscreen):

    """
    Removes all trials before the second sequence attended is achieved
    from the reactive period DataFrame. Counts the number of trials that
    remain after the removal and adds the trial in which the second sequence
    is reached.
    Merges the reactive period DataFrame after the removal with the blackscreen
    DataFrame period in an inner merge.

    Input:
        df_second_sequence_attended: DataFrame with the trial in which
                                     the second sequence attended is achieved.
        df_reactive_completed: DataFrame with correct reactive fixations
        df_blackscreen: DataFrame with fixationd in the anticipatory period.

    Output:
        df_trials_removed_after_second_sequence: DataFrame with the number
                                                  of trials that remain after
                                                  removal
        df_blackscreen_reactive: Merged DataFrames with the correct reactive
                                 fixations after removal and anticipatory
                                 period
    """

    # keep only trials with correct reactive looks
    reactive_correct = df_reactive_completed.query('correct_reactive == 1')
    # set subject as the index in df2
    df_second_sequence_attended.set_index('subject', inplace=True)
    # for df1 groupby subject and agg set onto trial
    df_reactive_set_trials = pd.DataFrame(reactive_correct.groupby('subject')['trial'].agg(set))
    # join the dataframes
    df_join = df_reactive_set_trials.join(df_second_sequence_attended)
    # this is required because set & range don't work with nan
    df_join['trial_second_sequence_attended'].fillna(0, inplace=True)
    # convert trial_n to a set; int is required because range doesn't work with float
    df_join['trial_second_sequence_attended'] = df_join['trial_second_sequence_attended'].apply(lambda x:
                                                                                                set(range(int(x)+1)))
    # take the set difference
    df_join['trials_remain'] = df_join['trial'] - df_join['trial_second_sequence_attended']
    # create df_final & convert remains back to a list so explode can be used
    df_trials_removed_after_second_sequence = pd.DataFrame(df_join['trials_remain'].map(list).map(sorted))
    df_trials_removed_after_second_sequence.rename(columns={'trials_remain': 'trial'}, inplace=True)
    # explode the lists
    df_trials_removed_after_second_sequence = df_trials_removed_after_second_sequence.explode('trial').\
        reset_index(drop=False)
    # reset index
    df_second_sequence_attended.reset_index(drop=False, inplace=True)
    # merge dfs
    df_trials_removed_after_second_sequence = pd.merge(df_trials_removed_after_second_sequence,
                                                       df_count_trials_remain,
                                                       on='subject', how='inner').merge(df_second_sequence_attended,
                                                                                        on='subject', how='inner')
    # set correct reactive to 1
    df_trials_removed_after_second_sequence['correct_reactive'] = 1

    # merge blackscreen (anticipations) and reactive with trials removed before second sequence attended
    df_trials_removed_after_second_sequence = pd.merge(df_trials_removed_after_second_sequence,
                                                       df_second_sequence_attended,
                                                       on='subject', how='inner')

    return df_trials_removed_after_second_sequence, df_blackscreen_reactive


# =============================================================================
#  LABEL VALID ANTICIPATIONS
# =============================================================================


def valid_anticipations(df_blackscreen_reactive):

    """
    Labels as valid anticipations only those in which a reactive fixation
    was found in the stimulus previous to the anticipatory period. If the
    fixation during the anticipatory period stays in the same place where the
    stimulus appeared in the reactive period, is it labeled as sticky fixation.
    If a correct anticipation and sticky fixations is found in the same trial,
    only the correct anticipation is computed (only in df_summarize_valid_anticipations)

    Input:
        df_blackscreen_reactive: DataFrame with correct reactive and anticipatory
                                 fixations after removing trials before the second
                                 sequence attended is achieved.

    Output:
        df_blackscreen_reactive: same input DataFrame with new columns labeling
                                 valid anticipations and sticky fixations.
        df_summarize_valid_anticipations: summary of correct anticipations and
                                          sticky fixations per participant.

    Notes:
        AOI_fix == 1 (left location)
        AOI_fix == 2 (right location)
    """

    # conditions valid anticipation
    condition_valid_anticipation_right = (df_blackscreen_reactive['AOI_fix'] == 2) & \
                                         (df_blackscreen_reactive['position'] == 1)
    condition_valid_anticipation_left = (df_blackscreen_reactive['AOI_fix'] == 1) & \
                                        (df_blackscreen_reactive['position'] == 2)
    # conditions sticky fixation
    condition_sticky_fixation_right = (df_blackscreen_reactive['AOI_fix'] == 2) & \
                                      (df_blackscreen_reactive['position'] == 2)
    condition_sticky_fixation_left = (df_blackscreen_reactive['AOI_fix'] == 1) & \
                                     (df_blackscreen_reactive['position'] == 1)
    # general conditions
    mask_valid_anticipation = condition_valid_anticipation_right | condition_valid_anticipation_left
    mask_sticky_fixation = condition_sticky_fixation_right | condition_sticky_fixation_left

    # set labels
    df_blackscreen_reactive.loc[mask_valid_anticipation, 'correct_anticipation'] = 1
    df_blackscreen_reactive.loc[mask_sticky_fixation, 'sticky_fixation'] = 1

    # resume valid anticipations
    df_summarize_valid_anticipations = df_blackscreen_reactive.groupby(['subject', 'trial']).agg(
        position=('position', 'mean'),
        correct_reactive=('correct_reactive', 'mean'),
        correct_anticipation=('correct_anticipation', 'max'),
        sticky_fixation=('sticky_fixation', 'max'),
        sequence=('sequence', 'max'),
        subgroup=('subgroup', 'max'))
    df_summarize_valid_anticipations.reset_index(drop=False, inplace=True)
    # if correct anticipation and sticky fixation are found in the same trial, keeps only correct anticipation
    df_summarize_valid_anticipations['sticky_fixation'] = np.where(
        df_summarize_valid_anticipations['correct_anticipation'].eq(1) &
        df_summarize_valid_anticipations['sticky_fixation'].eq(1), np.nan,
        df_summarize_valid_anticipations['sticky_fixation'])
    df_summarize_valid_anticipations.reset_index(drop=True, inplace=True)

    return df_blackscreen_reactive, df_summarize_valid_anticipations


# =============================================================================
#  COMPUTE BASIC STATISTICS BY SUBJECT
# =============================================================================


def statistics_subject(df_summarize_valid_anticipations, dict_reactive_by_subject,
                       df_trials_removed_after_second_sequence):

    """
    Done by subject:
    Compute basic statistics summarizing the number of correct anticipations and
    sticky fixations, the maximum trial completed and the number of total
    anticipations (correct and sticky fixations). Also maps the number of
    reactive fixations during the whole task. And adds the number of trials
    that remain after removal (second sequence achieved) and the trial in which
    this second sequence is achieved using an inner merge.

    Input:
        df_summarize_valid_anticipations: DataFrame with correct anticipations and
                                          sticky fixations.
        dict_reactive_by_subject: dictionary with the number of reactive fixations
                                  as values and participant's ID as keys.
        df_trials_removed_after_second_sequence: DataFrame with the number of
                                                  trials that remain after removal.
    Output:
        VSL_stats_subject: statistics computed by participant.
    """

    VSL_stats_subject = df_summarize_valid_anticipations.groupby(['subject']).agg(
        n_correct_anticipations=('correct_anticipation', 'sum'),
        n_sticky_fixation=('sticky_fixation', 'sum'),
        n_reactive_after_second_sequence=('correct_reactive', 'sum'),
        trial_max_completed=('trial', 'max'),
        n_total_anticipations=('trial', 'nunique')).reset_index(drop=False)
    # map into df
    VSL_stats_subject['n_reactive_all_task'] = VSL_stats_subject['subject'].map(dict_reactive_by_subject)
    # keep columns by subject
    trials_remain = df_trials_removed_after_second_sequence.groupby(['subject'])[['subject',
                                                                                  'trial_second_sequence_attended']].head(1)
    # merge with VSL stats
    VSL_stats_subject = VSL_stats_subject.merge(trials_remain, how='inner', on='subject')

    return VSL_stats_subject

# =============================================================================
#  COMPUTE BASIC STATISTICS BY SUBGROUP OF DATA
# =============================================================================


def statistics_subgroups(df_summarize_valid_anticipations, dict_reactive_by_subject_subgroup,
                         df_trials_removed_after_second_sequence):

    """
    Done by data subgroup:
    Compute basic statistics summarizing the number of correct anticipations and
    sticky fixations, the maximum trial completed and the number of total
    anticipations (correct and sticky fixations). Also maps the number of
    reactive fixations during the whole task. And adds the number of trials
    that remain after removal (second sequence achieved) and the trial in which
    this second sequence is achieved using an inner merge.

    Input:
        df_summarize_valid_anticipations: DataFrame with correct anticipations and
                                          sticky fixations.
        dict_reactive_by_subject: dictionary with the number of reactive fixations
                                  as values and participant's ID as keys.
        df_trials_removed_after_second_sequence: DataFrame with the number of
                                                  trials that remain after removal.
    Output:
        VSL_stats_subject: statistics computed by data subgroup.
    """

    VSL_stats_subgroups = df_summarize_valid_anticipations.groupby(['subject', 'subgroup']).agg(
        n_correct_anticipations=('correct_anticipation', 'sum'),
        n_sticky_fixations=('sticky_fixation', 'sum'),
        n_reactive_after_second_sequence=('correct_reactive', 'sum'),
        trial_max_completed=('trial', 'max'),
        n_total_anticipations=('trial', 'nunique')).reset_index(drop=False)
    # add subgroups removed during analysis
    list_subjects = list(VSL_stats_subgroups['subject'].unique())
    list_subgroups = [1, 2, 3, 4]
    # create a dict with sequences by subject
    dict_subjects_subgroups = dict.fromkeys(list_subjects, list_subgroups)
    # explode dict into a df
    df_subjects_subgroups = pd.DataFrame([dict_subjects_subgroups]).T.explode(0).reset_index(drop=False).\
        rename(columns={'index': 'subject', 0: 'subgroup'})
    # merge dfs - stats by subgroups with subgroups removed added again
    VSL_stats_subgroups = df_subjects_subgroups.merge(VSL_stats_subgroups, on=['subject', 'subgroup'], how='outer')
    # map into df
    VSL_stats_subgroups['n_reactive_all_task'] = VSL_stats_subgroups.set_index(['subject', 'subgroup']).index.\
        map(dict_reactive_by_subject_subgroup.get)
    # keep columns by subject
    trials_remain = df_trials_removed_after_second_sequence.groupby(['subject'])[['subject',
                                                                                  'trial_second_sequence_attended']].head(1)
    # merge with VSL stats
    VSL_stats_subgroups = VSL_stats_subgroups.merge(trials_remain, how='inner', on='subject')

    return VSL_stats_subgroups

# =============================================================================
#  CALL FUNCTIONS TO GET BASIC STATISTICS OUTPUT
# =============================================================================


def get_files_output():

    """
    Calls the necessary functions to process the data for the anticipatory and
    reactive period and saves the results in txt files in the indicated directory.

    Input:
        None

    Output:
        df_VSL_stats_by_subject: DataFrame with reduced data per participant
        df_VSL_stats_by_subgroup_pivot: DataFrame with reduced data per participant for
                                        each sub-block of data
    """

    # return processed files for blackscreen and reactive
    df_blackscreen, df_reactive = process_files()
    # return df with number of correct reactive by subject and dictionary with the same information
    df_reactive_completed, dict_reactive_by_subject, dict_reactive_by_subject_subgroup = correct_reactive(df_reactive)
    # return df with only trial_second_sequence_attended
    df_second_sequence_achieved = second_sequence_attended(df_reactive_completed)
    # return blackscreen and reactive dfs merged with correct reactive column
    df_trials_remain, df_blackscreen_reactive = remove_trials_before_second_sequence_attended(
        df_second_sequence_achieved, df_reactive_completed, df_blackscreen)
    # get valid anticipations and summary
    df_validated_anticipations, df_summary_valid_anticipations = valid_anticipations(df_blackscreen_reactive)
    # basic statistics
    df_VSL_stats_by_subject = statistics_subject(df_summary_valid_anticipations, dict_reactive_by_subject,
                                                 df_trials_remain)
    df_VSL_stats_by_subgroup = statistics_subgroups(df_summary_valid_anticipations, dict_reactive_by_subject_subgroup,
                                                    df_trials_remain)
    # pivot table
    df_VSL_stats_by_subgroup_pivot = df_VSL_stats_by_subgroup.pivot(index='subject', columns='subgroup',
                                                                    values=['n_correct_anticipations',
                                                                            'n_sticky_fixations',
                                                                            'n_reactive_after_second_sequence',
                                                                            'trial_max_completed',
                                                                            'n_total_anticipations',
                                                                            'n_reactive_all_task'])
    # save output
    df_VSL_stats_by_subject.to_csv(os.path.join(directory_results, 'VSL_stats_by_subject.txt'), sep=';', decimal=',')
    df_VSL_stats_by_subgroup_pivot.to_csv(os.path.join(directory_results, 'VSL_stats_by_subgroup.txt'), sep=';',
                                          decimal=',')

    return df_VSL_stats_by_subject, df_VSL_stats_by_subgroup_pivot


VSL_stats_subject, VSL_stats_subject_subgroup = get_files_output()
