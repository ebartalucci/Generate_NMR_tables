# Generate_NMR_tables
code to extract and generate nmr acquisition tables from bruker data


# Structure for the table:
needed files:
- pulseprogram: need a function that goes through the pulseprogram file and based on the type of experiment it finds (e.g. inept.juga, which is also in the acqu file), it allocates pulse variables to search, e.g. delays, pulses and power levels
- format.temp: searching through the file enables to allocate system of units to the values i need, e.g. pulses and or delays ecc. and eventual nomenclatures for the tables
- audita.txt: contain useful information eg on the kinetics for the experiment, owners, magnets and topspin version ((NUMBER, WHEN, WHO, WHERE, PROCESS, VERSION, WHAT))
- acqu/acqus: contain all necessary acquisition information. Indexing starts at zero, so for ex PLW12 for decoupling will be the number 13 in the list. Can use this file to set the intial stage for subsequent parsing routine, in a keywords based way.
- parameters to consider:

##$PULPROG -> fundamental, this defines the experiment, in this case <inept.juga>, so elif cycles
##$CNST -> search for index 2
##$CPDPRG -> if waltz64 low power 5kHz, elif spinal64 high power 90kHz, elif ...
##$NUC1, 2, 3 ... -> maybe useful
##$O1 need to calculate the center frequency, lace it to nuc1
##$P -> pulse lenght, this is experiment dependent, so for each one i manually need to define them
##$PCPD -> compute decoupling khz value, e.g. for lower than 90kHz
##$PLW -> link to P
##$SFO1 -> gives the magnet MHz, write short function to convert in tesla, link to NUC, so if NUC = 1H then convert
##$SPNAM -> shaped pulses, need to find a way
##$D -> delays, also to calculate the acq time
##$NS -> numbr of scan
##$TD -> size spectrum
##$SW -> spectral width
- temperature and MAS are the only two things not defined, this can be parsed in the title file