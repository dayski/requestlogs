from distutils.core import setup


def readme():
    with open('README.txt') as f:
        return f.read()

setup(
    name='RequestLogs',
    version='1.0dev',
    author='dayski',
    author_email='kapil@delhivery.com',
    packages=['requestlogs',],
    url='https://github.com/dayski/requestlogs',
    license='MIT',
    description='Request Log middleware',
    long_description=readme(),
    install_requires=[
        "Django >= 1.3.0",
        "pymongo >= 2.5.1",
        "celery",
        "elasticsearch == 1.0.0",
    ]
)
