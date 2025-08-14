from setuptools import find_packages, setup

setup(
    name="desafio-vendas-cli",
    version="0.1.0",
    description="CLI para processamento de vendas e geração de relatórios",
    author="Marcos Gomes",
    packages=find_packages(),
    install_requires=[],
    python_requires=">=3.12",
    entry_points={"console_scripts": ["vendas-cli=parser.relatorios:parser"]},
    include_package_data=True,
)
