# Authenticate NASA Earthdata Login

import netrc, fsspec, aiohttp


def authenticate(site):
    try:
        (username, account, password) = netrc.netrc().authenticators(site)  # Get login information
        fsspec.config.conf['https'] = dict(
            client_kwargs={'auth': aiohttp.BasicAuth(username, password)})  # Add login information to HTTPS requests
        print("Authenticated as " + username + " for " + site)
    except Exception as err:
        raise SystemExit("""Could not authenticate. Check that a NetRC 
file is present in your home directory with login credentials 
for """ + site + """ (see 
https://wiki.earthdata.nasa.gov/display/EL/How+To+Access+Data+With+cURL+And+Wget). 
Please *do not* place the NetRC file in this cloned repository as if you did, your 
credentials would be published with your changes.""")

def remove():
    print("Removing authentication")
    del fsspec.config.conf['https']