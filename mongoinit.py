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
	CFVars.insert({"Variable": "Surface Temperature (SST+Land)",                "Var Name": "ts",       "CF Standard Name": "surface_temperature",                             "Units": "K"})
	CFVars.insert({"Variable": "Mean sea level pressure",                       "Var Name": "psl",      "CF Standard Name": "air_pressure_at_sea_level",                       "Units": "Pa"})
	CFVars.insert({"Variable": "Convective precipitation",                      "Var Name": "precc",    "CF Standard Name": "convective_precipitation_rate",                   "Units": "m s-1"})
	CFVars.insert({"Variable": "Downward surface solar",                        "Var Name": "rsds",     "CF Standard Name": "surface_downwelling_shortwave_flux_in_air",       "Units": "W m-2"})
	CFVars.insert({"Variable": "Downward surface longwave",                     "Var Name": "rlds",     "CF Standard Name": "surface_downwelling_longwave_flux_in_air",        "Units": "W m-2"})
	CFVars.insert({"Variable": "Net surface solar",                             "Var Name": "rss",      "CF Standard Name": "surface_net_downward_shortwave_flux",             "Units": "W m-2"})
	CFVars.insert({"Variable": "Net surface longwave",                          "Var Name": "rls",      "CF Standard Name": "surface_net_downward_longwave_flux",              "Units": "W m-2"})
	CFVars.insert({"Variable": "Top net solar",                                 "Var Name": "rst",      "CF Standard Name": "toa_net_downward_shortwave_flux",                 "Units": "W m-2"})
	CFVars.insert({"Variable": "Top net longwave",                              "Var Name": "rlt",      "CF Standard Name": "toa_net_downward_longwave_flux",                  "Units": "W m-2"})
	CFVars.insert({"Variable": "Surface latent flux",                           "Var Name": "hflsd",    "CF Standard Name": "surface_downward_latent_heat_flux",               "Units": "W m-2"})
	CFVars.insert({"Variable": "Surface sensible flux",                         "Var Name": "hfssd",    "CF Standard Name": "surface_downward_sensible_heat_flux",             "Units": "W m-2"})
	CFVars.insert({"Variable": "Total cloud cover",                             "Var Name": "clt",      "CF Standard Name": "cloud_area_fraction",                             "Units": "1"})
	CFVars.insert({"Variable": "Geopotential",                                  "Var Name": "g",        "CF Standard Name": "geopotential",                                    "Units": "m2 s-2"})
	CFVars.insert({"Variable": "Temperature",                                   "Var Name": "ta",       "CF Standard Name": "air_temperature",                                 "Units": "K"})
	CFVars.insert({"Variable": "Zonal velocity",                                "Var Name": "ua",       "CF Standard Name": "eastward_wind",                                   "Units": "m s-1"})
	CFVars.insert({"Variable": "Meridional velocity",                           "Var Name": "va",       "CF Standard Name": "northward_wind",                                  "Units": "m s-1"})
	CFVars.insert({"Variable": "Specific humidity",                             "Var Name": "hus",      "CF Standard Name": "specific_humidity",                               "Units": "1"})
	CFVars.insert({"Variable": "Potential temperature",                         "Var Name": "thetao",   "CF Standard Name": "sea_water_potential_temperature",                 "Units": "K"})
	CFVars.insert({"Variable": "Salinity",                                      "Var Name": "so",       "CF Standard Name": "sea_water_salinity",                              "Units": "1e-3"})
	CFVars.insert({"Variable": "Zonal velocity",                                "Var Name": "uo",       "CF Standard Name": "sea_water_x_velocity",                            "Units": "m s-1"})
	CFVars.insert({"Variable": "Meridional velocity",                           "Var Name": "vo",       "CF Standard Name": "sea_water_y_velocity",                            "Units": "m s-1"})
	CFVars.insert({"Variable": "Vertical velocity",                             "Var Name": "wo",       "CF Standard Name": "upward_sea_water_velocity",                       "Units": "m s-1"})
	CFVars.insert({"Variable": "Sea level",                                     "Var Name": "zoh",      "CF Standard Name": "sea_surface_height_above_geoid",                  "Units": "m"})
	CFVars.insert({"Variable": "Mixed layer depth",                             "Var Name": "zmlo",     "CF Standard Name": "ocean_mixed_layer_thickness",                     "Units": "m"})
	CFVars.insert({"Variable": "Sea-ice thickness",                             "Var Name": "sit",      "CF Standard Name": "sea_ice_thickness",                               "Units": "m"})
	CFVars.insert({"Variable": "2m T daily max",                                "Var Name": "tasmax",   "CF Standard Name": "air_temperature",                                 "Units": "K"})
	CFVars.insert({"Variable": "2m T daily min",                                "Var Name": "tasmin",   "CF Standard Name": "air_temperature",                                 "Units": "K"})
	CFVars.insert({"Variable": "2m temperature",                                "Var Name": "tas",      "CF Standard Name": "air_temperature",                                 "Units": "K"})
	CFVars.insert({"Variable": "10m wind (u)",                                  "Var Name": "uas",      "CF Standard Name": "eastward_wind",                                   "Units": "m s-1"})
	CFVars.insert({"Variable": "10m wind (v)",                                  "Var Name": "vas",      "CF Standard Name": "northward_wind",                                  "Units": "m s-1"})
	CFVars.insert({"Variable": "Water equivalent snow depth",                   "Var Name": "snowhlnd", "CF Standard Name": "water_equivalent_snow_depth",                     "Units": "m"})
	CFVars.insert({"Variable": "Total soil moisture",                           "Var Name": "mrsov",    "CF Standard Name": "volume_fraction_of_condensed_water_in_soil",      "Units": "1"})
	CFVars.insert({"Variable": "Surface stress (x)",                            "Var Name": "stx",      "CF Standard Name": "surface_zonal_stress_positive_to_the_west",       "Units": "Pa"})
	CFVars.insert({"Variable": "Surface stress (y)",                            "Var Name": "sty",      "CF Standard Name": "surface_meridional_stress_positive_to_the_north", "Units": "Pa"})
	CFVars.insert({"Variable": "Precipitable water",                            "Var Name": "tqm",      "CF Standard Name": "total_column_vertically_integrated_water",        "Units": "kg m-2"})
	CFVars.insert({"Variable": "2m dewpoint temperature",                       "Var Name": "tdps",     "CF Standard Name": "dew_point_temperature",                           "Units": "K"})
	CFVars.insert({"Variable": "Latitude",                                      "Var Name": "lat",      "CF Standard Name": "latitude",                                        "Units": "degree_north"})
	CFVars.insert({"Variable": "Longitude",                                     "Var Name": "lon",      "CF Standard Name": "longitude",                                       "Units": "degree_east"})
	CFVars.insert({"Variable": "Time",                                          "Var Name": "time",     "CF Standard Name": "time",                                            "Units": "s"})
	CFVars.insert({"Variable": "Height",                                        "Var Name": "zh",       "CF Standard Name": "height",                                          "Units": "m"})
	CFVars.insert({"Variable": "Precipitation Flux",                            "Var Name": "pr",       "CF Standard Name": "precipitation_flux",                              "Units": "kg m-2 s-1"})
	CFVars.insert({"Variable": "Depth",                                         "Var Name": "lev",       "CF Standard Name": "depth",                                          "Units": "m"})
	CFVars.insert({"Variable": "Sea-ice area fraction",                         "Var Name": "sic",       "CF Standard Name": "sea_ice_area_fraction",                          "Units": "1"})
	CFVars.insert({"Variable": "Air pressure",                                  "Var Name": "plev",      "CF Standard Name": "air_pressure",                                   "Units": "Pa"})
	CFVars.insert({"Variable": "Total Precipitation",                           "Var Name": "prlr",      "CF Standard Name": "lwe_precipitation_rate",                         "Units": "m s-1"})
	CFVars.insert({"Variable": "Sea Water Temperature",                         "Var Name": "to",        "CF Standard Name": "sea_water_temperature",                          "Units": "K"})
	CFVars.insert({"Variable": "Large scale precipitation",                     "Var Name": "precl",    "CF Standard Name": "stratiform_precipitation_flux",                   "Units": "kg m-2 s-1"})
	CFVars.insert({"Variable": "Total runoff",                                  "Var Name": "mrro",     "CF Standard Name": "runoff_flux",                                     "Units": "kg m-2 s-1"})
	
	# Not Verified
	CFVars.insert({"Variable": "Fresh water flux",                              "Var Name": "fwf",      "CF Standard Name": "fresh_water_flux",                                "Units": "XXXXXX"})
	CFVars.insert({"Variable": "Sea-ice extent",                                "Var Name": "XXXXXXXX", "CF Standard Name": "sea_ice_extent",                                  "Units": "m2"})
	CFVars.insert({"Variable": "Vertical integrated moisture flux convergence", "Var Name": "vimfc",    "CF Standard Name": "XXXXXXXXXXXXXX",                                  "Units": "XXXXXX"})
	CFVars.insert({"Variable": "Ground heat flux",                              "Var Name": "XXXXXXXX", "CF Standard Name": "XXXXXXXXXXXXXX",                                  "Units": "W m-2"})
	CFVars.insert({"Variable": "Velocity potential 850 hPa",                    "Var Name": "XXXX",     "CF Standard Name": "velocity_potential_850_hpa",                      "Units": "m2 s-1"})
	CFVars.insert({"Variable": "Velocity potential 200 hPa",                    "Var Name": "XXXX",     "CF Standard Name": "velocity_potential_200_hpa",                      "Units": "m2 s-1"})
	CFVars.insert({"Variable": "Stream function 850 hPa",                       "Var Name": "XXXX",     "CF Standard Name": "stream_function_850_hpa",                         "Units": "m2 s-1"})
	CFVars.insert({"Variable": "Stream function 200 hPa",                       "Var Name": "XXXX",     "CF Standard Name": "stream_function_200_hpa",                         "Units": "m2 s-1"})
	#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------


	# VALID FREQUENCIES TABLE
	#----------------------------------------------------------------------------------------------------------
	ValidFreq.insert({"Frequency": "3hr"})
	ValidFreq.insert({"Frequency": "6hr"})
	ValidFreq.insert({"Frequency": "day"})
	ValidFreq.insert({"Frequency": "mon"})
	ValidFreq.insert({"Frequency": "Omon"})
	ValidFreq.insert({"Frequency": "yr"})
	#----------------------------------------------------------------------------------------------------------



	# STANDARD NAME KNOWN FIXES TABLE
	#-----------------------------------------------------------------------------------------------------------
	StandardNameFixes.insert({"Incorrect Standard Name": "air temp",                                        "Var Name": "tasmax",    "Known Fix": "air_temperature"})
	StandardNameFixes.insert({"Incorrect Standard Name": "air temp",                                        "Var Name": "tasmin",    "Known Fix": "air_temperature"})
	StandardNameFixes.insert({"Incorrect Standard Name": "air temperature",                                 "Var Name": "TA",        "Known Fix": "air_temperature"})
	StandardNameFixes.insert({"Incorrect Standard Name": "air temperature",                                 "Var Name": "ta",        "Known Fix": "air_temperature"})
	StandardNameFixes.insert({"Incorrect Standard Name": "zonal velocity",                                  "Var Name": "uo",        "Known Fix": "sea_water_x_velocity"})
	StandardNameFixes.insert({"Incorrect Standard Name": "lat",                                             "Var Name": "lat",       "Known Fix": "latitude"})
	StandardNameFixes.insert({"Incorrect Standard Name": "geopotential height (above sea level)",           "Var Name": "G",         "Known Fix": "geopotential"})
	StandardNameFixes.insert({"Incorrect Standard Name": "geopotential height (above sea level)",           "Var Name": "g",         "Known Fix": "geopotential"})
	StandardNameFixes.insert({"Incorrect Standard Name": "surface latent heat flux",                        "Var Name": "LHFLX",     "Known Fix": "surface_downward_latent_heat_flux"})
	StandardNameFixes.insert({"Incorrect Standard Name": "specific humidity",                               "Var Name": "HUS",       "Known Fix": "specific_humidity"})
	StandardNameFixes.insert({"Incorrect Standard Name": "total soil liquid water in total 15 columnn",     "Var Name": "MRSOV",     "Known Fix": "volume_fraction_of_condensed_water_in_soil"})
	StandardNameFixes.insert({"Incorrect Standard Name": "air pressure at sea level",                       "Var Name": "PSL",       "Known Fix": "air_pressure_at_sea_level"})
	StandardNameFixes.insert({"Incorrect Standard Name": "net longwave flux at surface",                    "Var Name": "FLNS",      "Known Fix": "surface_net_downward_longwave_flux"})
	StandardNameFixes.insert({"Incorrect Standard Name": "net longwave flux at top of model",               "Var Name": "FLNT",      "Known Fix": "toa_net_downward_longwave_flux"})
	StandardNameFixes.insert({"Incorrect Standard Name": "net solar flux at surface",                       "Var Name": "FSNS",      "Known Fix": "surface_net_downward_shortwave_flux"})
	StandardNameFixes.insert({"Incorrect Standard Name": "net solar flux at top of model",                  "Var Name": "FSNT",      "Known Fix": "toa_net_downward_shortwave_flux"})
	StandardNameFixes.insert({"Incorrect Standard Name": "total runoff (qover + qdrai + qrgwl)",            "Var Name": "TOTRUNOFF", "Known Fix": "total_runoff"})
	StandardNameFixes.insert({"Incorrect Standard Name": "zonal surface stress",                            "Var Name": "STX",       "Known Fix": "surface_zonal_stress_positive_to_the_west"})
	StandardNameFixes.insert({"Incorrect Standard Name": "meridional surface stress",                       "Var Name": "STY",       "Known Fix": "surface_meridional_stress_positive_to_the_north"})
	StandardNameFixes.insert({"Incorrect Standard Name": "salinity",                                        "Var Name": "SO",        "Known Fix": "sea_water_salinity"})
	StandardNameFixes.insert({"Incorrect Standard Name": "temperature",                                     "Var Name": "TO",        "Known Fix": "sea_water_temperature"})
	StandardNameFixes.insert({"Incorrect Standard Name": "surface_meridional_stress_positive_to_the_south", "Var Name": "sty",       "Known Fix": "surface_meridional_stress_positive_to_the_north"})
	StandardNameFixes.insert({"Incorrect Standard Name": "north_wind",                                      "Var Name": "va",        "Known Fix": "northward_wind"})
	StandardNameFixes.insert({"Incorrect Standard Name": "east_wind",                                       "Var Name": "ua",        "Known Fix": "eastward_wind"})
	#-----------------------------------------------------------------------------------------------------------




	# VARIABLE NAME KNOWN FIXES TABLE
	#-----------------------------------------------------------------------------------------------------------
	VarNameFixes.insert({"Incorrect Var Name": "height", "CF Standard Name": "height",                                          "Known Fix": "zh"})
	VarNameFixes.insert({"Incorrect Var Name": "LAT",    "CF Standard Name": "latitude",                                        "Known Fix": "lat"})
	VarNameFixes.insert({"Incorrect Var Name": "LON",    "CF Standard Name": "longitude",                                       "Known Fix": "lon"})
	VarNameFixes.insert({"Incorrect Var Name": "G",      "CF Standard Name": "geopotential",                                    "Known Fix": "g"})
	VarNameFixes.insert({"Incorrect Var Name": "t",      "CF Standard Name": "air_temperature",                                 "Known Fix": "ta"})
	VarNameFixes.insert({"Incorrect Var Name": "LHFLX",  "CF Standard Name": "surface_downward_latent_heat_flux",               "Known Fix": "hflsd"})
	VarNameFixes.insert({"Incorrect Var Name": "HUS",    "CF Standard Name": "specific_humidity",                               "Known Fix": "hus"})
	VarNameFixes.insert({"Incorrect Var Name": "MRSOV",  "CF Standard Name": "volume_fraction_of_condensed_water_in_soil",      "Known Fix": "mrsov"})
	VarNameFixes.insert({"Incorrect Var Name": "PSL",    "CF Standard Name": "air_pressure_at_sea_level",                       "Known Fix": "psl"})
	VarNameFixes.insert({"Incorrect Var Name": "FLNS",   "CF Standard Name": "surface_net_downward_longwave_flux",              "Known Fix": "rls"})
	VarNameFixes.insert({"Incorrect Var Name": "FLNT",   "CF Standard Name": "toa_net_downward_longwave_flux",                  "Known Fix": "rlt"})
	VarNameFixes.insert({"Incorrect Var Name": "FSNS",   "CF Standard Name": "surface_net_downward_shortwave_flux",             "Known Fix": "rss"})
	VarNameFixes.insert({"Incorrect Var Name": "FSNT",   "CF Standard Name": "toa_net_downward_shortwave_flux",                 "Known Fix": "rst"})
	VarNameFixes.insert({"Incorrect Var Name": "STX",    "CF Standard Name": "surface_zonal_stress_positive_to_the_west",       "Known Fix": "stx"})
	VarNameFixes.insert({"Incorrect Var Name": "STY",    "CF Standard Name": "surface_meridional_stress_positive_to_the_north", "Known Fix": "sty"})
	VarNameFixes.insert({"Incorrect Var Name": "zos",    "CF Standard Name": "sea_surface_height_above_geoid",                  "Known Fix": "zoh"})
	VarNameFixes.insert({"Incorrect Var Name": "lev",    "CF Standard Name": "air_pressure",                                    "Known Fix": "plev"})
	VarNameFixes.insert({"Incorrect Var Name": "SO",     "CF Standard Name": "sea_water_salinity",                              "Known Fix": "so"})
	VarNameFixes.insert({"Incorrect Var Name": "TO",     "CF Standard Name": "sea_water_temperature",                           "Known Fix": "to"})
	VarNameFixes.insert({"Incorrect Var Name": "TA",     "CF Standard Name": "air_temperature",                                 "Known Fix": "ta"})

	#-----------------------------------------------------------------------------------------------------------



	# FREQUENCIES KNOWN FIXES TABLE
	#-----------------------------------------------------------------------------------------------------------
	FreqFixes.insert({"Incorrect Freq": "month", "Known Fix": "mon"})