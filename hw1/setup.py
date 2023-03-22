import setuptools

setuptools.setup(
    name='ast_visualizer',
    version='1.0.3',
    author='Mark Vavilov',
    packages=['ast_visualizer'],
    url='https://github.com/vavilovm/hse-python-2023',
    python_requires='>=3.9',
    install_requires=['networkx==3.0', 'graphviz==0.20.1', 'pyparsing==3.0.9', 'pydot==1.4.2'],
)
