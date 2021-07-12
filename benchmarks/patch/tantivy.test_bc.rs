use tantivy::tokenizer::{TokenizerManager, TextAnalyzer};
use std::time::SystemTime;
use std::time::Duration;
use std::io;
use std::io::Write as IoWrite;

fn now() -> SystemTime {
    return SystemTime::now();
}

fn elapsed(start: SystemTime) -> (Duration, bool) {
    match start.elapsed() {
        Ok(delta) => return (delta, false),
        _ => return (Duration::new(0, 0), true),
    }
}

fn bench_test(n_iter: usize, ALICE_TXT: &str, tokenizer: &TextAnalyzer) {
    for _ in 0..n_iter {
        let mut word_count = 0;
        let mut token_stream = tokenizer.token_stream(ALICE_TXT);
        while token_stream.advance() {
            word_count += 1;
        }
        assert_eq!(word_count, 30_731);
    }
}

#[no_mangle]
#[inline(never)]
fn bench() {
    // setup

    const ALICE_TXT: &'static str = include_str!("../benches/alice.txt");
    let start = now();
    let mut timing_error: bool = false;
    let n_iterations: usize = 1000;

    let tokenizer_manager = TokenizerManager::default();
    let tokenizer = tokenizer_manager.get("default").unwrap();

    // bench
    bench_test(n_iterations, ALICE_TXT, &tokenizer);

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
