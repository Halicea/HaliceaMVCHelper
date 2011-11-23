#!/usr/bin/env python
import sys
import logging
try:
    from halicea import hal
except:
    print "Hal web is not located in your python path"
    print "accessing halweb thru path {{hal_path}}"
    sys.path.append("{{hal_path}}")
    import hal
if __name__=='__main__':
    hal.main_safe(sys.argv)