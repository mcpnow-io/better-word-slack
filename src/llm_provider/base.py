from abc import ABC, abstractmethod


class LLMProvider(ABC):
    @abstractmethod
    def generate_content(self, prompt: str) -> str:
        """
        Generate content using the specified model and input contents.

        :param prompt: The input text to generate content from.
        :return: Generated content as a string.
        """
        pass

    def generate_content_enhanced(self, prompt: str) -> str:
        """
        Enhanced content generation method. Should be overridden by providers that support it.
        Default implementation raises NotImplementedError.

        :param prompt: The input text to generate content from.
        :return: Generated content as a string.
        :raises NotImplementedError: If the provider doesn't support enhanced generation.
        """
        raise NotImplementedError(
            "Enhanced content generation not supported by this provider"
        )

    def has_enhanced_method(self) -> bool:
        """
        Check if this provider supports the enhanced generate_content method.

        :return: True if generate_content_enhanced is implemented, False otherwise.
        """
        try:
            # Try to call the method with a test to see if it's implemented
            # We check if the method is overridden from the base class
            return (
                type(self).generate_content_enhanced
                != LLMProvider.generate_content_enhanced
            )
        except AttributeError:
            return False

    def generate_content_auto(self, prompt: str) -> str:
        """
        Automatically choose between enhanced and regular content generation.
        Uses generate_content_enhanced if available, otherwise falls back to generate_content.

        :param prompt: The input text to generate content from.
        :return: Generated content as a string.
        """
        if self.has_enhanced_method():
            return self.generate_content_enhanced(prompt)
        else:
            return self.generate_content(prompt)
