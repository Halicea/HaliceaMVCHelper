#{%block imports%}
from Controllers import ShellControllers
from Controllers import HalWebControllers
#{%endblock%}
webapphandlers = [
#{%block ApplicationControllers %}



#{%block ShellControllers%}
('/admin/Shell', ShellControllers.FrontPageController),
('/admin/stat.do', ShellControllers.StatementController),
#{%endblock%}

#{%block HalWebControllers%}
('/', HalWebControllers.WelcomeController),
#{%endblock%}

#{%endblock%}
]

