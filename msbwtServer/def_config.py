# Configuration values for msbwtServer
# Values can be accessed at app.config['KEY']

#### General Info ####

# General service information

DATA = {
    'name': "Name of Dataset or Preference",
    'description': "Description of dataset",
}

##### DATABASE ####

# Location of Database file
DB_ROOT = '/path/to/database/file.sqlite'

# Location of Hosts file
HOST_ROOT='/path/to/host/file'

# Duration that queries remain in database (minutes)
HOST_QUERY_TIMING = 5
