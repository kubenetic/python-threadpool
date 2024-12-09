# Process queued data with a worker pool

## Problem

I have a queue of data that I want to process concurrently using a pool of worker threads. This project is just a PoC
to demonstrate how to use the `concurrent.futures` module to process queued data with a worker pool. The experience
that I gained from this project will be useful for example in an application where a centralized TCP logging server
receives log messages from multiple clients and processes them concurrently.

### What does the asterisk mean in `def __init__(self, maxsize=0, *, ctx):`
The asterisk sign is used to enforce that any arguments appearing after the * must be passed as keyword arguments 
rather than positional arguments.

#### Positional and Keyword Arguments:
In Python, function arguments can typically be passed either positionally or by keyword:

```python
def example(a, b):
    pass

example(1, 2)          # Positional
example(a=1, b=2)      # Keyword
```

However, with the *, you can enforce that some arguments must only be passed by keyword.

#### What the * Does:
The * marks the end of positional arguments and the beginning of keyword-only arguments. In this case:

```python
def __init__(self, maxsize=0, *, ctx):
```

The `maxsize` can be passed either positionally or as a keyword argument and `ctx` must be passed as a keyword argument:

```python
obj = MyClass(10, ctx="some_value")   # Valid
obj = MyClass(maxsize=10, ctx="some_value")  # Valid
obj = MyClass(10, "some_value")      # Invalid, ctx must be keyword
```

#### Why Use *?
* **Readability:** By enforcing keyword-only arguments, the code becomes more readable and explicit, especially for 
  arguments that might otherwise be confusing.
  
  Example:
    ```python
    def configure_logging(level, *, log_file=None):
        pass

    configure_logging(10, log_file="app.log")  # Clear and explicit
    configure_logging(10, "app.log")          # Ambiguous (Is "app.log" the level?)
    ```

* **Future-Proofing:** Adding the * helps ensure compatibility if you want to add additional positional arguments in  
  the future without breaking existing code.