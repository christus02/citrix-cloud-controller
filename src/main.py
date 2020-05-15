import sys, os
sys.path.append(os.path.abspath(os.path.join('..', 'pkg')))

# Now do your import
from pkg.gcp import api

api.run_server()