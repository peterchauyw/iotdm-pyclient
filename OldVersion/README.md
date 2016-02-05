# Guide to Adding ODL Robot Tests
This document describes the setup and on-going tasks related to adding ODL/Robot test cases to the IoTDM project.

##Quick Overview
If you're like me, you might not want to read this entire document before you start doing things.

Here's a quick survival guide:

1. Make sure you have the tools you need: python2.7, pip, pybot, requests, pep8, git, git-review.
1. Make sure you can check in/out code from ODL/git/gerrit.
2. Checkout integration repo with via: `git clone ssh://YOUR-ODL-USERNAME@git.opendaylight.org:29418/integration`
3. "Attach" git-review to integration repo checkout via: `cd integration ; git review -s`
1. Add one or two test cases by adding to `020-iotdm-mini.robot` or other existing robot file under `integration/test/csit/suites/iotdm/basic`
1. Create a new set of test cases by creating a new `999-lolcats.robot` file under `integration/test/csit/suites/iotdm/basic`
1. Updates to Joe's Python libraries are made in `integration/csit/libraries/iotdm.py` or `integration/csit/libraries/riotdm.py`
2. Submit changes to gerrit via: `git add -A ; git commit -s ; git review`
3. In Gerrit, `+1` John or Lionel and `+2` Luiz or Vratko.
4. If your review is `-1` or `-2`, answer the criticisms in Gerrit, then (optionally) fix, and re-send via: `git commit -a --amend ; git review`

Performing one of the above steps might require reading the relevant section below or asking Joe.

Advanced tasks might require reading the wiki ([RelEng](https://wiki.opendaylight.org/view/RelEng), [Integration_Group](https://wiki.opendaylight.org/view/CrossProject:Integration_Group)), getting assistance from the IRC (`freenode.net` : `#opendaylight-releng` and `#opendaylight-integration`) or the mailing lists (`infrastructure@lists.opendaylight.org ` and `integration-dev@lists.opendaylight.org`).

## Setup
You'll need the following items to add a Robot test:

* Python 2.7
* (OSX only) homebrew
* `pip` and `easy_install`
* Robot Framework
* Requests library
* NumPy library (optional)
* PEP8 tools
* git
* git-review
* ODL Gerrit/git-review setup
* builder repo
* integration repo

### Python 2.7
Python 2.7 is used for all Robot tests on ODL.

On OSX and Ubuntu 14.04, Python 2.7 should already be available.

### homebrew
Homebrew is used to easily install many Open Source projects on OSX.

To install it, paste this at a terminal:

```
ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

### `pip` and `easy install`
`pip` is one of the standard Python library installation tools.
If you can't install a library or application via `pip`, try the same with `easy_install`.

On OSX, you can typically use `pip` from your user account.

On Linux, install `pip` via `sudo apt-get install python-pip`. One difference between OSX and Linux is that on Linux, `pip` and `easy_install` require root or sudo privileges.

`easy_install` is another standard Python library installation tools.

### Robot framework
Install the Robot framework via the command `pip install robotframework`.

### Requests library
Joe's Python IoTDM library uses the Requests library to perform HTTP requests. Requests is also part of the standard set of ODL Robot libraries.

Install via `pip install requests`.

### NumPy library
I'm experimenting with the NumPy library for statistics in my local tests. NumPy is not installed in the default ODL Robot libraries, but if it proves useful, I'll propose its addition to the Integration and Releng teams.

Install via `pip install numpy`.

### PEP8 tools
`pep8` is used by the Python code validation check-in triggers in Jenkins. It makes sure your Python code follows basic coding standards, and you should certainly run this on any python code you check into the integration repo.

Install via `pip install pep8`.

Usage is `pep8 name-of-python-script-to-check.py`. It will tell you where in your code you've violated the "standards".

A quick note about Python standards enforced by the integration team:

* Make sure you use four spaces for tabbing (and NEVER use the literal tab character).
* Separate functions/methods with two blank lines.
* Make sure no line of comments or code are wider than 79 characters.

The automated checking tools will enforce these standards and your human reviewer will probably fuss at you too.

### git
On OSX, git is already installed.

For Ubuntu, install via `sudo apt-get install git`.

### git-review
`git-review` makes using Gerrit easier (i.e. avoids several manual steps to submit Gerrit patches).

Install via `pip install git-review`.

### git/git-review basic work-flow
This pattern is shown in the builder repo and integration repo sections but in short, follow this pattern:

* Get your repo:

```
git clone ssh://YOUR-ODL-USERNAME@git.opendaylight.org:29418/ODL-REPO-OF-INTEREST
cd ODL-REPO-OF-INTEREST
git review -s # this connects your local repo to Gerrit
```

* Make changes to repo
* Push changes to repo:

```
git add -A
git commit -s
git review
```
* Add `+1` and `+2` reviewers in Gerrit
* Check for and respond to comments in Gerrit
* Change code based on comments in Gerrit
* If there are changes to make:

```
git commit -a --amend
git review
```
* Repeat as necessary


### Robot Sublime Text package
https://packagecontrol.io/packages/Robot%20Framework%20Assistant


### ODL Gerrit/git-review setup
In order to submit your Robot tests via gerrit, you'll need an account on ODL.

Visit [ODL Gerrit Setup](https://wiki.opendaylight.org/view/OpenDaylight_Controller:Gerrit_Setup) page for full instructions on setting up you ODL/gerrit account. It's an accurate and straight-forward set of directions so there's no advantage in repeating them here.

For usage of Gerrit/git-review, the following pages are useful:

* [Gerrit review quick intro](https://gerrit-review.googlesource.com/Documentation/intro-quick.html)
* [Gerrit/git-review help](http://www.mediawiki.org/wiki/Gerrit/git-review)

### builder repo

[https://wiki.opendaylight.org/view/Simultaneous_Release:Cutting_Stability_Branches]()

The builder repo, for our purposes, tells Jenkins which Robot tests to run. It's "owned" by the ODL releng team.

Generally, we don't need to edit this file unless we want to add a new class of test, or change which kind of build trigger which of our tests. Before doing either of those things, check with Lionel, or John.

To get this repo, do:

```
git clone ssh://YOUR-ODL-USERNAME@git.opendaylight.org:29418/releng/builder
cd builder
git review -s # this connects your local repo to gerrit
```

The files I added were:

* `builder/jjb/iotdm/iotdm-csit-basic-master.yaml` (designates the "basic" test in the integration repo and is detailed below) 
* `builder/jjb/iotdm/iotdm-distribution.yaml` (connects our master build branch and tests with Jenkins and is detailed below)

I commited my changes by:

```
git add -A
git commit -s
git review
```

The final command `git review` will print a gerrit URL where I added reviewers.

Changes to the builder repo require a releng member with `+2` capabilities  (Luis Gomez, Thanh Ha) and a `+1` IoTDM project owner (Lionel or John).

### integration repo
The integration repo is where our test libraries, robot tests, and testplans live. It's "owned" by the ODL integration team.

We'll mainly change files here as we develop new tests.

To get this repo, do:

```
git clone ssh://YOUR-ODL-USERNAME@git.opendaylight.org:29418/integration
cd integration
git review -s # this connects your local repo to gerrit
```

When you've added or changed items in the integration repo, you should commit in the same way I mentioned in the builder repo section.

#### testing libraries
Whenever there is a function or library you need to support your robot tests, you'll need to add them to the common library located at `integration/csit/libraries`.

For IoTDM, I added the two libraries `iotdm.py` and `riotdm.py`.

`iotdm.py` is my "public" IoTDM access library for Python.

`riotdm.py` is a library with functionality tailored to robot test cases.

These are split because we'll want to be diciplined about what goes into the public library and what goes into the ODL testing library since each usage has differing requirements. Also, the robot test cases seem to be oriented to functions with long descriptive names, so `riotdm.py` provides this.

#### robot tests

Within the integration repo, I created the directories named `iotdm/basic` under `integration/csit/suites`.

The top part, `iotdm` is obviously where all the tests related to IoTDM live. Underneath this, we can have varying kinds of tests grouped by directory.

To start, we only have one directory of tests, called `basic`. Underneath this directory, lives one or more individual robot test files. Read the next section about `testplans` for how this directory is known to Jenkins.

At the current time, we only have two robot tests in place, named:

* `integration/test/csit/suites/iotdm/basic/010_Restconf_OK.robot`
* `integration/test/csit/suites/iotdm/basic/020-iotdm-mini.robot`

The first one just does a basic Restconf connection to ODL (this is a template test case from the ODL wiki), the second has our beginning CRUD tests.

You create new test cases by either adding to one of the existing robot tests, or by creating a new file of robot tests (use `020-iotdm-mini.robot` as a starting template).

Please note that robot tests should be created with a `.robot` extension (rather than the `.tsv` extensions I shared earlier). By convention, `.robot` test files should use four spaces rather than tab characters, and the `***Settings***` section should use the spacing as shown in `020-iotdm-mini.robot`.

The robot test files are run in numeric order by their file name.

#### testplans
The thing that ties everything we've done so far together is the test plan in `integration/test/csit/testplans/iotdm-basic.txt`.

This file lists the full path for each directory containing our test cases.

As I mentioned earlier, our two test case files `010_Restconf_OK.robot` and `020-iotdm-mini.robot` are in `integration/test/csit/suites/iotdm/basic`, so it should be no surprise that our current testplan file contains the line:

```
integration/test/csit/suites/iotdm/basic
```

While it may be possible to include other directory names here, I've not yet tested this, as I've been lead to believe that the name `basic` is also required for the builder repo files and hence Jenkins to properly select the tests.

## Reference

### `builder/jjb/iotdm/iotdm-csit-basic-master.yaml`
The important part of this file is the section `functionality: basic`, which indicates that inside the `integration` repo that we use the testplan `integration/test/csit/testplans/iotdm-basic.txt`

```
- project:
    name: iotdm-csit-basic-master
    jobs:
        - '{project}-csit-1node-cds-{functionality}-{install}-{stream}'
        - '{project}-csit-verify-{functionality}-{stream}'

    # The project name
    project: 'iotdm'

    # The functionality under test
    functionality: 'basic'

    # Project branches
    stream:
        - master:
            branch: 'master'

    install:
        - only:
            scope: 'only'
        - all:
            scope: 'all'

    # Features to install
    install-features: 'odl-iotdm-onem2m'

    # Robot custom options
    robot-options: ''

    # Trigger jobs (upstream dependencies)
    trigger-jobs: 'iotdm-distribution-{stream}'
```

### `builder/jjb/iotdm/iotdm-distribution.yaml`

This file should rarely be changed, probably only if we want to use a different branch besides `master`.

```
- project:
    name: iotdm-distribution
    jobs:
        - '{project}-distribution-{stream}'

    # The project name
    project: 'iotdm'

    # The project branches
    stream:
        - master:
            branch: 'master'

    jdk: 'openjdk7'
```

### `integration/test/csit/suites/iotdm/basic/020-iotdm-mini.robot`
A short portion of `020-iotdm-mini.robot` is shown here for reference, please note the use of 4 spaces for tabs and how the `***Settings***` section is spaced. Not following these conventions will quickly get your test cases rejected from gerrit (as well as public humiliation on the IRC and mailing lists):

```
***Settings***
Library           ../../../libraries/iotdm.py
Library           ../../../libraries/riotdm.py
Library           Collections

***Variables***
${httphost}    ${CONTROLLER}
${httpuser}    admin
${httppass}    admin
${rt_ae}    2
${rt_container}    3
${rt_contentInstance}    4

***Test Cases***
Basic HTTP CRUD Test
    ${iserver}=    Connect To IoTDM    ${httphost}    ${httpuser}    ${httppass}    http
    #
    ${r}=    Create Resource    ${iserver}    InCSE1    ${rt_ae}
    ${ae}=    ResId    ${r}
    ${status_code}=    Status Code    ${r}
    ${text}=    Text    ${r}
    ${json}=    Json    ${r}
    ${elapsed}=    Elapsed    ${r}
```

### `integration/test/csit/testplans/iotdm-basic.txt`
This is pretty straight-forward as mentioned in the testplan section of the document, but for completeness, I've pasted the entire contents of our testplan here:

```
# Place the suites in run order:
integration/test/csit/suites/iotdm/basic
```
