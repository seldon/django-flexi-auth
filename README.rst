Overwiew
========
``django-flexi-auth`` is a simple, but flexible, role-based access-control engine for Django.

Features
========

Inspired to ``django-permissions``, it goes some steps further in various directions, providing advanced features such as:

* context-sensitive roles (aka *parametric roles*, i.e. roles bound to one or more parameters);
* per-instance (row-level) permissions (aka *object-permissions*);
* dynamic permission checking: access-control policies are defined via a specific API on model classes, so they can be as flexible as needed by the application at hand;
* a custom Django authentication backend: permissions can be checked in the "Django way", i.e. calling the method ``user.has_perm()``.


Custom settings
===============

ROLES_LIST
----------
:Name: ROLES_LIST
:Type: 
    A tuple/list of 2-tuples of the form ``(<name>, <description>)``. ``<name>`` must be a string (100 char max), while ``<description>`` can be a string 
    or a localized string.
:Default: ``()``
:Description: 
    A list of the general roles allowed in a given application domain (as strings); they are used as a "base" for building parametric roles of that kind.   
    *Example*: on a multi-site publishing platform, there could be an ``EDITOR`` general role, but the actual (parametric) roles are tied with a specific 
    site.

PARAM_CHOICES
-------------
:Name: PARAM_CHOICES
:Type: 
    A tuple/list of 2-tuples of the form ``(<name>, <full name>)``. ``<name>`` must be a string (20 char max), while ``<full name>`` can be a string 
    or a localized string.
:Default: ``()``
:Description: 
    A list of the parameters (as strings) allowed in a given application domain for binding to roles.
    *Example*: on a multi-site publishing platform, there could be a ``site`` parameter, representing a specific website instance.


VALID_PARAMS_FOR_ROLES
----------------------
:Name: VALID_PARAMS_FOR_ROLES
:Type: 
    A dictionary made by entries of the form ``{<role name>: {<parameter name>: <parameter type>, ..}}``, where ``<role name>`` is the name of one of the 
    general roles allowed within the application domain, ``<parameter name>`` is the name of one of the parameters that may be bound to that role 
    (must be an element of ``PARAM_CHOICES``), and ``<parameter type>`` is the type of that parameter (a model), expressed as a string of the format 
    ``app_label.model_name``.    
:Default: ``{}``
:Description: 
    This dictionary represents the constraints posed by the application-domain on the parameters a general role can be tied to (with respect to their name, 
    type, number).  A missing dictionary keys for a role means that that a role can take any number of parameters of any kind (among those declared in the
    ``PARAM_CHOICES`` configuration setting).
