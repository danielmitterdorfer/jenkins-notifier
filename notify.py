#!/usr/local/bin/python3

#
# Note: Ideally the shebang line would contain /usr/bin/env python3 instead of the
#       hardcoded path but it seems the user's environment is not inherited by
#       LaunchAgents (at least not on El Capitan).
#

import configparser
import os
import sys
import urllib.parse


import jenkins
import pync


def read(section, key, default_value):
    if key in section:
        value = section[key]
        if len(value) > 0:
            return value
        else:
            return default_value
    else:
        return default_value


JENKINS_URL = "jenkins.url"


def main():
    config_file = "%s/.jenkins-notifier/config.ini" % os.getenv("HOME")

    config = configparser.ConfigParser()
    config.read(config_file)

    if not "url" in config[JENKINS_URL]:
        print("Invalid configuration in [%s]" % config_file, file=sys.stderr)
        print("", file=sys.stderr)
        print("Please add a Jenkins URL in [%s]" % config_file, file=sys.stderr)
        exit(1)

    jenkins_url = config[JENKINS_URL]["url"]
    jenkins_server = jenkins.Jenkins(jenkins_url)
    print("Checking for updated builds on %s" % jenkins_url)

    for section in config.sections():
        if section == JENKINS_URL:
            continue
        job = section
        last_known_build_number = int(read(job, "build_number", 0))
        last_known_build_status = read(job, "build_status", "Unknown")

        job_info = jenkins_server.get_job_info(section)
        latest_build = job_info["builds"][0]
        if latest_build["number"] > last_known_build_number:
            # check details
            build_info = jenkins_server.get_build_info(section, latest_build["number"])
            # is it already finished and the status has also changed?
            if build_info["result"]:
                if build_info["result"] != last_known_build_status:
                    # Show info
                    pync.Notifier.notify("%s build #%d: %s" % (job, latest_build["number"], build_info["result"]),
                                         title="Build status: %s" % build_info["result"],
                                         open="%sconsole" % urllib.parse.unquote(latest_build["url"]))
                # Update file
                config[job]["build_number"] = str(latest_build["number"])
                config[job]["build_status"] = build_info["result"]

    with open(config_file, "w") as f:
        config.write(f)
    print("Finished")


if __name__ == "__main__":
    main()
