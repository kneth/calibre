##    Copyright (C) 2006 Kovid Goyal kovid@kovidgoyal.net
##    This program is free software; you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation; either version 2 of the License, or
##    (at your option) any later version.
##
##    This program is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License for more details.
##
##    You should have received a copy of the GNU General Public License along
##    with this program; if not, write to the Free Software Foundation, Inc.,
##    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#!/usr/bin/env python
import sys, re
sys.path.append('src')
from libprs500 import __version__ as VERSION

import ez_setup
ez_setup.use_setuptools()
from setuptools import setup, find_packages


################################# py2exe #######################################
py2exe_options = {}
if sys.argv[1] == 'py2exe':
    py2exe_dir = 'C:\libprs500'
    f = open('installer.nsi', 'r+')
    src = f.read()
    f.seek(0)
    src = re.sub('(define PRODUCT_VERSION).*', r'\1 "'+VERSION+'"', src)
    src = re.sub('(define PY2EXE_DIR).*', r'\1 "'+py2exe_dir+'"', src)
    f.write(src)
    f.close()
    try:
        import py2exe
        console = [
                    {'script' : 'src/libprs500/cli/main.py', 'dest_base':'prs500'},
                    {'script' : 'src/libprs500/lrf/html/convert_from.py', 'dest_base':'html2lrf'},
                    {'script' : 'src/libprs500/lrf/txt/convert_from.py', 'dest_base':'txt2lrf'},
                    {'script' : 'src/libprs500/lrf/meta.py', 'dest_base':'lrf-meta'},
                    {'script' : 'src/libprs500/metadata/rtf.py', 'dest_base':'rtf-meta'},
                  ]
        windows = [{'script' : 'src/libprs500/gui/main.py', 'dest_base':'prs500-gui',
                    'icon_resources':[(1,'icons/library.ico')]}]
        excludes = ["Tkconstants", "Tkinter", "tcl", "_imagingtk", 
                    "ImageTk", "FixTk"]
        options = { 'py2exe' : {'includes' : ['sip', 'pkg_resources'], 
                                'dist_dir' : py2exe_dir,
                                'packages' : ['PIL'],
                                'excludes' : excludes}}
        py2exe_options = {'console'  : console, 'windows' : windows, 
                          'options'  : options, 'excludes' : excludes}
    except ImportError:
        print >>sys.stderr, 'Must be in Windows to run py2exe'
        sys.exit(1)
################################################################################
    

if sys.hexversion < 0x2050000:
    print >> sys.stderr, "You must use python >= 2.5 Try invoking this script as python2.5 setup.py."
    print >> sys.stderr, "If you are using easy_install, try easy_install-2.5"
    sys.exit(1)
    

setup(
      name='libprs500', 
      packages = find_packages('src'), 
      package_dir = { '' : 'src' }, 
      version=VERSION, 
      author='Kovid Goyal', 
      author_email='kovid@kovidgoyal.net', 
      url = 'http://libprs500.kovidgoyal.net', 
      package_data = { \
                        'libprs500.gui' : ['*.ui'], \
                        'libprs500.lrf' : ['*.jar', '*.jpg'], \
                        'libprs500.metadata' : ['*.pl'] \
                     }, 
      entry_points = {
        'console_scripts': [ \
                             'prs500 = libprs500.cli.main:main', \
                             'lrf-meta = libprs500.lrf.meta:main', \
                             'rtf-meta = libprs500.metadata.rtf:main', \
                             'txt2lrf = libprs500.lrf.makelrf:txt', \
                             'html2lrf = libprs500.lrf.html.convert_from:main',\
                           ], 
        'gui_scripts'    : [ 'prs500-gui = libprs500.gui.main:main']
      }, 
      zip_safe = True,
      description = 
                  """
                  Library to interface with the Sony Portable Reader 500 
                  over USB. Also has a GUI with library management features.
                  """, 
      long_description = 
      """
      libprs500 is a ebook management application. It maintains an ebook library
      and allows for easy transfer of books from the library to an ebook reader.
      At the moment, it supports the `SONY Portable Reader`_.
      
      It can also convert various popular ebook formats into LRF, the native
      ebook format of the SONY Reader.
      
      For screenshots: https://libprs500.kovidgoyal.net/wiki/Screenshots
      
      For installation/usage instructions please see 
      https://libprs500.kovidgoyal.net/wiki/WikiStart#Installation
      
      For SVN access: svn co https://svn.kovidgoyal.net/code/libprs500
      
        .. _SONY Portable Reader: http://Sony.com/reader
        .. _USB: http://www.usb.org  
      """, 
      license = 'GPL', 
      classifiers = [
        'Development Status :: 3 - Alpha', 
        'Environment :: Console', 
        'Environment :: X11 Applications :: Qt', 
        'Intended Audience :: Developers', 
        'Intended Audience :: End Users/Desktop', 
        'License :: OSI Approved :: GNU General Public License (GPL)', 
        'Natural Language :: English', 
        'Operating System :: POSIX :: Linux', 
        'Programming Language :: Python', 
        'Topic :: Software Development :: Libraries :: Python Modules', 
        'Topic :: System :: Hardware :: Hardware Drivers'
        ],
        **py2exe_options   
     )

try:
  import PyQt4
except ImportError:
  print "You do not have PyQt4 installed. The GUI will not work.", \
        "You can obtain PyQt4 from http://www.riverbankcomputing.co.uk/pyqt/download.php"
else:
  import PyQt4.QtCore
  if PyQt4.QtCore.PYQT_VERSION < 0x40101:
    print "WARNING: The GUI needs PyQt >= 4.1.1"
