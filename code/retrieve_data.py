import os
import wget
import shutil
from datetime import datetime

# --- Create folder for datasets, destory if existing
data_path = 'datasets/'
if os.path.exists( data_path ):
    shutil.rmtree( data_path )
os.makedirs( data_path )

# --- Read urls in
fname = "./datasets.txt"
f_url = open( fname , 'r' )
urls = [line.rstrip() for line in f_url.readlines()]
f_url.close()

# --- Download datasets
output_fnames = [ 'covid19.csv' , 'weather.csv' , 'crash.csv' ]

for i in range( len(urls) ) :
#for i in range( 0 , 2 ) :
    # Remove newline at the end
    url = urls[i].splitlines()[0]
    print( "\n'{}' downloading: {}".format( output_fnames[i], datetime.now() ) )
    wget.download( url , data_path + output_fnames[i] )
    print( "\n'{}' downloaded: {}".format( output_fnames[i] , datetime.now() ) )
