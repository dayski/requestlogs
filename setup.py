from distutils.core import setup

setup(
    name='RequestLogs',
    version='0.2adev',
    author='dayski',
    author_email='kapil@delhivery.com',
    packages=['requestlogs',],
    url='https://github.com/dayski/requestlogs',
    license='LICENSE.txt',
    description='Request Log middleware',
    long_description=open('README').read(),
    install_requires=[
        "Django >= 1.3.1",
        "pymongo >= 2.5.1",
        "celery",
    ]
)
