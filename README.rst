========================
HalWeb Framework 
========================
Note
----
**This is initial release of HalWeb, there will be changes incompatible with the current one. so please be patient.**

If you are eager to try it you need manualy to setup the **AppenginePath** in the **config.py** to HalWeb installation.

Offcourse you need to have Appengine on your system

Install
-------
Any of this three shoud work:

    shell>python setup.py install
    or
    shell>easy_install halweb
    or
    shell>python setup.py install`

Some Examples
-------------

Creating a project
``````````````````
        1. open hal.py in your shell by typing **hal**::
            
            cmd>hal

        2. Create a project::
            
            shell>hal
            hal>project /home/myhome/MyProjects/TestProject

        3. Run your project::
            
            shell>cd /home/myhome/MyProjects/TestProject
            shell>python manage.py
            hal>run

        **Woalla you have your project setup and running**  

Creating Model, View, Controller, Form and Handler in your Project
``````````````````````````````````````````````````````````````````
        Open the *manage.py* console in you project and type: ::
            
            hal>>mvcfh Galery.Photo

        *The console will give you the opportunity to setup the model*::
            
            ..............class Galery.Photo(db.Model):
            Property0>........

        *Populate it like this*::
            
            ..............class Galery.Photo(db.Model):
            Property0>........Name str required=True
            Property1>........Description txt
            Property2>........DateCreated date
            Property3>........Content blob
            Property4>........MimeType str
            Property5>........
            Save Galery.Photo?(y/n) y

        With this you have defined the Model, It's controller, forms and also address binding 
        which is added in the handlerMap.py file
        
        You can also add different Models under the 'Package' Galery and use them in the code
        
        **Later you can**

Manipulate you *Galery Package*
`````````````````````````````````
    With  
    
    Exporting it to some directory::
    
         hal>pack package Galery /some/destination/NameOfThePackage   
     
    Also unpack it from there to some other Hal project::
        
        hal>unpack package Galery /from/the/package/directory
    
    Or delete it if you were just playing::
    
        hal>del package Galery
    
    **Note: Official Online Hal Packages Repository is comming soon**
            
Continue Exploring ;)
`````````````````````


**I'll put more in near future, explaining how betautifully it works. :)**

.. image:: http://www.python.org/images/python-logo.gif 

.. image:: http://code.google.com/appengine/images/appengine_lowres.png

