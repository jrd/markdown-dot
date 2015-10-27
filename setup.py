from setuptools import setup, find_packages

setup(
    name="Markdown dot extension",
    version="0.1.5",
    py_modules=["mdx_dot"],
    install_requires=['Markdown>=2.5.0'],
    author="Jawher and Cyrille Pontvieux",
    author_email="cyrille@enialis.net",
    description="Markdown dot extension",
    license="MIT",
    keywords="markdown dot graphviz",
    url="https://github.com/jrd/markdown-dot",
)
