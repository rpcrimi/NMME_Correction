import pymongo

def run():
	connection = pymongo.MongoClient()

	db                = connection["Attribute_Correction"]
	CFVars            = db["CFVars"]
	ValidFreq         = db["ValidFreq"]
	StandardNameFixes = db["StandardNameFixes"]
	VarNameFixes      = db["VarNameFixes"]
	FreqFixes         = db["FreqFixes"]
	FileNameChanges   = db["FileNameChanges"]

	# CF VARIABLES TABLE
	#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	CFVars.insert_one({"Variable": "Surface Temperature (SST+Land)",                "Var Name": "ts",       "CF Standard Name": "surface_temperature",                             "Units": "K"})
	CFVars.insert_one({"Variable": "Mean sea level pressure",                       "Var Name": "psl",      "CF Standard Name": "air_pressure_at_sea_level",                       "Units": "Pa"})
	CFVars.insert_one({"Variable": "Convective precipitation",                      "Var Name": "precc",    "CF Standard Name": "convective_precipitation_rate",                   "Units": "m s-1"})
	CFVars.insert_one({"Variable": "Downward surface solar",                        "Var Name": "rsds",     "CF Standard Name": "surface_downwelling_shortwave_flux_in_air",       "Units": "W m-2"})
	CFVars.insert_one({"Variable": "Downward surface longwave",                     "Var Name": "rlds",     "CF Standard Name": "surface_downwelling_longwave_flux_in_air",        "Units": "W m-2"})
	CFVars.insert_one({"Variable": "Net surface solar",                             "Var Name": "rss",      "CF Standard Name": "surface_net_downward_shortwave_flux",             "Units": "W m-2"})
	CFVars.insert_one({"Variable": "Net surface longwave",                          "Var Name": "rls",      "CF Standard Name": "surface_net_downward_longwave_flux",              "Units": "W m-2"})
	CFVars.insert_one({"Variable": "Top net solar",                                 "Var Name": "rst",      "CF Standard Name": "toa_net_downward_shortwave_flux",                 "Units": "W m-2"})
	CFVars.insert_one({"Variable": "Top net longwave",                              "Var Name": "rlt",      "CF Standard Name": "toa_net_downward_longwave_flux",                  "Units": "W m-2"})
	CFVars.insert_one({"Variable": "Surface latent flux",                           "Var Name": "hflsd",    "CF Standard Name": "surface_downward_latent_heat_flux",               "Units": "W m-2"})
	CFVars.insert_one({"Variable": "Surface sensible flux",                         "Var Name": "hfssd",    "CF Standard Name": "surface_downward_sensible_heat_flux",             "Units": "W m-2"})
	CFVars.insert_one({"Variable": "Total cloud cover",                             "Var Name": "clt",      "CF Standard Name": "cloud_area_fraction",                             "Units": "1"})
	CFVars.insert_one({"Variable": "Geopotential",                                  "Var Name": "g",        "CF Standard Name": "geopotential",                                    "Units": "m2 s-2"})
	CFVars.insert_one({"Variable": "Temperature",                                   "Var Name": "ta",       "CF Standard Name": "air_temperature",                                 "Units": "K"})
	CFVars.insert_one({"Variable": "Zonal velocity",                                "Var Name": "ua",       "CF Standard Name": "eastward_wind",                                   "Units": "m s-1"})
	CFVars.insert_one({"Variable": "Meridional velocity",                           "Var Name": "va",       "CF Standard Name": "northward_wind",                                  "Units": "m s-1"})
	CFVars.insert_one({"Variable": "Specific humidity",                             "Var Name": "hus",      "CF Standard Name": "specific_humidity",                               "Units": "1"})
	CFVars.insert_one({"Variable": "Potential temperature",                         "Var Name": "thetao",   "CF Standard Name": "sea_water_potential_temperature",                 "Units": "K"})
	CFVars.insert_one({"Variable": "Salinity",                                      "Var Name": "so",       "CF Standard Name": "sea_water_salinity",                              "Units": "1e-3"})
	CFVars.insert_one({"Variable": "Zonal velocity",                                "Var Name": "uo",       "CF Standard Name": "sea_water_x_velocity",                            "Units": "m s-1"})
	CFVars.insert_one({"Variable": "Meridional velocity",                           "Var Name": "vo",       "CF Standard Name": "sea_water_y_velocity",                            "Units": "m s-1"})
	CFVars.insert_one({"Variable": "Vertical velocity",                             "Var Name": "wo",       "CF Standard Name": "upward_sea_water_velocity",                       "Units": "m s-1"})
	CFVars.insert_one({"Variable": "Sea level",                                     "Var Name": "zoh",      "CF Standard Name": "sea_surface_height_above_geoid",                  "Units": "m"})
	CFVars.insert_one({"Variable": "Mixed layer depth",                             "Var Name": "zmlo",     "CF Standard Name": "ocean_mixed_layer_thickness",                     "Units": "m"})
	CFVars.insert_one({"Variable": "Sea-ice thickness",                             "Var Name": "sit",      "CF Standard Name": "sea_ice_thickness",                               "Units": "m"})
	CFVars.insert_one({"Variable": "2m T daily max",                                "Var Name": "tasmax",   "CF Standard Name": "air_temperature",                                 "Units": "K"})
	CFVars.insert_one({"Variable": "2m T daily min",                                "Var Name": "tasmin",   "CF Standard Name": "air_temperature",                                 "Units": "K"})
	CFVars.insert_one({"Variable": "2m temperature",                                "Var Name": "tas",      "CF Standard Name": "air_temperature",                                 "Units": "K"})
	CFVars.insert_one({"Variable": "10m wind (u)",                                  "Var Name": "uas",      "CF Standard Name": "eastward_wind",                                   "Units": "m s-1"})
	CFVars.insert_one({"Variable": "10m wind (v)",                                  "Var Name": "vas",      "CF Standard Name": "northward_wind",                                  "Units": "m s-1"})
	CFVars.insert_one({"Variable": "Water equivalent snow depth",                   "Var Name": "snowhlnd", "CF Standard Name": "lwe_thickness_of_surface_snow_amount",            "Units": "m"})
	CFVars.insert_one({"Variable": "Total soil moisture",                           "Var Name": "mrsov",    "CF Standard Name": "volume_fraction_of_condensed_water_in_soil",      "Units": "1"})
	CFVars.insert_one({"Variable": "Surface stress (x)",                            "Var Name": "stx",      "CF Standard Name": "surface_zonal_stress_positive_to_the_west",       "Units": "Pa"})
	CFVars.insert_one({"Variable": "Surface stress (y)",                            "Var Name": "sty",      "CF Standard Name": "surface_meridional_stress_positive_to_the_north", "Units": "Pa"})
	CFVars.insert_one({"Variable": "Precipitable water",                            "Var Name": "tqm",      "CF Standard Name": "total_column_vertically_integrated_water",        "Units": "kg m-2"})
	CFVars.insert_one({"Variable": "2m dewpoint temperature",                       "Var Name": "tdps",     "CF Standard Name": "dew_point_temperature",                           "Units": "K"})
	CFVars.insert_one({"Variable": "Latitude",                                      "Var Name": "lat",      "CF Standard Name": "latitude",                                        "Units": "degree_north"})
	CFVars.insert_one({"Variable": "Longitude",                                     "Var Name": "lon",      "CF Standard Name": "longitude",                                       "Units": "degree_east"})
	CFVars.insert_one({"Variable": "Time",                                          "Var Name": "time",     "CF Standard Name": "time",                                            "Units": "s"})
	CFVars.insert_one({"Variable": "Height",                                        "Var Name": "zh",       "CF Standard Name": "height",                                          "Units": "m"})
	CFVars.insert_one({"Variable": "Precipitation Flux",                            "Var Name": "pr",       "CF Standard Name": "precipitation_flux",                              "Units": "kg m-2 s-1"})
	CFVars.insert_one({"Variable": "Depth",                                         "Var Name": "lev",      "CF Standard Name": "depth",                                           "Units": "m"})
	CFVars.insert_one({"Variable": "Sea-ice area fraction",                         "Var Name": "sic",      "CF Standard Name": "sea_ice_area_fraction",                           "Units": "1"})
	CFVars.insert_one({"Variable": "Air pressure",                                  "Var Name": "plev",     "CF Standard Name": "air_pressure",                                    "Units": "Pa"})
	CFVars.insert_one({"Variable": "Total Precipitation",                           "Var Name": "prlr",     "CF Standard Name": "lwe_precipitation_rate",                          "Units": "m s-1"})
	CFVars.insert_one({"Variable": "Sea Water Temperature",                         "Var Name": "to",       "CF Standard Name": "sea_water_temperature",                           "Units": "K"})
	CFVars.insert_one({"Variable": "Large scale precipitation",                     "Var Name": "precl",    "CF Standard Name": "stratiform_precipitation_flux",                   "Units": "kg m-2 s-1"})
	CFVars.insert_one({"Variable": "Total runoff",                                  "Var Name": "mrro",     "CF Standard Name": "runoff_flux",                                     "Units": "kg m-2 s-1"})
	CFVars.insert_one({"Variable": "Surface Runoff Flux",                           "Var Name": "mrros",    "CF Standard Name": "surface_runoff_flux",                             "Units": "kg m-2 s-1"})
	CFVars.insert_one({"Variable": "Ocean Mixed Layer Thickness Defined by Sigma T","Var Name": "mlotst",   "CF Standard Name": "ocean_mixed_layer_thickness_defined_by_sigma_t",  "Units": "m"})
	
	# Not Verified
	CFVars.insert_one({"Variable": "Fresh water flux",                              "Var Name": "fwf",      "CF Standard Name": "fresh_water_flux",                                "Units": "XXXXXX"})
	CFVars.insert_one({"Variable": "Sea-ice extent",                                "Var Name": "XXXXXXXX", "CF Standard Name": "sea_ice_extent",                                  "Units": "m2"})
	CFVars.insert_one({"Variable": "Vertical integrated moisture flux convergence", "Var Name": "vimfc",    "CF Standard Name": "XXXXXXXXXXXXXX",                                  "Units": "XXXXXX"})
	CFVars.insert_one({"Variable": "Ground heat flux",                              "Var Name": "XXXXXXXX", "CF Standard Name": "XXXXXXXXXXXXXX",                                  "Units": "W m-2"})
	CFVars.insert_one({"Variable": "Velocity potential 850 hPa",                    "Var Name": "XXXX",     "CF Standard Name": "velocity_potential_850_hpa",                      "Units": "m2 s-1"})
	CFVars.insert_one({"Variable": "Velocity potential 200 hPa",                    "Var Name": "XXXX",     "CF Standard Name": "velocity_potential_200_hpa",                      "Units": "m2 s-1"})
	CFVars.insert_one({"Variable": "Stream function 850 hPa",                       "Var Name": "XXXX",     "CF Standard Name": "stream_function_850_hpa",                         "Units": "m2 s-1"})
	CFVars.insert_one({"Variable": "Stream function 200 hPa",                       "Var Name": "XXXX",     "CF Standard Name": "stream_function_200_hpa",                         "Units": "m2 s-1"})
	#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------


	# VALID FREQUENCIES TABLE
	#----------------------------------------------------------------------------------------------------------
	ValidFreq.insert_one({"Frequency": "3hr"})
	ValidFreq.insert_one({"Frequency": "6hr"})
	ValidFreq.insert_one({"Frequency": "day"})
	ValidFreq.insert_one({"Frequency": "mon"})
	ValidFreq.insert_one({"Frequency": "Omon"})
	ValidFreq.insert_one({"Frequency": "yr"})
	#----------------------------------------------------------------------------------------------------------



	# STANDARD NAME KNOWN FIXES TABLE
	#-----------------------------------------------------------------------------------------------------------
	StandardNameFixes.insert_one({"Incorrect Standard Name": "air temp",                                        "Var Name": "tasmax",    "Known Fix": "air_temperature"})
	StandardNameFixes.insert_one({"Incorrect Standard Name": "air temp",                                        "Var Name": "tasmin",    "Known Fix": "air_temperature"})
	StandardNameFixes.insert_one({"Incorrect Standard Name": "air temperature",                                 "Var Name": "TA",        "Known Fix": "air_temperature"})
	StandardNameFixes.insert_one({"Incorrect Standard Name": "air temperature",                                 "Var Name": "ta",        "Known Fix": "air_temperature"})
	StandardNameFixes.insert_one({"Incorrect Standard Name": "zonal velocity",                                  "Var Name": "uo",        "Known Fix": "sea_water_x_velocity"})
	StandardNameFixes.insert_one({"Incorrect Standard Name": "lat",                                             "Var Name": "lat",       "Known Fix": "latitude"})
	StandardNameFixes.insert_one({"Incorrect Standard Name": "geopotential height (above sea level)",           "Var Name": "G",         "Known Fix": "geopotential"})
	StandardNameFixes.insert_one({"Incorrect Standard Name": "geopotential height (above sea level)",           "Var Name": "g",         "Known Fix": "geopotential"})
	StandardNameFixes.insert_one({"Incorrect Standard Name": "surface latent heat flux",                        "Var Name": "LHFLX",     "Known Fix": "surface_downward_latent_heat_flux"})
	StandardNameFixes.insert_one({"Incorrect Standard Name": "specific humidity",                               "Var Name": "HUS",       "Known Fix": "specific_humidity"})
	StandardNameFixes.insert_one({"Incorrect Standard Name": "total soil liquid water in total 15 columnn",     "Var Name": "MRSOV",     "Known Fix": "volume_fraction_of_condensed_water_in_soil"})
	StandardNameFixes.insert_one({"Incorrect Standard Name": "air pressure at sea level",                       "Var Name": "PSL",       "Known Fix": "air_pressure_at_sea_level"})
	StandardNameFixes.insert_one({"Incorrect Standard Name": "net longwave flux at surface",                    "Var Name": "FLNS",      "Known Fix": "surface_net_downward_longwave_flux"})
	StandardNameFixes.insert_one({"Incorrect Standard Name": "net longwave flux at top of model",               "Var Name": "FLNT",      "Known Fix": "toa_net_downward_longwave_flux"})
	StandardNameFixes.insert_one({"Incorrect Standard Name": "net solar flux at surface",                       "Var Name": "FSNS",      "Known Fix": "surface_net_downward_shortwave_flux"})
	StandardNameFixes.insert_one({"Incorrect Standard Name": "net solar flux at top of model",                  "Var Name": "FSNT",      "Known Fix": "toa_net_downward_shortwave_flux"})
	StandardNameFixes.insert_one({"Incorrect Standard Name": "total runoff (qover + qdrai + qrgwl)",            "Var Name": "TOTRUNOFF", "Known Fix": "total_runoff"})
	StandardNameFixes.insert_one({"Incorrect Standard Name": "zonal surface stress",                            "Var Name": "STX",       "Known Fix": "surface_zonal_stress_positive_to_the_west"})
	StandardNameFixes.insert_one({"Incorrect Standard Name": "meridional surface stress",                       "Var Name": "STY",       "Known Fix": "surface_meridional_stress_positive_to_the_north"})
	StandardNameFixes.insert_one({"Incorrect Standard Name": "salinity",                                        "Var Name": "SO",        "Known Fix": "sea_water_salinity"})
	StandardNameFixes.insert_one({"Incorrect Standard Name": "temperature",                                     "Var Name": "TO",        "Known Fix": "sea_water_temperature"})
	StandardNameFixes.insert_one({"Incorrect Standard Name": "surface_meridional_stress_positive_to_the_south", "Var Name": "sty",       "Known Fix": "surface_meridional_stress_positive_to_the_north"})
	StandardNameFixes.insert_one({"Incorrect Standard Name": "north_wind",                                      "Var Name": "va",        "Known Fix": "northward_wind"})
	StandardNameFixes.insert_one({"Incorrect Standard Name": "east_wind",                                       "Var Name": "ua",        "Known Fix": "eastward_wind"})
	StandardNameFixes.insert_one({"Incorrect Standard Name": "volume_fraction_of_water_in_soil",                "Var Name": "mrsov",     "Known Fix": "volume_fraction_of_condensed_water_in_soil"})
	StandardNameFixes.insert_one({"Incorrect Standard Name": "toa_outgoing_longwave_flux",                      "Var Name": "rlt",       "Known Fix": "toa_net_downward_longwave_flux"})
	StandardNameFixes.insert_one({"Incorrect Standard Name": "surface_downward_x_stress",                       "Var Name": "stx",       "Known Fix": "surface_zonal_stress_positive_to_the_west"})
	StandardNameFixes.insert_one({"Incorrect Standard Name": "surface_downward_y_stress",                       "Var Name": "sty",       "Known Fix": "surface_meridional_stress_positive_to_the_north"})
	StandardNameFixes.insert_one({"Incorrect Standard Name": "atmosphere_mass_content_of_water",                "Var Name": "tqm",       "Known Fix": "total_column_vertically_integrated_water"})
	StandardNameFixes.insert_one({"Incorrect Standard Name": "surface_net_downward_shortwave",                  "Var Name": "pr",        "Known Fix": "precipitation_flux"})
	StandardNameFixes.insert_one({"Incorrect Standard Name": "temperature",                                     "Var Name": "ta",        "Known Fix": "air_temperature"})
	StandardNameFixes.insert_one({"Incorrect Standard Name": "surface latent heat flux",                        "Var Name": "hflsd",     "Known Fix": "surface_downward_latent_heat_flux"})
	StandardNameFixes.insert_one({"Incorrect Standard Name": "surface sensible heat flux",                      "Var Name": "hfssd",     "Known Fix": "surface_downward_sensible_heat_flux"})
	StandardNameFixes.insert_one({"Incorrect Standard Name": "specific humidity",                               "Var Name": "hus",       "Known Fix": "specific_humidity"})
	StandardNameFixes.insert_one({"Incorrect Standard Name": "total soil liquid water in total 15 columnn",     "Var Name": "mrsov",     "Known Fix": "volume_fraction_of_condensed_water_in_soil"})
	StandardNameFixes.insert_one({"Incorrect Standard Name": "large scale precipitation rate",                  "Var Name": "precl",     "Known Fix": "stratiform_precipitation_flux"})
	StandardNameFixes.insert_one({"Incorrect Standard Name": "air pressure at sea level",                       "Var Name": "psl",       "Known Fix": "air_pressure_at_sea_level"})
	StandardNameFixes.insert_one({"Incorrect Standard Name": "net longwave flux at surface",                    "Var Name": "rls",       "Known Fix": "surface_net_downward_longwave_flux"})
	StandardNameFixes.insert_one({"Incorrect Standard Name": "net longwave flux at top of model",               "Var Name": "rlt",       "Known Fix": "toa_net_downward_longwave_flux"})
	StandardNameFixes.insert_one({"Incorrect Standard Name": "net solar flux at surface",                       "Var Name": "rss",       "Known Fix": "surface_net_downward_shortwave_flux"})
	StandardNameFixes.insert_one({"Incorrect Standard Name": "net solar flux at top of model",                  "Var Name": "rst",       "Known Fix": "toa_net_downward_shortwave_flux"})
	StandardNameFixes.insert_one({"Incorrect Standard Name": "zonal surface stress",                            "Var Name": "stx",       "Known Fix": "surface_zonal_stress_positive_to_the_west"})
	StandardNameFixes.insert_one({"Incorrect Standard Name": "meridional surface stress",                       "Var Name": "sty",       "Known Fix": "surface_meridional_stress_positive_to_the_north"})
	StandardNameFixes.insert_one({"Incorrect Standard Name": "eastward wind",                                   "Var Name": "ua",        "Known Fix": "eastward_wind"})
	StandardNameFixes.insert_one({"Incorrect Standard Name": "northward wind",                                  "Var Name": "va",        "Known Fix": "northward_wind"})
	StandardNameFixes.insert_one({"Incorrect Standard Name": "surface temperature",                             "Var Name": "ts",        "Known Fix": "surface_temperature"})


	#-----------------------------------------------------------------------------------------------------------




	# VARIABLE NAME KNOWN FIXES TABLE
	#-----------------------------------------------------------------------------------------------------------
	VarNameFixes.insert_one({"Incorrect Var Name": "height",    "CF Standard Name": "height",                                          "Known Fix": "zh"})
	VarNameFixes.insert_one({"Incorrect Var Name": "LAT",       "CF Standard Name": "latitude",                                        "Known Fix": "lat"})
	VarNameFixes.insert_one({"Incorrect Var Name": "LON",       "CF Standard Name": "longitude",                                       "Known Fix": "lon"})
	VarNameFixes.insert_one({"Incorrect Var Name": "G",         "CF Standard Name": "geopotential",                                    "Known Fix": "g"})
	VarNameFixes.insert_one({"Incorrect Var Name": "t",         "CF Standard Name": "air_temperature",                                 "Known Fix": "ta"})
	VarNameFixes.insert_one({"Incorrect Var Name": "LHFLX",     "CF Standard Name": "surface_downward_latent_heat_flux",               "Known Fix": "hflsd"})
	VarNameFixes.insert_one({"Incorrect Var Name": "HUS",       "CF Standard Name": "specific_humidity",                               "Known Fix": "hus"})
	VarNameFixes.insert_one({"Incorrect Var Name": "MRSOV",     "CF Standard Name": "volume_fraction_of_condensed_water_in_soil",      "Known Fix": "mrsov"})
	VarNameFixes.insert_one({"Incorrect Var Name": "PSL",       "CF Standard Name": "air_pressure_at_sea_level",                       "Known Fix": "psl"})
	VarNameFixes.insert_one({"Incorrect Var Name": "FLNS",      "CF Standard Name": "surface_net_downward_longwave_flux",              "Known Fix": "rls"})
	VarNameFixes.insert_one({"Incorrect Var Name": "FLNT",      "CF Standard Name": "toa_net_downward_longwave_flux",                  "Known Fix": "rlt"})
	VarNameFixes.insert_one({"Incorrect Var Name": "FSNS",      "CF Standard Name": "surface_net_downward_shortwave_flux",             "Known Fix": "rss"})
	VarNameFixes.insert_one({"Incorrect Var Name": "FSNT",      "CF Standard Name": "toa_net_downward_shortwave_flux",                 "Known Fix": "rst"})
	VarNameFixes.insert_one({"Incorrect Var Name": "STX",       "CF Standard Name": "surface_zonal_stress_positive_to_the_west",       "Known Fix": "stx"})
	VarNameFixes.insert_one({"Incorrect Var Name": "STY",       "CF Standard Name": "surface_meridional_stress_positive_to_the_north", "Known Fix": "sty"})
	VarNameFixes.insert_one({"Incorrect Var Name": "zos",       "CF Standard Name": "sea_surface_height_above_geoid",                  "Known Fix": "zoh"})
	VarNameFixes.insert_one({"Incorrect Var Name": "lev",       "CF Standard Name": "air_pressure",                                    "Known Fix": "plev"})
	VarNameFixes.insert_one({"Incorrect Var Name": "SO",        "CF Standard Name": "sea_water_salinity",                              "Known Fix": "so"})
	VarNameFixes.insert_one({"Incorrect Var Name": "TO",        "CF Standard Name": "sea_water_temperature",                           "Known Fix": "to"})
	VarNameFixes.insert_one({"Incorrect Var Name": "TA",        "CF Standard Name": "air_temperature",                                 "Known Fix": "ta"})
	VarNameFixes.insert_one({"Incorrect Var Name": "runoff",    "CF Standard Name": "surface_runoff_flux",                             "Known Fix": "mrros"})
	VarNameFixes.insert_one({"Incorrect Var Name": "snowhland", "CF Standard Name": "lwe_thickness_of_surface_snow_amount",            "Known Fix": "snowhlnd"})
	VarNameFixes.insert_one({"Incorrect Var Name": "SHFLX",     "CF Standard Name": "surface sensible heat flux",                      "Known Fix": "hfssd"})
	VarNameFixes.insert_one({"Incorrect Var Name": "PRECL",     "CF Standard Name": "large scale precipitation rate",                  "Known Fix": "precl"})
	VarNameFixes.insert_one({"Incorrect Var Name": "TASMAX",    "CF Standard Name": "air_temperature",                                 "Known Fix": "tasmax"})
	VarNameFixes.insert_one({"Incorrect Var Name": "TASMIN",    "CF Standard Name": "air_temperature",                                 "Known Fix": "tasmin"})
	VarNameFixes.insert_one({"Incorrect Var Name": "TS",        "CF Standard Name": "surface temperature",                             "Known Fix": "ts"})
	VarNameFixes.insert_one({"Incorrect Var Name": "UA",        "CF Standard Name": "eastward wind",                                   "Known Fix": "ua"})
	VarNameFixes.insert_one({"Incorrect Var Name": "VA",        "CF Standard Name": "northward wind",                                  "Known Fix": "va"})
	VarNameFixes.insert_one({"Incorrect Var Name": "STY",       "CF Standard Name": "surface_meridional_stress_positive_to_the_north", "Known Fix": "sty"})

	#-----------------------------------------------------------------------------------------------------------



	# FREQUENCIES KNOWN FIXES TABLE
	#-----------------------------------------------------------------------------------------------------------
	FreqFixes.insert_one({"Incorrect Freq": "month", "Known Fix": "mon"})