import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='igv-reports',
                 packages=['igv_reports'],
                 version='0.9.1',
                 description='Creates self-contained html pages for visual variant review with IGV (igv.js).',
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 license='MIT',
                 author='Jim Robinson',
                 url='https://github.com/igvteam/igv-reports',
                 keywords=['igv', 'bioinformatics', 'genomics', 'visualization', 'variant' ],
                 classifiers=[
                     'Programming Language :: Python :: 3',
                     'Development Status :: 4 - Beta ',
                     'Intended Audience :: Science/Research',
                     'Intended Audience :: Developers',
                     'License :: OSI Approved :: MIT License',
                     'Topic :: Scientific/Engineering :: Bio-Informatics '
                 ],
                 install_requires=[
                     'pysam', 'intervalTree', 'requests'
                 ],
                 entry_points={
                     'console_scripts': [
                         'create_report=igv_reports.report:main',
                         'create_datauri=igv_reports.datauri:main'
                     ],
                 },
                 package_data={'igv_reports': ['templates/*']},
                 )
