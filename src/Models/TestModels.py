import settings
from google.appengine.ext import db
#{% block imports%}
#{%endblock%}
################

class Test(db.Model):
    """TODO: Describe Test"""
    p1= db.IntegerProperty()
    
    @classmethod
    def CreateNew(cls ,p1 , _isAutoInsert=False):
        result = cls(
                     p1=p1,)
        if _isAutoInsert: result.put()
        return result
    def __str__(self):
        #TODO: Change the method to represent something meaningful
        return 'Change __str__ method' 
## End Test

