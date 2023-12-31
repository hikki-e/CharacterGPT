import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="charactergpt-prompts",
    version="0.1.0",
    author="Hikki-e",
    author_email="zmk383@gmail.com",
    description="This library is designed to make the creation of characters for roll-play in ChatGPT much easier",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hikki-e/CharacterGPT",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
package_data={
        'charactergpt_prompts': ['additional_data/*', "jailbreaks/*", "character_examples/*"],
    },
include_package_data=True
)