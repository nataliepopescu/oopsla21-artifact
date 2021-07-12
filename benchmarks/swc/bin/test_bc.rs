use std::time::SystemTime;
use std::time::Duration;
use std::io;
use std::io::Write as IoWrite;
use swc::config::{Config, JscConfig, Options, SourceMapsConfig};
use swc_common::{
    errors::{ColorConfig, Handler},
    FileName, FilePathMapping, SourceMap,
};
use swc_ecma_parser::{JscTarget, Syntax, TsConfig};
use std::{sync::Arc};

static SOURCE: &str = include_str!("/scratch/ziyangx/benchmarks/swc/benches/assets/AjaxObservable.ts");

fn now() -> SystemTime {
    return SystemTime::now();
}

fn elapsed(start: SystemTime) -> (Duration, bool) {
    match start.elapsed() {
        Ok(delta) => return (delta, false),
        _ => return (Duration::new(0, 0), true),
    }
}

fn bench_test(n_iter: usize, c: &swc::Compiler, opts: &Options) {
    for _ in 0..n_iter {
        let fm = c.cm.new_source_file(
            FileName::Real("rxjs/src/internal/observable/dom/AjaxObservable.ts".into()),
            SOURCE.to_string(),
        );
        c.process_js_file(fm, opts);
    }
}

fn mk() -> swc::Compiler {
    let cm = Arc::new(SourceMap::new(FilePathMapping::empty()));
    let handler = Arc::new(Handler::with_tty_emitter(
        ColorConfig::Always,
        true,
        false,
        Some(cm.clone()),
    ));

    let c = swc::Compiler::new(cm.clone(), handler);

    c
}

#[no_mangle]
#[inline(never)]
fn bench() {
    // setup

    let start = now();
    let mut timing_error: bool = false;
    let n_iterations: usize = 1000;
    let c = mk();

    let opts = &Options {
        config: Config {
            jsc: JscConfig {
                target: Some(JscTarget::Es2020),
                syntax: Some(Syntax::Typescript(TsConfig {
                    ..Default::default()
                })),
                ..Default::default()
            },
            module: None,
            ..Default::default()
        },
        swcrc: false,
        is_module: true,
        ..Default::default()
    };
    // bench
    bench_test(n_iterations, &c, &opts);

    let (total, err) = elapsed(start);
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
