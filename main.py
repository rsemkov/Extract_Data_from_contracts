import re
import os


def governing_law_check(the_content):
    pattern = r"governed by the laws of the country of (\w+)"
    results = re.findall(pattern, the_content)
    return results[0]


def annual_leaves_check(the_content):
    pattern = r"(\d+) working days of paid annual leave"
    results = re.findall(pattern, the_content)
    return results[0]


def probation_period_check(the_content):
    pattern = r"probation period of (\w+\s\w+)"
    results = re.findall(pattern, the_content)
    return results[0]


def notice_type_check(the_content):
    pattern = r"giving (\w+\s\w+) notice"
    results = re.findall(pattern, the_content)
    return results[0]


def contract_type_check(the_content):
    if "Permanent" in the_content:
        return "Permanent"
    return "Temporary"


def compete_clause_check(the_content):
    if "Non-compete" in the_content:
        return "With"
    return "Without"


def find_salary_in_doc(the_content):
    pattern = r"BGN\s(\d+\s\d+)|BGN\s(\d+)"
    results = re.findall(pattern, the_content)

    # This will create a tuple with 1 legit and 1 empty result, we need to take out the empty one:
    the_result = [x for x in results[0] if x != ""]

    # Next, we need to convert strings like "2 600" to a 2600 int, by removing the whitespace and then convert to int:
    the_salary = int(the_result[0].replace(" ", ""))

    return the_salary


def dict_sorting(the_dict):
    sorted_dict = dict(sorted(the_dict.items(), key=lambda item: item[1], reverse=True))
    return sorted_dict


def generate_results_report(total_empl, total_salaries, perm_temp, compete_non_comp, notices, probations, leaves, laws):
    final_result_all_files = [f"The following report is analyzing {total_empl} labor contracts of employees."]

    final_result_all_files.append("\n1. Salaries:")
    final_result_all_files.append(f"The total monthly amount of employee salaries is: BGN {total_salaries}, "
                                  f"with a headcount of: {total_empl} employees. "
                                  f"\nThis makes for an average monthly salary of BGN {total_salaries / total_empl:.2f}")

    final_result_all_files.append("\n2. Contract types:")
    final_result_all_files.append(f"There are {perm_temp['Permanent']} Permanent contract/s, "
                                  f"and {perm_temp['Temporary']} Temporary contract/s.")

    final_result_all_files.append(f"There are {compete_non_comp['With']} contract/s With a Non-Compete Clause, "
                                  f"and {compete_non_comp['Without']} contract/s Without a Non-Compete Clause.")

    final_result_all_files.append("\n3. Notices:")
    for notice, count in notices.items():
        final_result_all_files.append(f"There are {count} contract/s with {notice} notice period. ")

    final_result_all_files.append("\n4. Probations:")
    for probation, count in probations.items():
        final_result_all_files.append(f"There are {count} contract/s with {probation} probation period. ")

    final_result_all_files.append("\n5. Annual Leaves:")
    for leave, count in leaves.items():
        final_result_all_files.append(f"There are {count} contract/s with {leave} days of annual leave. ")

    final_result_all_files.append("\n6. Governing Laws:")
    for country, count in laws.items():
        final_result_all_files.append(f"In {count} of the contract/s the governing law is: {country}. ")

    output_file_path = 'employee_contracts_report.txt'
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        for result in final_result_all_files:
            output_file.write(result + "\n")


def main():
    total_employees = 0
    total_all_salaries = 0
    contract_types_perm_or_temp = {"Permanent": 0, "Temporary": 0}
    contract_types_non_compete = {"With": 0, "Without": 0}
    contract_notice_periods = {}
    contract_probation_periods = {}
    contract_annual_leaves = {}
    contract_governing_laws = {}

    input_path = input("Please, enter the file path: ")

    # List all files in the directory
    file_list = os.listdir(input_path)

    # Iterate over each file
    for filename in file_list:
        # Construct the full path to the file
        current_file_path = os.path.join(input_path, filename)

        if os.path.isfile(current_file_path):
            with open(current_file_path, "r", encoding='utf-8') as file:
                content = file.read()
                total_employees += 1

            # counts total salaries
            current_salary_result = find_salary_in_doc(content)
            total_all_salaries += current_salary_result
            # counts contract types(perm or temp)
            contract_types_perm_or_temp[contract_type_check(content)] += 1
            # counts non-competes
            contract_types_non_compete[compete_clause_check(content)] += 1

            # counts notice periods:
            notice_period = notice_type_check(content)
            if notice_period not in contract_notice_periods.keys():
                contract_notice_periods[notice_period] = 0
            contract_notice_periods[notice_period] += 1

            # counts probation periods:
            probation_period = probation_period_check(content)
            if probation_period not in contract_probation_periods.keys():
                contract_probation_periods[probation_period] = 0
            contract_probation_periods[probation_period] += 1

            # counts annual leaves:
            annual_leave = annual_leaves_check(content)
            if annual_leave not in contract_annual_leaves.keys():
                contract_annual_leaves[annual_leave] = 0
            contract_annual_leaves[annual_leave] += 1

            # counts governing laws:
            governing_law = governing_law_check(content)
            if governing_law not in contract_governing_laws.keys():
                contract_governing_laws[governing_law] = 0
            contract_governing_laws[governing_law] += 1

    generate_results_report(total_employees, total_all_salaries, contract_types_perm_or_temp, contract_types_non_compete,
                            dict_sorting(contract_notice_periods), dict_sorting(contract_probation_periods),
                            dict_sorting(contract_annual_leaves), dict_sorting(contract_governing_laws))

    print("\nA report has been generated: employee_contracts_report.txt"
          "\nYou can find it in the root folder.")


if __name__ == "__main__":
    main()
