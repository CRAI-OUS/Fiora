import json
import os
import numpy as np
import mypy
import glob


class ReportMaker:
    """Class to report the results of the test suite into markdown or other types"""

    def __init__(self, suitename) -> None:
        self.suitename = suitename

    def load_json(self, json_path):
        """
        Load the json file
        """
        with open(json_path, "r") as infile:
            json_suite_test_file = json.load(infile)
        return json_suite_test_file

    def test_mean(self, json_ref, json_test):
        """
        Test the mean of the test suite
        """
        mean_ref = json_ref["mean"]
        mean_test = json_test["mean"]
        if mean_ref["max"] >= mean_test["max"] and mean_ref["min"] <= mean_test["min"]:
            return True
        else:
            return False

    def test_max_values(self, json_ref, json_test):
        """
        Test the max values of the test suite
        """
        max_values_ref = json_ref["max_values"]
        max_values_test = json_test["max_values"]
        if (
            max_values_ref["max"] >= max_values_test["max"]
            and max_values_ref["min"] <= max_values_test["min"]
        ):
            return True
        else:
            return False

    def test_min_values(self, json_ref, json_test):
        """
        Test the min values of the test suite
        """
        min_values_ref = json_ref["min_values"]
        min_values_test = json_test["min_values"]
        if (
            min_values_ref["max"] >= min_values_test["max"]
            and min_values_ref["min"] <= min_values_test["min"]
        ):
            return True
        else:
            return False

    def test_percentage_foreground(self, json_ref, json_test):
        """
        Test the percentage of foreground value of the test suite
        """
        percentage_foreground_ref = json_ref["percentage_foreground"]
        percentage_foreground_test = json_test["percentage_foreground"]
        if (
            percentage_foreground_ref["max"] >= percentage_foreground_test["max"]
            and percentage_foreground_ref["min"] <= percentage_foreground_test["min"]
        ):
            return True
        else:
            return False

    def test_num_nans(self, json_ref, json_test):
        """
        Test the number of nans of the test suite
        """
        num_nans_ref = json_ref["num_nans"]
        num_nans_test = json_test["num_nans"]
        if num_nans_ref["total"] == num_nans_test["total"]:
            return True
        else:
            return False

    def test_num_infs(self, json_ref, json_test):
        """
        Test the number of infs of the test suite
        """
        num_infs_ref = json_ref["num_infs"]
        num_infs_test = json_test["num_infs"]
        if num_infs_ref["total"] == num_infs_test["total"]:
            return True
        else:
            return False

    def test_types(self, json_ref, json_test):
        """
        Test the types of the test suite
        """
        types_ref = json_ref["types"]
        types_test = json_test["types"]
        if types_ref["unique_types"] == types_test["unique_types"]:
            return True
        else:
            return False

    def test_distribution(self, dist_metric_ref, dist_metric_test):
        """
        Test the distribution of the test suite
        """
        if (
            dist_metric_ref["max"] >= dist_metric_test["max"]
            and dist_metric_ref["min"] <= dist_metric_test["min"]
        ):
            return True
        else:
            return False

    def generate_report_markdown_validation(self, validation_id, data_path):
        """Generate the report markdown for the validation"""
        json_test = self.load_json(
            f"Fiora_strc/validations/{self.suitename}_{validation_id}.json"
        )
        json_ref = self.load_json(f"Fiora_strc/test_suites/{self.suitename}.json")
        markdown_document = f"""<center><img src="https://github.com/MartinRovang/Fiora/blob/master/flc_design2022080460426.jpg?raw=true" width="100">  <br><br> Target: <p>{data_path}</p>
        <br>"""
        test_results_json = {}
        for key in json_ref[self.suitename]:
            markdown_document += "<hr><br>"

            if key == "distribution":
                test_results_json[key] = {}
                markdown_document += """ 
                <table>
                <thead>
                    <tr class="header">
                        <th>Test</th>
                        <th>Quantile</th>
                        <th>Min value</th>
                        <th>Max value</th>
                    </tr>
                </thead>
                <tbody>
                """
                i = 0
                for quantile_ref, quantile_test in zip(
                    json_ref[self.suitename][key], json_test[self.suitename][key]
                ):
                    i += 1
                    test_result = self.test_distribution(
                        json_ref[self.suitename][key][quantile_ref],
                        json_test[self.suitename][key][quantile_test],
                    )
                    if test_result:
                        # if even
                        if i % 2 == 0:
                            markdown_document += f"""
                            <tr class="even">
                                <td>✅</td>
                                <td>{quantile_ref}</td>
                                <td>{json_ref[self.suitename][key][quantile_ref]["min"]}</td>
                                <td>{json_ref[self.suitename][key][quantile_ref]["max"]}</td>
                            </tr>
                            """
                        # if odd
                        else:
                            markdown_document += f"""
                            <tr class="odd">
                                <td>✅</td>
                                <td>{quantile_ref}</td>
                                <td>{json_ref[self.suitename][key][quantile_ref]["min"]}</td>
                                <td>{json_ref[self.suitename][key][quantile_ref]["max"]}</td>
                            </tr>


                            """

                    else:
                        # if odd
                        if i % 3 == 0:
                            markdown_document += f"""
                                <tr class="odd">
                                    <td>❌</td>
                                    <td>{quantile_ref}</td>
                                    <td>{json_ref[self.suitename][key][quantile_ref]['min']}</td>
                                    <td>{json_ref[self.suitename][key][quantile_ref]['max']}</td>
                                </tr>

                                
                                """
                        # if even
                        else:
                            markdown_document += f"""
                                <tr class="even">
                                    <td>❌</td>
                                    <td>{quantile_ref}</td>
                                    <td>{json_ref[self.suitename][key][quantile_ref]['min']}</td>
                                    <td>{json_ref[self.suitename][key][quantile_ref]['max']}</td>
                                </tr>

                                """
                    test_results_json[key][quantile_ref] = test_result

                markdown_document += """
                                </tbody>
                                </table>"""
                markdown_document += "</center><br>"

            if key == "mean":
                test_result = self.test_mean(
                    json_ref[self.suitename], json_test[self.suitename]
                )
                min_val = json_ref[self.suitename][key]["min"]
                max_val = json_ref[self.suitename][key]["max"]
                if test_result:
                    markdown_document += f"✅ mean must be greater than or equal to <code>{min_val}</code> and less than or equal to <code>{max_val}</code>\n"
                else:
                    markdown_document += f"❌ mean must be greater than or equal to <code>{min_val}</code> and less than or equal to <code>{max_val}</code>\n"
                test_results_json[key] = test_result

            if key == "max_values":
                min_val = json_ref[self.suitename][key]["min"]
                max_val = json_ref[self.suitename][key]["max"]
                test_result = self.test_max_values(
                    json_ref[self.suitename], json_test[self.suitename]
                )
                if test_result:
                    markdown_document += f"✅ maximum values must be greater than or equal to <code>{min_val}</code> and less than or equal to <code>{max_val}</code>\n"
                else:
                    markdown_document += f"❌ maximum values must be greater than or equal to <code>{min_val}</code> and less than or equal to <code>{max_val}</code>\n"
                test_results_json[key] = test_result

            if key == "min_values":
                min_val = json_ref[self.suitename][key]["min"]
                max_val = json_ref[self.suitename][key]["max"]
                test_result = self.test_min_values(
                    json_ref[self.suitename], json_test[self.suitename]
                )
                if test_result:
                    markdown_document += f"✅ minimum values must be greater than or equal to <code>{min_val}</code> and less than or equal to <code>{max_val}</code>\n"
                else:
                    markdown_document += f"❌ minimum values must be greater than or equal to <code>{min_val}</code> and less than or equal to <code>{max_val}</code>\n"

                test_results_json[key] = test_result

            if key == "percentage_foreground":
                min_val = json_ref[self.suitename][key]["min"]
                max_val = json_ref[self.suitename][key]["max"]
                test_result = self.test_percentage_foreground(
                    json_ref[self.suitename], json_test[self.suitename]
                )
                if test_result:
                    markdown_document += f"✅ percentage of foreground must be greater than or equal to <code>{min_val}</code> and less than or equal to <code>{max_val}</code>\n"
                else:
                    markdown_document += f"❌ percentage of foreground must be greater than or equal to <code>{min_val}</code> and less than or equal to <code>{max_val}</code>\n"
                test_results_json[key] = test_result
            if key == "num_nans":
                total = json_ref[self.suitename][key]["total"]
                test_result = self.test_num_nans(
                    json_ref[self.suitename], json_test[self.suitename]
                )
                if test_result:
                    markdown_document += (
                        f"✅ number of nans must be <code>{total}</code>\n"
                    )
                else:
                    markdown_document += (
                        f"❌ number of nans must be <code>{total}</code>\n"
                    )
                test_results_json[key] = test_result

            if key == "num_infs":
                total = json_ref[self.suitename][key]["total"]
                test_result = self.test_num_infs(
                    json_ref[self.suitename], json_test[self.suitename]
                )
                if test_result:
                    markdown_document += (
                        f"✅ number of infs must be <code>{total}</code>\n"
                    )
                else:
                    markdown_document += (
                        f"❌ number of infs must be <code>{total}</code>\n"
                    )
                test_results_json[key] = test_result

            if key == "types":
                unique_types = json_ref[self.suitename][key]["unique_types"]
                test_result = self.test_types(
                    json_ref[self.suitename], json_test[self.suitename]
                )
                markdown_document += "Types: "
                for typ_ in unique_types:
                    markdown_document += f"""<span style="background-color: #0000FF; color:white">{typ_}</span>"""
                if test_result:
                    markdown_document += (
                        f"✅ unique types must be <code>{unique_types}</code>\n"
                    )
                else:
                    markdown_document += (
                        f"❌ unique types must be <code>{unique_types}</code>\n"
                    )
                test_results_json[key] = test_result
        markdown_document += "</hr>"
        # save as markdown file
        with open(
            f"Fiora_strc/validations/reports/{self.suitename}_{validation_id}.html",
            "w",
            encoding="utf-8",
        ) as outfile:
            outfile.write(markdown_document)

        return test_results_json

    def generate_report_markdown(self):
        """Generate the report in markdown format"""
        json_path = f"Fiora_strc/test_suites/{self.suitename}.json"
        json_file = self.load_json(json_path)
        markdown_document = """<center><img src="https://github.com/MartinRovang/Fiora/blob/master/flc_design2022080460426.jpg?raw=true" width="100"> <br><br>"""
        for key in json_file[self.suitename]:
            markdown_document += "<hr><br>"

            if key == "distribution":
                markdown_document += """ 
                <table>
                <thead>
                    <tr class="header">
                        <th>Quantile</th>
                        <th>Min value</th>
                        <th>Max value</th>
                    </tr>
                </thead>
                <tbody>
                """
                i = 0
                for quantile_ref in json_file[self.suitename][key]:
                    i += 1
                    # if even
                    if i % 2 == 0:
                        markdown_document += f"""
                        <tr class="even">
                            <td>{quantile_ref}</td>
                            <td>{json_file[self.suitename][key][quantile_ref]["min"]}</td>
                            <td>{json_file[self.suitename][key][quantile_ref]["max"]}</td>
                        </tr>
                        """
                    # if odd
                    else:
                        markdown_document += f"""
                        <tr class="odd">
                            <td>{quantile_ref}</td>
                            <td>{json_file[self.suitename][key][quantile_ref]["min"]}</td>
                            <td>{json_file[self.suitename][key][quantile_ref]["max"]}</td>
                        </tr>
                        """

                markdown_document += """
                                </tbody>
                                </table>"""
                markdown_document += "</center><br>"

            if key == "mean":
                max_val = json_file[self.suitename][key]["max"]
                min_val = json_file[self.suitename][key]["min"]
                markdown_document += f"mean must be greater than or equal to <code>{min_val}</code> and less than or equal to <code>{max_val}</code>"

            if key == "max_values":
                max_val = json_file[self.suitename][key]["max"]
                min_val = json_file[self.suitename][key]["min"]

                markdown_document += f"maximum value must be greater than or equal to <code>{min_val}</code> and less than or equal to <code>{max_val}</code>"

            if key == "min_values":
                max_val = json_file[self.suitename][key]["max"]
                min_val = json_file[self.suitename][key]["min"]

                markdown_document += f"minimum value must be greater than or equal to <code>{min_val}</code> and less than or equal to <code>{max_val}</code>"

            if key == "percentage_foreground":
                max_val = json_file[self.suitename][key]["max"]
                min_val = json_file[self.suitename][key]["min"]

                markdown_document += f"percentage of foreground value must be greater than or equal to <code>{min_val}</code> and less than or equal to <code>{max_val}</code>"

            if key == "num_nans":
                total = json_file[self.suitename][key]["total"]

                markdown_document += f"Total number of nans <code>{total}</code>"

            if key == "num_infs":
                total = json_file[self.suitename][key]["total"]

                markdown_document += f"Total number of infs <code>{total}</code>"

            if key == "types":
                all_types = json_file[self.suitename][key]["unique_types"]
                markdown_document += "Types: "
                for typ_ in all_types:
                    markdown_document += f"""<span style="background-color: #0000FF; color:white">{typ_}</span>"""
            markdown_document += "</hr><br>"

        # save as markdown file
        with open(
            f"Fiora_strc/test_suites/reports/{self.suitename}.html", "w"
        ) as outfile:
            outfile.write(markdown_document)
