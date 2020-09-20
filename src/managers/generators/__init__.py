class AbstractShortKeyGenerator:

    def generate(self, url) -> str:
        raise NotImplementedError


class RandomShortKeyGenerator(AbstractShortKeyGenerator):
    pass


class UniqueShortKeyGenerator(AbstractShortKeyGenerator):
    pass
