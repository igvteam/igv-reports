File reader classes based on pysam API

General pattern

* create reader
```python
filereader = ReaderClass(path, options)
```

* fetch entire file
```python
data = filereader.slice()
```

* fetch file content for a genomic region
```python
data = filereader.slice(chr, start, end)
```



