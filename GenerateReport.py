import sys
import json
import ConfigParser
from time import strftime, localtime
from WeatherWebServicesCall import WeatherInfo_Extractor

TOT_RECS=0
INVALID_RECS=0

try:
    config = ConfigParser.ConfigParser()
    config.read('project.config')
    APP_ID = config.get('ENV', 'APP_ID')
    WEATHER_DATA_URL = config.get('ENV', 'WEATHER_DATA_URL')
    ELEVATION_DATA_URL = config.get('ENV', 'ELEVATION_DATA_URL')
    cntryDetails = open("locationdetails.txt","r")
    invalidRecs = open("ExceptionRecordLog.txt","w")
    weatherRep = open("WeatherReport.txt","w")

    for cntry in cntryDetails:
        locURL = WeatherInfo_Extractor(WEATHER_DATA_URL + cntry.strip() + '&appid=' + APP_ID)
        locDetails = locURL.getWeatherInfo()
        if locDetails["cod"] == "404":
            invalidRecs.write(cntry)
            INVALID_RECS=INVALID_RECS + 1
        elif locDetails["cod"] == "401":
            print "It seems there is a problem with API Key. Please validate."
            cntryDetails.close()
            invalidRecs.close()
            weatherRep.close()
            quit() 
        elif locDetails["cod"] == "999":
            print "Unhandled Exception occured. Please check the script."
            quit()
        else:
            latlon = str(locDetails["coord"]["lat"]) + ',' + str(locDetails["coord"]["lon"])
            elevURL = WeatherInfo_Extractor(ELEVATION_DATA_URL + latlon + '&sensor=true_or_false')
            posDetails = elevURL.getWeatherInfo()
            location = latlon + ',' + str(posDetails["results"][0]["elevation"])
            loctime = strftime("%Y-%m-%d %H:%M:%S", localtime(int(locDetails["dt"])))
            weatherRep.writelines("%s|%s|%s|%s|%s|%s|%s\n" % (locDetails["name"], location, loctime , locDetails["weather"][0]["main"], int(locDetails["main"]["temp"])-273.15, locDetails["main"]["pressure"], locDetails["main"]["humidity"]))
            del locURL, locDetails, latlon, elevURL, posDetails, location, loctime
            TOT_RECS = TOT_RECS + 1
        
except IOError, e:
    print "Error>>>>> IO Exception occured. Please check if you have provided location details in locationdetails.txt. \nAlso check the current user have permission to save the generated report in current location."
except IndexError, e:
    print "Error>>>>> Index error occured. This could be due to below: \n 1. API Key not provided as argument to the script.\n 2. Busy webservice that is used in this program. Since it is free service sometimes elelevation url doesn't respond as expected. Please try after some time."
except ConfigParser.NoOptionError, e:
    print "Error>>>>> Please check if project.config file is provided with appropriate options."
except ConfigParser.NoSectionError, e:
    print "Error>>>>> Please check if project.config file is provided with appropriate sections."
else:
    cntryDetails.close()
    invalidRecs.close()
    weatherRep.close()
    print "#################################.....REPORT SUMMARY.....######################################"
    print "        Total Records parsed          :" + str(TOT_RECS) 
    print "        Records parsed successfully   :" + str(TOT_RECS - INVALID_RECS)
    print "        Records with exception        :" + str(INVALID_RECS)
    print "###############################################################################################"
