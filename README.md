# RegistryFactory

![PyPI](https://img.shields.io/pypi/v/registry-factory)
![PyPI](https://img.shields.io/pypi/pyversions/registry-factory)
![PyPI](https://img.shields.io/github/license/aidd-msca/registry-factory)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1jlyEd1yxhvFCN82YqEFI82q2n0k_y06F?usp=sharing)


An abstract implementation of the software design pattern called registry proposed in (Hartog et. al., 2023), 
providing a factory for creating registries to which categorically similar modules can be organized.

**Content:** 
**[Installation](#installation)**
| **[Dependencies](#dependencies)**
| **[Usage](#usage)**
| **[Citation](#citation)**
| **[Code of Conduct](#code-of-conduct)**

### Overview
The registry design patterns provides a way to organize modular 
functionalities dynamically and achieve a unified, reusable, and interchangeable interface. 
It extends the Factory design pattern without the explicit class dependency. 
Additionally, the registry supports optional meta information such as versioning, accreditation, 
testing, etc. 
The UML diagrams show the differences between the factory and registry patterns. 
<p align="center">
  <br>
  <img alt="UML diagram of the pattern" src="figures/registry_uml.png">
  <br>
<i>Created with BioRender.com</i>
 </p>

## Installation

The codebase can be installed from PyPI using `pip`, or your package manager of choice, with

```bash
$ pip install registry-factory
```

## Dependencies

No third-party dependencies are required to use the minimal functionality of the RegistryFactory. 

## Usage

The workflow of creating a registry is the following. 1)  Identify a part of the code that can be 
separated from the rest. 2) Modularize the section to be independent of the rest of the code. 3) 
Create a registry from the RegistryFactory. 4) Register any modules that provide similar 
functionalities. 5) Call the optional module from the registry from the main workflow. See below. 
<p align="center">
  <br>
  <img alt="Workflow" src="figures/registry_creation.png" width="750">
  <br>
<i>Created with BioRender.com</i>
 </p>

Further available options and use-cases are described in the following sections.  

### A basic registry
A simple registry is created as such.

``` Python
from registry_factory.registration import RegistryFactory

class ModelRegistry(RegistryFactory):
    pass
```

Next, any models can be added to the ModelRegistry as such.

``` Python
import torch.nn as nn

@ModelRegistry.register(call_name="simple_model")
class SimpleModel(nn.Module):

    def __init__(self, layer_sizes) -> None:
        super(SimpleModel, self).__init__()
        dropout_rate = 0.25
        self.layers = nn.ModuleList()
        for layer in range(len(layer_sizes)-2):
            self.layers.append(
                nn.Sequential(
                    nn.Linear(hidden_layers[layer], hidden_layers[layer+1]),
                    nn.ReLU(),
                    nn.Dropout(p=dropout_rate)
                )
            )
        self.layers.append(
            nn.Sequential(
                nn.Linear(hidden_layers[-2], hidden_layers[-1])
            )
        )

    def forward(self, x):
        for layer in self.layers:
            x = layer(x)
        return x

```

### Shared modules
Describe the idea with shared module and give example.

``` Python

@ModelRegistry.register(call_name="simple_model")  
@dataclass(unsafe_hash=True)
class SimpleModelArguments():

    dropout_rate = 0.25
```

### Versioning and accreditation
Two examples of additional meta information that can be stored in a registry is module versioning 
and accreditation regarding how and to who credit should be attributed the module. 
Further explain the idea and give examples below.

At registration of a module, additional information can be supplied such as author, credit type and more. 
This information can be used to collect a summary of the accreditation required for all modules used in a given script. 

``` Python
@ModelRegistry.register(
    call_name="simple_model",
    author="Author name",
    credit_type=CreditType.REFERENCE,
    additional_information="Reference published work in (link)."
)
class SimpleModel(nn.Module):
    ...
```

An example summary of accreditation might look like,
``` Python
ModelRegistry.get_accreditation()
```

Further, the Config class can be used to read and update configurations across all modules, 
through yaml files or the command line interface.

### Testing and post checks
We also provide defining tests and post checks applied to all modules in a registry. Define test 
or post checks as follows when creating the registry.

``` Python
@ModelRegistry.register(
    call_name="simple_model",
    author="Author name",
    credit_type=CreditType.REFERENCE,
    additional_information="Reference published work in (link)."
)
class SimpleModel(nn.Module):
    ...
```

## Citation
Our paper in which we propose the registry design pattern, on which this package is built, is currently 
available as a preprint. If you make use of the design pattern or this package please cite our work accordingly.

```
@inproceedings{hartog2023registry,
    title={Registry: a design pattern to promote code reuse in machine learning-based drug discovery},
    author={Hartog, Peter and Svensson, Emma and Mervin, Lewis and Genheden, Samuel and Engkvist, Ola and Tetko, Igor},
    year={2023},
    note={Preprint}
}
```

### Funding

The work behind this package has received funding from the European Union’s Horizon 2020 
research and innovation programme under the Marie Skłodowska-Curie 
Actions, grant agreement “Advanced machine learning for Innovative Drug 
Discovery (AIDD)” No 956832”. [Homepage](https://ai-dd.eu/). 

![plot](figures/aidd.png)

## Code of Conduct

Everyone interacting in the codebase, issue trackers, chat rooms, and mailing lists is expected to follow the 
[PyPA Code of Conduct](https://www.pypa.io/en/latest/code-of-conduct/).

 
