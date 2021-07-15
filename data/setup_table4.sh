 #!/bin/bash
 SHA=a211dd5a7050b1f9e8a9870b95513060e72ac4a0
 wget https://github.com/wg/wrk/archive/${SHA}.tar.gz
 tar -xzf ${SHA}.tar.gz && rm ${SHA}.tar.gz
 
 cd wrk-${SHA} && make

 mv wrk ../../benchmarks

 cd .. && rm -rf wrk-${SHA}
