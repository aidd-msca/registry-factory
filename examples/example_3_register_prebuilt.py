from examples.example_1_create_factory import CustomFactory as Registries


def function_2():
    return "function_2"


def class_2():
    return "class_2"


Registries.Registry1.register_prebuilt("function_2")
Registries.Registry1.register_prebuilt("class_2")
