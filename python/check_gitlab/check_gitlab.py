#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

import nagiosplugin
import logging
import re


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


# TODO: Alert based on uptime (maybe even accepting external input)


#Function to check whether a variable is an integer

def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False



class Gitlab_Workhorse(nagiosplugin.Context):
    def evaluate(self, metric, resource):
        logging.debug('Metric value: %s' %metric.value)
        if metric.value[0] != 0:
            return self.result_cls(nagiosplugin.state.Ok, "Service: Gitlab-workhorse running", metric)
        else:
            return self.result_cls(nagiosplugin.state.Critical, "Service: Gitlab-workhorse not running", metric)

    def performance(self, metric, resource):
        perfname = metric.name + "_uptime"
        if metric.value[0] != 0:
            return nagiosplugin.performance.Performance(perfname, metric.value[1], 's')
        else:
            # We return perfdata equal to 0 while the service is down
            return nagiosplugin.performance.Performance(perfname, 0, 's')

class Gitlab_Redis(nagiosplugin.Context):
    def evaluate(self, metric, resource):
        if metric.value[0] != 0:
            return self.result_cls(nagiosplugin.state.Ok, "Service: Gitlab-redis running", metric)
        else:
            return self.result_cls(nagiosplugin.state.Critical, "Service: Gitlab-redis not running", metric)

    def performance(self, metric, resource):
        perfname = metric.name + "_uptime"
        if metric.value[0] != 0:
            return nagiosplugin.performance.Performance(perfname, metric.value[1], 's')
        else:
            # We return perfdata equal to 0 while the service is down
            return nagiosplugin.performance.Performance(perfname, 0, 's')

class Gitlab_Sidekiq(nagiosplugin.Context):
    def evaluate(self, metric, resource):
        if metric.value[0] != 0:
            return self.result_cls(nagiosplugin.state.Ok, "Service: Gitlab-sidekiq running", metric)
        else:
            return self.result_cls(nagiosplugin.state.Critical, "Service: Gitlab-sidekiq not running", metric)

    def performance(self, metric, resource):
        perfname = metric.name + "_uptime"
        if metric.value[0] != 0:
            return nagiosplugin.performance.Performance(perfname, metric.value[1], 's')
        else:
            # We return perfdata equal to 0 while the service is down
            return nagiosplugin.performance.Performance(perfname, 0, 's')

class Gitlab_Nginx(nagiosplugin.Context):
    def evaluate(self, metric, resource):
        if metric.value[0] != 0:
            return self.result_cls(nagiosplugin.state.Ok, "Service: Gitlab-nginx running", metric)
        else:
            return self.result_cls(nagiosplugin.state.Critical, "Service: Gitlab-nginx not running", metric)

    def performance(self, metric, resource):
        perfname = metric.name + "_uptime"
        if metric.value[0] != 0:
            return nagiosplugin.performance.Performance(perfname, metric.value[1], 's')
        else:
            # We return perfdata equal to 0 while the service is down
            return nagiosplugin.performance.Performance(perfname, 0, 's')



class Gitlab_Logrotate(nagiosplugin.Context):
    def evaluate(self, metric, resource):
        if metric.value[0] != 0:
            return self.result_cls(nagiosplugin.state.Ok, "Service: Gitlab-logrotate running", metric)
        else:
            return self.result_cls(nagiosplugin.state.Critical, "Service: Gitlab-logrotate not running", metric)

    def performance(self, metric, resource):
        perfname = metric.name + "_uptime"
        if metric.value[0] != 0:
            return nagiosplugin.performance.Performance(perfname, metric.value[1], 's')
        else:
            # We return perfdata equal to 0 while the service is down
            return nagiosplugin.performance.Performance(perfname, 0, 's')

class Gitlab_Unicorn(nagiosplugin.Context):
    def evaluate(self, metric, resource):
        if metric.value[0] != 0:
            return self.result_cls(nagiosplugin.state.Ok, "Service: Gitlab-Unicorn running", metric)
        else:
            return self.result_cls(nagiosplugin.state.Critical, "Service: Gitlab-Unicorn not running", metric)

    def performance(self, metric, resource):
        perfname = metric.name + "_uptime"
        if metric.value[0] != 0:
            return nagiosplugin.performance.Performance(perfname, metric.value[1], 's')
        else:
            # We return perfdata equal to 0 while the service is down
            return nagiosplugin.performance.Performance(perfname, 0, 's')



class Gitlab_Postgresql(nagiosplugin.Context):
    def evaluate(self, metric, resource):
        if metric.value[0] != 0:
            return self.result_cls(nagiosplugin.state.Ok, "Service: Gitlab-Postgresql running", metric)
        else:
            return self.result_cls(nagiosplugin.state.Critical, "Service: Gitlab-Postgresql not running", metric)

    def performance(self, metric, resource):
        perfname = metric.name + "_uptime"
        if metric.value[0] != 0:
            return nagiosplugin.performance.Performance(perfname, metric.value[1], 's')
        else:
            # We return perfdata equal to 0 while the service is down
            return nagiosplugin.performance.Performance(perfname, 0, 's')



class Gitlab(nagiosplugin.Resource):

    def probe(self):
        logging.debug('Parsing example log file' )
        services = self.services()
        logging.debug(services)

        yield nagiosplugin.Metric('gitlab_workhorse', services['gitlab-workhorse'])
        yield nagiosplugin.Metric('gitlab_redis', services['redis'])
        yield nagiosplugin.Metric('gitlab_sidekiq', services['sidekiq'])
        yield nagiosplugin.Metric('gitlab_nginx', services['nginx'])
        yield nagiosplugin.Metric('gitlab_logrotate', services['logrotate'])
        yield nagiosplugin.Metric('gitlab_unicorn', services['unicorn'])
        yield nagiosplugin.Metric('gitlab_postgresql', services['postgresql'])


# Parser for the services output, examples of the data can be found in the example_data folder

    def services(self):

        ## Uncomment the following line to load dummy data
        #f = open('example_data/gitlab.txt')
        import subprocess
        p = subprocess.Popen(["gitlab-ctl", "status"], stdout=subprocess.PIPE)
        dict = {}
        #
        for line in iter(p.stdout.readline, ''):
        ## Uncomment the following line when loading dummy data
        #for line in f:
            # We are just interested in the first half of the output (the one regarding the actual services)
            index = line.index(';')
            line = line[0:index]
            # We extract the service name between the the colons
            service = re.findall('\s\w+\-*\w+\S', line)
            service = service[0][1:-1]
            # We try to extract the PID number, if we get something other than a number, we set it to 0 (this triggers a
            # Critical output)
            try:
                pid = re.findall('\pid\s(\d+)', line)[0]
            except:
                pid = 0
            #if not RepresentsInt(pid):
            #    pid = 0
            # We extract the uptime in seconds here

            uptime = re.findall('\d+s', line)
            uptime = uptime[0][:-1]
            # We just add a new item to the Dict containing the PID and the uptime so it can be easily accessed by
            # service name
            dict[service] = [pid, uptime]
        return dict

class GitlabSummary(nagiosplugin.Summary):

    #def __init__(self):

    def ok(self,results):
        return "All services running"

    def problem(self,results):
        for i in results:
            if "not" in str(i):
                print(i)

        return ("At least one service is not running!")

@nagiosplugin.guarded
def main():
    check = nagiosplugin.Check(Gitlab())
    check.add(Gitlab_Workhorse('gitlab_workhorse'))
    check.add(Gitlab_Redis('gitlab_redis'))
    check.add(Gitlab_Sidekiq('gitlab_sidekiq'))
    check.add(Gitlab_Nginx('gitlab_nginx'))
    check.add(Gitlab_Logrotate('gitlab_logrotate'))
    check.add(Gitlab_Unicorn('gitlab_unicorn'))
    check.add(Gitlab_Postgresql('gitlab_postgresql'))
    check.add(GitlabSummary())
    check.main()

if __name__ == '__main__':
    main()




