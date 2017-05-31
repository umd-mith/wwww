
# coding: utf-8

# # Inspecting WARC
# 
# In this notebook we're going to use the Python [warcio](https://github.com/webrecorder/warcio) library to examine a [WARC](https://en.wikipedia.org/wiki/Web_ARChive) file. This particular WARC file was generated for the [Technoromanticism class blog](http://mith.umd.edu/eng738T/) Wordpress site using [wget](https://www.gnu.org/software/wget/):
# 
# ```
# wget --mirror --warc-file eng738T --no-parent http://mith.umd.edu/eng738T/
# ```
#  
# <img src="images/website.png" style="width: 70%; border: thin solid #ccc;">
# 
# The goal here isn't to learn how to generate a WARC file but to learn a little about the structure of a WARC file, and how to read it with Python.

# ## Imports
# 
# First we need to import some things to help us work with the WARC data. The first thing we need is [WebRecorder](https://webrecorder.io)'s [warcio](https://github.com/webrecorder/warcio) library that makes it possible to read and write WARC files from Python. We're going to be reading WARC data so we need to import the ArchiveIterator class that lets us walk through each record in a WARC file.

# In[1]:

from warcio.archiveiterator import ArchiveIterator


# We're going to be looking at links in HTML pages so we'll need a good HTML parser like [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#) for parsing the HTML. Python also comes with a handy [urlparse](https://docs.python.org/3.6/library/urllib.parse.html#urllib.parse.urlparse) function for parsing URLs:

# In[2]:

from bs4 import BeautifulSoup
from urllib.parse import urlparse


# ## Count Hostnames
# 
# Now that we've loaded the libraries we need let's create a dictionary to keep track of the hostnames we find in links on the website.

# In[3]:

counts = {}


# Now let's create a function that will take a WARC record as input and if the record is for an HTML response it will parse the HTML using BeautifulSoup, and then loop through all the anchor tags and count the host names used.

# In[4]:

def count_links(record):
    if "html" not in record.http_headers.get("content-type"):
        return
    doc = BeautifulSoup(record.raw_stream, "lxml")
    for link in doc.select("a"):
        url = urlparse(link["href"])
        counts[url.hostname] = counts.get(url.hostname, 0) + 1


# And now we can open up our WARC file and iterate through all the records. We are only interested in counting the urls the responses.

# In[ ]:

for record in ArchiveIterator(open("eng738T.warc.gz", "rb")):
    if record.rec_type == "response":
        count_links(record)


# In[6]:

print(counts)


# That's a bit of a jumble so let's print out the hostnames in order of how many links they have:

# In[18]:

for hostname in sorted(counts.keys(), key=counts.get, reverse=True):
    print("%-35s  %8i" %(hostname, counts[hostname]))


# In[ ]:



