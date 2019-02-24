**Simple shell**

### Getting started

To run interpreter execute `python3 bash.py` or build image with Dockerfile and run it

To run tests execute `python3 -m unittest discover tests/`

### Example of usage

``` 
> echo "Hello, world!"
Hello, world!
> FILE=bash.py
> cat $FILE
file content...
> cat $FILE | wc
    22      63     705
> echo 123 | wc
    1       1       4
> x=exit
> $x
```

You can use native bash command like `nano`

```
> nano
```
