from mock import patch
from src.binocular_sample import Condensed_Binocular


# Tests Reporting initialization
@patch("src.Condensed_Binocular.Env")
@patch("src.Condensed_Binocular.Run")
@patch("src.Condensed_Binocular.metrics_exporter")
@patch("src.Condensed_Binocular.stats_module")
def test_reporting_initialization(mock_stats, mock_exporter, mock_run, mock_env):
    # act
    reporting = Condensed_Binocular()

    # assert
    assert mock_env.call_count == 1
    assert mock_run.get_context.call_count == 1
    assert reporting.run_id is not None
    assert mock_exporter.new_metrics_exporter.call_count == 1
    assert reporting.exporter.add_telemetry_processor.call_count == 1
    mock_stats.stats.view_manager.register_exporter.assert_called_once_with(reporting.exporter)


# Tests report_metric method
@patch("src.Condensed_Binocular.Env")
@patch("src.Condensed_Binocular.Run")
@patch("src.Condensed_Binocular.metrics_exporter")
def test_report_metric_calls_aml_logging_with_parameters(mock_exporter, mock_run, mock_env):
    # arrange
    reporting = Condensed_Binocular()
    name = "FOO"
    metric = 1

    # act
    reporting.report_metric(name, metric)

    # assert
    reporting.run.log.assert_called_once_with(name, metric)


@patch("src.Condensed_Binocular.Env")
@patch("src.Condensed_Binocular.Run")
@patch("src.Condensed_Binocular.metrics_exporter")
def test_report_metric_calls_aml_parent_logging_with_parameters_if_parent_is_true_and_run_is_online(mock_exporter, mock_run, mock_env):
    # arrange
    reporting = Condensed_Binocular()
    reporting.offline_run = None
    name = "FOO"
    metric = 1
    report_parent_true = bool(True)

    # act
    reporting.report_metric(name, metric, report_to_parent=report_parent_true)

    # assert
    reporting.run.parent.log.assert_called_once_with(name, metric)


@patch("src.Condensed_Binocular.Env")
@patch("src.Condensed_Binocular.Run")
@patch("src.Condensed_Binocular.metrics_exporter")
def test_report_metric_doesnt_call_aml_parent_logging_if_parent_is_false_and_run_is_online(mock_exporter, mock_run, mock_env):
    # arrange
    reporting = Condensed_Binocular()
    reporting.offline_run = None
    name = "FOO"
    metric = 1
    report_parent_false = bool(False)

    # act
    reporting.report_metric(name, metric, report_to_parent=report_parent_false)

    # assert
    assert reporting.run.parent.log.call_count == 0


@patch("src.Condensed_Binocular.Env")
@patch("src.Condensed_Binocular.Run")
@patch("src.Condensed_Binocular.metrics_exporter")
def test_report_metric_doesnt_call_aml_parent_logging_if_run_is_offline(mock_exporter, mock_run, mock_env):
    # arrange
    reporting = Condensed_Binocular()
    name = "FOO"
    metric = 1
    report_parent_true = bool(True)

    # act
    reporting.report_metric(name, metric, report_to_parent=report_parent_true)

    # assert
    assert reporting.run.parent.log.call_count == 0


@patch("src.Condensed_Binocular.Env")
@patch("src.Condensed_Binocular.Run")
@patch("src.Condensed_Binocular.metrics_exporter")
@patch("src.Condensed_Binocular.measure_module")
@patch("src.Condensed_Binocular.Reporting.set_view")
def test_report_metric_calls_set_view_with_parameters(mock_view, mock_measuremodule, mock_exporter, mock_run, mock_env):
    # arrange
    reporting = Condensed_Binocular()
    name = "FOO"
    metric = 1
    description = "BAR"

    # act
    reporting.report_metric(name, metric, description)

    # assert
    mock_view.assert_called_once_with(name, description, mock_measuremodule.MeasureFloat(name, description))


@patch("src.Condensed_Binocular.Env")
@patch("src.Condensed_Binocular.Run")
@patch("src.Condensed_Binocular.metrics_exporter")
@patch("src.Condensed_Binocular.stats_module.stats.stats_recorder")
@patch("src.Condensed_Binocular.tag_map_module")
def test_report_metric_calls_measurementmap_record(mock_tagmap, mock_statsmodule, mock_exporter, mock_run, mock_env):
    # arrange
    reporting = Condensed_Binocular()

    # act
    reporting.report_metric("FOO", 1)

    # assert
    assert mock_statsmodule.new_measurement_map().record.call_count == 1


# Tests report_metric_with_run_tagging method
@patch("src.Condensed_Binocular.Env")
@patch("src.Condensed_Binocular.Run")
@patch("src.Condensed_Binocular.metrics_exporter")
def test_report_metric_with_run_tagging_calls_aml_logging_with_parameters(mock_exporter, mock_run, mock_env):
    # arrange
    reporting = Condensed_Binocular()
    name = "FOO"
    metric = 1

    # act
    reporting.report_metric_with_run_tagging(name, metric)

    # assert
    reporting.run.log.assert_called_once_with(name, metric)


@patch("src.Condensed_Binocular.Env")
@patch("src.Condensed_Binocular.Run")
@patch("src.Condensed_Binocular.metrics_exporter")
def test_report_metric_with_run_tagging_calls_aml_parent_logging_with_parameters_if_run_is_online(mock_exporter, mock_run, mock_env):
    # arrange
    reporting = Condensed_Binocular()
    reporting.offline_run = None
    name = "FOO"
    metric = 1

    # act
    reporting.report_metric_with_run_tagging(name, metric)

    # assert
    reporting.run.parent.log.assert_called_once_with(name, metric)


@patch("src.Condensed_Binocular.Env")
@patch("src.Condensed_Binocular.Run")
@patch("src.Condensed_Binocular.metrics_exporter")
def test_report_metric_with_run_tagging_doesnt_call_aml_parent_logging_if_run_is_offline(mock_exporter, mock_run, mock_env):
    # arrange
    reporting = Condensed_Binocular()
    name = "FOO"
    metric = 1

    # act
    reporting.report_metric_with_run_tagging(name, metric)

    # assert
    assert reporting.run.parent.log.call_count == 0


@patch("src.Condensed_Binocular.Env")
@patch("src.Condensed_Binocular.Run")
@patch("src.Condensed_Binocular.metrics_exporter")
def test_report_metric_with_run_tagging_calls_aml_parent_tagging_with_parameters_if_run_is_online(mock_exporter, mock_run, mock_env):
    # arrange
    reporting = Condensed_Binocular()
    reporting.offline_run = None
    name = "FOO"
    metric = 1

    # act
    reporting.report_metric_with_run_tagging(name, metric)

    # assert
    reporting.run.parent.tag.assert_called_once_with(name, metric)


@patch("src.Condensed_Binocular.Env")
@patch("src.Condensed_Binocular.Run")
@patch("src.Condensed_Binocular.metrics_exporter")
def test_report_metric_with_run_tagging_doesnt_call_aml_parent_tagging_if_run_is_offline(mock_exporter, mock_run, mock_env):
    # arrange
    reporting = Condensed_Binocular()
    name = "FOO"
    metric = 1

    # act
    reporting.report_metric_with_run_tagging(name, metric)

    # assert
    assert reporting.run.parent.tag.call_count == 0


@patch("src.Condensed_Binocular.Env")
@patch("src.Condensed_Binocular.Run")
@patch("src.Condensed_Binocular.metrics_exporter")
@patch("src.Condensed_Binocular.measure_module")
@patch("src.Condensed_Binocular.Reporting.set_view")
def test_report_metric_with_run_tagging_calls_set_view_with_parameters(mock_view, mock_measuremodule, mock_exporter, mock_run, mock_env):
    # arrange
    reporting = Condensed_Binocular()
    name = "FOO"
    metric = 1
    description = "BAR"

    # act
    reporting.report_metric_with_run_tagging(name, metric, description)

    # assert
    mock_view.assert_called_once_with(name, description, mock_measuremodule.MeasureFloat(name, description))


@patch("src.Condensed_Binocular.Env")
@patch("src.Condensed_Binocular.Run")
@patch("src.Condensed_Binocular.metrics_exporter")
@patch("src.Condensed_Binocular.stats_module.stats.stats_recorder")
@patch("src.Condensed_Binocular.tag_map_module")
def test_report_metric_with_run_tagging_calls_measurementmap_record(mock_tagmap, mock_statsmodule, mock_exporter, mock_run, mock_env):
    # arrange
    reporting = Condensed_Binocular()

    # act
    reporting.report_metric_with_run_tagging("FOO", 1)

    # assert
    assert mock_statsmodule.new_measurement_map().record.call_count == 1


# Tests report_list method
@patch("src.Condensed_Binocular.Env")
@patch("src.Condensed_Binocular.Run")
@patch("src.Condensed_Binocular.metrics_exporter")
def test_report_list_calls_aml_logging_with_parameters(mock_exporter, mock_run, mock_env):
    # arrange
    reporting = Condensed_Binocular()
    name = "FOO"
    metric_list = [1, 2, 3]

    # act
    reporting.report_list(name, metric_list)

    # assert
    reporting.run.log_list.assert_called_once_with(name, metric_list)


@patch("src.Condensed_Binocular.Env")
@patch("src.Condensed_Binocular.Run")
@patch("src.Condensed_Binocular.metrics_exporter")
def test_report_list_calls_aml_parent_logging_with_parameters_if_parent_is_true_and_run_is_online(mock_exporter, mock_run, mock_env):
    # arrange
    reporting = Condensed_Binocular()
    reporting.offline_run = None
    name = "FOO"
    metric_list = [1, 2, 3]
    report_parent_true = bool(True)

    # act
    reporting.report_list(name, metric_list, report_to_parent=report_parent_true)

    # assert
    reporting.run.parent.log_list.assert_called_once_with(name, metric_list)


@patch("src.Condensed_Binocular.Env")
@patch("src.Condensed_Binocular.Run")
@patch("src.Condensed_Binocular.metrics_exporter")
def test_report_list_doesnt_call_aml_parent_logging_if_parent_is_false_and_run_is_online(mock_exporter, mock_run, mock_env):
    # arrange
    reporting = Condensed_Binocular()
    reporting.offline_run = None
    name = "FOO"
    metric_list = [1, 2, 3]
    report_parent_false = bool(False)

    # act
    reporting.report_list(name, metric_list, report_to_parent=report_parent_false)

    # assert
    assert reporting.run.parent.log_list.call_count == 0


@patch("src.Condensed_Binocular.Env")
@patch("src.Condensed_Binocular.Run")
@patch("src.Condensed_Binocular.metrics_exporter")
def test_report_list_doesnt_call_aml_parent_logging_if_run_is_offline(mock_exporter, mock_run, mock_env):
    # arrange
    reporting = Condensed_Binocular()
    name = "FOO"
    metric_list = [1, 2, 3]
    report_parent_true = bool(True)

    # act
    reporting.report_list(name, metric_list, report_to_parent=report_parent_true)

    # assert
    assert reporting.run.parent.log_list.call_count == 0


# Tests report_row method
@patch("src.Condensed_Binocular.Env")
@patch("src.Condensed_Binocular.Run")
@patch("src.Condensed_Binocular.metrics_exporter")
def test_report_row_calls_aml_logging_with_parameters(mock_exporter, mock_run, mock_env):
    # arrange
    reporting = Condensed_Binocular()
    name = "FOO"
    x_axis = []
    y_axis = []

    # act
    reporting.report_row(name, x=x_axis, y=y_axis)

    # assert
    reporting.run.log_row.assert_called_once_with(name, x=x_axis, y=y_axis)


@patch("src.Condensed_Binocular.Env")
@patch("src.Condensed_Binocular.Run")
@patch("src.Condensed_Binocular.metrics_exporter")
def test_report_row_calls_aml_parent_logging_with_parameters_if_parent_is_true_and_run_is_online(mock_exporter, mock_run, mock_env):
    # arrange
    reporting = Condensed_Binocular()
    reporting.offline_run = None
    name = "FOO"
    x_axis = []
    y_axis = []
    report_parent_true = bool(True)

    # act
    reporting.report_row(name, report_to_parent=report_parent_true, x=x_axis, y=y_axis)

    # assert
    reporting.run.parent.log_row.assert_called_once_with(name, description="", x=x_axis, y=y_axis)


@patch("src.Condensed_Binocular.Env")
@patch("src.Condensed_Binocular.Run")
@patch("src.Condensed_Binocular.metrics_exporter")
def test_report_row_doesnt_call_aml_parent_logging_if_parent_is_false_and_run_is_online(mock_exporter, mock_run, mock_env):
    # arrange
    reporting = Condensed_Binocular()
    reporting.offline_run = None
    name = "FOO"
    x_axis = []
    y_axis = []
    report_parent_false = bool(False)

    # act
    reporting.report_row(name, report_to_parent=report_parent_false, x=x_axis, y=y_axis)

    # assert
    assert reporting.run.parent.log_row.call_count == 0


@patch("src.Condensed_Binocular.Env")
@patch("src.Condensed_Binocular.Run")
@patch("src.Condensed_Binocular.metrics_exporter")
def test_report_row_doesnt_call_aml_parent_logging_if_run_is_offline(mock_exporter, mock_run, mock_env):
    # arrange
    reporting = Condensed_Binocular()
    name = "FOO"
    x_axis = []
    y_axis = []
    report_parent_true = bool(True)

    # act
    reporting.report_row(name, report_to_parent=report_parent_true, x=x_axis, y=y_axis)

    # assert
    assert reporting.run.parent.report_row.call_count == 0


# Tests report_table method
@patch("src.Condensed_Binocular.Env")
@patch("src.Condensed_Binocular.Run")
@patch("src.Condensed_Binocular.metrics_exporter")
def test_report_table_calls_aml_logging_with_parameters(mock_exporter, mock_run, mock_env):
    # arrange
    reporting = Condensed_Binocular()
    name = "FOO"
    table = {}

    # act
    reporting.report_table(name, table)

    # assert
    reporting.run.log_table.assert_called_once_with(name, table)


@patch("src.Condensed_Binocular.Env")
@patch("src.Condensed_Binocular.Run")
@patch("src.Condensed_Binocular.metrics_exporter")
def test_report_table_calls_aml_parent_logging_with_parameters_if_parent_is_true_and_run_is_online(mock_exporter, mock_run, mock_env):
    # arrange
    reporting = Condensed_Binocular()
    reporting.offline_run = None
    name = "FOO"
    table = {}
    report_parent_true = bool(True)

    # act
    reporting.report_table(name, table, report_to_parent=report_parent_true)

    # assert
    reporting.run.parent.log_table.assert_called_once_with(name, table)


@patch("src.Condensed_Binocular.Env")
@patch("src.Condensed_Binocular.Run")
@patch("src.Condensed_Binocular.metrics_exporter")
def test_report_table_doesnt_call_aml_parent_logging_if_parent_is_false_and_run_is_online(mock_exporter, mock_run, mock_env):
    # arrange
    reporting = Condensed_Binocular()
    reporting.offline_run = None
    name = "FOO"
    table = {}
    report_parent_false = bool(False)

    # act
    reporting.report_table(name, table, report_to_parent=report_parent_false)

    # assert
    assert reporting.run.parent.log_table.call_count == 0


@patch("src.Condensed_Binocular.Env")
@patch("src.Condensed_Binocular.Run")
@patch("src.Condensed_Binocular.metrics_exporter")
def test_report_table_doesnt_call_aml_parent_logging_if_run_is_offline(mock_exporter, mock_run, mock_env):
    # arrange
    reporting = Condensed_Binocular()
    name = "FOO"
    table = {}
    report_parent_true = bool(True)

    # act
    reporting.report_table(name, table, report_to_parent=report_parent_true)

    # assert
    assert reporting.run.parent.report_table.call_count == 0


# Tests report_image method
@patch("src.Condensed_Binocular.Env")
@patch("src.Condensed_Binocular.Run")
@patch("src.Condensed_Binocular.metrics_exporter")
def test_report_image_calls_aml_logging_with_parameters(mock_exporter, mock_run, mock_env):
    # arrange
    reporting = Condensed_Binocular()
    name = "FOO"
    path = "./"

    # act
    reporting.report_image(name, path=path)

    # assert
    reporting.run.log_image.assert_called_once_with(name, path=path, plot=None)


# Tests get_run_id method
@patch("src.Condensed_Binocular.Env")
@patch("src.Condensed_Binocular.Run")
@patch("src.Condensed_Binocular.constants")
@patch("src.Condensed_Binocular.metrics_exporter")
def test_get_run_id_returns_run_id_when_context_online(mock_exporter, mock_constants, mock_run, mock_env):
    # arrange
    reporting = Condensed_Binocular()
    mock_constants.OFFLINE_RUN_PREFIX = "OfflineRun"
    mock_run.id = "Online"

    # act
    response = reporting.get_run_id(mock_run)

    # assert
    assert response == "Online"


@patch("src.Condensed_Binocular.Env")
@patch("src.Condensed_Binocular.Run")
@patch("src.Condensed_Binocular.constants")
@patch("src.Condensed_Binocular.metrics_exporter")
def test_get_run_id_returns_unique_id_when_context_offline(mock_exporter, mock_constants, mock_run, mock_env):
    # arrange
    reporting = Condensed_Binocular()
    mock_constants.OFFLINE_RUN_PREFIX = "OfflineRun"

    # act
    response = reporting.get_run_id(mock_run)

    # assert
    assert response != "OfflineRun"


# Tests set_view method
@patch("src.Condensed_Binocular.Env")
@patch("src.Condensed_Binocular.Run")
@patch("src.Condensed_Binocular.metrics_exporter")
@patch("src.Condensed_Binocular.measure_module")
@patch("src.Condensed_Binocular.stats_module")
def test_set_view_calls_register_view(mock_stats, mock_measuremodule, mock_exporter, mock_run, mock_env):
    # arrange
    reporting = Condensed_Binocular()
    metric = "FOO"
    description = "BAR"

    # act
    reporting.set_view(metric, description, mock_measuremodule.MeasureFloat())

    # assert
    assert mock_stats.stats.view_manager.register_view.call_count == 1
