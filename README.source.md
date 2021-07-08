- Run valgrind
`valgrind --tool=callgrind ./test_bc silesia-5.brotli`

- Parse valgrind output
`perl callgrind_get_unchecked_parser.perl --auto=yes callgrind.out.* cal.out`

- SourceNader will parse the output and generate the experiment results
`python Nader.py -r $(pwd)/brotli-expand -a $(pwd)/data/silesia-5.brotli -o brotli_result -t 10 -g cal.out`
