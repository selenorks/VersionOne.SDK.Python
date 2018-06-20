
importedOk=True

# Allow for tests that can't don't import this to use this file still
try:
    import v1pysdk
except ImportError:
    importedOk=False


class PublicTestServerConnection():
    username = 'admin'
    password = 'admin'
    address = 'www14.v1host.com'
    instance = 'v1sdktesting'
    #TODO: Add OAuth key

    def __init__():
        pass

    @staticmethod
    def getV1Meta():
        """Creates a V1Meta object from the default configuration and returns it
        """
        # If we couldn't import the v1pysdk, we can't create the object
        if not importedOk:
            return None
        else:
            return v1pysdk.V1Meta(
                instance_url = 'https://' + PublicTestServerConnection.address + '/' + PublicTestServerConnection.instance,
                username = PublicTestServerConnection.username,
                password = PublicTestServerConnection.password,
            )
