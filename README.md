# abstract-codebase

![PyPI](https://img.shields.io/pypi/v/abstract-codebase)
![PyPI](https://img.shields.io/pypi/pyversions/abstract-codebase)
![PyPI](https://img.shields.io/github/license/aidd-msca/abstract-codebase)

An abstract codebase with utilities for registering generic modules with an optional configuration setup and accreditation system.

## Installation

The codebase can be installed from PyPI using `pip`, or your package manager of choice, with

```bash
$ pip install abstract-codebase
```

## Dependencies

No dependencies to use the minimal Registry functionality. The configuration setup depends on yaml and hydra.

## Usage

### RegistryFactory 
The codebase provides a way to register generic modules into a codebase. 
First a specific Registry is created, e.g. for deep learning models. 

``` Python
from abstract_codebase.registration import RegistryFactory

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

### Configurations
Each registered module can be accompanied with a dataclass of settings with default values. 

``` Python

@ModelRegistry.register(call_name="simple_model")  
@dataclass(unsafe_hash=True)
class SimpleModelArguments():

    dropout_rate = 0.25
```

As such, the model can rather be defined as.

``` Python

@ModelRegistry.register(call_name="simple_mlp")
class SimpleModel(nn.Module):

    def __init__(self, layer_sizes, args: SimpleModelArguments) -> None:
        super(SimpleMLP, self).__init__()
        dropout_rate = args.dropout_rate
        ...

```

Further, the Config class can be used to read and update configurations across all modules, through yaml files or the command line interface.
### Accreditation
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

TODO exemplify an accreditation summery.
``` Python
ModelRegistry.get_accreditation()
```

## Code of Conduct

Everyone interacting in the codebase, issue trackers, chat rooms, and mailing lists is expected to follow the [PyPA Code of Conduct](https://www.pypa.io/en/latest/code-of-conduct/).

 