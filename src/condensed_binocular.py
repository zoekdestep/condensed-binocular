import uuid
import constants
from matplotlib import pyplot
from typing import Optional
from environs import Env
from azureml.core import Run
from opencensus.ext.azure import metrics_exporter
from opencensus.stats import aggregation as aggregation_module
from opencensus.stats import measure as measure_module
from opencensus.stats import stats as stats_module
from opencensus.stats import view as view_module
from opencensus.tags import tag_map as tag_map_module


class Condensed_Binocular:
    """ This class allows to report metrics to Azure ML and/or to Application Insights simultaneously.
    """

    def __init__(self):
        """Initializes Condensed_Binocular using the Run object of azureml.core, and adding a
        metric exporter for ApplicationInsights using the opencensus library.
        """
        env = Env()
        env.read_env()

        self.run = Run.get_context(allow_offline=True)
        self.run_id = self.get_run_id(self.run)
        self.offline_run = self.run.id.startswith(constants.OFFLINE_RUN_PREFIX)

        self.exporter = metrics_exporter.new_metrics_exporter(
            enable_standard_metrics=False,
            export_interval=0,
            connection_string=env("APP_INSIGHTS_CONNECTION_KEY"))
        self.exporter.add_telemetry_processor(self.callback_function)
        stats_module.stats.view_manager.register_exporter(self.exporter)

    def report_metric(self, name: str, value: float, description="", report_to_parent: bool = False):
        """Report a metric value to the AML run and to AppInsights.
        e.g. Condensed_Binocular.report_metric(name, value)
        :param name: The name of the metric.
        :param value: The value to be reported.
        :type value: Float or integer.
        :param description: An optional description about the metric.
        :param report_to_parent: Mark True if you want to report to AML parent run.
        """
        # Report to AML
        self.run.log(name, value)
        if report_to_parent and not self.offline_run:
            self.run.parent.log(name, value)

        # Report to AppInsights
        measurement_map = stats_module.stats.stats_recorder.new_measurement_map()
        tag_map = tag_map_module.TagMap()
        measure = measure_module.MeasureFloat(name, description)
        self.set_view(name, description, measure)
        measurement_map.measure_float_put(measure, value)
        measurement_map.record(tag_map)

    def report_metric_with_run_tagging(self, name: str, value: float, description=""):
        """Report a metric value to the AML run and to AppInsights, and tag the parent run with the metric.
        Please note tags are mutable. By default, this method reports to AML parent run.
        e.g. Condensed_Binocular.report_metric(name, value)
        :param name: The name of the metric.
        :param value: The value to be reported.
        :type value: Float or integer.
        :param description: An optional description about the metric.
        :param report_to_parent: Mark True if you want to report to AML parent run.
        """
        # Report to AML
        self.run.log(name, value)
        if not self.offline_run:
            self.run.parent.log(name, value)
            self.run.parent.tag(name, value)

        # Report to AppInsights
        measurement_map = stats_module.stats.stats_recorder.new_measurement_map()
        tag_map = tag_map_module.TagMap()
        measure = measure_module.MeasureFloat(name, description)
        self.set_view(name, description, measure)
        measurement_map.measure_float_put(measure, value)
        measurement_map.record(tag_map)

    def report_list(self, name: str, value: list, report_to_parent: bool = False):
        """Report a list of metric values to the AML run. Note: this does not report to AppInsights.
        e.g. Condensed_Binocular.report_list("accuracies", [0.6, 0.7, 0.87])
        :param name: The name of the metric.
        :type name: str
        :param value: The values to be reported.
        :type value: builtin.list
        :param report_to_parent: Mark True if you want to report to AML parent run.
        """
        self.run.log_list(name, value)
        if report_to_parent and not self.offline_run:
            self.run.parent.log_list(name, value)

    def report_row(self, name: str, report_to_parent: bool = False, **kwargs: dict):
        """Report a row metric to the AML run. Note: this does not report to AppInsights.
        e.g. Condensed_Binocular.report_row("citrus", fruit = citrus[index], size=sizes[index])
        :param name: The name of the metric.
        :param report_to_parent: Mark True if you want to report to AML parent run.
        :param kwargs: A dictionary of additional parameters. In this case, the columns of the metric.
        """
        self.run.log_row(name, **kwargs)
        if report_to_parent and not self.offline_run:
            self.run.parent.log_row(name, description="", **kwargs)

    def report_table(self, name: str, value: dict, report_to_parent: bool = False):
        """Report a table metric to the AML run. Note: this does not report to AppInsights.
        e.g. Condensed_Binocular.report_table("Y over X", {"x":[1, 2, 3], "y":[0.6, 0.7, 0.89]})
        :param name: The name of the metric.
        :param value: The table value of the metric, a dictionary where keys are columns to be reported.
        :param report_to_parent: Mark True if you want to report to AML parent run.
        """
        self.run.log_table(name, value)
        if report_to_parent and not self.offline_run:
            self.run.parent.log_table(name, value)

    def report_image(self, name: str, path: Optional[str] = None, plot: Optional[pyplot.plot] = None):
        """Report an image metric to the AML run. Note: this does not report to AppInsights.
        e.g. Condensed_Binocular.report_image("ROC", plot=plt)
        :param name: The name of the metric.
        :param path: The path or stream of the image.
        :param plot: The plot to report as an image.
        """
        self.run.log_image(name, path=path, plot=plot)

    def get_run_id(self, run):
        """Get the correlation ID in the following order:
        - If the script is running in an online context of AML, it retrieves the AML run id.
        - If the script is running in an offline context, it creates a unique id.
        :param run:
        :return: run_id
        """
        return run.id if not run.id.startswith(constants.OFFLINE_RUN_PREFIX) else str(uuid.uuid1())

    @staticmethod
    def set_view(metric, description, measure):
        """ Set the view for the custom metric.
        :param metric:
        :param description:
        :param measure:
        """
        prompt_view = view_module.View(metric, description, [], measure, aggregation_module.LastValueAggregation())
        stats_module.stats.view_manager.register_view(prompt_view)

    def callback_function(self, envelope):
        """ Attach a correlation_id as a custom dimension to the exporter just before sending the metrics.
        :param envelope:
        :return: Always return True (if False, it does not export metrics)
        """
        envelope.data.baseData.properties["Correlation_id"] = self.run_id
        return True
