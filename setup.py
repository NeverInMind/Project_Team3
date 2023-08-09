from setuptools import setup, find_namespace_packages

setup(name='power9bot',
      version='1.0.1',
      description='Assistant Ostap',
      url='https://github.com/NeverInMind/Project_Team3/',
      author='GOIT TEAM 3',
      author_email='',
      license='MIT',
      packages=find_namespace_packages(),
      include_package_data=True,
      package_data={'data': ['*.bin']},
      entry_points={'console_scripts': ['Ostap = Ostap.main:main']})