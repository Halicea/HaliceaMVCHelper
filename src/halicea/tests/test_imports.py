import os
from os.path import dirname, join as pjoin
PROJECT_LOC = os.path.abspath(pjoin(dirname(__file__), 'testProjectV1_Actual'))
INSTALL_LOC = os.path.abspath(dirname(dirname(dirname(__file__))))
TEMPLATE_LOC = pjoin(INSTALL_LOC, 'Templates')
print PROJECT_LOC, INSTALL_LOC, TEMPLATE_LOC