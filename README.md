jenkins-notifier
================

jenkins-notifier is a small utility that allows you to watch Jenkins builds.

Every time it is invoked, it checks for the status of all watched builds and creates a notification in the Mac OS X notification bar.

# Requirements

* Mac OS X 10.8 or later: As it uses Mac OS X notifications, jenkins-notifier works only on Mac OS X 10.8 or later.
* Python 3
* jenkins: Install with `pip3 install jenkins`
* pync: Install with `pip3 install pync`

# Installation

Ensure that all prerequisites are installed, then copy `notifier.py` to any directory, e.g. `~/bin` and run `chmod u+x notifier.py`.

# Usage

## Example

Consider you want to watch the builds "elastic+elasticsearch+master+macrobenchmark-periodic" and "elastic+elasticsearch+master+microbenchmark-periodic" at https://elasticsearch-ci.elastic.co.

1. Create `~/.jenkins-notifier/config.ini`
2. Add the following lines:

```
[jenkins.url]
url = https://elasticsearch-ci.elastic.co

[elastic+elasticsearch+master+macrobenchmark-periodic]

[elastic+elasticsearch+master+microbenchmark-periodic]
```

Now invoke jenkins-notifier: ``python3 notifier.py``. It will load the config file, check for build updates and show a notice for each update in the Mac OS X notification bar.

## Automatic regular invocation

Quite likely you don't want to invoke jenkins-notifier manually every time you want to check for build updates. Therefore, you can install jenkins-notifier as a launch agent.

Create a new file in `~/Library/LaunchAgents/org.github.jenkins-notifier.plist` with the following contents:

```plist
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>org.github.jenkins-notifier</string>

  <key>ProgramArguments</key>
  <array>
    <string>~/bin/notifier.py</string>
  </array>

  <key>Nice</key>
  <integer>1</integer>

  <key>StartInterval</key>
  <integer>300</integer>

  <key>RunAtLoad</key>
  <true/>

  <key>StandardErrorPath</key>
  <string>~/.jenkins-notifier/jenkins-notifier.err.log</string>

  <key>StandardOutPath</key>
  <string>~/.jenkins-notifier/jenkins-notifier.out.log</string>
</dict>
</plist>
```

Change the paths depending on the install location of jenkins-notifier. 

With this plist file, jenkins-notifier will check the CI server every 5 minutes (300 seconds) for build updates.

Finally register the launch agent with Mac OS X:

```
launchctl load ~/Library/LaunchAgents/org.github.jenkins-notifier.plist
```

After a restart, Mac OS X will pick up the plist file automatically.

If you are interested in more details about launch agents, check [Alvin Alexander's blog post about plist files](http://alvinalexander.com/mac-os-x/mac-osx-startup-crontab-launchd-jobs) (on which this description is based).

# License

'jenkins-notifier' is distributed under the terms of the [Apache Software Foundation license, version 2.0](http://www.apache.org/licenses/LICENSE-2.0.html).
