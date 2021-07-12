use std::time::SystemTime;
use std::time::Duration;
use std::io;
use std::io::Write as IoWrite;
use rustpython_vm::Interpreter;
use rustpython_vm::pyobject::PyResult;
use rustpython_compiler::Mode;

fn now() -> SystemTime {
    return SystemTime::now();
}

fn elapsed(start: SystemTime) -> (Duration, bool) {
    match start.elapsed() {
        Ok(delta) => return (delta, false),
        _ => return (Duration::new(0, 0), true),
    }
}

fn bench_test(n_iter: usize, name: &str, source: &str) -> (Duration, bool) {
    //let mut dur: Duration;
    //let mut b: bool;
    Interpreter::default().enter(|vm| {
        let start = now();
        for _ in 0..n_iter { 
            let code = vm.compile(source, Mode::Exec, name.to_owned()).unwrap();
            let scope = vm.new_scope_with_builtins();
            let res: PyResult = vm.run_code_obj(code.clone(), scope);
            vm.unwrap_pyresult(res);
        }
        elapsed(start)
    })
    //(dur, b)
}

#[no_mangle]
#[inline(never)]
fn bench() {
    // setup

    let mut timing_error: bool = false;
    let n_iterations: usize = 1;

    let contents = std::fs::read_to_string("/scratch/ziyangx/RustPython/benches/benchmarks/pystone.py").unwrap();
    let code_with_loops = format!("LOOPS = {}\n{}", 30000, contents);
    let code_str = code_with_loops.as_str();

    // bench
    let (total, err) = bench_test(n_iterations, "pystone", code_str);

    if err {
        timing_error = true;
    }

    if timing_error {
        let _r = writeln!(&mut io::stderr(), "{:}", "Timing error");
    } else {
        writeln!(&mut io::stderr(), "{:} {:} {:}.{:09}",
        n_iterations as u64,
        "Iterations; Time",
        total.as_secs(),
        total.subsec_nanos());
    }
}

fn main() {
    bench();
}
