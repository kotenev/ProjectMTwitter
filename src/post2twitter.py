# Gather command line arguments
import optparse
import mysql.connector

usage = "%prog [options] sample_barcode data_file"
version = "%prog 0.1"
parser = optparse.OptionParser(usage=usage, version=version)
parser.add_option("-t", "--tmp", dest="temp_dir",
                  help="Store intermediate files in a temp directory.",
                  default="/tmp/")
parser.add_option("-s", "--syslog", dest="syslog",
                  help="Location of syslog server", default='localhost')
parser.add_option("-p", "--syslog_port", dest="syslog_port",
                  help="Port to connect to syslog server on", default=514)
parser.add_option("-c", "--credentials", dest="credential_dir",
                  help="Directory containing credentials for twitter etc", default="creds")

(options, args) = parser.parse_args()


# Add a syslog handler for logging to graylog
import logging
import logging.handlers as handlers

logging.basicConfig(level=logging.INFO)
syslog = handlers.SysLogHandler(address=(options.syslog, options.syslog_port))
syslog.setFormatter(logging.Formatter('ProjectMTwitter:%(message)s'))
syslog.setLevel(logging.DEBUG)
logging.getLogger('').addHandler(syslog)
logging.info("Completed syslog setup")


# Sort out twitter credentials
logging.info("Sort out twitter credentials")
import os
import twitter
import json

creds = None
creds_path = os.path.join(options.credential_dir,'credentials.json')
logging.info("Path to creds is '%s'" % (creds_path))

with open(creds_path) as json_data:
    creds = json.load(json_data)

logging.info("credentials loaded")
api = twitter.Api(consumer_key=creds['consumer_key'],
                  consumer_secret=creds['consumer_secret'],
                  access_token_key=creds['access_token'],
                  access_token_secret=creds['access_token_secret'])

logging.info("verifying credentials")
logging.debug(api.VerifyCredentials())


# Load data
import numpy as np

data_file_name = args[1]
logging.info("loading data file '%s'" % (data_file_name))
a = np.loadtxt(data_file_name, unpack=True)


# Plot images to temp file
import pylab as pl
import matplotlib.pyplot as plt

fig1_file_name = os.path.join(options.temp_dir, 'pic1.png')
logging.info("Preparing '%s'" % (fig1_file_name))
plt.close()
plt.plot(a[0][100:7000],a[1][100:7000])
plt.ylabel('Intensity')
logging.info("Saving '%s'" % (fig1_file_name))
pl.savefig(fig1_file_name, bbox_inches='tight')

fig2_file_name = os.path.join(options.temp_dir, 'pic2.png')
logging.info("Preparing '%s'" % (fig2_file_name))
plt.close()
plt.plot(a[0][100:1000],a[1][100:1000])
plt.ylabel('Intensity')
logging.info("Saving '%s'" % (fig2_file_name))
pl.savefig(fig2_file_name, bbox_inches='tight')

fig3_file_name = os.path.join(options.temp_dir, 'pic3.png')
logging.info("Preparing '%s'" % (fig3_file_name))
plt.close()
plt.plot(a[0][1000:2000],a[1][1000:2000])
plt.ylabel('Intensity')
logging.info("Saving '%s'" % (fig3_file_name))
pl.savefig(fig3_file_name, bbox_inches='tight')

fig4_file_name = os.path.join(options.temp_dir, 'pic4.png')
logging.info("Preparing '%s'" % (fig4_file_name))
plt.close()
plt.plot(a[0][2000:3000],a[1][2000:3000])
plt.ylabel('Intensity')
logging.info("Saving '%s'" % (fig4_file_name))
pl.savefig(fig4_file_name, bbox_inches='tight')

# Connect to DB
conn = mysql.connector.connect(user='user', password='pw', host='host', database='db', port=int('port'))
if conn is not None:
    conn.autocommit=True
cursor = self.conn.cursor(dictionary=True)

# Retrieve the school name for the given sample barcode
barcode = sys.argv[-2]
query = """SELECT lab.name 
FROM Laboratory lab 
  INNER JOIN Person p on p.laboratoryId = lab.laboratoryId
  INNER JOIN LabContact lc on lc.personId = p.personId
  INNER JOIN Shipping s on s.returnLabContactId = lc.labContactId
  INNER JOIN Dewar d on d.shippingId = s.shippingId
  INNER JOIN Container c on c.dewarId = d.dewarId
  INNER JOIN BLSample bls on bls.containerId = c.containerId
WHERE
  bls.name = %s"""

cursor.execute(query, barcode)
rs = cursor.fetchone()
if len(rs) == 0:
    logging.error("Couldn't find a school for sample barcode %s" % barcode)

school = rs.iteritems().next()[1]
cursor.close()
conn.close()

# Look-up the twitter handle for the school 


# Post the update to twitter
logging.info("Posting update to twitter")
status = api.PostUpdate('Data collection test 1/... for @basham_mark',
                        media=[fig1_file_name,
                               fig2_file_name,
                               fig3_file_name,
                               fig4_file_name])


