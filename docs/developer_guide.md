# Developer Guide

Website is deployed in Kubernetes cluster. A deployment contains the following
containers:

- website: A Flask app with static files complied by Webpack.
- mixer: A Data Commons API server.
- esp: Google Extensive Service Proxy used for endpoints management.

[mixer](https://github.com/datacommonsorg/mixer) is a submodule of this Git
repo. The exact commit of the submodule is deployed together with the website so
it may not be the same version as in `https://api.datacommons.org/version`.
Make sure to update and track the mixer changes for a new deployment:

```bash
git submodule foreach git pull origin master
git submodule update --init --recursive
```

## Local Development with Flask

For changes that do not test GCP deployment or involve mixer changes, one can
simply run in a local environment (Mac or Linux machine). This way the local
Flask app talks to the [autopush mixer](https://autopush.api.datacommons.org).

Note: the `autopush mixer` contains the latest data and mixer code changes. It
is necessary to update the mixer submodule if compatibility is required between
website and mixer changes.

### Prerequisites

**WARNING**: Make sure to go through each of the following steps.

- Python

  Confirm the Python3 version is 3.11 or above. Otherwise install/upgrade your Python
  and confirm the version:

  ```bash
  python3 --version
  ```

  Set up your Python environment and update packages with:
  ```bash
  ./run_test.sh --setup_python
  ```

  If using version 3.12.x or above, you also need to run the following command, on macOs:
  ```bash
  brew install python-setuptools
  ```
  or for linux:
  ```bash
  pip install python-setuptools
  ```

- Node.js 18.4.0

  Install [`nodejs`](https://nodejs.org/en/download/) and
  [nvm](https://github.com/nvm-sh/nvm#installing-and-updating). Run the
  following command to use Node.js 18.4.0:

  ```bash
  nvm install 18.4.0
  nvm use 18.4.0
  ```

  To set this version as default:

  ```bash
  nvm alias default 18.4.0
  ```

- Protoc 3.21.12

  Install [`protoc`](https://grpc.io/docs/protoc-installation/) at version
  3.21.12.

  On MacOS, you can do this with Homebrew by running `brew install protobuf@21`.
  Be sure to update your path as described in the output (likely it'll instruct
  you to run
  `echo 'export PATH="/opt/homebrew/opt/protobuf@21/bin:$PATH"' >> ~/.zshrc`).

- [Optional] gcloud

  gcloud is required to make the place search working locallly. This requires
  installation of [`gcloud`](https://cloud.google.com/sdk/docs/install).

  Then ask Data Commons team to grant you permission for the Google Maps API key
  access.

  Finally authenticate locally with

  ```bash
  gcloud auth application-default login
  ```

### Package javascript and static assets

```bash
./run_npm.sh
```

This will watch static files change and re-build on code edit.

> NOTE: On macOS machines with a M1 chip, run the following command before running the above command.
> See [this](https://stackoverflow.com/a/71353060) for more details.

```bash
brew install pkg-config cairo pango libpng jpeg giflib librsvg
```

### Start the Flask Server

Start the flask webserver locally at localhost:8080

```bash
./run_server.sh
```

To enable NL search, language models must be enabled via `-m`:

```bash
./run_server.sh -m
```

If you don't have access to DataCommons maps API, can bring up website without
place search functionality

```bash
./run_server.sh -e lite
```

There are multiple environments for the server, specified by `-e` options.
For example, `custom` is for custom data commons and `iitm` is
for iitm data commons.

To start multiple instances, bind each server instance to a different port.
The following example will start localhost on port 8081. The default is 8080.

Please note the strict syntax requirements for the script, and leave a space
after the flag. So: `./run_server.sh -p 8081` but not `./run_server.sh -p=8081`.

#### 🛠️ Troubleshooting server startup
<details>
  <summary>
    <b>ModuleNotFoundError</b>: missing python libraries...
  </summary>
  Clear the environment and rebuild all required libraries by running:

  ```bash
  rm -rf .env
  ./run_test.sh --setup_python
  ```
</details>

### Start NL Server

Natural language models are hosted on a separate server. For features that
depend on it (all NL-based interfaces and endpoints), the NL server needs
to be brought up locally (in a separate process):

```bash
./run_nl_server.sh -p 6060
```

By default the NL server runs on port 6060.

If you run into problems starting the server, try running these commands before restarting the server:
```bash
./run_test.sh --setup_python
rm -rf ~/.datacommons
rm -rf /tmp/datcom-nl-models
rm -rf /tmp/datcom-nl-models-dev
```

### Use Local Mixer

If local mixer is needed, can start it locally by following [this
instruction](https://github.com/datacommonsorg/mixer/blob/master/docs/developer_guide.md#develop-mixer-locally-as-a-go-server-recommended).
This allows development with custom BigTable or mixer code change. Make sure to
also [run ESP locally](https://github.com/datacommonsorg/mixer/blob/master/docs/developer_guide.md#running-esp-locally).

Then start the Flask server with `-l` option to let it use the local mixer:

```bash
./run_server.sh -l
```

## Deploy local changes to dev insance in GCP

Commit all changes locally, so the local change is identified by a git hash.
Then run

```bash
gcloud auth login
gcloud auth configure-docker
./scripts/push_image.sh
./scripts/deploy_gke_helm.sh -e dev
```

The script builds docker image locally and tags it with the local git commit
hash at HEAD, then deploys to dev instance in GKE.

View the deployoment at [link](https://dev.datacommons.org).

## Run Tests

### Install web browser and webdriver

:exclamation:**IMPORTANT**: Make sure that your **ChromeDriver version** is
compatible with your **local Google Chrome version**.

Before running the tests, install the browser and webdriver. Here we recommend
you use Google Chrome browser and ChromeDriver.

- Chrome browser can be downloaded [here](https://www.google.com/chrome/).

- ChromeDriver can be downloaded
  [here](https://chromedriver.chromium.org/downloads/version-selection), or you
  can download it using package manager directly:

  ```bash
  npm install chromedriver
  ```

You can view the latest ChromeDriver version
[here](https://chromedriver.storage.googleapis.com/LATEST_RELEASE). Also make
sure PATH is updated with ChromeDriver location.

If using Linux system, you can run the following commands to download Chrome
browser and ChromeDriver, this will also include the path setup:

```bash
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb; sudo apt-get -fy install
CHROMEDRIVERV=$(curl https://chromedriver.storage.googleapis.com/LATEST_RELEASE)
wget https://chromedriver.storage.googleapis.com/${CHROMEDRIVERV}/chromedriver_linux64.zip
unset CHROMEDRIVERV
unzip chromedriver_linux64.zip
sudo mv chromedriver /usr/bin/chromedriver
sudo chown root:root /usr/bin/chromedriver
sudo chmod +x /usr/bin/chromedriver
```

:exclamation: NOTE: If using MacOS with an ARM processor (M1 chip), run local NL server before running the tests:

```bash
./run_nl_server.sh -p 6060
```

### Run all tests

```bash
./run_test.sh -a
```

### Update React test snapshots

```bash
cd static
npm test . -- -u
```

## Other Developing Tips

### Deploy latest code/data

The autopush instance(autopush.datacommons.org) always has the latest code and
data. For this to happen in other dev/demo instance, in a clean git checkout,
simply run:

```bash
./script/deploy_latest.sh <ENV_NAME> <REGION>
```

### Debug Flask in Visual Studio Code

1. [Optional] Update variables in 'env' of 'Flask' configurations in
   .vscode/launch.json as needed.

1. In the left hand side menu of VS Code, click on "Run and Debug".

1. On top of the "Run and Debug" pane, select "DC Website Flask" and click on
   the green "Play" button.

1. In "DEBUG CONSOLE" (not "TERMINAL"), check the server logs show up.

This brings up Flask server from the debugger. Now you can set break point and
inspect variables from the debugger pane.

TIPS: you can inspect variable in the botton of "DEBUG CONSOLE" window.

A full tutorial of debugging Flask app in Visual Studio Code is in
[here](https://code.visualstudio.com/docs/python/tutorial-flask).

### Manage Feature Flags

Feature flags are used to gate the rollout of features, and can easily be turned on/off in various environments. Please read the Feature Flags [guide](https://github.com/datacommonsorg/website/blob/master/docs/feature_flags.md).

### Add new charts in Place Page

1. Update [server/config/chart_config/](../server/config/chart_config)`<category>.json` with the new chart.

   ```javascript
      {
        "category": "", // The top level category this chart belongs to. Order of charts in the spec matters.
        "topic": "",  // Strongly encouraged - A page-level grouping for this chart.
        "titleId": "", // Strictly for translation purposes.
        "title": "", // Default (EN) display string
        "description": "", // Strictly for translation purposes.
        "statsVars": [""], // List of stat vars to include in the chart
        "isOverview": true, // Optional - default false. If the chart should be added to the overview page.
        "isChoropleth": true, // Optional - default false. If a map should be used to display the data
        "unit": "",
        "scaling": 100,
        "relatedChart": {  // Defined if there should be comparison charts added
          // All chart fields from above can be specified. If unspecified, it will be inherited.
        }
      }
   ```

1. Update related files.

   - If adding a new category, create a new config file in [server/chart_config](../server/chart_config) and add the new category to:

     - [static/js/shared/util.ts](../static/js/shared/util.ts)
     - [server/\_\_init\_\_.py](../server/__init__.py)

   - If a new stat var is introduced, also update:

     - Labels that appear as chips under comparison charts: [static/js/i18n/strings/en/stats_var_labels.json](../static/js/i18n/strings/en/stats_var_labels.json)
     - Titles on ranking pages: [static/js/i18n/strings/en/stats_var_titles.json](../static/js/i18n/strings/en/stats_var_titles.json)
     - New stat vars which have not been cached: [NEW_STAT_VARS](../server/configmodule.py)

   - If a new unit is required, update:
     - [static/js/i18n/i18n.tsx](../static/js/i18n/i18n.tsx)
     - [static/js/i18n/strings/\*/units.json](static/js/i18n/strings/en/units.json) (with display names and labels for the unit in **ALL** languages)

   Note: Please add very detailed descriptions to guide our translators. See localization.md for more details.

1. Run these commands:

   ```bash
   ./scripts/extract_messages.sh
   ./scripts/compile_messages.sh
   ```

1. **IMPORTANT**: Manually restart Flask to reload the config and translations. Most likely, this means re-running `run_server.py`

1. Test the data on a place page!

### Debugging Webdriver tests

- Disable headless mode in webdriver to follow the test in Chrome. Chrome
  features like the dev inspector are available in this mode which is useful
  combined with `sleep()` to give you time to inspect the page. To enter this
  mode, comment out this line in [base.py](../server/webdriver/base.py):

  ```python
  chrome_options.add_argument('--headless')
  ```

- Another option is to save a screenshot at various points of the test:

  ```python
  self.driver.save_screenshot(filename)
  ```

### GKE config

The GKE configuration is stored [here](../deploy/helm_charts/dc_website).

### Redis memcache

[Redis memcache](https://pantheon.corp.google.com/memorystore/redis/instances?project=datcom-website-prod)
is used for production deployment. Each cluster has a Redis instance located in
the same region.

### Testing cloudbuild changes

To test .yaml cloudbuild files, you can use cloud-build-local to dry run the file before actually pushing. Find documentation for how to install and use cloud-build-local [here](https://github.com/GoogleCloudPlatform/cloud-build-local).

### Inline Icons

The Data Commons site makes use of Material Design icons. In certain cases, font-based Material Design icon usage can result in
flashes of unstyled content that can be avoided by using SVG icons.

We have provided tools to facilitate the creation and use of Material SVG icons in both the Jinja template and in React components.
For instructions  on how to generate and use these SVGs and components, please see: [Icon Readme](../tools/resources/icons/README.md):
