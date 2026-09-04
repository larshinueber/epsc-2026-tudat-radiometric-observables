# EPSC 2026: Processing and Simulation of Radiometric Observations Using the Open-Source TU Delft Astrodynamics Toolbox (Tudat)

This repository contains the analysis code that was used in the poster titled "Processing and Simulation of Radiometric Observations Using the Open-Source TU Delft Astrodynamics Toolbox (Tudat)", presented at the Europlanet Science Congress 2026 (https://doi.org/10.5194/epsc2026-349).
A PDF version of the poster is stored in [EPSC_poster_Processing_Simulation_Radiometric_Observables_Using_Tudat.pdf](EPSC_poster_Processing_Simulation_Radiometric_Observables_Using_Tudat.pdf).

## Contents

The repository contains one Jupyter notebook per mission and file type:

- [grail_doppler_prefits.ipynb](grail_doppler_prefits.ipynb): GRAIL-A pre-fits from ODF (NASA TRK-2-18) files
- [mex_doppler_prefits.ipynb](mex_doppler_prefits.ipynb): Mars Express pre-fits from IFMS (ESA IFMS Level 2) files
- [mgn_doppler_prefits.ipynb](mgn_doppler_prefits.ipynb): Magellan pre-fits from ATDF (NASA TRK-2-25) files
- [mro_doppler_prefits.ipynb](mro_doppler_prefits.ipynb): MRO pre-fits from TNF (NASA TRK-2-34) files

The analysis in all notebooks follows a similar structure, with only minor differences between different notebooks.
To avoid duplication, only the [mro_doppler_prefits.ipynb](mro_doppler_prefits.ipynb) notebook contains more extensive documentation, while other notebooks only highlight the differences to the MRO analysis.
For a general introduction to using Tudat, see the [Tudat user guide](https://docs.tudat.space/en/latest/), the [list of examples](https://docs.tudat.space/en/latest/index-examples.html) therein, as well as the [tudatpy API reference](https://py.api.tudat.space/en/latest/).

## Usage

The results presented at EPSC have been obtained with tudatpy compiled locally from https://github.com/larshinueber/tudatpy/tree/feature/atdf-reader at commit a4c8d8f5e.
Once merged into the develop branch of tudatpy, a corresponding conda package version and installation instructions will be noted here.

Besides tudatpy, the `cmcrameri` Python package is required to recreate the colormaps used in the analysis.
With your conda environment activated, it can be installed through

```bash
conda install -c conda-forge cmcrameri
```

## References

The analysis is based on the following datasets:

- Magellan: https://doi.org/10.17189/1522511
- GRAIL-A: https://doi.org/10.17189/1519558
- Mars Express: https://doi.org/10.57780/esa-53ktg7l, https://doi.org/10.57780/esa-gxidlkt, https://doi.org/10.57780/esa-34ewi6a, https://doi.org/10.57780/esa-pgxj5wd, https://doi.org/10.57780/esa-30gu8gp, https://doi.org/10.57780/esa-h8yi287, https://doi.org/10.57780/esa-xwvg83d, https://doi.org/10.57780/esa-w8zdkpj
- Mars Reconnaissance Orbiter: https://doi.org/10.17189/1519443

For an exhaustive list of all data files used in the analysis and where to retrieve them from, see each of the Jupyter notebooks.

Additionally, we make heavy use of the SPICE toolkit, and navigation and ancillary data hosted by NAIF: https://doi.org/10.1016/0032-0633(95)00107-7, https://doi.org/10.1016/j.pss.2017.02.013.

The Scientific colour map batlow (http://doi.org/10.5281/zenodo.1243862) is used through the `cmcrameri` Python package (https://github.com/callumrollo/cmcrameri) to prevent visual distortion of the data and exclusion of readers with colour-vision deficiencies (https://doi.org/10.1038/s41467-020-19160-7).