Try the code below:

.. exec:code:: python
    :capture-stdout: file1.txt
    :capture-stderr: file2.txt

    import sys
    print("hello world")
    print("hello errors", file=sys.stderr)

It shall print the following text:

.. literalinclude:: file1.txt

And the following text in the standard error output stream:

.. literalinclude:: file2.txt

Pretty isn't it?
