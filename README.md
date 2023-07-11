# Weather Display

A simple Python program that retrieves weather data from different sources
and displays the data on the console or on a display.

## Installation

A [Python](https://www.python.org/) version of 3.11 or higher is needed.
The additional packages can be installed with
[pip](https://pip.pypa.io/en/stable/) using the following command:

```bash
pip install -r requirements.txt
```

The project documentation can be found in the docs folder and is generated
using [pdoc](https://pdoc.dev/) and the following command:

```bash
pdoc ./weather_display -o docs
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

MIT License

Copyright (c) 2023 Jan-Lukas Wolf

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
