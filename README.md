# condensed-binocular
A simple script to report ML metrics to Azure ML and Azure AppInsights at the same time! 🍭

## You might recognize these small annoyances:
- There is no out-of-the-box way to report metrics to AppInsights and Azure ML simultaneously == more lines of code than necessary.
- AML currently does not allow you to report metrics to both parent- and childrun simultaneously == more lines of code than necesary.

Therefore, this simple class aims to reduce lines of code for AML metric reporting, so reporting in Azure becomes a tiny bit more fun! Also, it includes tests!

## It's based on the following:
- The [metrics logging method of the Python Azure ML SDK](https://docs.microsoft.com/en-us/python/api/azureml-core/azureml.core.run.run?view=azure-ml-py#methods)
- The [OpenCensus Azure Monitor Exporter](https://pypi.org/project/opencensus-ext-azure/)

## It's actually very easy:
1. Make sure you have an (AML Workspace)[https://docs.microsoft.com/en-us/azure/machine-learning/concept-workspace]
2. Make sure you have an (AppInsights resource)[https://docs.microsoft.com/en-us/azure/azure-monitor/app/create-new-resource]
3. Add the xyz script in your project.
