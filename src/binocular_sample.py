# Basic example of how to log to AML and/or Appinsights:
import Condensed_Binocular

reporting = Condensed_Binocular()
reporting.report_metric("dummy value", 0.1, description="a random value to show reporting capabilities", report_to_parent=True)
