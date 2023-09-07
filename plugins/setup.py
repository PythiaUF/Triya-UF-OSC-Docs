from setuptools import setup, find_packages

setup(
    name="mkdocs-custom-plugins",
    version="0.0.2",
    install_requires=[
        "mkdocs-material",
        "pillow",
    ],
    packages=find_packages(),
    entry_points={
        "mkdocs.plugins": [
            "custom-cards = mkdocs_custom_plugins.social:CustomSocialPlugin",
        ]
    },
)
