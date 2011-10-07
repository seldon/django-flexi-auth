#!/usr/bin/env python 

from distutils.core import setup 
import os 

setup(
    name = "django-flexi-auth",
    version = "dev",
    description = """A simple, but flexible, role-based access-control engine for Django.
    
    Implement per-object permissions, a Django-compliant authorization backend, 
    and an easy-to-use and flexible authorization API to define model-specific 
    access-control policies.

    This software was originally developed within Gasista Felice <http://www.gasistafelice.org>,
    a project by REES Marche <http://www.reesmarche.org>.
    """, 
    author="Lorenzo Franceschini",
    author_email="lorenzo.franceschini@informaetica.it",
    url = "https://github.com/seldon/django-flexi-auth",
    packages = ["flexi_auth"],
    classifiers = ["Development Status :: 3 - Alpha",
                   "Environment :: Web Environment",
                   "Framework :: Django",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: GNU Affero General Public License v3",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python",
                   "Topic :: Utilities"],
)
