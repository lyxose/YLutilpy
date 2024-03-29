from setuptools import setup, find_packages

setup(
    name='YLutilpy',
    version='0.0.3',
    description='Some handy functions for Python data analysis',
    author='Yu-Xin Lu',
    author_email='1870562999@qq.com',
    url="https://github.com/lyxose/YLutilpy",
    install_requires=[
        'numpy'
    ], 
    extras_require={
        'create_video': ['opencv_python']
    },
    packages=find_packages(),
    python_requires='>=3'
)