from abstract_codebase.accreditation import Accreditation
from abstract_codebase.metacoding import MetaRegistry, UniqueDict
from abstract_codebase.registration import RegistryFactory


# Basic registry
class ModelRegistry1(MetaRegistry):
    index: UniqueDict = UniqueDict()


# Basic registry with shared index
class ModelRegistry2(MetaRegistry):
    pass


# AIDD registry
class ModelRegistry3(RegistryFactory):
    info = UniqueDict()
    index = UniqueDict()
    arguments = UniqueDict()

    accreditation: Accreditation = Accreditation()  # Optional for clarity


# AIDD registry with shared index, info, arguments and accreditation
class ModelRegistry4(RegistryFactory):
    pass
