from setuptools import setup

setup(
    name='unsorted',
    version='0.0.1',
    description='Access my files remotely',
    url='https://alde.nu/unsorted',
    author='Rickard Dybeck',
    author_email='r.dybeck@gmail.com',
    license='MIT',
    packages=['unsorted'],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'unsorted = unsorted.__main__:main',
        ]
    })
