from examples.example_1_create_factory import CustomFactory as Registries


@Registries.Registry1.register("function_1")
def function_1():
    return "function_1"


@Registries.Registry1.register("class_1")
def class_1():
    return "class_1"
