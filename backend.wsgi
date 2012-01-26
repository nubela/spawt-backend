import sys, os

cwd = os.path.dirname(os.path.realpath(__file__))

sys.path.append(os.path.join(cwd, "src"))
sys.path.append(os.path.join(cwd, "site-packages"))

activate_this = os.path.join(cwd, "v_env/bin/activate_this.py")
execfile(activate_this, dict(__file__=activate_this))

from ctrleff import get_app

application = get_app()