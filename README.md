# CriticalArcRemovalProblem



## Description

This software focuses on optimizing the completion time of a complex process, divided into a series of interdependent activities. In particular, it studies the possibility of
reducing overall times by removing some weak dependencies between activities.
In the context of an operational process, personnel assigned to a specific activity may often
be temporarily assigned to other tasks, or a lack of resources, such as machinery, may prevent the simultaneous execution of multiple activities. These factors generate precedence constraints
that define the order of execution of operations and can have a significant impact on the total duration of the project.
To improve efficiency, a company could invest financial resources to hire new staff or purchase equipment in order to eliminate some of these dependencies. However, the
main challenge is to identify which precedence constraints to modify in order to achieve the best possible result, considering both the available resources and the characteristics of the process.
This analysis focuses on identifying weak precedences whose removal can significantly reduce the overall project time. Specifically, the problem is addressed by simulating scenarios in which a maximum number of activities are removed based on the available budget.
In linear programming, this problem is known as the **Critical Arc Removal Problem” (CARP)**.
This software proposes the solution of the **Critical Arc Removal Problem (CARP)** using both exact optimization models implemented in **AMPL** and heuristic algorithms designed to efficiently handle large-scale instances of the problem.
The Critical Arc Removal Problem involves identifying a subset of critical edges (arcs) whose removal produces the greatest degradation of network performance under given constraints.

## Repository Structure

```text
CriticalArcRemovalProblem/
├── AMPL/                    # AMPL models
├── LICENSE                  # MIT o altra licenza
├── README.md                # documentazione principale
├── CITATION.cff             # metadati citazionali
├── dagGen.py                # generates examples
├── runAllExamples.py        # run experiments
└── requirements.txt         # dependencies
```

## 🧠 Key Features

- **Exact AMPL models** for small to medium-size instances
- **Heuristic algorithms** suited for large-scale graphs
- Support for custom input instances
- Demonstration scripts and reproducible examples

## Requirements

Python ≥ 3.9

AMPL (see AMPL documentation)

Solver (CPLEX, Gurobi, or open-source such as CBC)

Install all required dependencies using:
pip install -r requirements.txt

See requirements.txt for more datails.

## Runtime Requirements
- **Python:** 3.9 or higher
- **Memory:** at least 8GB recommended for large datasets
- **OS:** Linux, macOS, or Windows 10+

## Additional software requirement: AMPL
After installation, ensure that the ampl executable is available in the system PATH.
Additionally, at least one AMPL-compatible solver (e.g., CBC, Gurobi, CPLEX) must be installed and properly configured.

## Licensing note
This repository does not redistribute AMPL.
AMPL is proprietary software and is subject to its own license terms, which must be obtained independently by the user.

## Usage
To generate a graph from a JSON file containing tweets:
```bash
Usage: python runAllExamples.py

# Set the directory containing the .dat files
folder_path = "./"          # Modify with the actual path
output_file = "output.txt"  # File where results will be saved
# Path to the AMPL executable
ampl_executable = "./AMPL/ampl"  # Modify with the correct path

```

## Output

The output file contains detailed logs of the experimental runs, including parameter settings, execution results, and performance metrics for both AMPL optimization models and heuristic models.

## Example
```bash
python runAllExamples.py
```

## Reproducibility

All results are reproducible by: Using the same input dataset
Installing dependencies listed in requirements.txt
Running the provided scripts
Randomness (if any) should be controlled via fixed seeds in the code.

## License

This project is released under the MIT License.
See the LICENSE file for details.

## Citation

If you use BigDataGraph in academic work, please cite it as follows:

@software{CriticalArcRemovalProblem2025,
  title     = {CriticalArcRemovalProblem},
  author    = {Altarocca, Francesco},
  affiliation = {Independent Researcher},
  year      = {2025},
  publisher = {Zenodo},
  doi       = {https://doi.org/10.5281/zenodo.18089854}
}

## Disclaimer

This software is provided for **research and educational purposes only**.

The authors make **no guarantees** regarding the correctness, completeness, or suitability of the software for any specific task.  
Results obtained using this software should be **independently verified** before being used in scientific publications, decision-making processes, or production systems.

## Data and Ethical Use Notice

Users are solely responsible for ensuring that any data processed with this software complies with applicable laws, platform terms of service, and ethical research standards.

The author(s) assume **no responsibility** for improper, unlawful, or unethical use of third-party data, including but not limited to social media datasets.

## Limitation of Liability

Under no circumstances shall the author(s) be held liable for any direct, indirect, incidental, consequential, or special damages arising out of the use of, or inability to use, this software.

This includes, but is not limited to:
- data loss
- incorrect analyses or interpretations
- misuse of results
- system failures
- legal or ethical consequences related to data usage

By using this software, you acknowledge that you do so **at your own risk**.

## Author and Affiliation

**Francesco Altarocca**  
Affiliation: Independent Researcher  

*This work was developed independently and does not necessarily reflect the views of any current or past employer, institution, or organization.*
