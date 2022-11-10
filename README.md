# MicroView

<!-- badges: start -->
[![license](https://img.shields.io/badge/license-BSD%203--Clause-green)](https://github.com/dalmolingroup/microview/blob/master/LICENSE)
[![pytest status](https://github.com/dalmolingroup/microview/workflows/test-and-lint/badge.svg)](https://github.com/dalmolingroup/microview/actions)
[![documentation status](https://github.com/dalmolingroup/microview/workflows/docs/badge.svg)](https://dalmolingroup.github.io/MicroView/)
<!-- badges: end -->

MicroView, a reporting tool for taxonomic classification

MicroView agreggates results from taxonomic classification tools,
such as Kaiju and Kraken, building an interactive HTML report with
insightful visualizations.

Checkout the [full documentation](https://dalmolingroup.github.io/MicroView/).

## Quickstart

Install the package:

```sh
pip install microview
```

Go to your directory containing Kaiju/Kraken-style results and run:

```sh
microview -t .
```

Alternatively, if you have a CSV table defining result paths and contrasts, like this:

```
sample,group
result_1.tsv,group_one
result_2.tsv,group_two
...etc...
```

You can run MicroView like this:

```sh
microview -df contrast_table.csv -o report_with_table.html
```

Then, an HTML file named `microview_report.html` -
or the name you defined with the `-o` param -
should be available in your working directory,
try opening it with your browser!
