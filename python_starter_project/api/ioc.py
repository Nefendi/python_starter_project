from lagom.integrations.fast_api import FastApiIntegration

from python_starter_project.ioc.ioc import container

deps = FastApiIntegration(container)

lagom_depends = deps.depends
