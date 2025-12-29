# BigDataGraph

## Description

**BigDataGraph** is a Python-based project for **Social Network Analysis (SNA)** built from Twitter data provided in JSON format.  
The software constructs a **unified graph** representing relationships between users, hashtags, and retweets, enabling structural and semantic analysis of social interactions.

The project is designed for **big data processing**, **graph analytics**, and **network-based exploration** of relationships in general and use Jaccard similarity.

**BigDataGraph is intended for research and educational purposes in the fields of
data science, network science, and computational social analysis.**

---

## Repository Structure

```text
BigDataGraph/
├── bigdata/
│   └── Python modules implementing graph construction logic
├── main.py – core source code
├── requirements.txt – Python dependencies
├── LICENSE
└── README.md
```
## Requirements

Python ≥ 3.8

Install all required dependencies using:
pip install -r requirements.txt

Typical dependencies include libraries for data processing and graph construction (e.g., networkx).
See requirements.txt for more datails.

## Runtime Requirements

- **Python:** 3.8 or higher
- **Java:** 8 or 11 (required by PySpark)
- **Apache Spark:** 3.3.0 or higher
- **Memory:** at least 8GB recommended for large datasets
- **OS:** Linux, macOS, or Windows 10+

## Additional Notes

GraphFrames requires Apache Spark and the corresponding Scala version compatible with your Spark release.
Always check the official documentation: **GraphFrames for Spark**.

spaCy requires downloading the English language model:
python -m spacy download en_core_web_sm

## Usage

To generate a graph from a JSON file containing tweets:
```bash
Usage: python main.py input_file [--output_path] [--id_neighbours id] [--save_full_graph] [--save_pbi_report] [--save_word_cloud] [--only_tags_from_not_retweetted_posts]

INPUT_FILE
Path and filename: the input JSON file containing the data.

Optional arguments
--output_path OUTPUT_PATH
Output directory where results will be saved.
Default: ./outputs/

--id_neighbours ID
Compute and export the neighbours of a specific node (user ID).

--save_full_graph 
Save the complete generated graph to disk.
Default: False

--save_pbi_report 
Generate and save a Power BI–compatible report.
Default: False

--save_word_cloud 
Generate and save a word cloud from the extracted tags.
Default: False

--only_tags_from_not_retweetted_posts
Consider only hashtags extracted from non-retweeted posts.
Default: False
```

## Output

The software produces a graph containing:

- **Nodes**
  - Users
  - Hashtags

- **Edges**
  - Retweet relationships
  - Shared hashtags
  - Similarity relationships (e.g., Jaccard similarity)

Edges representing:
- retweet relationships
- shared hashtags
- similarity relationships (e.g., Jaccard similarity)

The resulting graph can be further analyzed using graph analysis tools such as NetworkX, Gephi, or custom analytics pipelines.

## Example
```bash
python main.py \
  --input datasets/data.json \
  --output results/ \
  --save_full_graph \
  --save_pbi_report \
  --save_word_cloud
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

@software{BigDataGraph2025,
  title     = {BigDataGraph},
  author    = {Altarocca, Francesco},
  affiliation = {Independent Researcher},
  year      = {2025},
  publisher = {Zenodo},
  doi       = {https://doi.org/10.5281/zenodo.18088015}
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
