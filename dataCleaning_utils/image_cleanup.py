#   @@@@@@@@@@@@@@@@@@@@@@@@
#   **Code by Aron Talai****
#   @@@@@@@@@@@@@@@@@@@@@@@@

# perfrom sanity checks on image quality in an unidentified image source

#def libs
import os
import io
import tqdm
import numpy as np
from tqdm import tqdm
import matplotlib.image as mpimg
import PySimpleGUI as sg
from skimage import io
import glob
import shutil
from os.path import dirname, abspath
import imghdr


def flag_corrupt_images(_path):

  image_formats = ['rgb','gif','pbm','pgm','ppm','tiff',
                    'rast','xbm','jpeg','jpg','bmp','png']

  # local init
  bad_io_images = []
  bad_hdr_images = []
  all_files = [f for f in os.listdir(_path)]
  moved_path = os.path.join(dirname(abspath(_path)),'moved_files')

  # warning on non-image data
  for i in range(0,len(range(0,len(all_files)))):
      if str(all_files[i]).split('.')[-1] not in image_formats:
          print ('Non-image data type detected! Consider using an initial sanity check on the directory.')


  # run tests
  print ('Running skimage quality check...\n')
  for i in tqdm(range(0,len(all_files))):
      try:image_check_io = io.imread(os.path.join(_path,all_files[i]))
      except:bad_io_images.append(all_files[i])

  if len(bad_io_images) == 0:
      print ('skimage test passed!\n')

  else:
      print ('Images that failed the skimage quality check:\n')
      for i in range(0,len(bad_io_images)):
          print (bad_io_images[i])

      print ('----------------------------------')


  print ('Running imghdr quality check...\n')
  for i in tqdm(range(0,len(all_files))):
      if str(imghdr.what(os.path.join(_path,all_files[i]))) == 'None':
          bad_hdr_images.append(all_files[i])

  if len(bad_hdr_images) == 0: 
      print ('Imaghdr test passed!\n')

  else:
      print ('Images that failed the imghdr quality check:\n')
      for i in range(0,len(bad_hdr_images)):
          print (bad_hdr_images[i])

      print ('----------------------------------')


  # Should I move the corrupt images
  if len(bad_io_images) != 0:

      for i in range(0,len(bad_io_images)):
        
          shutil.move(os.path.join(_path,bad_io_images[i]), os.path.join(moved_path,bad_io_images[i]))
          print (bad_io_images[i],' --> Has been moved to {}'.format(moved_path),'\n')
 

  if len(bad_hdr_images) != 0:

      for i in range(0,len(bad_hdr_images)):
        
          shutil.move(os.path.join(_path,bad_hdr_images[i]), os.path.join(moved_path,bad_hdr_images[i]))
          print (bad_hdr_images[i],' --> Has been moved to {}'.format(moved_path),'\n') 

class image_quality_test():

    def __init__(self,_path):

        self._path = _path


    def initial_sanity_check(self, path_to_images):

        self._path = path_to_images
        try:os.mkdir(os.path.join(dirname(abspath(_path)),'moved_files'))
        except: pass

        moved_path = os.path.join(dirname(abspath(_path)),'moved_files')

        all_files = [f for f in os.listdir(_path)]
        all_files_extensions = list(set([f.split('.')[-1] for f in os.listdir(_path)]))

        extension_results = np.zeros((len(all_files_extensions), 2), dtype=object)

        for i in range(0,len(all_files_extensions)):

            extension_results[i,0] = all_files_extensions[i]
            extension_results[i,1] = len(glob.glob1(_path,"*.{}".format(all_files_extensions[i])))

        print (extension_results) 

        # Should I move non-image files to another directory?
        for i in range(0,len(range(0,len(all_files)))):

            if str(all_files[i]).split('.')[-1] not in image_formats:
                shutil.move(os.path.join(_path,all_files[i]), os.path.join(moved_path,all_files[i]))
                print (all_files[i],' --> Has been moved to {}'.format(moved_path),'\n')

