# Weather Display

A simple Python program that retrieves weather data from different sources
and displays the data on the console or on a display.

## Installation

A [Python](https://www.python.org/) version of 3.9 or higher is needed.
The additional packages can be installed with
[pip](https://pip.pypa.io/en/stable/) using the following command:

```bash
pip install -r requirements.txt
```

The package as a whole can be installed from the released `.tar.gz` or `.whl`
file by using [pip](https://pip.pypa.io/en/stable/) as an install tool:

```bash
pip install weather_display-1.2.0.tar.gz
```

The project documentation can be found in the docs folder and is generated
using [pdoc](https://pdoc.dev/) and the following command:

```bash
pdoc weather_display -o docs
```

## Usage

The weather_display package can be executed directly with the following
python command from its parent directory:

```bash
python -m weather_display
```

## Acknowledgments

I would like to thank Marco Sudbrock for the idea to this project and
the [Deutscher Wetterdienst](https://www.dwd.de/) for providing their
weather data and API free of charge.

## License

[MIT License](https://github.com/jlwolf94/weather_display/blob/main/LICENSE)
