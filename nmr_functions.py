##########################################################################
#  LIST OF USEFUL EQUATIONS FOR CALCULATING BRUKER PULSE SEQ PARAMETERS  #
#                          ------------------                            #
#                          v.0.1 / 15.11.23                              #
#                          ETTORE BARTALUCCI                             #
##########################################################################

# Importing minimally necessary modules
import numpy as np

# Calculate length (uS) of a pulse from its frequency (kHz)
def freq_to_length(pulse_frequency):
    """
    Calculate the length of a pulse given its frequency.

    Parameters:
    - frequency (float): The frequency of the pulse.

    Returns:
    - float: The length of the pulse.
    """
    if pulse_frequency <= 0:
        raise ValueError("Frequency must be a positive number")
    
    pulse_length = 1 / (4 * pulse_frequency)
    
    return pulse_length


# Calculate frequency (kHz) of a pulse from its length (uS)
def length_to_freq(pulse_length):
    """
    Calculate the frequency of a pulse given its length.

    Parameters:
    - length (float): The length of the pulse.

    Returns:
    - float: The frequency of the pulse.
    """
    if pulse_length <= 0:
        raise ValueError("Length must be a positive number")
    
    pulse_frequency = 1 / (4 * pulse_length)
    return pulse_frequency


# Compute theoretical and experimental CP condition from pulse PLW
def compute_cp_condition(plw_cp_I, plw_cp_S, plw_I, plw_S):
    """
    Calculate the theoretical and real Cross-Polarization conditions (kHz) for MAS NMR experiments.

    Parameters:
    - plw_cp_I: power level from the CP contact on nucleus I
    - plw_cp_S: power level from the CP contact on nucleus S
    - plw_I: power level from the hard pulse on nucleus I
    - plw_S: power level from the hard pulse on nucleus S

    Returns:
    - cp_condition_I: The frequency of the CP pulse on nucleus I
    - cp_condition_S: The frequency of the CP pulse on nucleus S
    """
    # Theoretical CP condition calculator

    # Real CP condition calculator
