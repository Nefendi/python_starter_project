from lagom.integrations.fast_api import FastApiIntegration

from ioc.ioc import container

deps = FastApiIntegration(container)

lagom_depends = deps.depends
