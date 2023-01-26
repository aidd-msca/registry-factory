from registry_factory.factory import Factory


class CustomFactory(Factory):
    # Basic registry
    Registry1 = Factory.create_registry()

    # Shared registry
    Registry2 = Factory.create_registry(shared=True)

    # Shared registry, no versioning
    Registry3 = Factory.create_registry(shared=True, versioning=None)

    # Shared registry, custom post checks
    Registry4 = Factory.create_registry(shared=True, custom_post_checks=["your custom post checks here"])
