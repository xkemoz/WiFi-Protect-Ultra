import geoip2.database

# Path to the GeoLite2 database
GEOIP_DB_PATH = "/usr/share/GeoIP/GeoLite2-City.mmdb"

def get_location(ip):
    """ Determine the geographic location based on an IP address """
    try:
        reader = geoip2.database.Reader(GEOIP_DB_PATH)
        response = reader.city(ip)

        location_info = {
            "city": response.city.name or "Unknown",
            "country": response.country.name or "Unknown",
            "latitude": response.location.latitude if response.location.latitude else "Unknown",
            "longitude": response.location.longitude if response.location.longitude else "Unknown"
        }

        return location_info
    except Exception as e:
        return {"error": f"GeoIP Lookup Failed: {str(e)}"}
