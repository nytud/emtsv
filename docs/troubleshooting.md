# Troubleshooting

Below are some common error messages and the reasons why these appear.

## Errors like the one below appear if `JAVA_HOME` environment variable is not set properly.

```Python
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/usr/lib/python3.5/site-packages/jnius/__init__.py", line 13, in <module>
    from .reflect import *  # noqa
  File "/usr/lib/python3.5/site-packages/jnius/reflect.py", line 15, in <module>
    class Class(with_metaclass(MetaJavaClass, JavaClass)):
  File "/usr/lib/python3.5/site-packages/six.py", line 827, in __new__
    return meta(name, bases, d)
  File "jnius/jnius_export_class.pxi", line 111, in jnius.MetaJavaClass.__new__
  File "jnius/jnius_export_class.pxi", line 161, in jnius.MetaJavaClass.resolve_class
  File "jnius/jnius_env.pxi", line 11, in jnius.get_jnienv
  File "jnius/jnius_jvm_dlopen.pxi", line 90, in jnius.get_platform_jnienv
  File "jnius/jnius_jvm_dlopen.pxi", line 45, in jnius.create_jnienv
  File "/usr/lib/python3.5/os.py", line 725, in __getitem__
    raise KeyError(key) from None
KeyError: 'JAVA_HOME'
```

## Errors like the one below appear if the JRE version is not compatible.

```Python
Traceback (most recent call last):
  File "/app/emTagREST.py", line 12, in <module>
    prog = tagger(*args, **kwargs)
  File "/app/purepospy/purepospy.py", line 66, in __init__
    self._autoclass = import_pyjnius(PurePOS.class_path)
  File "/app/purepospy/purepospy.py", line 34, in import_pyjnius
    from jnius import autoclass
  File "/usr/lib/python3.7/site-packages/jnius/__init__.py", line 13, in <module>
    from .reflect import *  # noqa
  File "/usr/lib/python3.7/site-packages/jnius/reflect.py", line 15, in <module>
    class Class(with_metaclass(MetaJavaClass, JavaClass)):
  File "/usr/lib/python3.7/site-packages/six.py", line 827, in __new__
    return meta(name, bases, d)
  File "jnius/jnius_export_class.pxi", line 111, in jnius.MetaJavaClass.__new__
  File "jnius/jnius_export_class.pxi", line 161, in jnius.MetaJavaClass.resolve_class
  File "jnius/jnius_env.pxi", line 11, in jnius.get_jnienv
  File "jnius/jnius_jvm_dlopen.pxi", line 90, in jnius.get_platform_jnienv
  File "jnius/jnius_jvm_dlopen.pxi", line 59, in jnius.create_jnienv
SystemError: Error calling dlopen(b'/usr/lib/jvm/default-java/jre/lib/amd64/server/libjvm.so': b'/usr/lib/jvm/default-java/jre/lib/amd64/server/libjvm.so: cannot open shared object file: No such file or directory'
Exception ignored in: <_io.TextIOWrapper name='<stdout>' mode='w' encoding='UTF-8'>
BrokenPipeError: [Errno 32] Broken pipe
```

## Errors like the one below are due to missing modelfile because `git lfs` is not installed before clone.

```Python
  File "/app/purepospy/purepospy.py", line 168, in tag_sentence
    read_mod = serializer().readModelEx(self._model_jfile)
  File "jnius/jnius_export_class.pxi", line 733, in jnius.JavaMethod.__call__
  File "jnius/jnius_export_class.pxi", line 899, in jnius.JavaMethod.call_staticmethod
  File "jnius/jnius_utils.pxi", line 93, in jnius.check_exception
jnius.JavaException: JVM exception occurred: invalid stream header: 76657273
```

## Errors like the one below appear if no __Unicode-aware locale__ (eg. hu_HU.UTF-8) is set.

```Python
File "/app/emmorphpy/emmorphpy/emmorphpy.py", line 76, in _load_config
props = jprops.load_properties(fp)
File "/usr/lib/python3.6/site-packages/jprops.py", line 43, in load_properties
return mapping(iter_properties(fh))
File "/usr/lib/python3.6/site-packages/jprops.py", line 107, in iter_properties
for line in _property_lines(fh):
File "/usr/lib/python3.6/site-packages/jprops.py", line 271, in _property_lines
for line in _read_lines(fp):
File "/usr/lib/python3.6/site-packages/jprops.py", line 263, in _universal_newlines
for line in lines:
File "/usr/lib/python3.6/encodings/ascii.py", line 26, in decode
return codecs.ascii_decode(input, self.errors)[0]
UnicodeDecodeError: 'ascii' codec can't decode byte 0xc5 in position 603: ordinal not in range(128)
```

## Errors like the one below appear if the classpath in `jnius_config.get_classpath()` is not set properly.

Use `jnius_config.add_classpath(PATH)` to add the missing path to classpath in the main python file of the individual modules.

```Python
Traceback (most recent call last):
  File main.py, line 60, in <module>
    inited_tools = init_everything(tools)
  File "/app/xtsv/pipeline.py", line 32, in init_everything
    current_initialised_tools[prog_name] = prog(*prog_args, **prog_kwargs)  # Inint programs...
  File "/app/emdeppy/emdeppy/emdeppy.py", line 56, in __init__
    self._parser = self._autoclass('is2.parser.Parser')(self._jstr(model_file.encode('UTF-8')))
  File "/usr/local/lib/python3.5/dist-packages/jnius/reflect.py", line 159, in autoclass
    c = find_javaclass(clsname)
  File "jnius/jnius_export_func.pxi", line 26, in jnius.find_javaclass (jnius/jnius.c:17089)
jnius.JavaException: Class not found b'is2/parser/Parser'
```

## Errors like the one below appear if the input contains too long sentences which mostly are not real sentences but garbage data.

Please check the input and report any bugs in case the problem occurs on normal data with good RAM conditions.

```Python
Traceback (most recent call last):
  File main.py, line 21, in <module>
    sys.stdout.writelines(build_pipeline(sys.stdin, used_tools, inited_tools, conll_comments))
  File "/app/xtsv/tsvhandler.py", line 37, in process
    for sen_count, (sen, comment) in enumerate(sentence_iterator(stream, conll_comments)):
  File "/app/xtsv/tsvhandler.py", line 57, in sentence_iterator
    for line in input_stream:
  File "/app/xtsv/tsvhandler.py", line 42, in process
    yield from ('{0}\n'.format('\t'.join(tok)) for tok in internal_app.process_sentence(sen, field_values))
  File "/app/purepospy/purepospy.py", line 230, in process_sentence
    for tok, (_, lemma, hfstana) in zip(sen, self.tag_sentence(sent)):
  File "/app/purepospy/purepospy.py", line 210, in tag_sentence
    ret = self._tagger.tagSentenceEx(new_sent)
  File "jnius/jnius_export_class.pxi", line 1044, in jnius.JavaMultipleMethod.__call__
  File "jnius/jnius_export_class.pxi", line 766, in jnius.JavaMethod.__call__
  File "jnius/jnius_export_class.pxi", line 843, in jnius.JavaMethod.call_method
  File "jnius/jnius_utils.pxi", line 91, in jnius.check_exception
jnius.JavaException: JVM exception occurred: GC overhead limit exceeded
```

or

```Python
Traceback (most recent call last):
  File main.py, line 21, in <module>
    sys.stdout.writelines(build_pipeline(sys.stdin, used_tools, inited_tools, conll_comments))
  File "/app/xtsv/tsvhandler.py", line 37, in process
    for sen_count, (sen, comment) in enumerate(sentence_iterator(stream, conll_comments)):
  File "/app/xtsv/tsvhandler.py", line 57, in sentence_iterator
    for line in input_stream:
  File "/app/xtsv/tsvhandler.py", line 42, in process
    yield from ('{0}\n'.format('\t'.join(tok)) for tok in internal_app.process_sentence(sen, field_values))
  File "/app/purepospy/purepospy.py", line 230, in process_sentence
    for tok, (_, lemma, hfstana) in zip(sen, self.tag_sentence(sent)):
  File "/app/purepospy/purepospy.py", line 210, in tag_sentence
    ret = self._tagger.tagSentenceEx(new_sent)
  File "jnius/jnius_export_class.pxi", line 1044, in jnius.JavaMultipleMethod.__call__
  File "jnius/jnius_export_class.pxi", line 766, in jnius.JavaMethod.__call__
  File "jnius/jnius_export_class.pxi", line 843, in jnius.JavaMethod.call_method
  File "jnius/jnius_utils.pxi", line 91, in jnius.check_exception
jnius.JavaException: JVM exception occurred: Java heap space
```

or

```shell
quex/quex/code_base/buffer/Buffer.i:1075:	terminate called after throwing an instance of 'std::runtime_error'

  what():  Distance between lexeme start and current pointer exceeds buffer size.

(tried to load buffer forward). Please, compile with option



    QUEX_OPTION_INFORMATIVE_BUFFER_OVERFLOW_MESSAGE



in order to get a more informative output. Most likely, one of your patterns

eats more than you intended. Alternatively you might want to set the buffer

size to a greater value or use skippers (<skip: [ \n\t]> for example).



Aborted (core dumped)

WARNING: No blank line before EOF!
```

## Errors like the one below appear if quntoken version is <3.1.7 and emtsv version is <4.0.6

- The processing hang because Quntoken hangs on some input due to a deadlock found and fixed in later versions.
- The following exception is thrown when using PurePOS:

```
Traceback (most recent call last):
File "/usr/local/lib/python3.8/site-packages/xtsv/tsvhandler.py", line 67, in process
yield from ('{0}\n'.format('\t'.join(tok)) for tok in internal_app.process_sentence(sen, field_values))
File "/app/purepospy/purepospy/purepospy.py", line 183, in process_sentence
m[pos] = [(ana['lemma'], ana['tag']) for ana in json_loads(tok[field_indices[1]])] # lemma, tag
IndexError: list index out of range
```

The latter can be worked around by adding a newline to the end of the input. Updating quntoken and/or emtsv fixes both errors.
