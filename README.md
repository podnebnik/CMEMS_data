# CMEMS_data

Copernicus Marine Environment Monitoring Service  (CMEMS) data retrieval and plotting.

# Data retrieval requirements

* User account at https://marine.copernicus.eu/
* Python [2.7, 3.6 or 3.7] (https://www.python.org/downloads/)
* Motuclient [1.8 or higher] (https://marine.copernicus.eu/faq/what-are-the-motu-and-python-requirements/?idpage=169)

# Data retrieval example

Let's retrieve sea surface temperature (SST) from forecast MEDSEA_ANALYSIS_FORECAST_PHY_006_013-TDS in limited space-time domain. (All available products are listed [here](https://resources.marine.copernicus.eu/?option=com_csw&task=results&pk_vid=bf878f3427bd2be11611821870684780)).

After installing Motuclient, execute from command line:

```motuclient --motu http://nrt.cmems-du.eu/motu-web/Motu --service-id MEDSEA_ANALYSIS_FORECAST_PHY_006_013-TDS --product-id med00-cmcc-tem-an-fc-d --longitude-min 12 --longitude-max 22 --latitude-min 36 --latitude-max 45.97916793823242 --date-min "2021-02-05 12:00:00" --date-max "2021-02-05 12:00:00" --depth-min 1.0181 --depth-max 1.0184 --variable thetao --out-dir OUTFILE_DIR --out-name OUTFILE_NAME --user USERNAME --pwd PASSWORD```

This should initiate a download of a NetCDF file with the desired data.

# Data plotting example

See code `plot_CMEMS_field.py`. Executing this code should produce the following pdf:

![CMEMS_SST_20210205_1200.pdf](CMEMS_SST_20210205_1200.pdf)