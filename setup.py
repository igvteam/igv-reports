import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='igv-reports',
                 packages=['igv_reports'],
                 version='0.1.0',
                 description='Creates self-contained html pages for visual variant review with IGV (igv.js).',
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 license='MIT',
                 author='Jim Robinson',
                 url='https://github.com/igvteam/igv.js-reports',
                 # download_url='https://github.com/igvteam/igv.js-jupyter/archive/0.2.1.tar.gz',
                 keywords=['igv', 'bioinformatics', 'genomics', 'visualization', 'variant' ],
                 classifiers=[
                     'Development Status :: 4 - Beta',
                     'Intended Audience :: Science/Research',
                     'Intended Audience :: Developers',
                     'License :: OSI Approved :: MIT License',
                     'Programming Language :: Python'
                 ],
                 package_data={'igv_reports': ['templates/*']},
                 )
