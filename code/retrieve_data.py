import os
import wget
import shutil

# --- Create folder for datasets, destory if existing
data_path = 'datasets/'
if os.path.exists( data_path ):
    shutil.rmtree( data_path )
os.makedirs( data_path )

# --- Read urls in
fname = "./datasets.txt"
f_url = open( fname , 'r' )
urls = f_url.readlines()
f_url.close()

# --- Download datasets
output_fnames = [ 'crash.csv' , 'weather.csv' ]
for i in range( len(urls) ) :
    # Remove newline at the end
    url = urls[i].splitlines()[0]
    print( 'Downloading {}'.format( output_fnames[i] ) )
    wget.download( url , data_path + output_fnames[i] )
    print( '\n{} Finished'.format( output_fnames[i] ) )
