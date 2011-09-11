``django-flexi-auth`` is a simple, but flexible, role-based access-control engine for Django.

Inspired to ``django-permissions``, it goes some steps further in various directions, providing advanced features such as:

* context-sensitive roles (aka *parametric roles*, i.e. roles bound to one or more parameters);
* per-instance (row-level) permissions (aka *object-permissions*);
* dynamic permission checking: access-control policies are defined via a specific API on model classes, so they can be as flexible as needed by the application at hand;
* a custom Django authentication backend: permissions can be checked in the "Django way", i.e. calling the method ``user.has_perm()``.
