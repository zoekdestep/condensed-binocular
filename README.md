# condensed-binocular

A simple script to report ML metrics to Azure ML and Azure AppInsights at the same time!

## :sun_behind_rain_cloud: You might recognize these small annoyances:

- There is no out-of-the-box way to report metrics to AppInsights and Azure ML simultaneously == more lines of code than necessary.

- AML currently does not allow you to report metrics to both parent- and childrun simultaneously == more lines of code than necesary.

Therefore, this simple class aims to reduce lines of code for AML metric reporting, so reporting in Azure becomes a tiny bit more fun! Also, it follows some engineering best practices, like tests, environment variables and constants - you know, just as a reminder of what's nice.

## :mountain: It's based on the following:

- The [metrics logging method of the Python Azure ML SDK](https://docs.microsoft.com/en-us/python/api/azureml-core/azureml.core.run.run?view=azure-ml-py#methods)

- The [OpenCensus Azure Monitor Exporter](https://pypi.org/project/opencensus-ext-azure/)

## :lollipop: It's actually very simple:

1. Make sure you have an [AML Workspace](https://docs.microsoft.com/en-us/azure/machine-learning/concept-workspace)

2. Make sure you have an [AppInsights resource](https://docs.microsoft.com/en-us/azure/azure-monitor/app/create-new-resource)

3. Add the `condensed_binocular.py` script in your project. Don't forget to add the `.env` file and the `constants.py` file if feel like using them this way, and change accordingly.

4. Integrate in your code. See `binocular_sample.py` on how to use it.

5. Wait until your experiment ran, and check if the values show up in both the AML Experiment as in AppInsights.

6. PROFIT.

## :green_heart: Contribute

Not working as expected or nice little additions necessary? PRs are welcome! For major changes, please open an issue first.

